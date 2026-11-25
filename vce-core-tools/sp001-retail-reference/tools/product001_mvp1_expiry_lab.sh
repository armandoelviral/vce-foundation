#!/bin/bash
# Run the recovered-expiry experiment on the existing macOS lab deployment.
set -euo pipefail

mode="${1:-expiry}"
case "$mode" in
  expiry|revocation) ;;
  *) printf 'Usage: %s [expiry|revocation]\n' "$0" >&2; exit 2 ;;
esac

project="$(cd "$(dirname "$0")/.." && pwd)"
authority=/private/var/db/sp001-authority
gate=/private/var/db/sp001-gate
service=system/com.sp001.gate-lab
job=/Library/LaunchDaemons/com.sp001.gate-lab.plist
route=http://127.0.0.1:18766/laboratory/product001/mvp1/decisions
tool="$authority/runtime/tools/product001_mvp1_gate_lab.py"
python="$authority/venv/bin/python"

sudo -v
test "$(sudo -n -u _sp001authority /usr/bin/id -u)" = 602
test "$(sudo -n -u _sp001gate /usr/bin/id -u)" = 600
test "$(sudo -n -u _sp001commercial /usr/bin/id -u)" = 601
sudo plutil -lint "$job"
sudo -n -u _sp001authority "$python" "$tool" --help | grep -q -- '--interrupt-after-commit'
sudo install -m 0644 "$project/tools/product001_mvp1_gate_lab.py" "$tool"
register=src/sp001/infrastructure/sqlite_product001_mvp1_authorization_store.py
sudo install -m 0644 "$project/$register" "$authority/runtime/$register"
cd /

if [ "$mode" = revocation ]; then
  before="$(sudo -n -u _sp001authority /usr/bin/mktemp -d "$authority/run.XXXXXX")/state"
  sudo -n -u _sp001authority "$python" "$tool" issue "$before" \
    --authority-uid 602 --revocation-order before-consume
  sudo -n -u _sp001authority "$python" - "$before" <<'PY'
from contextlib import closing
from pathlib import Path
import sqlite3
import sys

state = Path(sys.argv[1])
handoff = state / "handoff"
with closing(sqlite3.connect((state / "authority.sqlite").as_uri() + "?mode=ro", uri=True)) as db:
    if db.execute("SELECT revoked FROM mvp1_authorizations").fetchall() != [(1,)]:
        raise SystemExit("Expected one revoked authorization")
    if db.execute("SELECT count(*) FROM mvp1_authorization_intents").fetchone() != (0,):
        raise SystemExit("Unexpected durable intent")
    events = db.execute(
        "SELECT kind FROM mvp1_authorization_transitions ORDER BY sequence"
    ).fetchall()
    if events != [("REVOKED",)]:
        raise SystemExit("Expected only a recorded revocation")
print("Authority order before case: REVOKED")
if (handoff / "trust.json").exists() or (handoff / "probe.curl").exists():
    raise SystemExit("Unexpected certificate delivery")
with closing(sqlite3.connect((handoff / "commercial.sqlite").as_uri() + "?mode=ro", uri=True)) as db:
    counts = db.execute("""
        SELECT (SELECT count(*) FROM product001_commercial_decisions),
               (SELECT count(*) FROM product001_commercial_decision_audit)
    """).fetchone()
if counts != (0, 0):
    raise SystemExit("Expected 0|0")
print("Before: revoked=1, durable intents=0, commercial=0|0")
PY
  issue_args=(--revocation-order after-consume)
else
  issue_args=(--commitment-ttl-seconds 30)
fi

run="$(sudo -n -u _sp001authority /usr/bin/mktemp -d "$authority/run.XXXXXX")"
state="$run/state"
handoff="$state/handoff"
code=0
sudo -n -u _sp001authority "$python" "$tool" issue "$state" --authority-uid 602 \
  --interrupt-after-commit "${issue_args[@]}" || code=$?
test "$code" = 75
printf 'Interruption after commit: %s\n' "$code"
first="$(sudo -n -u _sp001authority "$python" "$tool" recover "$state" --authority-uid 602)"
second="$(sudo -n -u _sp001authority "$python" "$tool" recover "$state" --authority-uid 602)"
test "$first" = "$second"
printf '%s\nRecovered run: %s\n' "$first" "$state"
deadline="${first##* }"
if [ "$mode" = revocation ]; then
  sudo -n -u _sp001authority "$python" - "$state/authority.sqlite" <<'PY'
from contextlib import closing
from pathlib import Path
import sqlite3
import sys

