"""
X Reply Monitor — polls big accounts every 5 minutes, drafts + posts replies automatically.

Usage: nohup python3 /home/marketingpatpat/openclaw/scripts/reply-monitor.py > /tmp/reply-monitor.log 2>&1 &

Runs forever. Kill with: pkill -f reply-monitor.py
"""
import json, time, random, os, urllib.request, subprocess
from datetime import datetime, timezone

# === CONFIG ===
WATCHLIST = [
    "sama",           # Sam Altman
    "AnthropicAI",    # Anthropic
    "OpenAI",         # OpenAI
    "gregisenberg",   # Side hustles / SaaS
    "TrungTPhan",     # Tech/business viral
    "levaboroshansky",# AI founders
    "taborosi",       # AI hot takes
    "marc_louvion",   # Indie hacker
    "danshipper",     # AI writing
    "swaboroda",      # AI builder
    "trikcode",       # AI startups
    "thegarrisonway", # Small biz
    "maboroshi_ai",   # AI tools
]

POLL_INTERVAL = 300  # 5 minutes
SEEN_FILE = "/home/marketingpatpat/openclaw/scripts/.seen_tweets.json"
REPLY_LOG = "/home/marketingpatpat/openclaw/social-posts/reply-log.md"
GEMINI_KEY = "AIzaSyBypvj2paAZYWCnZ4eG5O7qe2H2LjSL9Xk"
MY_HANDLE = "patrickssons"

# Automatyn mission context for Gemini reply drafting
SYSTEM_PROMPT = """You are Patrick's X reply ghostwriter. Patrick runs Automatyn (automatyn.co), an AI agent setup service for small businesses.

Write a reply to the tweet below. Rules:
- MAXIMUM CONTROVERSY optimised for views, followers, conversions
- Contrarian: challenge what people believe
- Position Patrick as someone who knows how AI agents actually work for small businesses
- Bridge to AI agent expertise where natural: "the setup file matters more than the model", "most bots fail because nobody wrote the rules", "the configuration is the product"
- Do NOT pitch Automatyn directly. Build authority and curiosity.
- Under 200 characters
- Sound human, not AI
- No em dashes
- No banned words: leverage, unlock, seamless, game-changer, revolutionary, cutting-edge, streamline, empower
- One strong opinion, not a question
- If the tweet has no bridge to AI/automation/small business, write a sharp general contrarian take instead

Output ONLY the reply text. Nothing else. No quotes, no explanation."""

def load_seen():
    if os.path.exists(SEEN_FILE):
        return json.load(open(SEEN_FILE))
    return {}

def save_seen(seen):
    json.dump(seen, open(SEEN_FILE, "w"))

def check_user(handle):
    """Fetch latest tweet from a user via fxtwitter"""
    try:
        req = urllib.request.Request(
            f"https://api.fxtwitter.com/{handle}",
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
            tweets = data.get("tweets", [])
            if tweets:
                t = tweets[0]
                return {
                    "id": t.get("id"),
                    "text": t.get("text", ""),
                    "url": t.get("url", ""),
                    "created": t.get("created_timestamp", 0),
                    "likes": t.get("likes", 0),
                    "replies": t.get("replies", 0),
                }
    except Exception as e:
        print(f"  err checking @{handle}: {e}")
    return None

def draft_reply(tweet_text):
    """Use Gemini to draft a reply"""
    prompt = f"{SYSTEM_PROMPT}\n\nTWEET TO REPLY TO:\n{tweet_text}"
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.9, "maxOutputTokens": 200}
    }
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_KEY}",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.loads(r.read())
            reply = d["candidates"][0]["content"]["parts"][0]["text"].strip()
            # Clean up any quotes Gemini might wrap it in
            reply = reply.strip('"').strip("'")
            if len(reply) > 280:
                reply = reply[:277] + "..."
            return reply
    except Exception as e:
        print(f"  gemini err: {e}")
    return None

