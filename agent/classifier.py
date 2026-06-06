"""Case classifier using Claude API.

Classifies immigration cases by analyzing the client's situation description
and extracting key signals and detected language.
"""

import json
import os
from typing import Any

import anthropic


async def classify_case(situation_description: str, visa_type: str) -> dict[str, Any]:
    """Classify immigration case using Claude API based on situation description."""
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    # Normalize visa_type to full category name - THIS IS THE PRIMARY SIGNAL
    visa_type_mapping = {
        "student": "student",
        "work": "work",
        "family": "family_reunification",
        "family_reunification": "family_reunification",
        "tourist": "tourist",
    }
    normalized_visa_type = visa_type_mapping.get(visa_type, "student")

    # Detect strong contradictions in text
    study_keywords = ["etudier", "etudes", "university", "studies", "school", "master", "student", "permit etudes", "cours", "studying", "university"]
    work_keywords = ["travail", "work", "job", "employment", "salary", "employer", "offre", "contrat", "permit de travail"]
    family_keywords = ["spouse", "conjoint", "époux", "épouse", "enfants", "children", "family", "mariage", "join"]

    has_study = any(kw in situation_description.lower() for kw in study_keywords)
    has_work = any(kw in situation_description.lower() for kw in work_keywords)
    has_family = any(kw in situation_description.lower() for kw in family_keywords)

    # Apply contradiction logic - only override if STRONG contradiction
    final_category = normalized_visa_type
    if normalized_visa_type == "work" and has_study and not has_work:
        final_category = "student"

    # System prompt - ask only for key signals and language, NOT category
    system_prompt = """Analyze this immigration case text. Return ONLY valid JSON.

Output ONLY language detected and key signals. DO NOT output detected_case_category - it will be provided separately.
JSON format:
{"key_signals": ["word1", "word2"], "language_detected": "fr|en|ar", "had_study_keywords": true/false, "had_work_keywords": true/false}"""

    user_message = f"""Text to classify: {situation_description}

Output ONLY this JSON, no other text:
{{"detected_case_category": "", "confidence": "", "key_signals": [], "language_detected": ""}}"""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-6-thinking",
            max_tokens=500,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}]
        )

        response_text = message.content[0].text.strip()

        # Handle potential markdown code blocks
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]

        result = json.loads(response_text.strip())

        # Validate and normalize the response
        valid_categories = {"student", "work", "family_reunification", "tourist"}
        valid_confidence = {"high", "medium", "low"}
        valid_languages = {"fr", "ar", "en"}

        # Determine confidence based on how well text matches the category
        # Use normalized_visa_type as primary, LLM only辅助
        key_signals = result.get("key_signals", [])
        had_study = result.get("had_study_keywords", False)
        had_work = result.get("had_work_keywords", False)

        # High confidence only if text aligns with visa_type
        confidence = "medium"
        if final_category == normalized_visa_type:
            if (has_study and final_category == "student") or (has_work and final_category == "work") or (has_family and final_category == "family_reunification"):
                confidence = "high"
        elif has_study or has_work or has_family:
            confidence = "medium"
        else:
            confidence = "low"

        return {
            "detected_case_category": final_category,
            "confidence": result.get("confidence", confidence)
            if result.get("confidence") in valid_confidence
            else confidence,
            "key_signals": key_signals,
            "language_detected": result.get("language_detected", "en")
            if result.get("language_detected") in valid_languages
            else "en",
        }

    except (json.JSONDecodeError, KeyError, ValueError) as e:
        # Return safe default on any parsing failure
        return {
            "detected_case_category": final_category,
            "confidence": "low",
            "key_signals": [],
            "language_detected": "en",
        }
    except Exception:
        # Return safe default on any other error
        return {
            "detected_case_category": final_category,
            "confidence": "low",
            "key_signals": [],
            "language_detected": "en",
        }
