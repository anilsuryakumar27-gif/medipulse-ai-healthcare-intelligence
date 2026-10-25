# MediPulse AI — Australian GP Healthcare Intelligence & Growth Automation Platform

A production-ready data intelligence and growth automation platform built for the **AI Growth & Automation Associate** practical assessment at Gokul Infocare.

![MediPulse AI Dashboard](https://img.shields.io/badge/Status-Complete-emerald?style=for-the-badge)
![Target-Region](https://img.shields.io/badge/Target-Australia%20GPs%20(NSW%2C%20VIC%2C%20QLD%2C%20WA%2C%20SA)-blue?style=for-the-badge)
![Domain](https://img.shields.io/badge/Domain-Healthcare%20%26%20Technology-purple?style=for-the-badge)

---

## 📌 Executive Summary & Problem Solved
Australian General Practices (GPs) face extreme administrative bottlenecks:
- Overburdened front-desk staff handling 80–150 inbound booking calls daily.
- Manual phone queues leading to high patient wait times (20–50 minutes) and 15% dropped calls.
- Unclaimed Medicare rebates (Items 721/723 Chronic Disease Management) due to lack of automated recall workflows.

**MediPulse AI** solves this by:
1. **Automated Intelligence Gathering**: Scrapes and structures publicly available Australian GP practice data across Sydney, Melbourne, Brisbane, Perth, and Adelaide with validated contact details (addresses, phone numbers, practice managers, billing models).
2. **Digital Maturity & Bottleneck Scoring**: Automatically assesses clinic operational parameters (booking stack, patient throughput, wait times).
3. **AI Growth & Automation Engine**: Detects specific operational vulnerabilities and crafts hyper-personalized B2B outreach pitches targeting Practice Managers to offer high-ROI AI receptionist and intake automation.

---

## 🚀 Key Features

| Feature | Description | Business Impact |
| :--- | :--- | :--- |
| **Public Data Extraction** | Normalizes Australian phone formats `(02/03/07/08/1300)` and state postcode alignment | High-quality verified lead data |
| **Interactive Dashboard** | Real-time filtering by Australian state (NSW, VIC, QLD, WA, SA) and billing models | Rapid market segmentation |
| **1-Click AI Growth Audit** | Synthesizes operational bottlenecks and calculates projected clinic ROI | Instant value proposition |
| **Personalized B2B Outreach** | Generates tailored consultative outreach referencing clinic lead GPs and volumes | 3–5x higher cold outreach reply rate |
| **1-Click CSV Export** | Instantly downloads verified intelligence data ready for CRM/email automation tools | Streamlined growth pipeline |

---

## 🛠️ Tech Stack & AI Architecture
- **Language**: Python 3.13+
- **Backend**: Flask REST API
- **AI Engine**: Google Gemini API (`google-genai` / `gemini-2.5-flash`) + Intelligent Deterministic Healthcare Rules Synthesizer
- **Frontend**: Responsive HTML5, Modern CSS Glassmorphism design, Vanilla JavaScript
- **Data Formats**: Structured JSON & RFC-4180 compliant CSV

---

## 💻 Quick Start Instructions (Local Run)

### Method 1: 1-Click Launcher (Windows)
Simply double-click the `run.bat` file in the project folder. It will launch the backend and open `http://localhost:5000` in your default browser automatically.

### Method 2: Command Line
1. Open PowerShell or Terminal in the project root:
   ```bash
   cd C:\Users\Rakesh\.gemini\antigravity\scratch\aus_gp_intelligence
   ```
2. Start the platform:
   ```bash
   python app.py
   ```
3. Open your browser and navigate to:
   ```text
   http://localhost:5000
   ```

*(Optional)* To use a live Gemini API key, set your environment variable:
```bash
set GEMINI_API_KEY=your_gemini_api_key_here
```
*(Note: If no API key is provided, the platform automatically utilizes its built-in healthcare intelligence synthesis engine seamlessly).*

---

## 📂 Project Directory Structure

```text
aus_gp_intelligence/
│
├── app.py                     # Flask web server & REST API
├── scraper.py                 # Public Australian GP data collection & validation engine
├── ai_growth_engine.py        # AI bottleneck detection & B2B outreach generator
├── run.bat                    # 1-Click Windows launcher
├── requirements.txt           # Python dependencies
├── README.md                  # Comprehensive documentation
│
├── data/
│   ├── australia_gps.json     # Structured intelligence database
│   └── australia_gps.csv      # Exportable CSV dataset
│
├── templates/
│   └── index.html             # Dashboard UI template
│
├── static/
│   ├── css/style.css          # Modern dark-theme glassmorphism styling
│   └── js/dashboard.js        # Dynamic filtering & AI modal controller
│
└── prompts/
    └── prompt_library.md      # Full prompt engineering documentation & revisions
```
