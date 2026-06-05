# VisaFlow Agent — Build Instructions

## What this project does
An AI agent for immigration consultants.
It collects client info in French/Arabic/English,
generates a missing document checklist,
and outputs a structured case file ready for review.

## Stack
- Python 3.11
- FastAPI
- Claude API (claude-sonnet-4-20250514)
- Pydantic (data validation)

## V1 Scope (keep it small)
- intake form via API endpoint (POST /intake)
- Claude processes the form and detects missing docs
- returns structured JSON case file
- language: French first, English fallback

## Out of scope for V1
- No UI
- No database
- No auth
- No WhatsApp yet

## How to run
uvicorn api.main:app --reload
