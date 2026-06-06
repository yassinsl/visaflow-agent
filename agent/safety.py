"""Safety check module for immigration case analysis."""

import re


def check_safety(situation_description: str, language: str = "en") -> dict:
    """Check if situation requires human consultant intervention."""
    redirect_messages = {
        "fr": "Cette question nécessite l'avis d'un consultant en immigration. Contactez directement votre conseiller.",
        "ar": "هذا السؤال يتطلب رأي مستشار متخصص. يرجى التواصل مع مستشارك مباشرة.",
        "en": "This requires advice from a qualified consultant. Please contact your consultant directly.",
    }

    UNSAFE_KEYWORDS = [
        "travailler", "travail pendant", "can i work",
        "eligible", "éligible", "accepté", "accepted",
        "refusé", "refused", "rejected", "chances",
        "garantie", "guarantee", "criminal", "criminel",
        "deportation", "expulsion", "previous refusal",
        "refus antérieur", "am i allowed", "puis-je",
        "will they", "est-ce qu'ils", "هل يمكنني",
        "هل سيقبلون", "ضمان", "رفض سابق",
        "droit de", "droits", "rights", "حقوق",
        "appel", "appeal", "طعن",
        "refus", "refusal", "رفض",
    ]

    text_lower = situation_description.lower()

    for keyword in UNSAFE_KEYWORDS:
        if keyword in text_lower:
            return {
                "is_safe": False,
                "redirect_message": redirect_messages.get(language, redirect_messages["en"]),
            }

    return {
        "is_safe": True,
        "redirect_message": None,
    }
