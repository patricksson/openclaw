// Audit indexing state of every blog/*.html via Google Search Console URL Inspection API.
// Outputs a bucketed summary so we know how many are stuck.
const fs = require('fs');
const path = require('path');
const { google } = require('googleapis');

const ROOT = '/home/marketingpatpat/openclaw/saas-api';
const CLIENT_PATH = path.join(ROOT, 'secrets', 'gsc-oauth-client.json');
const TOKEN_PATH = path.join(ROOT, 'secrets', 'gsc-token.json');
const SITE = 'sc-domain:automatyn.co'; // matches what gsc-fetch sees

const client = JSON.parse(fs.readFileSync(CLIENT_PATH, 'utf8')).installed;
const tokens = JSON.parse(fs.readFileSync(TOKEN_PATH, 'utf8'));
const oauth2 = new google.auth.OAuth2(client.client_id, client.client_secret);
oauth2.setCredentials(tokens);
const sc = google.searchconsole({ version: 'v1', auth: oauth2 });

(async () => {
  // List all blog files
  const blogDir = '/home/marketingpatpat/openclaw/blog';
  const slugs = fs.readdirSync(blogDir).filter(f => f.endsWith('.html') && f !== 'index.html');
  console.log(`Inspecting ${slugs.length} blog URLs...`);

  const buckets = {};
  const details = [];

  for (let i = 0; i < slugs.length; i++) {
    const slug = slugs[i];
    const url = `https://automatyn.co/blog/${slug}`;
    process.stdout.write(`[${i+1}/${slugs.length}] ${slug}...`);
    try {
      const r = await sc.urlInspection.index.inspect({
        requestBody: {
          inspectionUrl: url,
          siteUrl: SITE,
        },
      });
      const idx = r.data.inspectionResult?.indexStatusResult || {};
      const verdict = idx.verdict || 'UNKNOWN';
      const coverage = idx.coverageState || 'UNKNOWN';
      const robots = idx.robotsTxtState || '';
      const indexing = idx.indexingState || '';
      const lastCrawl = idx.lastCrawlTime || '';
      const k = `${verdict} :: ${coverage}`;
      buckets[k] = (buckets[k] || 0) + 1;
      details.push({ slug, verdict, coverage, robots, indexing, lastCrawl });
      console.log(` ${verdict} / ${coverage}`);
    } catch (e) {
      buckets['ERROR'] = (buckets['ERROR'] || 0) + 1;
      details.push({ slug, error: e.message });
      console.log(` ERROR ${e.message.slice(0,80)}`);
    }
    await new Promise(r => setTimeout(r, 300)); // rate limit politeness
  }

  console.log('\n\n=== SUMMARY ===');
  for (const [k, n] of Object.entries(buckets).sort((a,b) => b[1]-a[1])) {
    console.log(`  ${n.toString().padStart(4)}  ${k}`);
  }
  fs.writeFileSync('/tmp/gsc-coverage-detail.json', JSON.stringify(details, null, 2));
  console.log('\nFull detail written to /tmp/gsc-coverage-detail.json');
})().catch(e => { console.error(e); process.exit(1); });
