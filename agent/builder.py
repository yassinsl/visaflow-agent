"""Case file builder that orchestrates the classification and document detection."""

import json
from datetime import datetime

from agent.classifier import classify_case
from agent.schemas import CaseFile, CaseCategory, IntakeForm
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

    # Extract detected language for multilingual support
    detected_language = classification.get("language_detected", "en")

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

    # Step 4: Generate case summary using Python template
    case_summary = _generate_case_summary(
        client_name=form.full_name,
        nationality=form.nationality,
        destination=form.destination_country,
        visa_type=form.visa_type.value,
        missing_documents=missing_documents,
        language=detected_language,
    )

    # Step 5: Determine recommended next step
    next_step = _determine_next_step(missing_documents, detected_language)

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


def _generate_case_summary(
    client_name: str,
    nationality: str,
    destination: str,
    visa_type: str,
    missing_documents: list[str],
    language: str = "en",
) -> str:
    """Generate a case summary using Python templates.

    Args:
        client_name: Client's full name.
        nationality: Client's nationality.
        destination: Destination country.
        visa_type: Type of visa.
        missing_documents: List of missing document names.
        language: Detected language (fr, ar, or en).

    Returns:
        A professional summary in the detected language.
    """
    # Format missing documents
    docs_list = ", ".join(missing_documents) if missing_documents else "none"

    # Language-specific templates
    templates = {
        "fr": "{client_name} est un(e) ressortissant(e) {nationality} souhaitant obtenir un visa {visa_type} pour {destination}. Documents manquants: {missing_docs}. Veuillez rassembler ces documents avant de soumettre le dossier.",
        "ar": "{client_name} مواطن/ة من {nationality} يرغب في الحصول على تأشيرة {visa_type} إلى {destination}. الوثائق الناقصة: {missing_docs}. يرجى جمع هذه الوثائق قبل تقديم الملف.",
        "en": "{client_name} is a {nationality} national seeking a {visa_type} visa to {destination}. Missing documents: {missing_docs}. Please gather these documents before submitting the file.",
    }

    template = templates.get(language, templates["en"])

    return template.format(
        client_name=client_name,
        nationality=nationality,
        destination=destination,
        visa_type=visa_type,
        missing_docs=docs_list,
    )


def _determine_next_step(missing_documents: list[str], language: str = "en") -> str:
    """Determine the recommended next step in the client's language.

    Args:
        missing_documents: List of missing document names.
        language: Detected language (fr, ar, or en).

    Returns:
        Human-readable next step sentence in the detected language.
    """
    # Multilingual next step messages
    next_step_messages = {
        "fr": {
            "gather": "Rassembler les documents manquants avant de soumettre le dossier",
            "submit": "Le dossier est prêt à être soumis",
        },
        "ar": {
            "gather": "جمع الوثائق الناقصة قبل تقديم الملف",
            "submit": "الملف جاهز للتقديم",
        },
        "en": {
            "gather": "Gather the missing documents before submitting the file",
            "submit": "The file is ready to be submitted",
        },
    }

    messages = next_step_messages.get(language, next_step_messages["en"])

    if len(missing_documents) >= 1:
        return messages["gather"]
    return messages["submit"]
