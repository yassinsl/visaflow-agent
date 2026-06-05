"""Pydantic models for VisaFlow Agent."""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class VisaType(str, Enum):
    """Possible visa types for immigration cases."""

    STUDENT = "student"
    WORK = "work"
    FAMILY = "family"
    TOURIST = "tourist"


class LanguagePreference(str, Enum):
    """Supported languages for client communication."""

    FR = "fr"
    AR = "ar"
    EN = "en"


class CaseCategory(str, Enum):
    """Detected case categories based on client profile."""

    STUDENT_VISA = "student_visa"
    WORK_PERMIT = "work_permit"
    FAMILY_SPONSORSHIP = "family_sponsorship"
    TOURIST_VISA = "tourist_visa"
    EXPRESS_ENTRY = "express_entry"
    PROVINCIAL_NOMINEE = "provincial_nominee"
    OTHER = "other"


class RecommendedNextStep(str, Enum):
    """Recommended next steps for the case."""

    SUBMIT_APPLICATION = "submit_application"
    GATHER_MORE_DOCS = "gather_more_docs"
    SCHEDULE_CONSULTATION = "schedule_consultation"
    PENDING_REVIEW = "pending_review"


class IntakeForm(BaseModel):
    """Model representing client intake form submission.

    Contains personal information, contact details, case information,
    document checklist, and a free-text description of the client's situation.
    """

    # Personal Information
    full_name: str = Field(..., description="Client's full legal name")
    nationality: str = Field(..., description="Client's nationality")
    date_of_birth: str = Field(..., description="Date of birth in YYYY-MM-DD format")

    # Contact Information
    email: str = Field(..., description="Client's email address")
    phone_number: str = Field(..., description="International phone number with country code")

    # Case Information
    destination_country: str = Field(..., description="Country the client wants to immigrate to")
    visa_type: VisaType = Field(..., description="Type of visa being applied for")

    # Documents already provided (boolean checklist)
    has_passport: bool = Field(default=False, description="Client has a valid passport")
    has_birth_certificate: bool = Field(default=False, description="Client has birth certificate")
    has_bank_statements: bool = Field(default=False, description="Client has bank statements")
    has_employment_proof: bool = Field(default=False, description="Client has employment proof")
    has_housing_proof: bool = Field(default=False, description="Client has housing proof")

    # Free text description of situation
    situation_description: str = Field(
        ...,
        min_length=10,
        description="Client describes their situation in French, Arabic, or English"
    )

    # Language preference
    language_preference: LanguagePreference = Field(
        default=LanguagePreference.FR,
        description="Preferred language for communication (fr/ar/en)"
    )


class CaseFile(BaseModel):
    """Model representing the structured case file returned by the agent.

    Contains client information, detected case category, missing documents,
    agent-generated summary, recommended next steps, and metadata.
    """

    # Client identification
    client_name: str = Field(..., description="Client's full name")
    visa_type: VisaType = Field(..., description="Type of visa being applied for")

    # Agent analysis
    case_category: CaseCategory = Field(
        ...,
        description="Detected case category based on client profile"
    )
    missing_documents: list[str] = Field(
        default_factory=list,
        description="List of documents still needed for the application"
    )
    case_summary: str = Field(
        ...,
        description="Summary of the case written by the agent"
    )
    recommended_next_step: RecommendedNextStep = Field(
        ...,
        description="Recommended next step for this case"
    )

    # Metadata
    reviewed_by_human: bool = Field(
        default=False,
        description="Flag indicating if case has been reviewed by a human"
    )
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="Timestamp of when the case file was created"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "client_name": "John Doe",
                "visa_type": "student",
                "case_category": "student_visa",
                "missing_documents": ["bank_statements", "housing_proof"],
                "case_summary": "Client is a 24-year-old from Morocco applying for a student visa...",
                "recommended_next_step": "gather_more_docs",
                "reviewed_by_human": False,
                "created_at": "2026-06-05T10:30:00"
            }
        }
    }
