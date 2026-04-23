#!/usr/bin/env node
// Pull 7-day Search Console metrics for automatyn.co.
// Usage: node seo/gsc-fetch.js [days]   (default 7)

const fs = require('fs');
const path = require('path');
const { google } = require('googleapis');

const CLIENT_PATH = path.join(__dirname, '..', 'secrets', 'gsc-oauth-client.json');
const TOKEN_PATH = path.join(__dirname, '..', 'secrets', 'gsc-token.json');

if (!fs.existsSync(TOKEN_PATH)) {
  console.error('No token found. Run: node seo/gsc-auth.js');
  process.exit(1);
}

const client = JSON.parse(fs.readFileSync(CLIENT_PATH, 'utf8')).installed;
const tokens = JSON.parse(fs.readFileSync(TOKEN_PATH, 'utf8'));
const oauth2 = new google.auth.OAuth2(client.client_id, client.client_secret);
oauth2.setCredentials(tokens);

const wm = google.webmasters({ version: 'v3', auth: oauth2 });

const days = parseInt(process.argv[2] || '7', 10);
const end = new Date();
const start = new Date(Date.now() - days * 86400000);
const fmt = d => d.toISOString().slice(0, 10);

async function tryProperties() {
  const list = await wm.sites.list();
  const sites = (list.data.siteEntry || []).map(s => s.siteUrl);
  const prefer = sites.find(s => s.includes('automatyn.co'));
  if (!prefer) throw new Error('automatyn.co not found in GSC properties: ' + sites.join(', '));
  return prefer;
}

async function query(siteUrl, dims) {
  const res = await wm.searchanalytics.query({
    siteUrl,
    requestBody: {
      startDate: fmt(start),
      endDate: fmt(end),
      dimensions: dims,
      rowLimit: 25
    }
  });
  return res.data.rows || [];
}

(async () => {
  const siteUrl = await tryProperties();
  console.log(`\n=== Search Console — ${siteUrl} — ${fmt(start)} to ${fmt(end)} (${days}d) ===\n`);

  const totals = await query(siteUrl, []);
  if (totals.length) {
    const t = totals[0];
    console.log('TOTALS:');
    console.log(`  Impressions: ${t.impressions}`);
    console.log(`  Clicks:      ${t.clicks}`);
    console.log(`  CTR:         ${(t.ctr * 100).toFixed(2)}%`);
    console.log(`  Avg pos:     ${t.position.toFixed(1)}\n`);
  } else {
    console.log('No data yet — site may not have organic impressions in this window.\n');
  }

  const queries = await query(siteUrl, ['query']);
  console.log('TOP QUERIES (by impressions):');
  queries.slice(0, 15).forEach(r => {
    console.log(`  ${String(r.impressions).padStart(5)} imp / ${String(r.clicks).padStart(3)} clk / pos ${r.position.toFixed(1)}  ${r.keys[0]}`);
  });

  const pages = await query(siteUrl, ['page']);
  console.log('\nTOP PAGES (by impressions):');
  pages.slice(0, 10).forEach(r => {
    const url = r.keys[0].replace('https://automatyn.co', '');
    console.log(`  ${String(r.impressions).padStart(5)} imp / ${String(r.clicks).padStart(3)} clk / pos ${r.position.toFixed(1)}  ${url}`);
  });

  console.log('');
})().catch(e => { console.error('ERROR:', e.message); process.exit(1); });