def post_reply(tweet_url, reply_text):
    """Post reply via Playwright CDP"""
    script = f'''
import sys
from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    try:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:18800")
        context = browser.contexts[0]
        page = context.new_page()
        page.goto("{tweet_url}", timeout=30000)
        time.sleep(5)

        cdp = context.new_cdp_session(page)
        cdp.send("Browser.grantPermissions", {{
            "permissions": ["clipboardReadWrite", "clipboardSanitizedWrite"],
            "origin": "https://x.com"
        }})

        reply_box = page.query_selector('[data-testid="tweetTextarea_0"]')
        if reply_box:
            reply_box.click()
            time.sleep(0.5)
            cdp.send("Runtime.evaluate", {{
                "expression": "navigator.clipboard.writeText({repr(reply_text)})",
                "awaitPromise": True
            }})
            time.sleep(0.3)
            page.keyboard.press("Control+V")
            time.sleep(2)
            post_btn = page.query_selector('[data-testid="tweetButtonInline"]')
            if post_btn:
                post_btn.click()
                time.sleep(3)
                print("POSTED")
            else:
                print("NO_BUTTON")
        else:
            print("NO_REPLY_BOX")
        page.close()
        browser.close()
    except Exception as e:
        print(f"ERR: {{e}}")
'''
    result = subprocess.run(["python3", "-c", script], capture_output=True, text=True, timeout=60)
    return "POSTED" in result.stdout

def log_reply(handle, url, reply_text):
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    with open(REPLY_LOG, "a") as f:
        f.write(f"- {date} | @{handle} | {url} | {reply_text[:60]}\n")

def is_fresh(tweet, max_age_minutes=30):
    """Only reply to tweets under 30 minutes old"""
    if not tweet or not tweet.get("created"):
        return False
    now = time.time()
    age = now - tweet["created"]
    return age < (max_age_minutes * 60)

def already_replied(url):
    if not os.path.exists(REPLY_LOG):
        return False
    log = open(REPLY_LOG).read()
    return url in log

def already_replied_to_user_today(handle):
    if not os.path.exists(REPLY_LOG):
        return False
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    for line in open(REPLY_LOG):
        if today in line and f"@{handle}" in line:
            return True
    return False

# === MAIN LOOP ===
print(f"Reply Monitor started at {datetime.now(timezone.utc).isoformat()}")
print(f"Watching {len(WATCHLIST)} accounts, polling every {POLL_INTERVAL}s")
print(f"Only replying to tweets under 30 minutes old")

seen = load_seen()

while True:
    try:
        for handle in WATCHLIST:
            if handle.lower() == MY_HANDLE.lower():
                continue

            tweet = check_user(handle)
            if not tweet or not tweet.get("id"):
                continue

            tid = tweet["id"]

            # Skip if already seen
            if tid in seen:
                continue

            # Mark as seen regardless of whether we reply
            seen[tid] = time.time()
            save_seen(seen)

            # Skip if too old
            if not is_fresh(tweet, max_age_minutes=30):
                print(f"  @{handle}: new tweet but too old ({tid})")
                continue

            # Skip if already replied to this URL or user today
            if already_replied(tweet["url"]):
                continue
            if already_replied_to_user_today(handle):
                print(f"  @{handle}: already replied today, skipping")
                continue

            print(f"\n>>> NEW TWEET from @{handle} ({tweet['likes']} likes)")
            print(f"    {tweet['text'][:120]}")
            print(f"    {tweet['url']}")

            # Draft reply
            reply = draft_reply(tweet["text"])
            if not reply:
                print("  Failed to draft reply, skipping")
                continue

            print(f"    DRAFT: {reply}")

            # Post it
            success = post_reply(tweet["url"], reply)
            if success:
                print(f"    POSTED REPLY to @{handle}")
                log_reply(handle, tweet["url"], reply)
            else:
                print(f"    FAILED to post reply to @{handle}")

            # Wait 5-10 min before next reply to avoid spam
            wait = random.randint(300, 600)
            print(f"    Waiting {wait}s before next potential reply...")
            time.sleep(wait)

        # Clean old entries from seen (keep last 48 hours)
        cutoff = time.time() - (48 * 3600)
        seen = {k: v for k, v in seen.items() if v > cutoff}
        save_seen(seen)

    except Exception as e:
        print(f"Loop error: {e}")

    # Wait before next poll cycle
    print(f"\n--- sleeping {POLL_INTERVAL}s until next poll ---")
    time.sleep(POLL_INTERVAL)
