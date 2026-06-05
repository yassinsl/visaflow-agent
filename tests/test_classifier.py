"""Tests for the classify_case function in agent/classifier.py."""

import pytest

from agent.classifier import classify_case


@pytest.mark.asyncio
async def test_french_student():
    """Test French student case classification."""
    result = await classify_case(
        situation_description="Je souhaite poursuivre mes études de master en informatique au Canada l'année prochaine",
        visa_type="student"
    )

    print(f"Result: {result}")

    assert result["detected_case_category"] == "student", (
        f"Expected 'student', got '{result['detected_case_category']}'"
    )


@pytest.mark.asyncio
async def test_french_work():
    """Test French work case classification."""
    result = await classify_case(
        situation_description="J'ai reçu une offre d'emploi d'une entreprise canadienne et je veux obtenir un permis de travail",
        visa_type="work"
    )

    print(f"Result: {result}")

    assert result["detected_case_category"] == "work", (
        f"Expected 'work', got '{result['detected_case_category']}'"
    )


@pytest.mark.asyncio
async def test_arabic_family():
    """Test Arabic family reunification case classification."""
    result = await classify_case(
        situation_description="زوجي يقيم في كندا وأريد الالتحاق به مع أطفالنا",
        visa_type="family"
    )

    print(f"Result: {result}")

    assert result["detected_case_category"] == "family_reunification", (
        f"Expected 'family_reunification', got '{result['detected_case_category']}'"
    )


@pytest.mark.asyncio
async def test_english_tourist():
    """Test English tourist case classification."""
    result = await classify_case(
        situation_description="I want to visit my friend in Paris for two weeks this summer",
        visa_type="tourist"
    )

    print(f"Result: {result}")

    assert result["detected_case_category"] == "tourist", (
        f"Expected 'tourist', got '{result['detected_case_category']}'"
    )


@pytest.mark.asyncio
async def test_french_ambiguous_low_confidence():
    """Test French ambiguous case should have low or medium confidence."""
    result = await classify_case(
        situation_description="Je veux partir à l'étranger pour améliorer ma situation",
        visa_type="tourist"
    )

    print(f"Result: {result}")

    assert result["detected_case_category"] in {
        "student", "work", "family_reunification", "tourist"
    }, f"Invalid category: {result['detected_case_category']}"

    assert result["confidence"] != "high", (
        f"Expected confidence to be low or medium, got '{result['confidence']}'"
    )
