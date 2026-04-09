# Automatyn Business Plan

## What We Do
Professional OpenClaw setup and configuration service. We install, configure, secure, and deploy OpenClaw for businesses across Telegram, Discord, Slack, WhatsApp, and 20+ messaging platforms.

## Website
- **Live:** https://automatyn.co (custom domain, purchased 2026-04-04)
- **Old URL:** automatyn.github.io (redirects to automatyn.co)
- **Google Search Console:** Verified + sitemap submitted for automatyn.co
- **Bing Webmaster:** Indexed, IndexNow submitted
- **Design:** Midnight Operator theme (Cabinet Grotesk + DM Sans, cyan/emerald on black)
- **Key feature:** Interactive multi-platform WhatsApp/Telegram/Discord demo in hero

## Pricing (competitive positioning)

| Tier | Price | What's included |
|---|---|---|
| Starter | $400 | Installation, 1 channel, basic security, 14-day support |
| Pro (most popular) | $800 | 3 channels, custom agent + skills, security hardening, 30-day support |
| Business | $1,500 | Unlimited channels, custom integrations, Docker sandboxing, 90-day support, onboarding call |
| Monthly Support | $150/mo | Updates, troubleshooting, priority response, 1x 30-min remote session |

## Competitive Landscape

| Competitor | Starter Price | Notes |
|---|---|---|
| SetupOpenClaw.sh | $3,000 | Premium, managed + hardware |
| OpenClawRUs | $2,000 | Setup + repair |
| OpenClaw Expert | $499 | Fast 24h setup |
| MyClaw | $599 | Mac-focused, $299/mo support |
| **Automatyn** | **$400** | Lowest entry, same-day setup |

## USP / Differentiation
- **Radical transparency:** show exact process, total cost of ownership, no hidden fees
- **Lowest entry point** in the market at $400
- **Free audit via email** -- lower friction than competitors who only offer calls
- **Monthly support at $150/mo** undercuts MyClaw ($299/mo) with same features

## Delivery Workflow
1. Client shares screen or SSH access
2. Claude Code handles installation, configuration, security, testing
3. We supervise and deliver -- typical setup: 1-2 hours (Starter), 2-3 hours (Pro)
4. Monthly support: client reports issue, we troubleshoot via Claude Code

## TikTok Content Pipeline (NataliaAI)

### Architecture (Updated)
```
Telegram Bot (Gemini Flash) ──► Research trending hooks
                               ──► Write 6 hook texts + CTA
                               ──► Save to hooks-queue/ folder
                                         │
Claude Code ◄─────────────────────────────┘
  ├─ Read hook texts from hooks-queue/
  ├─ Generate Natalia images via Forge (trained LoRA)
  ├─ Animate images via ComfyUI Wan2.2 (image-to-video)
  ├─ Add text overlays (PIL/ffmpeg)
  ├─ Stitch 6 clips into one TikTok video (ffmpeg)
  ├─ Write TikTok caption + hashtags
  ├─ Self-review quality, regenerate if needed
  ├─ Upload to Postiz API → TikTok
  │
Telegram Bot ◄─── gets notified
  ├─ Track metrics (views, likes, shares)
  ├─ Analyze what's working
  └─ Suggest new hooks ──► repeat
```

### Image Generation Setup
- **Forge:** Running on laptop via Tailscale (100.107.24.7:7860)
- **Model:** JuggernautXL Ragnarok (SDXL, photorealistic)
- **Resolution:** 896x1152 (TikTok portrait, ~2s per image)
- **Style:** Natalia character (trained LoRA), lifestyle aesthetic
- **Natalia LoRA:** Consistent character across all content — builds audience recognition

### Video Generation Setup
- **ComfyUI:** Running on laptop via Tailscale (100.107.24.7:8188)
- **GPU:** RTX 4070 Laptop, 8GB VRAM
- **Model:** Wan2.2 Image-to-Video 14B (FP8 quantized, fits 8GB VRAM)
- **Speed LoRA:** LightX2V 4-step (generates in 4 steps instead of 20+)
- **Flow:** Forge generates still → Wan2.2 animates 3-4s clip → repeat x6 → stitch
- **Status:** Models downloading (2026-03-25), ~19GB total

### Quality Control
- Option 1 + locked prompt templates
- Self-review each image/video before marking as ready
- Generate multiple variations for key slides, pick best
- Avoid: hand gestures (deformation risk), text on screens (gibberish)

