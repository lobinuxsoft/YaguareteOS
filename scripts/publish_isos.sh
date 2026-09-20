#!/usr/bin/env bash
#
# Publishes the ISO of a stable release to archive.org, from a workstation.
#
# archive.org throttles a long transfer (measured ~15 MiB/s at the start
# falling to ~0.7 MiB/s after two hours), which is why this is not a CI job:
# from a workstation it can be watched, resumed and corrected.
#
# Flow: download the build-iso artifact -> verify its checksum -> upload ->
# wait for archive.org to index it -> add the link to the GitHub Release ->
# delete the local copy. Peak disk usage is one ISO.
#
# Usage:
#   scripts/publish_isos.sh [options]
#
#   --version V     release version, e.g. 20260919 or 20260919-2
#                   (default: latest stable release)
#   --run-id ID     build-iso run to take the artifact from
#                   (default: newest unexpired artifact for the version)
#   --workdir DIR   scratch dir (default: /var/mnt/DATA/_yaguarete_iso)
#   --keep          keep the local ISO after a verified upload
#   --dry-run       download and verify everything, upload nothing
#
# Requires: gh (authenticated), ia (`pip install internetarchive`, then
# `ia configure`), jq, curl, sha256sum.

set -euo pipefail

cd "$(dirname "$0")/.."

log() { printf '\033[1;33m==>\033[0m %s\n' "$*"; }
die() { printf '\033[1;31mERROR:\033[0m %s\n' "$*" >&2; exit 1; }

version=""
run_id=""
workdir="/var/mnt/DATA/_yaguarete_iso"
keep=false
dry_run=false

while [ $# -gt 0 ]; do
    case "$1" in
        --version) version="$2"; shift 2 ;;
        --run-id) run_id="$2"; shift 2 ;;
        --workdir) workdir="$2"; shift 2 ;;
        --keep) keep=true; shift ;;
        --dry-run) dry_run=true; shift ;;
        -h|--help) sed -n '2,25p' "$0"; exit 0 ;;
        *) die "unknown option: $1" ;;
    esac
done

for tool in gh ia jq curl sha256sum; do
    command -v "$tool" >/dev/null || die "$tool is not installed"
done

if [ -z "$version" ]; then
    tag=$(gh release view --json tagName --jq .tagName 2>/dev/null || true)
    [[ $tag == stable-* ]] || die "no stable release found; run promote.yml first"
    version=${tag#stable-}
fi
release_tag="stable-${version}"
identifier="yaguareteos-stable-${version}"
artifact="yaguareteos-${version}-iso"
iso_name="yaguareteos-${version}-x86_64.iso"
log "release ${release_tag} -> https://archive.org/details/${identifier}"

if [ -z "$run_id" ]; then
    run_id=$(gh api "repos/{owner}/{repo}/actions/artifacts?name=${artifact}" \
        --jq '.artifacts | map(select(.expired == false)) | .[0].workflow_run.id // empty')
    [ -n "$run_id" ] || die "no unexpired artifact ${artifact} (retention is 7 days): run build-iso.yml with version=${version}"
fi
log "build-iso run: ${run_id}"

mkdir -p "$workdir"
# `gh run download` stages the zip in $TMPDIR; /tmp is a RAM-backed tmpfs on
# Bazzite and fails at ~6 GB with "disk quota exceeded".
export TMPDIR="$workdir/.tmp"
mkdir -p "$TMPDIR"

dest="$workdir/$artifact"
if [ ! -f "$dest/$iso_name" ]; then
    log "downloading ${artifact}"
    gh run download "$run_id" --name "$artifact" --dir "$dest"
else
    log "reusing the already-downloaded ${artifact}"
fi

log "verifying checksum"
(cd "$dest" && sha256sum --check "${iso_name}-CHECKSUM")

if $dry_run; then
    log "(dry-run) would upload ${iso_name} ($(du -h "$dest/$iso_name" | cut -f1)) to ${identifier}"
    exit 0
fi

cp -f docs/assets/archive_thumb.png "$dest/__ia_thumb.png"

log "uploading ($(du -h "$dest/$iso_name" | cut -f1))"
ia upload "$identifier" \
    "$dest/$iso_name" "$dest/${iso_name}-CHECKSUM" "$dest/__ia_thumb.png" \
    --no-derive \
    --retries 5 \
    --metadata="title:YaguareteOS ${version}" \
    --metadata="creator:lobinuxsoft" \
    --metadata="description:YaguareteOS ${version}, stable release. Bootable, offline-installable x86_64 ISO of an atomic (bootc) Fedora 44 KDE Plasma gaming distribution built on the Anatase build system. Source: https://github.com/lobinuxsoft/YaguareteOS" \
    --metadata="subject:linux;distro;fedora;bootc;yaguarete;gaming;kde" \
    --metadata="licenseurl:https://www.gnu.org/licenses/agpl-3.0.html" \
    --metadata="mediatype:software" \
    --metadata="collection:opensource" \
    || log "ia upload returned non-zero; verifying server-side before giving up"

# `ia upload` can exit before archive.org has run archive.php on the item. A
# multi-GB ISO takes ~25 min to appear in the metadata API, and deleting the
# local copy before that is how an upload gets lost.
log "waiting for archive.org to index ${identifier}"
waited=0
until curl -fsSL "https://archive.org/metadata/${identifier}" 2>/dev/null \
        | jq -e --arg name "$iso_name" '(.files // []) | any(.name == $name)' >/dev/null; do
    waited=$((waited + 60))
    [ "$waited" -le 3600 ] || die "${identifier} not indexed after 60 min; check \`ia tasks ${identifier}\`"
    sleep 60
done
log "indexed after ~$((waited / 60)) min"

download_url="https://archive.org/download/${identifier}/${iso_name}"
status=$(curl -sI -r 0-1023 -o /dev/null -w '%{http_code}' -L "$download_url")
[ "$status" = 206 ] || die "${download_url} answered ${status}, expected 206"

body=$(gh release view "$release_tag" --json body --jq .body)
if [[ $body != *"archive.org/details/${identifier}"* ]]; then
    gh release edit "$release_tag" --notes "${body}

## ISO

- https://archive.org/details/${identifier}
- ${download_url}"
    log "release ${release_tag} updated with the ISO link"
fi

if $keep; then
    log "keeping ${dest} (--keep)"
else
    rm -rf "$dest"
    log "local copy deleted"
fi
rmdir "$TMPDIR" 2>/dev/null || true
log "done: https://archive.org/details/${identifier}"
