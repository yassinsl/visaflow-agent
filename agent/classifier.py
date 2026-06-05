"""Case classifier using Claude API."""

import json
import os
from typing import Any

import anthropic


async def classify_case(situation_description: str, visa_type: str) -> dict[str, Any]:
    """Classify the immigration case based on the client's situation description.

    Sends the situation description to Claude API which acts as an expert
    immigration consultant to analyze and classify the case.

    Args:
        situation_description: Free text describing the client's situation
            in French, Arabic, or English.
        visa_type: The visa type from the intake form (student/work/family/tourist).

    Returns:
        A dictionary containing:
        - detected_case_category: student, work, family_reunification, or tourist
        - confidence: high, medium, or low
        - key_signals: list of words/phrases that led to classification
        - language_detected: fr, ar, or en
    """
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    system_prompt = """You are an expert immigration consultant specializing in Canadian and North American immigration cases.
Your task is to analyze the client's situation description and classify their case.

Read the text carefully and return ONLY a JSON object (no other text) with these exact fields:
- detected_case_category: one of "student", "work", "family_reunification", "tourist"
- confidence: "high", "medium", or "low" - based on how clear the signals are
- key_signals: a list of words or phrases from the text that support this classification
- language_detected: "fr" for French, "ar" for Arabic, "en" for English

Analyze linguistic cues to determine the language - look for French words (le, la, les, etre, avoir, etc.),
Arabic script characters, or English words.

Example output format:
{"detected_case_category": "student", "confidence": "high", "key_signals": ["university", "study permit", "fall 2025"], "language_detected": "en"}"""

    user_message = f"""Analyze this immigration case description and return ONLY JSON:

Visa type from form: {visa_type}

Client's situation description:
{situation_description}

Return ONLY JSON, no other text."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=500,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}]
        )

        response_text = message.content[0].text.strip()

        # Try to parse as JSON
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

        return {
            "detected_case_category": result.get("detected_case_category", "student")
            if result.get("detected_case_category") in valid_categories
            else "student",
            "confidence": result.get("confidence", "low")
            if result.get("confidence") in valid_confidence
            else "low",
            "key_signals": result.get("key_signals", []),
            "language_detected": result.get("language_detected", "en")
            if result.get("language_detected") in valid_languages
            else "en",
        }

    except (json.JSONDecodeError, KeyError, ValueError) as e:
        # Return safe default on any parsing failure
        return {
            "detected_case_category": "student",
            "confidence": "low",
            "key_signals": [],
            "language_detected": "en",
        }
    except Exception:
        # Return safe default on any other error
        return {
            "detected_case_category": "student",
            "confidence": "low",
            "key_signals": [],
            "language_detected": "en",
        }
