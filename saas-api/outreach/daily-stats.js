// Nightly stats email to Pat (patricksson@gmail.com).
// Uses the same Gmail SMTP transport as sender.js.

const nodemailer = require('nodemailer');
const store = require('./leads-store');

const GMAIL_USER = process.env.GMAIL_USER || 'patrick@automatyn.co';
const GMAIL_APP_PASSWORD = process.env.GMAIL_APP_PASSWORD;
const REPORT_TO = process.env.OUTREACH_REPORT_TO || 'patricksson@gmail.com';

async function run() {
  if (!GMAIL_APP_PASSWORD) {
    console.log('GMAIL_APP_PASSWORD not set — printing stats only.');
    console.log(store.stats());
    return;
  }
  const s = store.stats();
  const today = new Date().toISOString().slice(0, 10);
  const subject = `[Outreach] ${today} — E1:${s.email1_sent_today} E2:${s.email2_sent_today} E3:${s.email3_sent_today} replies:${s.replied_total}`;
  const body = [
    `Outreach report — ${today}`,
    '',
    'Today:',
    `  Email 1 sent: ${s.email1_sent_today}`,
    `  Email 2 sent: ${s.email2_sent_today}`,
    `  Email 3 sent: ${s.email3_sent_today}`,
    '',
    'Totals:',
    `  Leads in DB: ${s.total}`,
    `  With email:  ${s.with_email}`,
    `  Personalised: ${s.personalised}`,
    `  Email 1 (lifetime): ${s.email1_sent_total}`,
    `  Email 2 (lifetime): ${s.email2_sent_total}`,
    `  Email 3 (lifetime): ${s.email3_sent_total}`,
    `  Replies: ${s.replied_total}`,
    `  Bounces: ${s.bounced_total}`,
    `  Unsubs:  ${s.unsubscribed_total}`,
    '',
    'Engagement:',
    `  E1 opens: ${s.email1_opens}/${s.email1_sent_total} (${s.email1_sent_total ? Math.round(100 * s.email1_opens / s.email1_sent_total) : 0}%)`,
    `  E2 opens: ${s.email2_opens}/${s.email2_sent_total} (${s.email2_sent_total ? Math.round(100 * s.email2_opens / s.email2_sent_total) : 0}%)`,
    `  E3 opens: ${s.email3_opens}/${s.email3_sent_total} (${s.email3_sent_total ? Math.round(100 * s.email3_opens / s.email3_sent_total) : 0}%)`,
  ].join('\n');

  const tx = nodemailer.createTransport({ service: 'gmail', auth: { user: GMAIL_USER, pass: GMAIL_APP_PASSWORD } });
  await tx.sendMail({ from: `Automatyn Outreach <${GMAIL_USER}>`, to: REPORT_TO, subject, text: body });
  console.log('Stats email sent to', REPORT_TO);
}

if (require.main === module) run().catch(e => { console.error(e); process.exit(1); });
module.exports = { run };
