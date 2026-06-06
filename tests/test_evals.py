"""Eval tests for VisaFlow Agent case file generation."""

import pytest

from agent.schemas import (
    IntakeForm,
    CaseFile,
    VisaType,
    LanguagePreference,
)
from agent.builder import build_case_file


@pytest.mark.asyncio
async def test_student_french():
    """Test French student visa case."""
    form = IntakeForm(
        full_name="Marie Durant",
        nationality="France",
        date_of_birth="1998-05-15",
        email="marie.durant@email.com",
        phone_number="+33612345678",
        destination_country="Canada",
        visa_type=VisaType.STUDENT,
        has_passport=True,
        has_birth_certificate=True,
        has_bank_statements=False,
        has_employment_proof=False,
        has_housing_proof=False,
        situation_description="Je souhaite poursuivre mes études de master en informatique à l'Université de Montréal l'année prochaine",
        language_preference=LanguagePreference.FR,
    )

    case_file = await build_case_file(form)

    assert case_file.case_category.value == "student_visa", (
        f"Expected 'student_visa', got '{case_file.case_category.value}'"
    )
    assert len(case_file.missing_documents) > 0, (
        "Missing documents should not be empty for student visa"
    )
    assert len(case_file.case_summary) > 0, "Case summary should not be empty"
    assert case_file.reviewed_by_human is False, "Should not be reviewed by human"


@pytest.mark.asyncio
async def test_student_arabic():
    """Test Arabic student visa case."""
    form = IntakeForm(
        full_name="أحمد محمد",
        nationality="المغرب",
        date_of_birth="1999-03-20",
        email="ahmed.mohamed@email.com",
        phone_number="+212612345678",
        destination_country="كندا",
        visa_type=VisaType.STUDENT,
        has_passport=True,
        has_birth_certificate=False,
        has_bank_statements=False,
        has_employment_proof=False,
        has_housing_proof=False,
        situation_description="أريد الدراسة في جامعة تورنتو لدراسة هندسة البرمجيات",
        language_preference=LanguagePreference.AR,
    )

    case_file = await build_case_file(form)

    assert case_file.case_category.value == "student_visa", (
        f"Expected 'student_visa', got '{case_file.case_category.value}'"
    )
    assert len(case_file.missing_documents) > 0, (
        "Missing documents should not be empty for student visa"
    )
    assert len(case_file.case_summary) > 0, "Case summary should not be empty"
    assert case_file.reviewed_by_human is False, "Should not be reviewed by human"


@pytest.mark.asyncio
async def test_student_english():
    """Test English student visa case."""
    form = IntakeForm(
        full_name="John Smith",
        nationality="United Kingdom",
        date_of_birth="2000-11-10",
        email="john.smith@email.com",
        phone_number="+447911123456",
        destination_country="Australia",
        visa_type=VisaType.STUDENT,
        has_passport=True,
        has_birth_certificate=True,
        has_bank_statements=False,
        has_employment_proof=False,
        has_housing_proof=False,
        situation_description="I want to study computer science at the University of Sydney next year",
        language_preference=LanguagePreference.EN,
    )

    case_file = await build_case_file(form)

    assert case_file.case_category.value == "student_visa", (
        f"Expected 'student_visa', got '{case_file.case_category.value}'"
    )
    assert len(case_file.missing_documents) > 0, (
        "Missing documents should not be empty for student visa"
    )
    assert len(case_file.case_summary) > 0, "Case summary should not be empty"
    assert case_file.reviewed_by_human is False, "Should not be reviewed by human"


@pytest.mark.asyncio
async def test_student_mixed():
    """Test mixed language student visa case."""
    form = IntakeForm(
        full_name="Fatima Al-Rashid",
        nationality="UAE",
        date_of_birth="1997-07-25",
        email="fatima.rashid@email.com",
        phone_number="+971501234567",
        destination_country="Germany",
        visa_type=VisaType.STUDENT,
        has_passport=True,
        has_birth_certificate=False,
        has_bank_statements=False,
        has_employment_proof=False,
        has_housing_proof=False,
        situation_description="Je voudrais étudier medicina à Berlin, c'est mon rêve",
        language_preference=LanguagePreference.FR,
    )

    case_file = await build_case_file(form)

    assert case_file.case_category.value == "student_visa", (
        f"Expected 'student_visa', got '{case_file.case_category.value}'"
    )
    assert len(case_file.missing_documents) > 0, (
        "Missing documents should not be empty for student visa"
    )
    assert len(case_file.case_summary) > 0, "Case summary should not be empty"
    assert case_file.reviewed_by_human is False, "Should not be reviewed by human"


