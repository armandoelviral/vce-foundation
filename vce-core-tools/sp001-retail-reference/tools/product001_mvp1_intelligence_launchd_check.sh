#!/bin/bash
set -euo pipefail
umask 077

if [ "$#" -lt 3 ]; then
  printf 'Uso: %s FIRMA_PY REVISION_JSON EQUIPO [EQUIPO...]\n' "$0" >&2
  exit 2
fi
project="$(cd "$(dirname "$0")/.." && pwd)"
python="$project/../.venv/bin/python"
signer="$1"
review="$2"
shift 2
work="$(mktemp -d "${TMPDIR:-/tmp}/sp001-intel-sign.XXXXXX")"
gate=/private/var/db/sp001-gate
authority=/private/var/db/sp001-authority
service=system/com.sp001.gate-lab
original=/Library/LaunchDaemons/com.sp001.gate-lab.plist

sudo -v
sudo launchctl print "$service" >/dev/null
test "$(id -u _sp001gate)" = 600
test "$(id -u _sp001commercial)" = 601
test "$(id -u _sp001authority)" = 602

"$python" "$signer" crear-clave --privada "$work/signing.raw" > "$work/signing.pub"
"$python" "$signer" firmar --privada "$work/signing.raw" --firmante analista-lab \
  --revision "$review" --equipos "$@" > "$work/authorization.json"
"$python" - "$review" "$work" <<'PY'
import json
from pathlib import Path
import sys

review = json.loads(Path(sys.argv[1]).read_text())
work = Path(sys.argv[2])
authorization = json.loads((work / "authorization.json").read_text())
(work / "body.json").write_text(json.dumps({
    "revision": review, "equipos": authorization["statement"]["devices"],
    "autorizacion": authorization,
}))
(work / "trust.json").write_text(json.dumps({
    "issuer": "sp001-lab", "subject": "approver",
    "signer_id": "analista-lab", "public_key_hex": (work / "signing.pub").read_text().strip(),
}))
PY

for file in tools/product001_mvp1_gate_lab.py \
  src/sp001/infrastructure/product001_mvp1_intelligence_lab.py; do
  sudo install -m 0644 "$project/$file" "$gate/runtime/$file"
done

cd /
run="$(sudo -n -u _sp001authority /usr/bin/mktemp -d "$authority/run.XXXXXX")/state"
sudo -n -u _sp001authority "$authority/venv/bin/python" \
  "$authority/runtime/tools/product001_mvp1_gate_lab.py" issue "$run" --authority-uid 602
handoff="$run/handoff"
isolated="$(sudo -n -u _sp001gate /usr/bin/mktemp -d "$gate/intelligence-run.XXXXXX")"
state="$isolated/lab-state"
sudo -n -u _sp001gate /bin/mkdir -m 0700 "$state"
sudo install -o _sp001gate -g staff -m 0600 "$work/trust.json" "$isolated/intelligence-trust.json"
for file in access-public.pem trust.json commercial.sqlite; do
  sudo install -o _sp001gate -g staff -m 0600 "$handoff/$file" "$state/$file"
done
sudo ditto "$handoff/documents" "$state/documents"
sudo chown -R _sp001gate:staff "$state/documents"

job_dir="$(sudo /usr/bin/mktemp -d /private/var/tmp/sp001-intel-launchd.XXXXXX)"
job="$job_dir/gate.plist"
sudo cp "$original" "$job"
sudo /usr/libexec/PlistBuddy -c "Set :ProgramArguments:3 $state" "$job"
sudo /usr/libexec/PlistBuddy -c 'Add :ProgramArguments:6 string --enable-intelligence' "$job"
sudo plutil -lint "$job"

replaced=0
restore() {
  if [ "$replaced" = 1 ]; then
    if sudo launchctl print "$service" >/dev/null 2>&1; then
      sudo launchctl bootout "$service" || return 1
      sleep 3
    fi
    sudo launchctl bootstrap system "$original" || return 1
    printf 'Gate habitual restaurado\n'
  fi
}
trap restore EXIT

sudo launchctl bootout "$service"
replaced=1
sleep 3
sudo launchctl bootstrap system "$job"
route=http://127.0.0.1:18766/laboratory/vce/intelligence/version-checks
status=000
for attempt in 1 2 3 4 5 6 7 8 9 10; do
  status="$(/usr/bin/curl -q --noproxy '*' --max-time 2 -s \
    -o /dev/null -w '%{http_code}' -X POST -d '{}' "$route")" || status=000
  [ "$status" = 401 ] && break
  sleep 1
done
test "$status" = 401

request() {
  {
    printf 'url = "%s"\nheader = "Content-Type: application/json"\n' "$route"
    sudo -n -u _sp001authority /usr/bin/grep '^header = "Authorization: Bearer ' "$handoff/probe.curl"
    "$python" -c 'import json,sys; print("data-binary = " + json.dumps(open(sys.argv[1]).read()))' "$work/body.json"
  } | sudo -n -u _sp001commercial /usr/bin/curl -q --noproxy '*' \
    --max-time 5 -sS -o /dev/null -w '%{http_code}' --config -
}
first="$(request)"
second="$(request)"
printf 'Primera solicitud: HTTP %s\nReenvío: HTTP %s\n' "$first" "$second"
test "$first" = 200
test "$second" = 409

sudo -n -u _sp001gate "$gate/venv/bin/python" - "$isolated/intelligence.sqlite" "$@" <<'PY'
from contextlib import closing
from pathlib import Path
import sqlite3
import sys

database = Path(sys.argv[1]).as_uri() + "?mode=ro"
with closing(sqlite3.connect(database, uri=True)) as db:
    consumed = db.execute("SELECT signer_id, principal_issuer, principal_subject FROM intelligence_consumption").fetchall()
    observed = db.execute("SELECT device FROM intelligence_observations ORDER BY device").fetchall()
if consumed != [("analista-lab", "sp001-lab", "approver")]:
    raise SystemExit("FALLO: identidad o consumo inesperados")
if observed != [(device,) for device in sorted(sys.argv[2:])]:
    raise SystemExit("FALLO: observaciones fuera del alcance")
print(f"PASS: identidad autenticada, 1 consumo y {len(observed)} observaciones simuladas")
PY

restore
replaced=0
trap - EXIT
printf 'SQLite de evidencia: %s/intelligence.sqlite\n' "$isolated"
