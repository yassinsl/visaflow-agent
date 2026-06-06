# VisaFlow Agent

AI-powered multilingual intake agent for immigration consultants.
Supports French, Arabic and English.

## Install
pip install -r requirements.txt

## Run
uvicorn api.main:app --reload

## Test
curl -X POST http://localhost:8000/intake \
-H "Content-Type: application/json" \
-d '{
  "full_name": "Youssef El Amrani",
  "nationality": "Moroccan",
  "date_of_birth": "1995-06-15",
  "email": "youssef@example.com",
  "phone": "0612345678",
  "destination_country": "Canada",
  "visa_type": "student",
  "has_passport": true,
  "has_birth_certificate": false,
  "has_bank_statements": false,
  "has_employment_proof": false,
  "has_housing_proof": false,
  "situation_description": "Je souhaite poursuivre mon master au Canada",
  "language": "fr"
}'

## Safety
All outputs are drafts for human review only.
The agent never gives legal advice.
