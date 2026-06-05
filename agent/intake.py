"""Intake agent that processes client forms using Claude API."""

import json
import os
from typing import Any

from anthropic import Anthropic


def process_intake_form(form_data: dict[str, Any]) -> dict[str, Any]:
    """
    Process a client intake form and generate a structured case file.

    Args:
        form_data: Dictionary containing the intake form fields.

    Returns:
        A structured case file with client info, missing documents, summary,
        next steps, and language used.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is not set")

    client = Anthropic(api_key=api_key)

    # Extract form fields for the prompt
    full_name = form_data.get("full_name", "")
    nationality = form_data.get("nationality", "")
    destination = form_data.get("destination_country", "")
    visa_type = form_data.get("visa_type", "")
    language = form_data.get("language", "fr")

    # Map language code to full name
    lang_map = {"fr": "French", "ar": "Arabic", "en": "English"}
    lang_name = lang_map.get(language, "French")

    # List of documents the client has
    documents_provided = []
    if form_data.get("has_passport"):
        documents_provided.append("passport")
    if form_data.get("has_birth_certificate"):
        documents_provided.append("birth certificate")
    if form_data.get("has_bank_statements"):
        documents_provided.append("bank statements")
    if form_data.get("has_employment_proof"):
        documents_provided.append("employment proof")

    # Build the prompt for Claude
    prompt = f"""You are an immigration consultant assistant. Your task is to analyze a client intake form and generate a structured case file.

## Client Information
- Full Name: {full_name}
- Nationality: {nationality}
- Destination Country: {destination}
- Visa Type: {visa_type}
- Language: {lang_name}

## Documents Provided
{', '.join(documents_provided) if documents_provided else "No documents provided"}

## Your Task
Analyze this case and return a JSON object with the following structure:
```json
{{
    "client_name": "string",
    "visa_type": "string",
    "destination": "string",
    "missing_documents": ["list of missing documents"],
    "case_summary": "short 1-2 sentence summary",
    "next_step": "recommendation for the consultant",
    "language_used": "language used in the response"
}}
```

Determine which documents are typically required for a {visa_type} to {destination} and identify what's missing. Provide practical next steps.

Respond ONLY with valid JSON, no additional text."""

    # Call Claude API
    message = client.messages.create(
        model="claude-sonnet-4-6-thinking",
        max_tokens=1024,
        system="You are an expert immigration consultant assistant. You analyze client intake forms and generate structured case files with missing document checklists and next steps.",
        messages=[{"role": "user", "content": prompt}],
    )

    # Parse the JSON response
    response_text = message.content[0].text.strip()

    # Extract JSON from response (in case Claude wraps it in markdown)
    if "```json" in response_text:
        json_start = response_text.find("```json") + 7
        json_end = response_text.find("```", json_start)
        response_text = response_text[json_start:json_end].strip()
    elif "```" in response_text:
        json_start = response_text.find("```") + 3
        json_end = response_text.find("```", json_start)
        response_text = response_text[json_start:json_end].strip()

    result = json.loads(response_text)

    # Ensure language_used is set
    if "language_used" not in result:
        result["language_used"] = lang_name

    return result