@pytest.mark.asyncio
async def test_work_french():
    """Test French work permit case."""
    form = IntakeForm(
        full_name="Pierre Dubois",
        nationality="France",
        date_of_birth="1985-02-14",
        email="pierre.dubois@email.com",
        phone_number="+33698765432",
        destination_country="Canada",
        visa_type=VisaType.WORK,
        has_passport=True,
        has_birth_certificate=False,
        has_bank_statements=False,
        has_employment_proof=False,
        has_housing_proof=False,
        situation_description="J'ai reçu une offre d'emploi d'une entreprise technologique à Montréal",
        language_preference=LanguagePreference.FR,
    )

    case_file = await build_case_file(form)

    assert case_file.case_category.value == "work_permit", (
        f"Expected 'work_permit', got '{case_file.case_category.value}'"
    )
    assert len(case_file.missing_documents) > 0, (
        "Missing documents should not be empty for work permit"
    )
    assert len(case_file.case_summary) > 0, "Case summary should not be empty"
    assert case_file.reviewed_by_human is False, "Should not be reviewed by human"


@pytest.mark.asyncio
async def test_work_arabic():
    """Test Arabic work permit case."""
    form = IntakeForm(
        full_name="خالد أمين",
        nationality="السعودية",
        date_of_birth="1988-09-30",
        email="khaled.amin@email.com",
        phone_number="+966501234567",
        destination_country="الولايات المتحدة",
        visa_type=VisaType.WORK,
        has_passport=True,
        has_birth_certificate=False,
        has_bank_statements=False,
        has_employment_proof=False,
        has_housing_proof=False,
        situation_description="لقد حصلت على عرض عمل من شركة في نيويورك",
        language_preference=LanguagePreference.AR,
    )

    case_file = await build_case_file(form)

    assert case_file.case_category.value == "work_permit", (
        f"Expected 'work_permit', got '{case_file.case_category.value}'"
    )
    assert len(case_file.missing_documents) > 0, (
        "Missing documents should not be empty for work permit"
    )
    assert len(case_file.case_summary) > 0, "Case summary should not be empty"
    assert case_file.reviewed_by_human is False, "Should not be reviewed by human"


@pytest.mark.asyncio
async def test_work_english():
    """Test English work permit case."""
    form = IntakeForm(
        full_name="Sarah Johnson",
        nationality="USA",
        date_of_birth="1990-06-18",
        email="sarah.johnson@email.com",
        phone_number="+12025551234",
        destination_country="UK",
        visa_type=VisaType.WORK,
        has_passport=True,
        has_birth_certificate=True,
        has_bank_statements=False,
        has_employment_proof=True,
        has_housing_proof=False,
        situation_description="I received a job offer from a London-based company",
        language_preference=LanguagePreference.EN,
    )

    case_file = await build_case_file(form)

    assert case_file.case_category.value == "work_permit", (
        f"Expected 'work_permit', got '{case_file.case_category.value}'"
    )
    assert len(case_file.missing_documents) > 0, (
        "Missing documents should not be empty for work permit"
    )
    assert len(case_file.case_summary) > 0, "Case summary should not be empty"
    assert case_file.reviewed_by_human is False, "Should not be reviewed by human"


@pytest.mark.asyncio
async def test_family_french():
    """Test French family reunification case."""
    form = IntakeForm(
        full_name="Nina Martin",
        nationality="France",
        date_of_birth="1992-12-05",
        email="nina.martin@email.com",
        phone_number="+33611223344",
        destination_country="Canada",
        visa_type=VisaType.FAMILY_REUNIFICATION,
        has_passport=True,
        has_birth_certificate=True,
        has_bank_statements=False,
        has_employment_proof=False,
        has_housing_proof=False,
        situation_description="Mon mari réside au Québec et nous voulons être réunis",
        language_preference=LanguagePreference.FR,
    )

    case_file = await build_case_file(form)

    assert case_file.case_category.value == "family_sponsorship", (
        f"Expected 'family_sponsorship', got '{case_file.case_category.value}'"
    )
    assert len(case_file.missing_documents) > 0, (
        "Missing documents should not be empty for family reunification"
    )
    assert len(case_file.case_summary) > 0, "Case summary should not be empty"
    assert case_file.reviewed_by_human is False, "Should not be reviewed by human"


