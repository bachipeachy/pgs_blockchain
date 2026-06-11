/**
 * pgs_bridge.js — Thin JS bridge for PGS HTTP testbed.
 *
 * Zero schema awareness. Zero workflow branching. Zero validation.
 * PGS handles all business logic. This bridge only:
 * - Harvests form inputs into nested JSON
 * - POSTs to /api/run
 * - Renders the canonical response envelope
 */

async function submitWorkflow(formId) {
    const form = document.getElementById(formId);
    const resultDiv = document.getElementById('result');
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;

    // Harvest payload from data-field attributes
    const payload = {};
    form.querySelectorAll('[data-field]').forEach(function(input) {
        const raw = input.value;
        if (raw !== '') {
            const value = input.type === 'number' ? Number(raw) : raw;
            setDeep(payload, input.getAttribute('data-field'), value);
        }
    });

    const workflowCode = form.getAttribute('data-workflow');
    const structureCode = form.getAttribute('data-structure'); // Add this line

    submitBtn.disabled = true;
    submitBtn.textContent = 'Executing...';

    // Clear previous result to create visible transition on re-submit
    resultDiv.className = 'result-panel';
    resultDiv.style.display = 'none';
    resultDiv.innerHTML = '';

    try {
        const response = await fetch('/api/run', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                workflow_code: workflowCode,
                payload: payload,
                structure: structureCode // Add this line
            })
        });

        const result = await response.json();
        renderResult(resultDiv, result);

    } catch (e) {
        renderError(resultDiv, e.message);
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = originalText;
    }
}

function renderResult(el, result) {
    const isSuccess = result.status === 'SUCCESS';
    const isRepeat = result.already_submitted === true;
    el.className = 'result-panel visible ' + (isRepeat ? 'already-submitted' : (isSuccess ? 'success' : 'error'));
    el.style.display = '';

    // Persist actor_id from successful result so subsequent forms can pre-fill it
    if (isSuccess && result.result_payload && result.result_payload.actor_id) {
        sessionStorage.setItem('pgs_actor_id', result.result_payload.actor_id);
    }

    let html = '';
    if (isRepeat) {
        html += '<span class="status-badge repeat">ALREADY SUBMITTED</span>';
        html += '<div class="result-field"><span class="label">Note</span> '
             +  '<span class="value">This request was already processed. Persistent data is unchanged.</span></div>';
    } else {
        html += '<span class="status-badge">' + result.status + '</span>';
    }

    if (result.trace_id) {
        html += '<div class="result-field"><span class="label">Trace ID</span> '
             +  '<span class="value">' + result.trace_id + '</span></div>';
    }
    if (result.duration_ms !== undefined) {
        html += '<div class="result-field"><span class="label">Duration</span> '
             +  '<span class="value">' + result.duration_ms + 'ms</span></div>';
    }
    if (result.workflow_code) {
        html += '<div class="result-field"><span class="label">Workflow</span> '
             +  '<span class="value">' + result.workflow_code + '</span></div>';
    }
    if (result.message) {
        html += '<div class="result-field"><span class="label">Message</span> '
             +  '<span class="value">' + result.message + '</span></div>';
    }

    // Show key payload highlights
    const p = result.result_payload || {};
    if (p.actor_id) {
        html += '<div class="result-field"><span class="label">Actor ID</span> '
             +  '<span class="value">' + p.actor_id + '</span></div>';
    }
    if (p.wallet_id) {
        html += '<div class="result-field"><span class="label">Wallet ID</span> '
             +  '<span class="value">' + p.wallet_id + '</span></div>';
    }
    if (p.eoa_address) {
        html += '<div class="result-field"><span class="label">EOA Address</span> '
             +  '<span class="value">' + p.eoa_address + '</span></div>';
    }
    if (p.utxo_address) {
        html += '<div class="result-field"><span class="label">UTXO Address</span> '
             +  '<span class="value">' + p.utxo_address + '</span></div>';
    }
    if (p.block_id) {
        html += '<div class="result-field"><span class="label">Block ID</span> '
             +  '<span class="value">' + p.block_id + '</span></div>';
    }
    if (p.tx_id) {
        html += '<div class="result-field"><span class="label">TX ID</span> '
             +  '<span class="value">' + p.tx_id + '</span></div>';
    }
    if (p.tx_hash) {
        html += '<div class="result-field"><span class="label">TX Hash</span> '
             +  '<span class="value">' + p.tx_hash + '</span></div>';
    }
    if (p.from_address) {
        html += '<div class="result-field"><span class="label">From</span> '
             +  '<span class="value">' + p.from_address + '</span></div>';
    }
    if (p.to_address) {
        html += '<div class="result-field"><span class="label">To</span> '
             +  '<span class="value">' + p.to_address + '</span></div>';
    }
    if (p.nonce !== undefined) {
        html += '<div class="result-field"><span class="label">Nonce</span> '
             +  '<span class="value">' + p.nonce + '</span></div>';
    }

    html += '<div class="result-json">' + escapeHtml(JSON.stringify(result, null, 2)) + '</div>';
    el.innerHTML = html;
}

function renderError(el, msg) {
    el.className = 'result-panel visible error';
    el.style.display = '';
    el.innerHTML = '<span class="status-badge">TRANSPORT ERROR</span>'
        + '<div class="result-field"><span class="label">Message</span> '
        + '<span class="value">' + escapeHtml(msg) + '</span></div>';
}

function setDeep(obj, path, value) {
    const parts = path.split('.');
    let current = obj;
    for (let i = 0; i < parts.length - 1; i++) {
        if (!current[parts[i]]) current[parts[i]] = {};
        current = current[parts[i]];
    }
    current[parts[parts.length - 1]] = value;
}

function escapeHtml(str) {
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

// Pre-fill actor_id on page load if available from a prior step
document.addEventListener('DOMContentLoaded', function() {
    const actorIdInput = document.getElementById('actor_id');
    if (actorIdInput) {
        const stored = sessionStorage.getItem('pgs_actor_id');
        if (stored) actorIdInput.value = stored;
    }
});
