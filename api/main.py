"""FastAPI application for VisaFlow Agent."""

from datetime import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from agent.schemas import IntakeForm as SchemaIntakeForm, CaseFile, VisaType, LanguagePreference
from agent.builder import build_case_file

app = FastAPI(
    title="VisaFlow Agent",
    description="AI agent for immigration consultants - collects client info and generates case files",
    version="1.0.0",
)


class IntakeForm(BaseModel):
    """Client intake form data."""

    full_name: str = Field(..., description="Full name of the client")
    nationality: str = Field(..., description="Country of nationality")
    date_of_birth: str = Field(..., description="Date of birth in YYYY-MM-DD format")
    email: str = Field(..., description="Client's email address")
    phone: str = Field(..., description="Client's phone number")
    destination_country: str = Field(..., description="Country where visa is being applied")
    visa_type: str = Field(..., description="Type of visa being applied for")
    has_passport: bool = Field(default=False, description="Client has a valid passport")
    has_birth_certificate: bool = Field(default=False, description="Client has birth certificate")
    has_bank_statements: bool = Field(default=False, description="Client has bank statements")
    has_employment_proof: bool = Field(default=False, description="Client has employment proof")
    has_housing_proof: bool = Field(default=False, description="Client has housing proof")
    situation_description: str = Field(..., description="Client describes their situation")
    language: str = Field(default="fr", description="Preferred language: fr, ar, or en")


@app.get("/")
def root() -> dict:
    """Root endpoint for health check."""
    return {"status": "ok", "service": "VisaFlow Agent"}


@app.post("/intake")
async def intake(form: IntakeForm) -> dict:
    """
    Process a client intake form and generate a structured case file.

    Args:
        form: The intake form with client information and available documents.

    Returns:
        A structured case file with missing documents, summary, and recommendations.
    """
    try:
        # Convert to schema IntakeForm with proper enum values
        schema_form = SchemaIntakeForm(
            full_name=form.full_name,
            nationality=form.nationality,
            date_of_birth=form.date_of_birth,
            email=form.email,
            phone_number=form.phone,
            destination_country=form.destination_country,
            visa_type=VisaType(form.visa_type),
            has_passport=form.has_passport,
            has_birth_certificate=form.has_birth_certificate,
            has_bank_statements=form.has_bank_statements,
            has_employment_proof=form.has_employment_proof,
            has_housing_proof=form.has_housing_proof,
            situation_description=form.situation_description,
            language_preference=LanguagePreference(form.language),
        )

        # Build the case file
        case_file = await build_case_file(schema_form)
        return case_file.model_dump(mode="json")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing intake: {str(e)}")
