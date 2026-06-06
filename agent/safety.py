"""Safety check module for immigration case analysis."""

import os
import re

import anthropic


def check_safety(situation_description: str, language: str = "en") -> dict:
    """Check if the situation description requires human consultant intervention.

    Args:
        situation_description: The client's free-text description of their situation.
        language: The client's language preference (fr, ar, en).

    Returns:
        Dict with is_safe and redirect_message keys.
    """
    redirect_messages = {
        "fr": "Cette question nécessite l'avis d'un consultant en immigration. Contactez directement votre conseiller.",
        "ar": "هذا السؤال يتطلب رأي مستشار متخصص. يرجى التواصل مع مستشارك مباشرة.",
        "en": "This requires advice from a qualified consultant. Please contact your consultant directly.",
    }

    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    prompt = f"""Analyze this immigration case description and determine if it needs human consultant intervention.

Check for:
1. Legal questions (rights, appeals, refusals, work rights, study rights)
2. Requests for guarantees or predictions ("will I get the visa", "am I eligible")
3. Sensitive content (criminal record, deportation, previous refusals)

Case: {situation_description}

Respond with JSON only:
{{"needs_consultant": true or false}}"""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-6-thinking",
            max_tokens=100,
            messages=[{"role": "user", "content": prompt}]
        )

        response = message.content[0].text.strip()

        if "true" in response.lower():
            return {
                "is_safe": False,
                "redirect_message": redirect_messages.get(language, redirect_messages["en"]),
            }
    except Exception:
        pass

    return {
        "is_safe": True,
        "redirect_message": None,
    }
