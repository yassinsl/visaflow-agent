"""Debug classifier output."""

import asyncio
import os
import json

import anthropic

os.environ.setdefault("ANTHROPIC_API_KEY", "qua-9620b7afeda20abf3848f85aef3e8d1e")

async def debug():
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    situation = "J'ai reçu une offre d'emploi d'une entreprise canadienne et je veux obtenir un permis de travail"

    system_prompt = """You are an expert immigration consultant specializing in Canadian and North American immigration cases.
Your task is to analyze the client's situation description and classify their case ACCURATELY.

CRITICAL RULES:
1. Read the free text carefully, word by word
2. Look for these specific signals in ANY language:
   - Student: étudier, master, universite, universite, ecole, studies, studying, study permit,vdash,formation
   - Work: emploi, travail, offre, contrat, entreprise, work permit, job, salarie, salary, عمل, poste
   - Family: conjoint, epoux, enfants, rejoindre, famille, marriage, spouse, زوج,زوجة, اطفال, regroupement
   - Tourist: visiter, vacances, tourisme, ami, voyage, tourism, visitor,visit, سياحة,Governor

3. NEVER default to student — if unsure between categories, return tourist with confidence: low
4. Use visa_type from the form as a hint, but OVERRIDE if the free text clearly indicates otherwise
5. ALWAYS return valid JSON only — no extra text, no markdown

Output format:
{"detected_case_category": "work", "confidence": "high", "key_signals": ["offre d'emploi"], "language_detected": "fr"}"""

    user_message = f"""Analyze this immigration case description and return ONLY JSON:

Visa type from form: work

Client's situation description:
{situation}

Return ONLY JSON, no other text."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-6-thinking",
            max_tokens=500,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}]
        )

        print(f"Response type: {type(message)}")
        print(f"Response: {message}")
        print(f"Content: {message.content}")
        if message.content:
            print(f"First content: {message.content[0]}")
            print(f"Text: {message.content[0].text}")
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")

asyncio.run(debug())
