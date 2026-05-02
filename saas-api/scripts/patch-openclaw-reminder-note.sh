#!/bin/bash
# Suppresses OpenClaw's "Note: I did not schedule a reminder..." leak.
# OpenClaw appends this note to outbound payloads when the LLM says
# "I'll follow up" / "I'll remind you" without scheduling a cron. The note
# is intended as an internal nudge for the next turn but ends up in the
# customer's WhatsApp reply.
#
# Patch: turn appendUnscheduledReminderNote into an identity function.
# Idempotent — safe to re-run.

set -euo pipefail

TARGET="/usr/lib/node_modules/openclaw/dist/agent-runner.runtime-CH0aH7T6.js"
MARKER="automatyn-reminder-note-suppressed"

if [ ! -f "$TARGET" ]; then
  echo "OpenClaw agent-runner not found at $TARGET" >&2
  exit 1
fi

if grep -q "$MARKER" "$TARGET"; then
  echo "Reminder-note patch already applied."
  exit 0
fi

sudo sed -i 's|function appendUnscheduledReminderNote(payloads) {|function appendUnscheduledReminderNote(payloads) { return payloads; /* automatyn-reminder-note-suppressed */|' "$TARGET"

if grep -q "$MARKER" "$TARGET"; then
  echo "Reminder-note patch applied."
else
  echo "Patch failed — anchor not found in $TARGET" >&2
  exit 1
fi