### Postiz Integration
- **API Key:** Configured
- **TikTok Account:** realnataliana
- **Status:** Photo carousel posting broken (known Postiz bug #1338, #1220)
- **Workaround:** Convert slides to video → post as video (more reliable)
- **Fallback:** DIRECT_POST mode for video, skip UPLOAD/draft mode
- **Issue:** TikTok 5 pending shares limit may block posts — clear inbox first

## Progress Log

### 2026-03-25 (Session 1)
- Website fully redesigned: Satoshi font, gradient wordmark, dark theme
- Removed fake testimonials, replaced with honest copy
- Added free email audit CTA
- Competitive pricing set: $400 / $800 / $1,500
- SEO overhaul: keyword-optimized meta, sitemap, robots.txt
- Repo renamed to automatyn.github.io (root domain for SEO)
- Google Search Console verified + sitemap submitted
- Tested full TikTok slide generation pipeline via Forge
- Generated 6-slide carousel with self-review process (all 6 slides in hooks-queue/test-job-001/)
- Generated 3 variations for slide 5, selected best (penthouse + multiple devices)
- Designed split workflow: Telegram bot (research/overlay/metrics) + Claude Code (image gen)

### 2026-03-25 (Session 2)
- Connected Postiz API to TikTok (realnataliana account)
- Uploaded all 6 slides to Postiz successfully
- Attempted carousel post → discovered Postiz TikTok photo posting is broken (bugs #1338, #1220, #1059)
- Attempted video post (ffmpeg slideshow from 6 slides, 21s, 1.3MB) → also ERROR state
- Investigated root cause: Postiz code drops privacy_level in UPLOAD mode + TikTok 5 pending shares limit
- Contacted Postiz support — confirmed it's a known issue
- Decision: switch to video format instead of photo carousels
- Set up ComfyUI connection (100.107.24.7:8188, RTX 4070, 8GB VRAM)
- Started downloading Wan2.2 i2v models (~19GB): main model, text encoder, VAE, speed LoRA
- Decided to use Natalia character (trained LoRA) for all TikTok content — builds consistent brand
- Pipeline upgraded: still images → animated video clips → stitched TikTok video
- Claude Code now handles: image gen, video gen, text overlay, captions, Postiz upload (full pipeline)

### 2026-04-04 (Major Session)
- Custom domain purchased: automatyn.co ($12.48/yr on Namecheap)
- DNS configured, GitHub Pages serving on automatyn.co
- HTTPS enabled, all 65 internal URLs migrated from github.io
- Google Search Console verified for automatyn.co + sitemap submitted
- Bing indexed + IndexNow submitted for instant ChatGPT visibility
- GEO optimization: robots.txt (allows all AI crawlers), llms.txt, enhanced JSON-LD schema
- Answer-first content added for LLM crawler extraction
- Blog post #2 published: "What is OpenClaw and Why Every Business Needs It in 2026"
- Blog trigger updated to daily (using $100 Anthropic credit)
- WhatsApp demo added to homepage — cycles through 3 business types
- Demo upgraded to multi-platform: WhatsApp/Telegram/Discord with platform-specific UI
- Full site redesign: Midnight Operator theme (3 iterations)
  - v1: Gold/amber (rejected — looked muddy)
  - v2: LocalClaw-style split hero (rejected — copycat)
  - v3: Demo-centrepiece with flanking stats (final — unique)
- Applied frontend-design skill + antigravity skills (ux-persuasion, loss-aversion, marketing-psychology)
- Persuasion architecture implemented:
  - Section reorder: Comparison → Case Study → Price Anchoring → Pricing
  - Price anchoring: VA $2K/mo vs SaaS $200/mo vs Automatyn $400 one-time
  - Loss framing: "Every week without automation is lost time and missed leads"
  - Risk-reversal: 14-day guarantee on every pricing CTA
  - Varied CTAs: Get Started / Book Free Call / Talk to Us
- Launch discount banner: "First 5 setups at 50% off"
- Email forwarding: support@automatyn.co → patrickssons@outlook.com
- Brevo email sequence running (Day 2/5/7 follow-ups)
- Product Hunt launch scheduled for 2026-04-05 (12:01 AM Pacific)
- PH monitoring script created (ph_monitor.py)
- Browser Use + Frontend Design skills installed for Claude Code
- Antigravity Awesome Skills installed (1,234+ skills)
- ChatGPT confirmed finding automatyn.co when queried directly
- Favicon: cyan "A" on dark background
- Logo: "Automatyn." clean typographic (Cabinet Grotesk)
- Blog posts updated to match Midnight Operator theme
- Content ready to publish: 3 Medium articles, 10 Quora answers, 16 directory listings

### Audit Scores (2026-04-04)
| Skill | Score |
|---|---|
| Frontend Design | 4.4/5 |
| UX Persuasion (Fogg/Cialdini) | 4.4/5 |
| Loss Aversion (Kahneman) | 5.0/5 |
| Marketing Psychology (PLFS) | 3.8/5 |
| Landing Page Generator (PAS) | 4.8/5 |
| **Overall** | **4.5/5** |

### LLM Visibility (2026-04-04)
| Platform | Status |
|---|---|
| ChatGPT | ✅ Found when queried directly |
| Copilot | ✅ Bing indexed |
| Perplexity | ⚠️ Pending (1-3 days) |
| Google Gemini | ⚠️ Pending (1-3 days) |
| Google Search | ⚠️ Minimal — domain is new |
| Bing Search | ✅ Indexed (22 mentions) |

## Next Steps
- [ ] Product Hunt launch (2026-04-05) — monitor + reply to all comments
- [ ] Publish 3 Medium articles (copy ready)
- [ ] Post 10 Quora answers (copy ready)
- [ ] Submit to G2 when account unblocks
- [ ] Create Google Business Profile
- [ ] Get first paying customer → get testimonial → add to site
- [ ] Add testimonial section to homepage (PLFS +12 gap)
- [ ] Dev.to RSS import for blog syndication
- [ ] LinkedIn company page + articles
- [ ] Test Wan2.2 video pipeline for TikTok content
- [ ] Consider configuring Claude Haiku as bot fallback ($100 credit)
