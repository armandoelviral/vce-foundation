#!/bin/bash
set -euo pipefail

repo="$(git rev-parse --show-toplevel)/vce-core-tools/sp001-retail-reference"
gate=/private/var/db/sp001-gate
authority=/private/var/db/sp001-authority
service=system/com.sp001.gate-lab
original=/Library/LaunchDaemons/com.sp001.gate-lab.plist
route=http://127.0.0.1:18766/laboratory/product001/mvp1

sudo -v
test "$(id -u _sp001gate)" = 600
test "$(id -u _sp001commercial)" = 601
test "$(id -u _sp001authority)" = 602
sudo -n -u _sp001gate /bin/test -f "$gate/receipt-key.raw"
sudo launchctl print "$service" >/dev/null

for file in \
  src/sp001/infrastructure/product001_mvp1_gate_bootstrap.py \
  src/sp001/infrastructure/product001_mvp1_http_host.py \
  src/sp001/infrastructure/product001_mvp1_protected_composition.py \
  src/sp001/services/authenticated_product001_commercial_approval.py \
  tools/product001_mvp1_gate_lab.py; do
  sudo install -m 0644 "$repo/$file" "$gate/runtime/$file"
done

cd /
sandbox="$(sudo /usr/bin/mktemp -d /private/var/tmp/sp001-receipt-launchd.XXXXXX)"
job="$sandbox/gate.plist"
replaced=0
restore() {
  if [ "$replaced" = 1 ]; then
    if sudo launchctl print "$service" >/dev/null 2>&1; then
      sudo launchctl bootout "$service" || return 1
      sleep 3
    fi
    sudo launchctl bootstrap system "$original" || return 1
    printf 'Original Gate launchd configuration reloaded\n'
  fi
}
trap restore EXIT

run="$(sudo -n -u _sp001authority /usr/bin/mktemp -d "$authority/run.XXXXXX")/state"
sudo -n -u _sp001authority "$authority/venv/bin/python" \
  "$authority/runtime/tools/product001_mvp1_gate_lab.py" issue "$run" --authority-uid 602
handoff="$run/handoff"
state="$(sudo -n -u _sp001gate /usr/bin/mktemp -d "$gate/receipt-run.XXXXXX")"
for file in access-public.pem trust.json commercial.sqlite; do
  sudo install -o _sp001gate -g staff -m 0600 "$handoff/$file" "$state/$file"
done
sudo ditto "$handoff/documents" "$state/documents"
sudo chown -R _sp001gate:staff "$state/documents"

sudo cp "$original" "$job"
sudo /usr/libexec/PlistBuddy -c "Set :ProgramArguments:3 $state" "$job"
sudo /usr/libexec/PlistBuddy -c 'Add :ProgramArguments:6 string --enable-receipts' "$job"
sudo /usr/libexec/PlistBuddy -c 'Add :ProgramArguments:7 string --interrupt-before-receipt' "$job"
sudo plutil -lint "$job"

ready() {
  local code=000
  for attempt in 1 2 3 4 5 6 7 8 9 10; do
    code="$(/usr/bin/curl -q --noproxy '*' --max-time 2 -s \
      -o /dev/null -w '%{http_code}' -X POST -d '{}' "$route/decisions")" || code=000
    if [ "$code" = 401 ]; then return 0; fi
    sleep 1
  done
  sudo launchctl print "$service"
  return 1
}

sudo launchctl bootout "$service"
replaced=1
sleep 3
sudo launchctl bootstrap system "$job"
ready

code=0
sudo -n -u _sp001authority /bin/cat "$handoff/probe.curl" |
  sudo -n -u _sp001commercial /usr/bin/curl -q --noproxy '*' --max-time 5 -fsS --config - ||
  code=$?
test "$code" = 52
exit_code=
for attempt in 1 2 3 4 5; do
  exit_code="$(sudo launchctl print "$service" 2>/dev/null |
    awk '$1 == "last" && $2 == "exit" && $3 == "code" && $4 == "=" {print $5; exit}')" || exit_code=
  case "$exit_code" in
    76|EX_PROTOCOL) break ;;
  esac
  sleep 1
done
case "$exit_code" in
  76|EX_PROTOCOL) ;;
  *) printf 'Expected Gate exit 76, got %s\n' "${exit_code:-unavailable}" >&2; exit 1 ;;
esac
printf 'PASS: empty HTTP reply and Gate exit 76\n'

sudo launchctl bootout "$service"
sleep 3
sudo /usr/libexec/PlistBuddy -c 'Delete :ProgramArguments:7' "$job"
sudo launchctl bootstrap system "$job"
ready

recover() {
  sudo -n -u _sp001authority /usr/bin/sed 's@/mvp1/decisions"@/mvp1/receipts"@' "$handoff/probe.curl" |
    sudo -n -u _sp001commercial /usr/bin/curl -q --noproxy '*' --max-time 5 -fsS --config -
}
first="$(recover)"
second="$(recover)"
test "$first" = "$second"
printf 'PASS: identical receipt in two HTTP recoveries\n'

{
  sudo -n -u _sp001authority /usr/bin/grep '^data-binary = ' "$handoff/probe.curl"
  printf '%s\n' "$first"
} | sudo -n -u _sp001gate /usr/bin/env PYTHONPATH="$gate/runtime/src" \
    "$gate/venv/bin/python" -c '
from base64 import b64decode
from contextlib import closing
import json
from pathlib import Path
import sqlite3
import sys

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from sp001.contracts.product001_mvp1_commitment_certificate import CommitmentContextV1
from sp001.contracts.product001_mvp1_commercial_receipt import (
    CommercialReceiptStatementV1, CommercialReceiptV1, verify_commercial_receipt,
)
from sp001.infrastructure.product001_mvp1_http_codec import decode_product001_mvp1_commitment_certificate

body = json.loads(json.loads(sys.stdin.readline().split(" = ", 1)[1]))
certificate = decode_product001_mvp1_commitment_certificate(body["certificate"])
envelope = json.load(sys.stdin)["receipt"]
if envelope["version"] != 1:
    raise SystemExit("Unexpected receipt version")
statement = envelope["statement"]
statement["context"] = CommitmentContextV1(**statement["context"])
receipt = CommercialReceiptV1(
    CommercialReceiptStatementV1(**statement),
    b64decode(envelope["signature_b64"], validate=True),
)
key = Ed25519PrivateKey.from_private_bytes(Path(sys.argv[1]).read_bytes()).public_key()
verify_commercial_receipt(
    receipt, certificate=certificate, trusted_gate_id="sp001-gate-lab", trusted_gate_key=key,
)
with closing(sqlite3.connect(Path(sys.argv[2]).as_uri() + "?mode=ro", uri=True)) as db:
    counts = db.execute("""
      SELECT (SELECT count(*) FROM product001_commercial_decisions),
             (SELECT count(*) FROM product001_commercial_decision_audit)
    """).fetchone()
if counts != (1, 1):
    raise SystemExit(f"Expected 1|1, got {counts}")
print("PASS: Gate signature verified")
print("1|1")
' "$gate/receipt-key.raw" "$state/commercial.sqlite"

restore
replaced=0
trap - EXIT
printf 'Evidence database: %s/commercial.sqlite\n' "$state"
