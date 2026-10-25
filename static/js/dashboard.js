/**
 * MediPulse AI - Dashboard Frontend Controller
 * Handles interactive filtering, AI analysis triggering, modal rendering, and CSV exports.
 */

let allClinics = [];

document.addEventListener('DOMContentLoaded', () => {
  loadStats();
  loadClinics();
  setupEventListeners();
});

function setupEventListeners() {
  const searchInput = document.getElementById('searchInput');
  const stateFilter = document.getElementById('stateFilter');
  const billingFilter = document.getElementById('billingFilter');
  const rescrapeBtn = document.getElementById('rescrapeBtn');
  const closeModalBtn = document.getElementById('closeModalBtn');
  const auditModal = document.getElementById('auditModal');

  searchInput.addEventListener('input', debounce(filterAndRender, 200));
  stateFilter.addEventListener('change', filterAndRender);
  billingFilter.addEventListener('change', filterAndRender);

  rescrapeBtn.addEventListener('click', handleRescrape);
  closeModalBtn.addEventListener('click', () => auditModal.classList.add('hidden'));

  // Close modal on background click
  auditModal.addEventListener('click', (e) => {
    if (e.target === auditModal) {
      auditModal.classList.add('hidden');
    }
  });
}

async function loadStats() {
  try {
    const res = await fetch('/api/stats');
    const data = await res.json();
    document.getElementById('kpiTotal').textContent = data.total_practices;
    document.getElementById('kpiVerified').textContent = data.verified_contact_rate;
    document.getElementById('kpiBulk').textContent = data.bulk_billing_ratio;
    document.getElementById('kpiAudits').textContent = `${data.audits_generated} Ready`;
  } catch (err) {
    console.error('Failed to load KPIs:', err);
  }
}

async function loadClinics() {
  try {
    const res = await fetch('/api/clinics');
    const json = await res.json();
    allClinics = json.data || [];
    filterAndRender();
  } catch (err) {
    console.error('Failed to load clinics:', err);
    document.getElementById('clinicsTableBody').innerHTML = `
      <tr><td colspan="6" style="text-align: center; color: #f43f5e; padding: 2rem;">
        Failed to load GP intelligence. Ensure local backend is running.
      </td></tr>`;
  }
}

function filterAndRender() {
  const query = document.getElementById('searchInput').value.trim().toLowerCase();
  const state = document.getElementById('stateFilter').value;
  const billing = document.getElementById('billingFilter').value;

  const filtered = allClinics.filter(item => {
    if (state !== 'ALL' && item.state !== state) return false;
    if (billing !== 'ALL' && item.billing_type !== billing) return false;
    if (query) {
      const haystack = `${item.name} ${item.suburb} ${item.lead_gp} ${item.practice_manager}`.toLowerCase();
      if (!haystack.includes(query)) return false;
    }
    return true;
  });

  renderTable(filtered);
}

function renderTable(clinics) {
  const tbody = document.getElementById('clinicsTableBody');
  document.getElementById('recordCount').textContent = clinics.length;

  if (clinics.length === 0) {
    tbody.innerHTML = `
      <tr><td colspan="6" style="text-align: center; color: #94a3b8; padding: 3rem;">
        No clinics found matching your filter criteria.
      </td></tr>`;
    return;
  }

  tbody.innerHTML = clinics.map(c => {
    const stateTagClass = `tag-${c.state.toLowerCase()}`;
    const billingClass = c.billing_type === 'Bulk Billing' ? 'pill-bulk' : 
                         c.billing_type === 'Private' ? 'pill-private' : 'pill-mixed';
    
    const maturityClass = c.digital_maturity_score.includes('High') ? 'maturity-high' :
                          c.digital_maturity_score.includes('Low') ? 'maturity-low' : 'maturity-med';

    return `
      <tr>
        <td>
          <div class="clinic-title">${escapeHtml(c.name)}</div>
          <div class="clinic-geo">
            <span class="state-tag ${stateTagClass}">${c.state}</span>
            <span>${escapeHtml(c.suburb)}, ${c.postcode}</span>
          </div>
        </td>
        <td>
          <div class="contact-name">${escapeHtml(c.lead_gp)}</div>
          <div class="contact-role">Mgr: ${escapeHtml(c.practice_manager)}</div>
        </td>
        <td>
          <div><strong>📞</strong> ${escapeHtml(c.phone)}</div>
          <a href="mailto:${escapeHtml(c.email)}" class="contact-link">✉️ ${escapeHtml(c.email)}</a>
        </td>
        <td>
          <span class="pill-badge ${billingClass}">${escapeHtml(c.billing_type)}</span>
          <div class="meta-stats">~${c.patient_volume_daily} pts/day • ${c.estimated_wait_time_mins}m wait</div>
          <div class="meta-stats" style="color: #64748b;">Sys: ${escapeHtml(c.booking_system)}</div>
        </td>
        <td>
          <span class="maturity-badge ${maturityClass}">
            ● ${escapeHtml(c.digital_maturity_score)}
          </span>
        </td>
        <td class="text-right">
          <button class="btn btn-ai" onclick="runAiAudit('${c.id}')" id="btn-ai-${c.id}">
            ✨ AI Growth Audit
          </button>
        </td>
      </tr>
    `;
  }).join('');
}

