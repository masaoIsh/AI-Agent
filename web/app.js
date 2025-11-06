function isoDate(d) {
  return d.toISOString().slice(0, 10);
}

function threeYearsAgoAndToday() {
  const end = new Date();
  const start = new Date();
  start.setFullYear(end.getFullYear() - 3);
  return { start: isoDate(start), end: isoDate(end) };
}

function collectTickers() {
  const inputs = Array.from(document.querySelectorAll('#ticker-form .cell'));
  const symbols = inputs.map((el) => (el.value || '').trim().toUpperCase()).filter(Boolean);
  return symbols;
}

function renderKV(obj) {
  if (!obj || typeof obj !== 'object') return String(obj);
  const lines = [];
  for (const key of Object.keys(obj)) {
    const val = obj[key];
    lines.push(`${key}: ${typeof val === 'number' ? val.toFixed(6) : JSON.stringify(val)}`);
  }
  return lines.join('\n');
}

async function runModel() {
  const status = document.getElementById('status');
  const results = document.getElementById('results');
  results.hidden = true;

  const symbols = collectTickers();
  if (symbols.length !== 10) {
    status.textContent = `Please input exactly 10 tickers (got ${symbols.length}).`;
    return;
  }

  const { start, end } = threeYearsAgoAndToday();
  const use_oos = document.getElementById('use-oos').checked;
  const rebalance = document.getElementById('rebalance').value;
  const strategy = document.getElementById('strategy').value;

  status.textContent = 'Agents debating… optimizing… (this can take a bit)';

  // Get API URL from environment variable or use default
  const API_URL = window.API_URL || 'https://your-api.railway.app'; // Replace with your Railway/Render URL
  
  try {
    const resp = await fetch(`${API_URL}/sector-analysis`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ symbols, start, end, rebalance, strategy, use_oos }),
    });

    if (!resp.ok) {
      const err = await resp.json().catch(() => ({}));
      throw new Error(err?.detail?.error || JSON.stringify(err) || 'Request failed');
    }
    const data = await resp.json();

    const picks = data?.agent || {};
    const weights = data?.weights_last || {};
    const metrics = data?.metrics || {};

    document.getElementById('agent-picks').textContent = [
      `Selected: ${Array.isArray(picks.selected_stocks) ? picks.selected_stocks.join(', ') : '—'}`,
      `AvgConfidence: ${typeof picks.avg_confidence === 'number' ? picks.avg_confidence.toFixed(3) : '—'}`,
      picks.ranked_stocks ? `Ranked: ${JSON.stringify(picks.ranked_stocks).slice(0, 800)}…` : ''
    ].filter(Boolean).join('\n');

    document.getElementById('weights').textContent = renderKV(weights);
    document.getElementById('metrics').textContent = renderKV(metrics);

    results.hidden = false;
    status.textContent = 'Done.';
  } catch (e) {
    status.textContent = `Error: ${e.message}`;
  }
}

document.getElementById('run').addEventListener('click', (e) => {
  e.preventDefault();
  runModel();
});

// Fill default tickers
document.getElementById('fill-default').addEventListener('click', () => {
  const defaultTickers = ['AAPL', 'MSFT', 'AMD', 'INTC', 'NVDA', 'ORCL', 'IBM', 'ADBE', 'SA', 'CRM'];
  const inputs = Array.from(document.querySelectorAll('#ticker-form .cell'));
  defaultTickers.forEach((ticker, index) => {
    if (inputs[index]) {
      inputs[index].value = ticker;
    }
  });
});

// Tab switching
document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const targetTab = btn.dataset.tab;
    
    // Update button states
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    
    // Update panel visibility - completely separate panels
    const inputPanel = document.getElementById('tab-input');
    const howItWorksPanel = document.getElementById('tab-how-it-works');
    
    if (targetTab === 'input') {
      inputPanel.hidden = false;
      howItWorksPanel.hidden = true;
    } else if (targetTab === 'how-it-works') {
      inputPanel.hidden = true;
      howItWorksPanel.hidden = false;
    }
  });
});