with closing(sqlite3.connect(Path(sys.argv[1]).as_uri() + "?mode=ro", uri=True)) as db:
    events = db.execute(
        "SELECT kind FROM mvp1_authorization_transitions ORDER BY sequence"
    ).fetchall()
if events != [("CONSUMED",), ("REVOKED",)]:
    raise SystemExit("Expected consumption followed by revocation")
print("Authority order after case: CONSUMED -> REVOKED")
PY
fi

incoming="$(sudo -n -u _sp001gate /usr/bin/mktemp -d "$gate/incoming.XXXXXX")"
for file in access-public.pem trust.json commercial.sqlite; do
  sudo install -o _sp001gate -g staff -m 0600 "$handoff/$file" "$incoming/$file"
done
sudo ditto "$handoff/documents" "$incoming/documents"
sudo chown -R _sp001gate:staff "$incoming/documents"
sudo cmp "$handoff/trust.json" "$incoming/trust.json"

if sudo launchctl print "$service" >/dev/null 2>&1; then
  sudo launchctl bootout "$service"
fi
archive="$(sudo /usr/bin/mktemp -d "$gate/archive.XXXXXX")"
sudo mv "$gate/lab-state" "$archive/"
sudo mv "$incoming" "$gate/lab-state"
printf 'Previous state archived at %s\n' "$archive"
sleep 2
if ! sudo launchctl bootstrap system "$job"; then
  sleep 3
  if ! sudo launchctl print "$service" >/dev/null 2>&1; then
    sudo launchctl bootstrap system "$job"
  fi
fi

status=000
for attempt in 1 2 3 4 5 6 7 8 9 10; do
  status="$(/usr/bin/curl -q --noproxy '*' --max-time 2 -s \
    -o /dev/null -w '%{http_code}' -X POST -d '{}' "$route")" || status=000
  [ "$status" = 401 ] && break
  sleep 1
done
test "$status" = 401
if [ "$mode" = revocation ]; then
  for expected in '{"recorded":true}' '{"recorded":false}'; do
    answer="$(
      sudo -n -u _sp001authority /bin/cat "$handoff/probe.curl" |
        sudo -n -u _sp001commercial /usr/bin/curl -q --noproxy '*' \
          --max-time 5 -fsS --config -
    )"
    printf '%s\n' "$answer"
    test "$answer" = "$expected"
  done
  count=1
else
while [ "$(date +%s)" -lt "$deadline" ]; do sleep 1; done

sudo -n -u _sp001authority "$python" - "$state" <<'PY'
from contextlib import closing
import json
from pathlib import Path
import sqlite3
import sys
from time import time

import jwt

state = Path(sys.argv[1])
handoff = state / "handoff"
credential = json.loads((state / "recovery.json").read_text())["credential"]
claims = jwt.decode(
    credential,
    (handoff / "access-public.pem").read_bytes(),
    algorithms=["RS256"],
    issuer="sp001-lab",
    audience="sp001-commercial-lab",
)
with closing(sqlite3.connect((handoff / "commercial.sqlite").as_uri() + "?mode=ro", uri=True)) as db:
    definition, revoked = db.execute("SELECT definition, revoked FROM product001_commercial_grants").fetchone()
grant = json.loads(definition)
now = int(time())
if revoked or not grant["valid_from"] <= now < grant["expires_at"] - 6 or claims["exp"] <= now + 6:
    raise SystemExit("JWT or grant lacks the remaining lifetime required for the HTTP probe")
print("JWT and grant still valid")
PY

status="$(
  sudo -n -u _sp001authority /bin/cat "$handoff/probe.curl" |
    sudo -n -u _sp001commercial /usr/bin/curl -q --noproxy '*' \
      --max-time 5 -sS -o /dev/null -w '%{http_code}' --config -
)"
printf 'Expired certificate: HTTP %s\n' "$status"
test "$status" = 403
count=0
fi
sudo -n -u _sp001gate "$gate/venv/bin/python" - "$count" <<'PY'
from contextlib import closing
import sqlite3
import sys

uri = "file:/private/var/db/sp001-gate/lab-state/commercial.sqlite?mode=ro"
with closing(sqlite3.connect(uri, uri=True)) as db:
    counts = db.execute("""
        SELECT (SELECT count(*) FROM product001_commercial_decisions),
               (SELECT count(*) FROM product001_commercial_decision_audit)
    """).fetchone()
print(*counts, sep="|")
expected = int(sys.argv[1])
if counts != (expected, expected):
    raise SystemExit(f"Expected {expected}|{expected}")
PY
