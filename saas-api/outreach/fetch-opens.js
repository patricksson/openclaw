// Pulls open events from Brevo and marks leads with opened_at / open_count.
//
// Usage: node outreach/fetch-opens.js [hoursBack=48]
//
// Requires BREVO_API_KEY. Uses GET /v3/smtp/statistics/events?event=opened.
// Matches events to leads by messageId stored on the lead (email1_message_id etc).

const https = require('https');
const store = require('./leads-store');

const BREVO_API_KEY = process.env.BREVO_API_KEY;
const HOURS_BACK = parseInt(process.argv[2], 10) || 48;

if (!BREVO_API_KEY) {
  console.error('BREVO_API_KEY not set.');
  process.exit(1);
}

function fetchEvents(startDate, endDate, offset = 0, limit = 100) {
  return new Promise((resolve, reject) => {
    const q = `event=opened&startDate=${encodeURIComponent(startDate)}&endDate=${encodeURIComponent(endDate)}&limit=${limit}&offset=${offset}&sort=desc`;
    const req = https.request(`https://api.brevo.com/v3/smtp/statistics/events?${q}`, {
      method: 'GET',
      headers: { 'accept': 'application/json', 'api-key': BREVO_API_KEY },
      timeout: 20000,
    }, (res) => {
      let d = '';
      res.on('data', c => d += c);
      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          try { resolve(JSON.parse(d)); } catch (e) { reject(e); }
        } else reject(new Error(`Brevo ${res.statusCode}: ${d}`));
      });
    });
    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('Brevo timeout')); });
    req.end();
  });
}

function buildMsgIndex() {
  const idx = new Map();
  for (const lead of store.listAll()) {
    for (const step of [1, 2, 3]) {
      const mid = lead[`email${step}_message_id`];
      if (mid) idx.set(mid, { leadId: lead.id, step });
    }
  }
  return idx;
}

function buildEmailIndex() {
  const idx = new Map();
  for (const lead of store.listAll()) {
    if (!lead.email) continue;
    idx.set(lead.email.toLowerCase(), lead);
  }
  return idx;
}

(async () => {
  const startDate = new Date(Date.now() - HOURS_BACK * 3600 * 1000).toISOString().slice(0, 10);
  const endDate = new Date().toISOString().slice(0, 10);
  console.log(`Fetching opens ${startDate} → ${endDate} (${HOURS_BACK}h back)`);
  const midIdx = buildMsgIndex();
  const emailIdx = buildEmailIndex();

  let offset = 0, total = 0, matched = 0;
  const seenMid = new Set();
  const seenEmailStep = new Set();
  while (true) {
    const page = await fetchEvents(startDate, endDate, offset, 100);
    const events = page.events || [];
    if (!events.length) break;
    for (const ev of events) {
      total++;
      let leadId = null, step = null;

      if (ev.messageId && midIdx.has(ev.messageId)) {
        ({ leadId, step } = midIdx.get(ev.messageId));
        if (seenMid.has(ev.messageId)) continue;
        seenMid.add(ev.messageId);
      } else if (ev.email && emailIdx.has(ev.email.toLowerCase())) {
        const lead = emailIdx.get(ev.email.toLowerCase());
        leadId = lead.id;
        if (lead.email1_sent) step = 1;
        else if (lead.email2_sent) step = 2;
        else if (lead.email3_sent) step = 3;
        else continue;
        const key = `${leadId}:${step}`;
        if (seenEmailStep.has(key)) continue;
        seenEmailStep.add(key);
      } else continue;

      const openAtKey = `email${step}_opened_at`;
      const openCountKey = `email${step}_open_count`;
      const lead = store.getById(leadId);
      if (!lead) continue;
      const patch = {};
      if (!lead[openAtKey]) patch[openAtKey] = ev.date || new Date().toISOString();
      patch[openCountKey] = (lead[openCountKey] || 0) + 1;
      store.update(leadId, patch);
      matched++;
    }
    if (events.length < 100) break;
    offset += 100;
    if (offset > 1000) break;
  }
  console.log(`Scanned ${total} open events, matched ${matched} to leads.`);
})().catch(e => { console.error(e); process.exit(1); });
