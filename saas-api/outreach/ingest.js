// Ingest leads from Google Places API directly (bypasses n8n).
// Searches for plumbers in a list of UK cities and upserts them into the store.
//
// Usage:
//   GOOGLE_PLACES_API_KEY=... node ingest.js [city1,city2,...]
//
// Default cities: London + major UK cities. Use the arg to narrow down.

const store = require('./leads-store');

const API_KEY = process.env.GOOGLE_PLACES_API_KEY;
const DEFAULT_CITIES = [
  'London', 'Birmingham', 'Manchester', 'Leeds', 'Liverpool',
  'Sheffield', 'Bristol', 'Nottingham', 'Newcastle', 'Leicester',
  'Glasgow', 'Edinburgh', 'Cardiff',
];

async function searchCity(city) {
  const url = 'https://places.googleapis.com/v1/places:searchText';
  const body = { textQuery: `plumbers in ${city} UK`, pageSize: 20 };
  const all = [];
  let pageToken = null;
  // Up to 3 pages (~60 results) per city
  for (let i = 0; i < 3; i++) {
    const payload = pageToken ? { ...body, pageToken } : body;
    const res = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': API_KEY,
        'X-Goog-FieldMask': 'places.id,places.displayName,places.formattedAddress,places.internationalPhoneNumber,places.websiteUri,places.rating,places.userRatingCount,nextPageToken',
      },
      body: JSON.stringify(payload),
    });
    if (!res.ok) {
      const txt = await res.text();
      throw new Error(`Places API ${res.status}: ${txt}`);
    }
    const data = await res.json();
    for (const p of (data.places || [])) all.push(p);
    if (!data.nextPageToken) break;
    pageToken = data.nextPageToken;
    await new Promise(r => setTimeout(r, 2000)); // nextPageToken needs a short delay
  }
  return all;
}

async function run(cities) {
  if (!API_KEY) throw new Error('GOOGLE_PLACES_API_KEY not set');
  let created = 0, updated = 0, skipped = 0;
  for (const city of cities) {
    console.log(`\n[${city}] searching...`);
    const places = await searchCity(city);
    console.log(`  ${places.length} places`);
    for (const p of places) {
      const name = p.displayName?.text || '';
      if (!name) { skipped++; continue; }
      const partial = {
        business_name: name,
        website: p.websiteUri || '',
        phone: p.internationalPhoneNumber || '',
        address: p.formattedAddress || '',
        city,
        rating: p.rating || null,
        review_count: p.userRatingCount || null,
      };
      const r = store.upsert(partial);
      if (r.created) created++; else updated++;
    }
  }
  console.log(`\nDone. Created ${created}, updated ${updated}, skipped ${skipped}.`);
  console.log(store.stats());
}

if (require.main === module) {
  const arg = process.argv[2];
  const cities = arg ? arg.split(',').map(s => s.trim()).filter(Boolean) : DEFAULT_CITIES;
  run(cities).catch(err => { console.error(err); process.exit(1); });
}

module.exports = { run };
