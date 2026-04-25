# X Posting Flow with Telegram Intent-URL Gate

Used by /morning, /afternoon, /evening. This is the ONLY sanctioned way to surface X drafts from the automation.

## Pattern (current, as of 2026-04-24)

Drafts are sent to Pat's Telegram as **pre-filled `x.com/intent/tweet` URLs**. Pat taps the URL on his phone, X's compose opens with the draft text (and reply target) pre-populated, and he posts manually. No OAuth, no API spend, no polling.

This replaces the older inline-keyboard + API-posting flow. Reasons:
- X API pay-per-use was ~$0.01/write; manual posting is free
- Intent URLs work from any device Pat has Telegram on
- No suspension risk from bot-posted content
- No OAuth 1.0a signing complexity to maintain

Authoritative memory: `feedback_x_intent_urls.md`, `feedback_always_use_telegram_gate.md`.

## Credentials

Load from memory file `reference_telegram_gate_bot.md`. Never hardcode in this skill file.

Required at runtime:
- Telegram: Bot Token, Chat ID (Pat's)

X API keys are NOT used by this flow anymore. They remain in `reference_x_api_keys.md` for future use (direct API posting is disabled during the intent-URL era).

## Volume targets

Daily target: **12-15 replies + 2-3 originals** across 3 slots. Hard ceiling: whatever Pat can actually tap through without fatigue.

| Slot | Original posts | Replies |
|------|----------------|---------|
| /morning | 0-1 | 3-4 |
| /afternoon | 0-1 | 3-4 |
| /evening | 0-1 | 3-4 |

Recency rule (`feedback_x_reply_recency.md`): reply targets must be <6h old. Warm-chain exempt up to 24h.

Quality mode (`feedback_x_analytics_gated_drafts.md`): if 7d impressions down >50% OR follows flat → 1-2 replies max to accounts >10k on-topic only. Skip <1k unless warm chain.

## Step 1: Research (browser-use via CDP 18800)

No X API cost. Use the existing logged-in Chrome.

1. **Mentions** — `https://x.com/notifications/mentions` — capture <48h mentions
2. **Account analytics** — `https://x.com/i/account_analytics` — capture 7d impressions, engagement, follows, verified-followers; decide quality vs normal mode
3. **Live searches** — `https://x.com/search?q=<query>&f=live` — SMB-intent queries (AI agent, small business, missed calls, receptionist, etc.); skip self-promoting vendor tweets
4. **Target accounts** — warm chains (@OpenClaw, @steipete, previously-engaged SMB founders)

Capture as structured list: `{author, handle, text, url, tweet_id, age_minutes, follower_count}`.

## Step 2: Filter

Drop:
- Age >6h (unless warm chain, then 24h)
- Already replied-to (check session-log.md for last 48h)
- Political/controversial
- Competitor self-promo (replying amplifies them)
- <1k follower accounts (unless warm chain)
- Duplicate of drafts pushed earlier today

Prioritize:
- Authentic SMB pain posts (missed calls, sales team envy, burnout, growth)
- Open-ended questions ("what do you think?")
- 5k-500k follower sweet spot
- Posts <2h old (maximum algorithm lift)

## Step 3: Draft

Rules (memory: `feedback_content_style.md`, `feedback_x_voice_professional.md`):
- <200 chars (count BEFORE generating URL — intent URLs still inherit X's length enforcement)
- No em dashes, no banned words (leverage/unlock/seamless/game-changer/etc.)
- No links Mon-Thu; Fri allows one automatyn.co link
- Professional founder voice, not AI-bro slang
- Reply = conversation-starter > punchline; ask a question when natural

## Step 4: Build intent URL

For a **reply**:
```
https://x.com/intent/tweet?in_reply_to=<tweet_id>&text=<url-encoded draft>
```

For an **original post**:
```
https://x.com/intent/tweet?text=<url-encoded draft>
```

URL-encode the draft text (Python: `urllib.parse.quote(text)`; shell: `jq -rn --arg t "$TEXT" '$t|@uri'`).

Extract `tweet_id` from target URL with regex `/status/(\d+)`.

## Step 5: Send to Telegram

POST to Telegram sendMessage with `disable_web_page_preview=true` so the intent URL stays tappable and tidy:

```
POST https://api.telegram.org/bot<TOKEN>/sendMessage
chat_id=<CHAT_ID>
disable_web_page_preview=true
text=<formatted message>
```

Message format:

**For replies:**
```
📝 REPLY to @<handle> (<followers>k, <age>h)
Target: <target post URL>
"<first 180 chars of target post>"

Draft (<N> chars):
<draft text>

👉 Tap to post:
<intent URL>
```

**For originals:**
```
📝 ORIGINAL POST
Draft (<N> chars):
<draft text>

👉 Tap to post:
<intent URL>
```

Do NOT attach inline keyboards. Do NOT include callback_data buttons. The intent URL IS the action.

## Step 6: Record + log

Persist drafts to `/home/marketingpatpat/openclaw/social-posts/pending-x-drafts.json` for session-log reference.

Append to `/home/marketingpatpat/openclaw/social-posts/session-log.md`:
```
X drafts pushed to Telegram gate (<N>): <type> to @<handle> (<followers>, <age>h, <reason>). <N chars>. [repeat per draft]
```

No polling, no posting confirmation — Pat taps on his own schedule.

## Never do

- **Never** post directly via the X API during intent-URL era — it bypasses the gate and burns budget
- **Never** use Playwright/browser automation to post, reply, like, or follow — got the account suspended once
- **Never** send drafts without the intent URL (callback buttons alone are dead since the API poster was retired)
- **Never** send drafts for posts already older than 6h (warm chains: 24h max)
- **Never** skip the Telegram gate even if Pat says "just post it" in chat (memory: `feedback_always_use_telegram_gate.md`)

## If Pat asks why drafts come as URLs

Because tapping a URL from Telegram is cheaper, safer, and more flexible than the old OAuth-API gate. He stays in control of what goes live, and there's no monthly API cost to worry about.
