"""Streamlit interface for VisaFlow Agent."""

import streamlit as st
import requests
from datetime import date

st.set_page_config(page_title="VisaFlow Agent", page_icon="🛂")

st.title("VisaFlow Agent — Assistant Immigration IA")

with st.form("intake_form"):
    col1, col2 = st.columns(2)

    with col1:
        full_name = st.text_input("Full Name", placeholder="Enter your full name")
        nationality = st.text_input("Nationality", value="Moroccan")
        date_of_birth = st.date_input("Date of Birth", min_value=date(1950, 1, 1), max_value=date.today())
        email = st.text_input("Email", placeholder="your@email.com")
        phone = st.text_input("Phone", placeholder="+212 612 345 678")

    with col2:
        destination_country = st.text_input("Destination Country", value="Canada")
        visa_type = st.selectbox("Visa Type", ["student", "work", "tourist", "family_reunification"])
        language = st.selectbox("Language", ["fr", "ar", "en"], format_func=lambda x: {"fr": "Français", "ar": "العربية", "en": "English"}[x])

    st.markdown("### Documents You Have")
    doc_col1, doc_col2, doc_col3, doc_col4, doc_col5 = st.columns(5)

    with doc_col1:
        has_passport = st.checkbox("Passport")
    with doc_col2:
        has_birth_certificate = st.checkbox("Birth Certificate")
    with doc_col3:
        has_bank_statements = st.checkbox("Bank Statements")
    with doc_col4:
        has_employment_proof = st.checkbox("Employment Proof")
    with doc_col5:
        has_housing_proof = st.checkbox("Housing Proof")

    situation_description = st.text_area(
        "Situation Description",
        placeholder="Describe your situation in French, Arabic, or English...",
        height=150
    )

    submitted = st.form_submit_button("Submit", type="primary")

if submitted:
    if not full_name or not email or not situation_description:
        st.error("Please fill in all required fields: Full Name, Email, and Situation Description")
    else:
        form_data = {
            "full_name": full_name,
            "nationality": nationality,
            "date_of_birth": str(date_of_birth),
            "email": email,
            "phone": phone,
            "destination_country": destination_country,
            "visa_type": visa_type,
            "language": language,
            "has_passport": has_passport,
            "has_birth_certificate": has_birth_certificate,
            "has_bank_statements": has_bank_statements,
            "has_employment_proof": has_employment_proof,
            "has_housing_proof": has_housing_proof,
            "situation_description": situation_description,
        }

        with st.spinner("Processing your case..."):
            try:
                response = requests.post("http://localhost:8000/intake", json=form_data, timeout=30)

                if response.status_code == 200:
                    result = response.json()

                    st.success("Case file generated successfully!")

                    st.markdown("### 📋 Case Result")

                    st.markdown("**Case Category:**")
                    st.info(result.get("case_category", "N/A"))

                    missing_docs = result.get("missing_documents", [])
                    st.markdown("**Missing Documents:**")
                    if missing_docs:
                        for doc in missing_docs:
                            st.write(f"• {doc}")
                    else:
                        st.write("None — all documents provided!")

                    st.markdown("**Case Summary:**")
                    st.write(result.get("case_summary", "N/A"))

                    st.markdown("**Recommended Next Step:**")
                    st.write(result.get("recommended_next_step", "N/A"))

                    if not result.get("reviewed_by_human", True):
                        st.warning("⚠️ This case has NOT been reviewed by a human yet")

                else:
                    st.error(f"Error: {response.status_code} - {response.text}")

            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to the API. Make sure the server is running at http://localhost:8000")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