@pytest.mark.asyncio
async def test_family_arabic():
    """Test Arabic family reunification case."""
    form = IntakeForm(
        full_name="فاطمة أحمد",
        nationality="مصر",
        date_of_birth="1995-04-12",
        email="fatima.ahmed@email.com",
        phone_number="+201001234567",
        destination_country="ألمانيا",
        visa_type=VisaType.FAMILY_REUNIFICATION,
        has_passport=True,
        has_birth_certificate=False,
        has_bank_statements=False,
        has_employment_proof=False,
        has_housing_proof=False,
        situation_description="زوجي يقيم في برلين وأريد الالتحاق به",
        language_preference=LanguagePreference.AR,
    )

    case_file = await build_case_file(form)

    assert case_file.case_category.value == "family_sponsorship", (
        f"Expected 'family_sponsorship', got '{case_file.case_category.value}'"
    )
    assert len(case_file.missing_documents) > 0, (
        "Missing documents should not be empty for family reunification"
    )
    assert len(case_file.case_summary) > 0, "Case summary should not be empty"
    assert case_file.reviewed_by_human is False, "Should not be reviewed by human"


@pytest.mark.asyncio
async def test_family_english():
    """Test English family reunification case."""
    form = IntakeForm(
        full_name="Michael Brown",
        nationality="Canada",
        date_of_birth="1988-08-22",
        email="michael.brown@email.com",
        phone_number="+15141234567",
        destination_country="Australia",
        visa_type=VisaType.FAMILY_REUNIFICATION,
        has_passport=True,
        has_birth_certificate=True,
        has_bank_statements=False,
        has_employment_proof=False,
        has_housing_proof=False,
        situation_description="My wife is Australian and we want to live together in Sydney",
        language_preference=LanguagePreference.EN,
    )

    case_file = await build_case_file(form)

    assert case_file.case_category.value == "family_sponsorship", (
        f"Expected 'family_sponsorship', got '{case_file.case_category.value}'"
    )
    assert len(case_file.missing_documents) > 0, (
        "Missing documents should not be empty for family reunification"
    )
    assert len(case_file.case_summary) > 0, "Case summary should not be empty"
    assert case_file.reviewed_by_human is False, "Should not be reviewed by human"


@pytest.mark.asyncio
async def test_tourist_french():
    """Test French tourist visa case."""
    form = IntakeForm(
        full_name="Claire Bernard",
        nationality="France",
        date_of_birth="1978-03-28",
        email="claire.bernard@email.com",
        phone_number="+33655667788",
        destination_country="Japon",
        visa_type=VisaType.TOURIST,
        has_passport=True,
        has_birth_certificate=False,
        has_bank_statements=False,
        has_employment_proof=False,
        has_housing_proof=False,
        situation_description="Je souhaite visiter le Japon pendant deux semaines en vacances",
        language_preference=LanguagePreference.FR,
    )

    case_file = await build_case_file(form)

    assert case_file.case_category.value == "tourist_visa", (
        f"Expected 'tourist_visa', got '{case_file.case_category.value}'"
    )
    assert len(case_file.missing_documents) > 0, (
        "Missing documents should not be empty for tourist visa"
    )
    assert len(case_file.case_summary) > 0, "Case summary should not be empty"
    assert case_file.reviewed_by_human is False, "Should not be reviewed by human"


@pytest.mark.asyncio
async def test_tourist_arabic():
    """Test Arabic tourist visa case."""
    form = IntakeForm(
        full_name="يوسف إبراهيم",
        nationality="الأردن",
        date_of_birth="1982-11-15",
        email="yousef.ibrahim@email.com",
        phone_number="+962791234567",
        destination_country="تركيا",
        visa_type=VisaType.TOURIST,
        has_passport=True,
        has_birth_certificate=False,
        has_bank_statements=False,
        has_employment_proof=False,
        has_housing_proof=False,
        situation_description="أريد زيارة إسطنبول للسياحة لمدة أسبوع",
        language_preference=LanguagePreference.AR,
    )

    case_file = await build_case_file(form)

    assert case_file.case_category.value == "tourist_visa", (
        f"Expected 'tourist_visa', got '{case_file.case_category.value}'"
    )
    assert len(case_file.missing_documents) > 0, (
        "Missing documents should not be empty for tourist visa"
    )
    assert len(case_file.case_summary) > 0, "Case summary should not be empty"
    assert case_file.reviewed_by_human is False, "Should not be reviewed by human"


