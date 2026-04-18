module.exports = {
  content: [
    './*.html',
    './blog/*.html',
  ],
  safelist: [
    { pattern: /^(bg|text|border|ring)-(red|amber|emerald|cyan|zinc|gray|white|black)-(50|100|200|300|400|500|600|700|800|900)$/ },
    { pattern: /^(text|bg)-(white|black)$/ },
    { pattern: /^bg-\[#[0-9a-fA-F]+\]$/ },
    { pattern: /^text-\[#[0-9a-fA-F]+\]$/ },
    'lead-badge',
    'open',
    'active',
    'visible',
    'danger',
    'warning',
  ],
  theme: { extend: {} },
  plugins: [],
};
