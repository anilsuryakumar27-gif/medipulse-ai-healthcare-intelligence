# MediPulse AI — Prompt Engineering Documentation & Iteration Log

**Role Evaluated:** AI Growth & Automation Associate  
**Candidate Submission Deliverable:** #2 (Prompt Documentation)  
**Domain:** Healthcare & Technology (Australian General Practice Intelligence & Growth)

---

## Executive Summary
This document provides a transparent, end-to-end record of all prompts utilized to research, design, structure, and generate the **MediPulse AI** platform. It demonstrates:
- **Iterative Prompt Engineering**: How prompts evolved from generic first drafts (V1) to structured, highly contextual production prompts (V2 and V3).
- **Domain Grounding**: Integrating Australian healthcare nuances (Medicare Items 721/723 Care Plans, RACGP standards, Practice Management Software like Best Practice/HotDoc).
- **Prompt Engineering Techniques**: Persona adoption, structured JSON enforcement, few-shot prompting, negative constraints, and tone calibration.

---

## Table of Contents
1. [Prompt Chain 1: Healthcare Data Schema & Extraction Design](#prompt-chain-1-healthcare-data-schema--extraction-design)
2. [Prompt Chain 2: Operational Bottleneck & Clinical ROI Synthesizer](#prompt-chain-2-operational-bottleneck--clinical-roi-synthesizer)
3. [Prompt Chain 3: Hyper-Personalized B2B Growth Outreach Generator](#prompt-chain-3-hyper-personalized-b2b-growth-outreach-generator)
4. [Prompt Chain 4: Interactive Dashboard Architecture & UI Development](#prompt-chain-4-interactive-dashboard-architecture--ui-development)
5. [Key Prompt Engineering Insights & Lessons Learned](#key-prompt-engineering-insights--lessons-learned)

---

## Prompt Chain 1: Healthcare Data Schema & Extraction Design

### Objective
Define a robust data schema to scrape and organize publicly listed Australian General Practitioners (GPs) with validated contact channels and operational metadata.

### 🔴 Version 1 (Initial / Naive Prompt)
```text
Give me a list of GP clinics in Australia and their contact info for a scraper script.
```
* **Evaluation & Deficiencies:**
  - Too vague: Returned unstructured mock data without key operational variables.
  - Lacked Australian geographical and phone standard validation (no distinction between NSW `02` or VIC `03` area codes).
  - Missed crucial B2B growth variables (practice manager name, booking systems, billing model).

---

### 🟢 Version 2 (Refined & Production Prompt)
```text
Act as a Principal Healthcare Data Architect and Growth Strategist for the Australian primary healthcare market.

I am developing an automated data intelligence crawler to map General Practices across major metro hubs (Sydney NSW, Melbourne VIC, Brisbane QLD, Perth WA, Adelaide SA).

Design a production-grade JSON schema and sample data model for Australian GP practices. The schema must include:
1. Clinic identification: Practice Name, Street Address, Suburb, State, Postcode.
2. Verified Contact Data: Primary landline phone formatted in Australian standards (e.g., '(02) 9xxx xxxx' or '1300 xxx xxx'), direct reception email, and official website URL.
3. Key Stakeholders: Principal GP (with Australian credentials like MBBS, FRACGP) and Practice Manager name.
4. Operational Metrics: Daily estimated patient volume, average waiting room delay, billing model (Bulk Billing, Mixed Billing, Private), and current booking tech stack (e.g., HotDoc, Healthengine, Phone Queue).
5. Digital Maturity Indicator: An automated scoring metric based on their digital intake and telehealth readiness.

Provide Python regex validation functions for Australian phone numbers and state-to-postcode alignment.
```
* **Why This Worked Better:**
  - Ensured data realism and consistency with actual Australian healthcare directories (Healthdirect, HotDoc).
  - Captured critical growth outreach anchors (`practice_manager`, `booking_system`, `billing_type`).
  - Added deterministic regex verification preventing dirty data in the pipeline.

---

## Prompt Chain 2: Operational Bottleneck & Clinical ROI Synthesizer

### Objective
Analyze raw practice data to detect high-friction administrative bottlenecks and quantify financial ROI from AI automation.

### 🔴 Version 1 (Initial Prompt)
```text
Analyze this clinic and tell me what problems they have and how AI can help them save money:
[Clinic Data Input]
```
* **Evaluation & Deficiencies:**
  - Hallucinated generic AI solutions (e.g., "Use ChatGPT to answer emails") that do not comply with Australian privacy (RACGP privacy guidelines).
  - Failed to connect specific clinic numbers (e.g. 140 patients/day) to concrete staffing costs or lost revenue.

---

### 🟢 Version 2 (Refined with Role Prompting & Guardrails)
```text
System Persona:
You are an Australian Healthcare Operations Consultant specializing in General Practice clinic optimization and automation.

Context & Guardrails:
- Respect Australian privacy laws and RACGP digital standards.
- Ground all bottleneck analyses in the specific clinic parameters provided (daily volume, current booking system, telehealth status).
- Distinguish between Bulk Billing clinics (who face razor-thin margins and need high throughput) and Mixed/Private clinics (who prioritize patient retention and reduced phone wait times).

Input Practice Profile:
- Practice: {clinic_name}
- Location: {suburb}, {state}
- Daily Volume: {patient_volume_daily} patients
- Current Booking: {booking_system}
- Telehealth Status: {telehealth_available}
- Average Wait Time: {estimated_wait_time_mins} minutes

Task:
1. Identify exactly 3 specific operational vulnerabilities causing revenue leakage or front-desk burnout.
2. Formulate a targeted AI solution (e.g., 24/7 Voice AI Receptionist integrated with Best Practice/MedicalDirector, Automated Pre-Consultation Intake, or Care Plan Recall Automation).
3. Compute conservative estimated monthly financial savings in AUD, assuming:
   - Front-desk hourly rate: $36 AUD/hr.
   - Dropped call rate reduction: 12-18%.
   - Chronic Disease Management (Item 721/723) recall recapture rate.

Output strictly valid JSON matching the schema:
{
  "bottlenecks": [string, string, string],
  "recommended_solution": string,
  "projected_monthly_savings_aud": integer
}
```
* **Why This Worked Better:**
  - Produced hyper-realistic diagnostic points (e.g., front-desk phone congestion during peak morning hours).
  - Accurate Australian financial modeling ($AUD, reception wage baselines, Medicare care plan numbers).

---

## Prompt Chain 3: Hyper-Personalized B2B Growth Outreach Generator

### Objective
Generate high-converting, non-spammy B2B consultative emails to Practice Managers and Principal Doctors.

### 🔴 Version 1 (Generic Cold Email)
```text
Write a sales pitch email to the practice manager selling them our AI automation software.
```
* **Resulting Output:**
  *"Subject: Transform your clinic with revolutionary AI!! Dear Manager, Are you tired of manual tasks? Our groundbreaking AI software is the ultimate solution..."*
* **Evaluation & Deficiencies:**
  - Sounded like generic spam; would immediately be deleted or sent to junk folder.
  - Lacked personalization, empathy, and Australian business etiquette.
  - No clear low-friction call-to-action (CTA).

---

### 🟢 Version 2 (Iterative Refinement with Persona, Context & Anti-Hype Constraints)
```text
Act as an AI Growth Specialist who understands Australian medical practice workflows.

Draft a concise, consultative cold email to the Practice Manager:
- Recipient: {practice_manager} at {name}
- Principal GP: {lead_gp}
- Location: {suburb}, {state}
- Key Pain Points Identified: {bottlenecks}
- Proposed Solution: {recommended_solution}

Strict Constraints:
1. Tone: Respectful, consultative, low-pressure, Australian professional. Do not use buzzwords like 'revolutionary', 'game-changing', or 'synergy'.
2. Opening: Reference their specific practice, location, and the scale of their patient volume ({patient_volume_daily} patients/day).
3. Value Proposition: Quantify real benefits in 3 concise bullet points (staff phone workload, pre-intake speed, Medicare care plan recall).
4. Doctor Addressing: Accurately address the doctor by surname (e.g., "Dr. Jenkins"), removing any academic post-nominals like MBBS or FRACGP.
5. Call to Action (CTA): Propose a low-friction "7-minute casual screen share" with a specific day and time.
6. Sender Sign-off: Local Australian contact details (Melbourne / Sydney).
```
* **Why This Worked Better:**
  - High open and response probability: reads like a thoughtful peer consultant who researched their specific clinic.
  - Avoided awkward phrasing (e.g., properly parsed "Dr. Jenkins" instead of "Dr. Sarah Jenkins (FRACGP)").
  - Provided a zero-risk, time-bounded CTA (7 minutes).

---

## Prompt Chain 4: Interactive Dashboard Architecture & UI Development

### Objective
Guide the code generation for a responsive, modern web application dashboard that showcases data intelligence and live AI interaction.

### 🟢 Prompt
```text
Create a modern, full-stack dashboard for the Australian GP Intelligence & AI Growth tool using Python Flask and modern HTML5/CSS/JavaScript.

Design Requirements:
1. Header: Professional health-tech branding ('MediPulse AI Australia') with Australian flag indicator, scraper refresh trigger, and 1-click CSV export button.
2. KPI Metrics Grid: 4 cards displaying Total Practices, Verified Contact Rate (%), Bulk Billing Ratio, and AI Audits Generated.
3. Dynamic Filters: Instant search box (querying clinic name, doctor, or suburb) and dropdowns for State (NSW, VIC, QLD, WA, SA) and Billing Type (Bulk, Mixed, Private).
4. Intelligence Table: Modern dark-theme glassmorphism table displaying clinic details, lead GP, practice manager, formatted phone numbers, email links, and digital maturity badges.
5. Interactive AI Modal: An action button '✨ AI Growth Audit' on every row that triggers an asynchronous API call, showing:
   - Warning badges for detected bottlenecks.
   - Proposed AI solution.
   - Monthly projected savings in AUD.
   - Formatted B2B outreach email with a 1-click 'Copy to Clipboard' button with toast notification.
6. Reliability: Ensure the frontend handles loading and error states gracefully, with zero external CDN dependencies required for core functionality.
```

---

## Key Prompt Engineering Insights & Lessons Learned

| Challenge Encountered | Prompt Engineering Solution |
| :--- | :--- |
| **Hallucinated US-centric medical terms** (e.g. HIPAA, HMO, Medicare Part B) | Explicitly constrained system instructions with Australian primary care ontology (RACGP, AHPRA, Medicare Benefits Schedule 721/723 CDM). |
| **Aggressive, spam-like sales tone** | Implemented negative prompt constraints banning hype keywords and enforcing a consultative peer tone. |
| **Parsing errors on Australian doctor credentials** | Added prompt instructions and regex preprocessing to strip post-nominals (`(FRACGP)`, `MBBS`) from doctor surnames. |
| **API reliability & cost concerns during testing** | Built a dual-engine architecture: prompt design matches live LLM JSON output while maintaining a local deterministic synthesizer for guaranteed zero-downtime demos. |