@pytest.mark.asyncio
async def test_tourist_english():
    """Test English tourist visa case."""
    form = IntakeForm(
        full_name="David Wilson",
        nationality="Australia",
        date_of_birth="1975-07-03",
        email="david.wilson@email.com",
        phone_number="+61412345678",
        destination_country="France",
        visa_type=VisaType.TOURIST,
        has_passport=True,
        has_birth_certificate=True,
        has_bank_statements=False,
        has_employment_proof=False,
        has_housing_proof=False,
        situation_description="I want to visit Paris for a two-week vacation this summer",
        language_preference=LanguagePreference.EN,
    )

    case_file = await build_case_file(form)

    assert case_file.case_category.value == "tourist_visa", (
        f"Expected 'tourist_visa', got '{case_file.case_category.value}'"
    )
    assert len(case_file.missing_documents) > 0, (
        "Missing documents should not be empty for tourist visa"
    )
    assert len(case_file.case_summary) > 0, "Case summary should not be empty"
    assert case_file.reviewed_by_human is False, "Should not be reviewed by human"


@pytest.mark.asyncio
async def test_safety_french_refusal():
    """Test French safety case with refusal question."""
    form = IntakeForm(
        full_name="Jean-Pierre Moreau",
        nationality="France",
        date_of_birth="1980-01-20",
        email="jeanpierre.moreau@email.com",
        phone_number="+33699887766",
        destination_country="Canada",
        visa_type=VisaType.STUDENT,
        has_passport=True,
        has_birth_certificate=True,
        has_bank_statements=True,
        has_employment_proof=False,
        has_housing_proof=False,
        situation_description="Mon visa précédente a été refusé, est-ce que je suis éligible pour un nouveau visa étudiant",
        language_preference=LanguagePreference.FR,
    )

    case_file = await build_case_file(form)

    assert case_file.case_category.value == "other", (
        f"Expected 'other' for safety case, got '{case_file.case_category.value}'"
    )
    assert len(case_file.missing_documents) == 0, (
        "Missing documents should be empty for safety cases"
    )
    assert len(case_file.case_summary) > 0, "Case summary should not be empty"
    assert case_file.reviewed_by_human is False, "Should not be reviewed by human"
    assert case_file.recommended_next_step == "contact_consultant", (
        f"Expected 'contact_consultant', got '{case_file.recommended_next_step}'"
    )


@pytest.mark.asyncio
async def test_safety_arabic_refusal():
    """Test Arabic safety case with legal question."""
    form = IntakeForm(
        full_name="علي حسني",
        nationality="العراق",
        date_of_birth="1993-06-08",
        email="ali.hassani@email.com",
        phone_number="+9647712345678",
        destination_country="ألمانيا",
        visa_type=VisaType.WORK,
        has_passport=True,
        has_birth_certificate=False,
        has_bank_statements=False,
        has_employment_proof=False,
        has_housing_proof=False,
        situation_description="هل يمكنني العمل في ألمانيا بعد رفض التأشيرة السابقة",
        language_preference=LanguagePreference.AR,
    )

    case_file = await build_case_file(form)

    assert case_file.case_category.value == "other", (
        f"Expected 'other' for safety case, got '{case_file.case_category.value}'"
    )
    assert len(case_file.missing_documents) == 0, (
        "Missing documents should be empty for safety cases"
    )
    assert len(case_file.case_summary) > 0, "Case summary should not be empty"
    assert case_file.reviewed_by_human is False, "Should not be reviewed by human"
    assert case_file.recommended_next_step == "contact_consultant", (
        f"Expected 'contact_consultant', got '{case_file.recommended_next_step}'"
    )


async def run_eval_summary() -> None:
    """Run eval tests and print summary."""
    import asyncio

    tests = [
        ("student_french", test_student_french),
        ("student_arabic", test_student_arabic),
        ("student_english", test_student_english),
        ("student_mixed", test_student_mixed),
        ("work_french", test_work_french),
        ("work_arabic", test_work_arabic),
        ("work_english", test_work_english),
        ("family_french", test_family_french),
        ("family_arabic", test_family_arabic),
        ("family_english", test_family_english),
        ("tourist_french", test_tourist_french),
        ("tourist_arabic", test_tourist_arabic),
        ("tourist_english", test_tourist_english),
        ("safety_french_refusal", test_safety_french_refusal),
        ("safety_arabic_refusal", test_safety_arabic_refusal),
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        try:
            asyncio.run(test_func())
            passed += 1
            print(f"PASS: {test_name}")
        except Exception as e:
            failed += 1
            print(f"FAIL: {test_name} - {e}")

    total = passed + failed
    accuracy = (passed / total * 100) if total > 0 else 0

    print("\n" + "=" * 50)
    print(f"Total tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Accuracy: {accuracy:.1f}%")
    print("=" * 50)


if __name__ == "__main__":
    import asyncio
    asyncio.run(run_eval_summary())
