"""Document checklist logic based on visa type and destination country."""

from agent.schemas import VisaType


# Required documents per visa type
REQUIRED_DOCUMENTS: dict[VisaType, tuple[str, ...]] = {
    VisaType.STUDENT: (
        "passport",
        "birth_certificate",
        "bank_statements",
        "acceptance_letter",
        "language_certificate",
        "housing_proof",
    ),
    VisaType.WORK: (
        "passport",
        "birth_certificate",
        "bank_statements",
        "employment_proof",
        "work_contract",
        "housing_proof",
    ),
    VisaType.FAMILY_REUNIFICATION: (
        "passport",
        "birth_certificate",
        "bank_statements",
        "marriage_certificate",
        "sponsor_documents",
        "housing_proof",
    ),
    VisaType.TOURIST: (
        "passport",
        "bank_statements",
        "travel_insurance",
        "accommodation_proof",
        "return_ticket",
    ),
}


def get_required_documents(
    visa_type: VisaType, destination_country: str
) -> list[str]:
    """Get the list of required documents for a specific visa type and destination.

    Args:
        visa_type: The type of visa being applied for.
        destination_country: The destination country (currently not used but
            available for future country-specific logic).

    Returns:
        List of required document names for this visa category.
    """
    # Currently destination_country is not used, but kept as parameter
    # for future country-specific document requirements
    _ = destination_country  # Explicitly unused for now

    return list(REQUIRED_DOCUMENTS.get(visa_type, ()))