async function runAiAudit(clinicId) {
  const btn = document.getElementById(`btn-ai-${clinicId}`);
  const originalText = btn.innerHTML;
  btn.innerHTML = `⏳ Analyzing...`;
  btn.disabled = true;

  try {
    const res = await fetch(`/api/analyze/${clinicId}`, { method: 'POST' });
    const data = await res.json();
    if (data.success && data.audit) {
      openAuditModal(data.audit);
      loadStats(); // Update audit count KPI
    } else {
      alert('Failed to generate audit. Please try again.');
    }
  } catch (err) {
    console.error('Audit generation error:', err);
    alert('Error connecting to AI engine.');
  } finally {
    btn.innerHTML = originalText;
    btn.disabled = false;
  }
}

function openAuditModal(audit) {
  const clinic = allClinics.find(c => c.id === audit.clinic_id) || {};
  document.getElementById('modalClinicName').textContent = audit.clinic_name;
  document.getElementById('modalClinicLocation').textContent = `${clinic.address || ''}, ${clinic.suburb || ''} ${clinic.state || ''} ${clinic.postcode || ''}`;

  const bottlenecksHtml = audit.bottlenecks.map(b => `
    <div class="bottleneck-card">
      <span style="font-size: 1.1rem;">⚠️</span>
      <div>${escapeHtml(b)}</div>
    </div>
  `).join('');

  const modalBody = document.getElementById('modalContent');
  modalBody.innerHTML = `
    <div>
      <div class="audit-section-title">🔍 Identified Operational & Technology Bottlenecks</div>
      ${bottlenecksHtml}
    </div>

    <div>
      <div class="audit-section-title">💡 Proposed AI Automation Solution</div>
      <div class="solution-box">
        ${escapeHtml(audit.recommended_solution)}
      </div>
    </div>

    <div class="roi-metric">
      <div>
        <div style="font-size: 0.8rem; color: #94a3b8; font-weight: 600;">PROJECTED CLINIC SAVINGS & RECLAIMED BILLING</div>
        <div style="font-size: 0.75rem; color: #64748b;">Based on reception phone triage time savings + automated 721 care plan recall</div>
      </div>
      <div class="roi-metric-val">~$${audit.projected_monthly_savings_aud.toLocaleString()} AUD / mo</div>
    </div>

    <div>
      <div class="audit-section-title">✉️ Hyper-Personalized Consultative B2B Outreach Email</div>
      <div class="email-preview-box">
        <div class="email-header-meta">
          <div class="email-meta-row">
            <span class="email-meta-label">To:</span>
            <span>${escapeHtml(audit.outreach_email.recipient)}</span>
          </div>
          <div class="email-meta-row">
            <span class="email-meta-label">Subject:</span>
            <span style="font-weight: 600; color: #38bdf8;">${escapeHtml(audit.outreach_email.subject)}</span>
          </div>
        </div>
        <div class="email-body-content" id="emailBodyToCopy">${escapeHtml(audit.outreach_email.body)}</div>
        <div class="email-footer-actions">
          <button class="btn btn-primary" onclick="copyEmailToClipboard()">
            📋 Copy Email to Clipboard
          </button>
        </div>
      </div>
    </div>
  `;

  document.getElementById('auditModal').classList.remove('hidden');
}

function copyEmailToClipboard() {
  const emailText = document.getElementById('emailBodyToCopy').innerText;
  navigator.clipboard.writeText(emailText).then(() => {
    showToast('Outreach email copied to clipboard!');
  }).catch(err => {
    console.error('Clipboard copy failed:', err);
    showToast('Failed to copy. Please select text manually.');
  });
}

function showToast(msg) {
  const toast = document.getElementById('toast');
  toast.textContent = msg;
  toast.classList.remove('hidden');
  setTimeout(() => {
    toast.classList.add('hidden');
  }, 2500);
}

async function handleRescrape() {
  const btn = document.getElementById('rescrapeBtn');
  const originalHtml = btn.innerHTML;
  btn.innerHTML = `⏳ Scraping...`;
  btn.disabled = true;

  try {
    const res = await fetch('/api/rescrape', { method: 'POST' });
    const data = await res.json();
    if (data.success) {
      await loadClinics();
      await loadStats();
      showToast(`Scraper finished: ${data.count} practices indexed!`);
    }
  } catch (err) {
    alert('Scraper execution failed.');
  } finally {
    btn.innerHTML = originalHtml;
    btn.disabled = false;
  }
}

function debounce(fn, delay) {
  let timer;
  return function(...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(this, args), delay);
  };
}

function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}
