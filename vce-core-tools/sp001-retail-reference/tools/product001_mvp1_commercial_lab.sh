#!/bin/sh
# One-shot commercial client for the supervised PRODUCT-001 laboratory.
set -eu
umask 077
export LC_ALL=C

client=/private/var/db/sp001-commercial
gate=/private/var/db/sp001-gate/lab-state
route=http://127.0.0.1:18766/laboratory/product001/mvp1/decisions
uid=$(/usr/bin/id -u)
if [ "$uid" != 601 ]; then
    printf 'Unexpected client UID %s\n' "$uid" >&2
    exit 1
fi

exec > "$client/result.txt" 2>&1
printf 'Client UID: %s\n' "$uid"

verify_no_write() {
    filename=$1
    if error=$( ( : >> "$gate/$filename" ) 2>&1 ); then
        printf 'FAIL: writable %s\n' "$filename"
        exit 1
    fi
    case "$error" in
        *"Permission denied"*) printf 'Write denied: %s\n' "$filename" ;;
        *) printf 'FAIL: unexpected open error for %s: %s\n' "$filename" "$error"
           exit 1 ;;
    esac
}

verify_no_write trust.json
verify_no_write authority.sqlite
verify_no_write commercial.sqlite

status=$(/usr/bin/curl -q --noproxy '*' --max-time 5 -sS -o /dev/null \
    -w '%{http_code}' -X POST -d '{}' "$route")
printf 'Missing credential: HTTP %s\n' "$status"
test "$status" = 401

send_proposal() {
    /usr/bin/curl -q --noproxy '*' --max-time 5 -fsS --config "$client/probe.curl"
}

first=$(send_proposal)
printf 'First proposal: %s\n' "$first"
test "$first" = '{"recorded":true}'

replay=$(send_proposal)
printf 'Repeated proposal: %s\n' "$replay"
test "$replay" = '{"recorded":false}'

printf 'PASS: supervised commercial laboratory client\n'
