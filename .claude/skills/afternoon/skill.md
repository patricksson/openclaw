---
name: afternoon
description: Midday run — generate TikTok carousels, check triggers, post content, check stats
user_invocable: true
---

# Afternoon Routine

Midday content production and monitoring. Do NOT ask for permission. Execute everything and report.

## Step 0: Recap of Last /morning

Read `/home/marketingpatpat/openclaw/social-posts/session-log.md` and find the most recent `/morning` entry. Print a brief recap.

## Step 1: Check Content Machine Trigger

The Content Machine trigger fires at 14:00 UTC daily. Use RemoteTrigger tool (load via ToolSearch) to check trigger `trig_01VCuzhEoftowx3adqtibsP5`:
- Is it still enabled?
- Did it fire? Check git log for new commits since this morning
- If it auto-disabled, re-enable it immediately

## Step 2: Check X Account Status

```
curl -s "https://api.fxtwitter.com/patrickssons"
```
If 404, still suspended. Skip X steps. If user data returned, account is back.

**IF X IS BACK:** Use X API v2 for posting. NEVER use Playwright. Set up API credentials if not done.

## Step 3: Generate TikTok Carousels (2-3 per session)

**USE LARRY-BRAIN FRAMEWORK** from /home/marketingpatpat/.openclaw/workspace/skills/larry-marketing/references/slide-structure.md

**Check TikTok trending hashtags first:**
Visit https://ads.tiktok.com/business/creativecenter/inspiration/popular/hashtag/pc/en via Playwright (read-only).

**Hook selection — Tier 1 (Person + Conflict) performs best:**
- Family hooks get highest views (Mum: 806, Dad: 801, Boss: 652)
- Use a different conflict character than morning session
- Clickbait POV title: "POV: Your therapist sees your income", "POV: Your neighbour finds out"

**For each carousel:**
1. Write hook using larry-brain Tier 1 formula
2. Generate 6 FACELESS images using Gemini API:
   - Key: AIzaSyAmPorlpwgAun4Ublvz0yUq4orDCqVTlQ0
   - Model: gemini-3-pro-image-preview
   - ALL faceless (behind, hands, overhead, over shoulder)
   - Dark moody aesthetic matching existing TikTok videos
3. Burn text overlays using burn_text.py at /home/marketingpatpat/openclaw-full/tiktok-marketing/generated/2026-04-08/burn_text.py
4. Upload to Postiz and create TikTok post (content_posting_method:"UPLOAD")
5. Caption: max 5 hashtags. Clickbait POV title.

Postiz credentials:
- Token: 3991893608a82e890e652dc586fbf227e46d37647533419980e05d3681e7fa26
- TikTok integration: cmmzd0apq03pmp30yh70b3uti

## Step 4: Check TikTok Stats

```
yt-dlp --flat-playlist --dump-json "https://www.tiktok.com/@realnataliana"
```
Report views, likes, top performers. Compare with morning stats.

## Step 5: Post LinkedIn (if not posted in morning)

Post 1 LinkedIn update via Postiz if morning didn't post one.
- LinkedIn integration: cmnmbgu9r04w4so0ygvvi0ere

## Step 6: Check TikTok DMs

Remind Pat to check TikTok DMs for potential leads. If someone asks "is this real?" or "how does this work?", reply as Natalia (happy customer), not as the founder:
- "Yeah! I got mine set up by this guy who does it for small businesses. Want me to send you his details?"

## Step 7: Report

```
AFTERNOON REPORT — [DATE]
===========================
X STATUS: [suspended/reinstated]
TRIGGERS: Content Machine [status]
TIKTOK: [videos, views, likes]
  New carousels: [hooks pushed]
  Top performer: [title + views]
  DMs: [any new leads?]
LINKEDIN: [posted/skipped]
```

## Step 8: Write Session Log

Append to `/home/marketingpatpat/openclaw/social-posts/session-log.md` and commit/push.

## Content Rules (MUST follow everywhere)
- NEVER use em dashes
- NEVER use banned words (leverage, unlock, seamless, etc.)
- No fake prices. Real: $400 / $800 / $1500 + $150/mo
- NEVER use Playwright to post/reply/like on any platform with an API
- Sound human and professional, not AI-generated
