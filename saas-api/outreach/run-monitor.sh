#!/bin/bash
# Wrapper for cron: load BREVO_API_KEY from user-readable shadow, run monitor.js.
# Shadow file at ~/.automatyn-monitor.env (chmod 600). Only contains BREVO_API_KEY,
# the only env var the monitor needs.
set -e
if [ -f "$HOME/.automatyn-monitor.env" ]; then
  set -a
  source "$HOME/.automatyn-monitor.env"
  set +a
fi
cd /home/marketingpatpat/openclaw/saas-api
exec /usr/bin/node outreach/monitor.js
