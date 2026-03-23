# OpenClaw Setup Service Website

A high-converting landing page for selling OpenClaw setup services.

## Quick Deploy (Free)

### Option 1: GitHub Pages (Recommended)

```bash
# 1. Create a new GitHub repository called "OCBusiness"

# 2. Push this code
cd OCBusiness
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/OCBusiness.git
git push -u origin main

# 3. Enable GitHub Pages
# Go to: Repository Settings → Pages → Source: main branch → Save

# 4. Your site will be live at:
# https://YOUR_USERNAME.github.io/OCBusiness
```

### Option 2: Vercel (Faster)

```bash
# 1. Install Vercel CLI
npm i -g vercel

# 2. Deploy
cd OCBusiness
vercel

# 3. Follow the prompts, your site will be live in seconds
```

### Option 3: Netlify

```bash
# 1. Install Netlify CLI
npm i -g netlify-cli

# 2. Deploy
cd OCBusiness
netlify deploy --prod
```

## Customization

### Update Branding

Edit `index.html` and search for:
- "OpenClaw Setup Service" — change company name
- "support@openclaw-setup.com" — change contact email
- Pricing values in the HTML

### Add Payment Integration

The current form generates a setup script. To accept payments:

1. **Gumroad** (Easiest):
   - Create a Gumroad product
   - Replace the form submit with a Gumroad checkout link
   - Gumroad handles payment + delivery

2. **Stripe Checkout**:
   - Create a Stripe account
   - Add Stripe Checkout integration
   - Modify the form to redirect to Stripe

3. **PayPal**:
   - Create PayPal buttons
   - Replace form submit with PayPal button

### Connect a Custom Domain

**GitHub Pages:**
1. Go to Repository Settings → Pages → Custom domain
2. Enter your domain (e.g., `openclaw-setup.com`)
3. Add CNAME record in your DNS: `your-username.github.io`

**Vercel/Netlify:**
1. Go to Project Settings → Domains
2. Add your domain and follow DNS instructions

## File Structure

```
OCBusiness/
├── index.html          # Main landing page
├── BUSINESS_PLAN.md    # Business implementation plan
├── README.md           # This file
└── scripts/            # (Optional) Additional setup scripts
```

## Features

- ✅ Responsive design (mobile-friendly)
- ✅ High-converting pricing tiers
- ✅ Interactive setup wizard
- ✅ Custom script generator
- ✅ SEO-optimized
- ✅ No backend required (100% client-side)
- ✅ Fast loading (Tailwind CDN)

## Cost Breakdown

| Item | Cost |
|------|------|
| Website hosting | $0 |
| Domain (optional) | ~$10/year |
| Payment processing | % per sale |
| **Total startup** | **$0** |

## Next Steps

1. Deploy the website (GitHub Pages)
2. Create a Gumroad product for payments
3. Set up a support email
4. Start marketing on TikTok/Reddit

See `BUSINESS_PLAN.md` for the complete implementation checklist.