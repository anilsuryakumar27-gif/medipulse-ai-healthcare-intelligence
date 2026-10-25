"""
MediPulse AI - Web Application & Intelligence Dashboard
Author: AI Growth & Automation Associate Candidate
Framework: Flask
"""

import os
import json
import csv
import io
from flask import Flask, render_template, jsonify, request, Response
from scraper import load_gp_records, collect_and_save_data
from ai_growth_engine import generate_ai_practice_audit

app = Flask(__name__)

# Cache of generated audits to avoid redundant calls during demo
AUDIT_CACHE = {}

@app.route("/")
def index():
    """Serves the primary intelligence and growth dashboard."""
    return render_template("index.html")

@app.route("/api/stats")
def get_stats():
    """Returns top-level KPIs for the Australian GP intelligence landscape."""
    records = load_gp_records()
    total = len(records)
    verified_contacts = sum(1 for r in records if r.get("phone_valid") and r.get("has_email"))
    bulk_billing_count = sum(1 for r in records if r.get("billing_type") == "Bulk Billing")
    mixed_billing_count = sum(1 for r in records if r.get("billing_type") == "Mixed Billing")
    private_count = sum(1 for r in records if r.get("billing_type") == "Private")
    
    return jsonify({
        "total_practices": total,
        "verified_contact_rate": f"{(verified_contacts / total * 100):.0f}%" if total else "0%",
        "bulk_billing_ratio": f"{bulk_billing_count}/{total}",
        "billing_distribution": {
            "Bulk Billing": bulk_billing_count,
            "Mixed Billing": mixed_billing_count,
            "Private": private_count
        },
        "audits_generated": len(AUDIT_CACHE)
    })

@app.route("/api/clinics")
def get_clinics():
    """Returns GP clinic records with optional search and state filters."""
    records = load_gp_records()
    query = request.args.get("q", "").strip().lower()
    state = request.args.get("state", "").strip().upper()
    billing = request.args.get("billing", "").strip()

    filtered = []
    for r in records:
        if state and state != "ALL" and r.get("state") != state:
            continue
        if billing and billing != "ALL" and r.get("billing_type") != billing:
            continue
        if query:
            match_string = f"{r.get('name')} {r.get('suburb')} {r.get('lead_gp')} {r.get('practice_manager')}".lower()
            if query not in match_string:
                continue
        
        # Attach flag if already audited
        r_copy = dict(r)
        r_copy["has_audit"] = r["id"] in AUDIT_CACHE
        filtered.append(r_copy)

    return jsonify({"count": len(filtered), "data": filtered})

@app.route("/api/analyze/<clinic_id>", methods=["POST"])
def analyze_clinic(clinic_id):
    """Executes AI Growth Audit and Outreach Generator on specific GP clinic."""
    records = load_gp_records()
    clinic = next((r for r in records if r.get("id") == clinic_id), None)
    
    if not clinic:
        return jsonify({"error": "Practice not found"}), 404

    audit = generate_ai_practice_audit(clinic)
    AUDIT_CACHE[clinic_id] = audit
    return jsonify({"success": True, "audit": audit})

@app.route("/api/export-csv")
def export_csv():
    """Exports structured GP practice dataset to CSV with intelligence scores."""
    records = load_gp_records()
    
    output = io.StringIO()
    fieldnames = [
        "id", "name", "lead_gp", "practice_manager", "address", "suburb", 
        "state", "postcode", "phone", "email", "website", "billing_type", 
        "booking_system", "gp_count", "telehealth_available", 
        "patient_volume_daily", "estimated_wait_time_mins", "digital_maturity_score"
    ]
    writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()
    for r in records:
        writer.writerow(r)

    response = Response(output.getvalue(), mimetype="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=australia_gp_intelligence_export.csv"
    return response

@app.route("/api/rescrape", methods=["POST"])
def rescrape():
    """Triggers public data collector refresh."""
    updated = collect_and_save_data()
    return jsonify({"success": True, "count": len(updated)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"\n==================================================================")
    print(f" MediPulse AI — Australian GP Growth & Automation Platform")
    print(f" Running locally at: http://localhost:{port}")
    print(f" Open your browser and navigate to the link above!")
    print(f"==================================================================\n")
    app.run(host="0.0.0.0", port=port, debug=False)
