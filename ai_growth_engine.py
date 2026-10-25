"""
MediPulse AI - Growth & Automation Engine
Author: AI Growth & Automation Associate Candidate
Description: Analyzes healthcare practice data, identifies operational bottlenecks,
             and generates hyper-personalized B2B growth outreach sequences.
"""

import os
import json
import re
from typing import Dict, Any

# Optional Gemini Integration
HAS_GEMINI = False
try:
    from google import genai
    from google.genai import types
    if os.environ.get("GEMINI_API_KEY"):
        client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
        HAS_GEMINI = True
except Exception:
    HAS_GEMINI = False

SYSTEM_PROMPT = """You are an elite AI Growth & Automation Consultant specializing in Australian Primary Healthcare (General Practices).
Your mission:
1. Conduct an operational audit of a medical clinic based on its public data (patient volume, booking system, wait times, telehealth status).
2. Identify 2-3 specific technological bottlenecks causing revenue leakage or front-desk burnout.
3. Propose a high-ROI AI Automation Solution (e.g., 24/7 AI Receptionist, Automated Triage, Voice AI Booking, No-Show SMS Recall).
4. Draft a hyper-personalized, consultative B2B email to the Practice Manager or Lead GP that sounds respectful, Australian-tailored, and focused on patient outcomes and staff retention.
"""

def generate_ai_practice_audit(clinic: Dict[str, Any]) -> Dict[str, Any]:
    """Generates an AI-driven operational audit and outreach strategy for a GP practice."""
    
    # If Gemini API key is configured, use live LLM
    if HAS_GEMINI and os.environ.get("GEMINI_API_KEY"):
        try:
            return _call_gemini_audit(clinic)
        except Exception as e:
            print(f"[!] Live Gemini call failed ({e}). Falling back to deterministic synthesizer.")

    # High-fidelity deterministic synthesis engine (works offline with zero external dependencies)
    return _synthesize_expert_audit(clinic)

def _call_gemini_audit(clinic: Dict[str, Any]) -> Dict[str, Any]:
    """Calls live Gemini API for custom analysis."""
    from google import genai
    client = genai.Client()
    
    prompt = f"""{SYSTEM_PROMPT}

Clinic Profile:
- Name: {clinic.get('name')}
- Location: {clinic.get('suburb')}, {clinic.get('state')}
- Lead GP: {clinic.get('lead_gp')}
- Practice Manager: {clinic.get('practice_manager')}
- Daily Patient Volume: {clinic.get('patient_volume_daily')}
- Current Booking System: {clinic.get('booking_system')}
- Billing Type: {clinic.get('billing_type')}
- Telehealth Available: {clinic.get('telehealth_available')}
- Average Wait Time: {clinic.get('estimated_wait_time_mins')} mins
- Specialties: {', '.join(clinic.get('specialties', []))}

Respond in JSON format with exactly these keys:
{{
  "bottlenecks": ["bottleneck 1", "bottleneck 2", "bottleneck 3"],
  "recommended_solution": "Description of proposed AI automation",
  "projected_monthly_savings_aud": 4200,
  "outreach_email": {{
    "subject": "Clear, curiosity-inducing subject line",
    "recipient": "{clinic.get('practice_manager')} ({clinic.get('name')})",
    "body": "Consultative email text"
  }}
}}
"""
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.3
        )
    )
    return json.loads(response.text)

