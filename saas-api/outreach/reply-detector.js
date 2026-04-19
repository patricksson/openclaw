// Reply detector — polls Gmail inbox for messages from leads.
// When a lead replies, mark replied=true so follow-ups stop.
//
// Uses Gmail API (OAuth) — not IMAP. Requires a refresh token for patrick@automatyn.co.
// Env:
//   GMAIL_OAUTH_CLIENT_ID
//   GMAIL_OAUTH_CLIENT_SECRET
//   GMAIL_OAUTH_REFRESH_TOKEN
//
// One-off setup to get a refresh token is documented in README.md.
// Until those are set, this script exits cleanly with a message.

const { google } = require('googleapis');
const store = require('./leads-store');

const CID = process.env.GMAIL_OAUTH_CLIENT_ID;
const CSECRET = process.env.GMAIL_OAUTH_CLIENT_SECRET;
const RTOK = process.env.GMAIL_OAUTH_REFRESH_TOKEN;

async function gmailClient() {
  const oauth2 = new google.auth.OAuth2(CID, CSECRET);
  oauth2.setCredentials({ refresh_token: RTOK });
  return google.gmail({ version: 'v1', auth: oauth2 });
}

// Bounce detection: Gmail flags bounces from mailer-daemon with a failed-recipient header.
function extractFailedRecipient(headers, snippet) {
  const h = (name) => (headers.find(x => x.name.toLowerCase() === name.toLowerCase()) || {}).value || '';
  const xFailed = h('X-Failed-Recipients');
  if (xFailed) return xFailed.trim();
  // Fallback: pull first email from snippet
  const m = snippet && snippet.match(/([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})/);
  return m ? m[1] : null;
}

async function run(lookbackHours = 24) {
  if (!CID || !CSECRET || !RTOK) {
    console.log('Gmail OAuth env not set — skipping. See outreach/README.md.');
    return;
  }
  const gmail = await gmailClient();
  const afterTs = Math.floor((Date.now() - lookbackHours * 3600 * 1000) / 1000);
  const q = `in:inbox after:${afterTs}`;
  let replyCount = 0, bounceCount = 0;

  const list = await gmail.users.messages.list({ userId: 'me', q, maxResults: 100 });
  const msgs = list.data.messages || [];
  console.log(`Scanning ${msgs.length} inbox messages...`);

  for (const { id } of msgs) {
    const msg = await gmail.users.messages.get({ userId: 'me', id, format: 'metadata', metadataHeaders: ['From', 'Subject', 'X-Failed-Recipients', 'Auto-Submitted'] });
    const headers = msg.data.payload.headers || [];
    const fromHdr = (headers.find(h => h.name === 'From') || {}).value || '';
    const subj = (headers.find(h => h.name === 'Subject') || {}).value || '';
    const fromEmailMatch = fromHdr.match(/([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})/);
    const fromEmail = fromEmailMatch ? fromEmailMatch[1].toLowerCase() : null;
    if (!fromEmail) continue;

    // Bounce? mailer-daemon, delivery failure, etc.
    const isBounce = /mailer-daemon|postmaster@/i.test(fromHdr) || /delivery\s*(status|failure)|returned mail|undeliver/i.test(subj);
    if (isBounce) {
      const failed = extractFailedRecipient(headers, msg.data.snippet);
      if (failed) {
        const lead = store.findByEmail(failed);
        if (lead && !lead.bounced) {
          store.update(lead.id, { bounced: true });
          bounceCount++;
          console.log(`  ✗ bounce: ${failed} (${lead.business_name})`);
        }
      }
      continue;
    }

    // Reply? from matches a lead's email
    const lead = store.findByEmail(fromEmail);
    if (lead && !lead.replied) {
      store.update(lead.id, { replied: true });
      replyCount++;
      console.log(`  ✓ reply from ${fromEmail} (${lead.business_name}) — "${subj}"`);
    }
  }
  console.log(`Done. Replies: ${replyCount}, bounces: ${bounceCount}.`);
}

if (require.main === module) {
  const hours = parseInt(process.argv[2], 10) || 24;
  run(hours).catch(err => { console.error(err); process.exit(1); });
}

module.exports = { run };
