#!/usr/bin/env node
/**
 * Regenerate 3 blog hero images using Gemini image generation.
 * Run this when Gemini free tier quota resets (daily ~07:00 UTC).
 *
 * Usage: node regen-blog-images.js
 *
 * Tries models in order: gemini-3-pro-image-preview, gemini-3.1-flash-image-preview, nano-banana-pro-preview
 * Tries both API keys. Saves to blog/images/ and exits.
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

const BLOG_IMAGES_DIR = path.join(__dirname, '..', 'blog', 'images');

// Load .env if present
const envPath = path.join(__dirname, '..', '.env');
if (fs.existsSync(envPath)) {
  for (const line of fs.readFileSync(envPath, 'utf-8').split('\n')) {
    const m = line.match(/^([A-Z_][A-Z0-9_]*)=(.*)$/);
    if (m && !process.env[m[1]]) process.env[m[1]] = m[2].trim();
  }
}

// Read keys from GEMINI_KEYS env var (comma-separated)
const KEYS = (process.env.GEMINI_KEYS || '').split(',').map(k => k.trim()).filter(Boolean);
if (!KEYS.length) {
  console.error('No API keys found. Set GEMINI_KEYS in .env (comma-separated).');
  process.exit(1);
}

const MODELS = [
  'gemini-3-pro-image-preview',
  'gemini-3.1-flash-image-preview',
  'gemini-2.5-flash-image',
  'nano-banana-pro-preview',
];

const IMAGES = [
  {
    filename: 'best-whatsapp-bot-hero.jpg',
    prompt: 'Professional photograph of a small business owner standing behind the counter of their shop, looking at their smartphone which shows a WhatsApp conversation. The shop is a cosy independent retail store with warm lighting. The owner looks pleased and relaxed. Shot from a slight angle, natural ambient lighting, shallow depth of field. No text overlays, no logos, no UI elements in the image. Photorealistic, editorial quality, landscape orientation 16:9.',
  },
  {
    filename: 'ai-receptionist-hero.jpg',
    prompt: 'Modern small business reception desk with a sleek desk phone and a laptop open on the counter. Soft warm lighting, minimalist interior design, a small potted plant on the desk. The scene suggests a professional but approachable business environment like a dental clinic or salon. No people visible, focus on the clean welcoming reception area. No text overlays, no logos. Photorealistic, editorial quality, landscape orientation 16:9.',
  },
  {
    filename: 'chatbot-setup-hero.jpg',
    prompt: 'Close-up of a person\'s hands holding a smartphone, the screen glowing softly. They are sitting at a wooden desk in a home office or small business setting. A laptop is open in the background, slightly out of focus. Warm natural light from a window. The mood is productive and focused. No text on screen visible, no logos. Photorealistic, editorial quality, landscape orientation 16:9.',
  },
];

function generateImage(prompt, model, key) {
  return new Promise((resolve, reject) => {
    const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${key}`;
    const body = JSON.stringify({
      contents: [{ role: 'user', parts: [{ text: prompt }] }],
      generationConfig: { responseModalities: ['IMAGE', 'TEXT'] },
    });

    const req = https.request(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(body) },
      timeout: 60000,
    }, (res) => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        try {
          const d = JSON.parse(data);
          if (d.error) {
            return reject(new Error(`${d.error.code}: ${d.error.message.slice(0, 120)}`));
          }
          const parts = d.candidates?.[0]?.content?.parts || [];
          for (const p of parts) {
            if (p.inlineData?.mimeType?.startsWith('image/')) {
              return resolve(Buffer.from(p.inlineData.data, 'base64'));
            }
          }
          reject(new Error('No image in response'));
        } catch (e) {
          reject(new Error(`Parse error: ${e.message}`));
        }
      });
    });
    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('Timeout')); });
    req.write(body);
    req.end();
  });
}

async function tryGenerate(prompt) {
  for (const model of MODELS) {
    for (const key of KEYS) {
      try {
        console.log(`  Trying ${model} (key ...${key.slice(-6)})...`);
        const buf = await generateImage(prompt, model, key);
        console.log(`  ✅ Success! ${buf.length} bytes`);
        return buf;
      } catch (err) {
        console.log(`  ❌ ${err.message}`);
        if (!err.message.includes('429')) {
          // Non-rate-limit error, try next model
          break;
        }
        // Rate limited on this key, try next key for same model
      }
    }
  }
  return null;
}

async function main() {
  console.log('=== Blog Hero Image Regeneration ===');
  console.log(`Output dir: ${BLOG_IMAGES_DIR}`);
  console.log(`Time: ${new Date().toISOString()}\n`);

  let success = 0;
  let failed = 0;

  for (const img of IMAGES) {
    console.log(`[${img.filename}]`);
    const buf = await tryGenerate(img.prompt);
    if (buf) {
      const outPath = path.join(BLOG_IMAGES_DIR, img.filename);
      fs.writeFileSync(outPath, buf);
      console.log(`  Saved: ${outPath} (${(buf.length / 1024).toFixed(0)} KB)\n`);
      success++;
    } else {
      console.log(`  FAILED: All models/keys exhausted\n`);
      failed++;
    }

    // Small delay between images to avoid burst rate limits
    if (IMAGES.indexOf(img) < IMAGES.length - 1) {
      await new Promise(r => setTimeout(r, 3000));
    }
  }

  console.log(`\n=== Done: ${success} generated, ${failed} failed ===`);

  if (success > 0) {
    console.log('\nNext steps:');
    console.log('  cd /home/marketingpatpat/openclaw');
    console.log('  git add blog/images/best-whatsapp-bot-hero.jpg blog/images/ai-receptionist-hero.jpg blog/images/chatbot-setup-hero.jpg');
    console.log('  git commit -m "regen: replace Pollinations blog heroes with Gemini images"');
    console.log('  git push');
  }

  process.exit(failed > 0 ? 1 : 0);
}

main().catch(err => {
  console.error('Fatal:', err);
  process.exit(1);
});