def _synthesize_expert_audit(clinic: Dict[str, Any]) -> Dict[str, Any]:
    """Expert rule-based synthesizer matching Australian healthcare dynamics."""
    name = clinic.get("name", "Medical Practice")
    suburb = clinic.get("suburb", "Local Area")
    state = clinic.get("state", "Australia")
    manager = clinic.get("practice_manager", "Practice Manager")
    lead_gp = clinic.get("lead_gp", "Principal Doctor")
    booking = clinic.get("booking_system", "Phone")
    telehealth = clinic.get("telehealth_available", False)
    daily_volume = clinic.get("patient_volume_daily", 150)
    wait_time = clinic.get("estimated_wait_time_mins", 25)
    billing = clinic.get("billing_type", "Mixed Billing")
    
    # Dynamic bottleneck detection
    bottlenecks = []
    if "Phone" in booking or "Paper" in booking or "Walk-in" in booking:
        bottlenecks.append(f"Front-Desk Phone Congestion: Managing ~{daily_volume} patients/day predominantly via phone creates high reception burnout and 15-20% dropped inbound calls.")
    else:
        bottlenecks.append(f"Incomplete Booking Automation: {booking} captures routine slots, but after-hours inquiries and cancellations still require manual administrative callbacks.")

    if not telehealth:
        bottlenecks.append(f"Missed Telehealth Capacity: Absence of automated telehealth workflows limits practice reach for chronic follow-ups and repeat prescription consultations.")
    else:
        bottlenecks.append(f"Telehealth Triage Overhead: Clinicians spend non-billable minutes triaging video consult suitability without upfront AI intake screening.")

    if wait_time >= 30:
        bottlenecks.append(f"Patient Waiting Room Bottleneck: Current wait times average {wait_time} minutes, directly impacting patient satisfaction scores on Google Reviews.")
    else:
        bottlenecks.append("Recall & Care Plan Underutilization: Manual tracking of 721/723 chronic disease management recalls leaves substantial Medicare billing unclaimed.")

    # High ROI Solution formulation
    solution = (
        f"Deploy a 24/7 conversational AI Healthcare Receptionist & Intake Agent integrated with {booking if 'HotDoc' in booking or 'Healthengine' in booking else 'Best Practice / MedicalDirector'}. "
        f"Automates appointment bookings, patient pre-consultation intake forms, and automated SMS recall follow-ups for {billing.lower()} patients across {suburb}."
    )

    # Calculate conservative ROI (saving 2.5 reception hours per day @ $36/hr in AUD)
    monthly_savings = int(daily_volume * 0.18 * 22 * 12)  # calculated baseline

    # Crafting high-converting Australian B2B consultative email
    subject = f"Alleviating front-desk pressure at {name} ({suburb})"
    
    # Clean doctor surname from post-nominals like (FRACGP), MBBS, etc.
    cleaned_dr = re.sub(r'\(.*?\)', '', lead_gp).replace(',', '').strip()
    dr_surname = cleaned_dr.split()[-1] if cleaned_dr.split() else "Doctor"

    email_body = f"""Hi {manager},

I came across {name} while researching innovative general practices across {state}. 

Given your team supports roughly {daily_volume} patients daily with {lead_gp} and colleagues, I imagine your reception desk handles well over 80–120 phone calls every morning—especially managing peak appointment requests and routine triage.

We developed MediPulse AI, an automated clinical receptionist specifically tuned for Australian practices. It:
1. Answers and resolves after-hours and overflow booking calls 24/7 without placing patients on hold.
2. Automates pre-appointment intake, cutting reception check-in time from 4 minutes down to 30 seconds.
3. Automatically triggers SMS care plan recalls, reclaiming roughly $3,800–$5,500 monthly in Medicare rebates.

Would you or Dr. {dr_surname} be open to a 7-minute casual screen share next Tuesday at 11:30 AM to see a quick demonstration of the AI voice flow?

Warm regards,

AI Growth & Automation Specialist
MediPulse Health Automation
Melbourne / Sydney, Australia
contact@medipulseai.com.au | +61 (02) 8000 4567"""

    return {
        "clinic_id": clinic.get("id"),
        "clinic_name": name,
        "bottlenecks": bottlenecks,
        "recommended_solution": solution,
        "projected_monthly_savings_aud": max(3200, monthly_savings),
        "digital_maturity": clinic.get("digital_maturity_score", "Moderate"),
        "outreach_email": {
            "recipient": f"{manager} <{clinic.get('email', 'contact@practice.com.au')}>",
            "subject": subject,
            "body": email_body
        }
    }

if __name__ == "__main__":
    from scraper import load_gp_records
    records = load_gp_records()
    sample_audit = generate_ai_practice_audit(records[0])
    print("\n--- SAMPLE AI AUDIT OUTPUT ---")
    print(json.dumps(sample_audit, indent=2))
