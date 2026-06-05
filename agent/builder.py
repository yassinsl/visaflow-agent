"""Case file builder that orchestrates the classification and document detection."""

import json
import os
from datetime import datetime

import anthropic

from agent.classifier import classify_case
from agent.schemas import CaseFile, CaseCategory, RecommendedNextStep, IntakeForm
from agent.checklist import get_required_documents


# Document field to name mapping
DOCUMENT_FIELDS = {
    "has_passport": "passport",
    "has_birth_certificate": "birth_certificate",
    "has_bank_statements": "bank_statements",
    "has_employment_proof": "employment_proof",
    "has_housing_proof": "housing_proof",
}

# Map visa_type to case category
VISA_TYPE_TO_CATEGORY = {
    "student": CaseCategory.STUDENT_VISA,
    "work": CaseCategory.WORK_PERMIT,
    "family": CaseCategory.FAMILY_SPONSORSHIP,
    "family_reunification": CaseCategory.FAMILY_SPONSORSHIP,
    "tourist": CaseCategory.TOURIST_VISA,
}


async def build_case_file(form: IntakeForm) -> CaseFile:
    """Build a complete case file from a validated intake form.

    Args:
        form: Validated IntakeForm object with client information.

    Returns:
        Complete CaseFile with all fields populated.
    """
    # Step 1: Classify the case
    classification = await classify_case(
        situation_description=form.situation_description,
        visa_type=form.visa_type.value,
    )

    # Step 2: Determine required documents based on visa type
    required_docs = get_required_documents(form.visa_type, form.destination_country)

    # Map form fields to document names
    form_doc_mapping: dict[str, str] = {
        "has_passport": "passport",
        "has_birth_certificate": "birth_certificate",
        "has_bank_statements": "bank_statements",
        "has_employment_proof": "employment_proof",
        "has_housing_proof": "housing_proof",
        "has_acceptance_letter": "acceptance_letter",
        "has_language_certificate": "language_certificate",
        "has_work_contract": "work_contract",
        "has_marriage_certificate": "marriage_certificate",
        "has_sponsor_documents": "sponsor_documents",
        "has_travel_insurance": "travel_insurance",
        "has_accommodation_proof": "accommodation_proof",
        "has_return_ticket": "return_ticket",
    }

    # Find missing documents by checking what's required vs what's provided
    provided_docs: set[str] = set()
    for field_name, doc_name in form_doc_mapping.items():
        if getattr(form, field_name, False):
            provided_docs.add(doc_name)

    missing_documents = [doc for doc in required_docs if doc not in provided_docs]

    # Step 3: Map visa_type to case category
    case_category = VISA_TYPE_TO_CATEGORY.get(
        form.visa_type.value, CaseCategory.OTHER
    )

    # Step 4: Generate case summary using Claude API
    case_summary = await _generate_case_summary(
        client_name=form.full_name,
        nationality=form.nationality,
        destination=form.destination_country,
        visa_type=form.visa_type.value,
        missing_documents=missing_documents,
        situation_description=form.situation_description,
    )

    # Step 5: Determine recommended next step
    next_step = _determine_next_step(missing_documents)

    return CaseFile(
        client_name=form.full_name,
        visa_type=form.visa_type,
        case_category=case_category,
        missing_documents=missing_documents,
        case_summary=case_summary,
        recommended_next_step=next_step,
        reviewed_by_human=False,
        created_at=datetime.now(),
    )


async def _generate_case_summary(
    client_name: str,
    nationality: str,
    destination: str,
    visa_type: str,
    missing_documents: list[str],
    situation_description: str,
) -> str:
    """Generate a professional case summary in French using Claude API.

    Args:
        client_name: Client's full name.
        nationality: Client's nationality.
        destination: Destination country.
        visa_type: Type of visa.
        missing_documents: List of missing document names.
        situation_description: Client's free-text situation description.

    Returns:
        A 3-4 sentence professional summary in French.
    """
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    # Format missing documents for the prompt
    docs_list = ", ".join(missing_documents) if missing_documents else "aucun document"

    prompt = f"""Rédigez un résumé professionnel en français pour ce dossier:

Client: {client_name}
Nationalité: {nationality}
Destination: {destination}
Type de visa: {visa_type}
Description: {situation_description}
Documents manquants: {docs_list}

Résumé (3-4 phrases max):"""

    message = client.messages.create(
        model="claude-sonnet-4-6-thinking",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )

    summary = message.content[0].text.strip()

    # Clean up if returned with markdown
    if summary.startswith("```"):
        summary = summary.split("```")[1].strip()
    if summary.startswith("fr"):
        summary = summary[2:].strip()

    return summary


def _determine_next_step(missing_documents: list[str]) -> RecommendedNextStep:
    """Determine the recommended next step based on missing documents.

    Args:
        missing_documents: List of missing document names.

    Returns:
        Recommended next step enum value.
    """
    # If too many documents missing, need to gather more
    if len(missing_documents) >= 4:
        return RecommendedNextStep.GATHER_MORE_DOCS

    # If only a few documents missing, still gather more
    if len(missing_documents) >= 1:
        return RecommendedNextStep.GATHER_MORE_DOCS

    # Otherwise, ready to submit
    return RecommendedNextStep.SUBMIT_APPLICATION
