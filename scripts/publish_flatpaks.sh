#!/usr/bin/env bash
set -euo pipefail

# Builds every YaguareteOS-owned flatpak declared in YaguareteOS.yml and
# publishes them to the classic (ostree + summary, plain static HTTP) Flatpak
# repo hosted at https://lobinuxsoft.github.io/YaguareteOS-flatpaks/
# (gh-pages branch of lobinuxsoft/YaguareteOS-flatpaks), signed with our own
# GPG key.
#
# Why classic and not OCI: Flatpak-over-OCI needs the registry to implement
# the flatpak-oci-specs index protocol, which no major hosted registry
# (GHCR included) supports. The classic format is plain static HTTP -- what
# Flathub itself ran on for years -- and GitHub Pages serves it fine. See
# cards/base/atomic/flatpak/yaguarete.flatpakrepo for the client-side remote
# config this publishes for.
#
# Required environment variables:
#   FLATPAK_GPG_PRIVATE_KEY  ASCII-armored private key content
#   FLATPAK_GPG_PASSWORD     passphrase for the above
#   FLATPAKS_REPO_SSH_URL    e.g. git@github.com:lobinuxsoft/YaguareteOS-flatpaks.git
# GIT_SSH_COMMAND / a loaded ssh-agent must already grant push access to that
# repo (see .github/workflows/publish-flatpaks.yml for how CI sets this up).
#
# Usage: scripts/publish_flatpaks.sh [--no-push]

cd "$(dirname "$0")/.."

flatpak_names=(ark filelight gwenview kate kcalc okular steam)

repo_dir=$(mktemp -d)
clone_dir=$(mktemp -d)
gnupg_home=$(mktemp -d)
export GNUPGHOME="$gnupg_home"
chmod 700 "$gnupg_home"

cleanup() {
    rm -rf "$repo_dir" "$clone_dir" "$gnupg_home"
}
trap cleanup EXIT

echo "Cloning existing repo tree from ${FLATPAKS_REPO_SSH_URL} (gh-pages)..."
git clone --depth 1 --branch gh-pages "${FLATPAKS_REPO_SSH_URL}" "$clone_dir"
if [ -d "$clone_dir/objects" ]; then
    cp -a "$clone_dir/." "$repo_dir/"
fi

printf '%s' "${FLATPAK_GPG_PRIVATE_KEY}" | \
    gpg --batch --pinentry-mode loopback --passphrase "${FLATPAK_GPG_PASSWORD}" --import
gpg_fingerprint=$(gpg --list-secret-keys --with-colons | awk -F: '/^fpr/{print $10; exit}')
if [ -z "${gpg_fingerprint}" ]; then
    echo "failed to import the YaguareteOS Flatpak repo signing key" >&2
    exit 1
fi

for name in "${flatpak_names[@]}"; do
    card="flatpaks/${name}"
    echo "=== Building ${card} ==="
    venv/bin/ludos build --force --flatpak "${card}" YaguareteOS.yml
    image="localhost/flatpaks:${name}"
    mnt=$(buildah unshare podman image mount "${image}")
    flatpak build-export --no-update-summary "${repo_dir}" "${mnt}" stable
    buildah unshare podman image unmount "${image}"
done

echo "=== Signing and updating the repo summary ==="
flatpak build-update-repo \
    --gpg-sign="${gpg_fingerprint}" \
    --gpg-homedir="${gnupg_home}" \
    "${repo_dir}"

if [ "${1:-}" = "--no-push" ]; then
    echo "Built and signed at ${repo_dir}, not pushing (--no-push)."
    exit 0
fi

rsync -a --delete --exclude .git "${repo_dir}/" "${clone_dir}/"
cd "${clone_dir}"
git add -A
if git diff --cached --quiet; then
    echo "Nothing changed, skipping push."
    exit 0
fi
git -c user.name="YaguareteOS CI" -c user.email="ci@yaguareteos.invalid" \
    commit -m "chore: publish flatpaks $(date -u +%Y-%m-%dT%H:%M:%SZ)"
git push origin gh-pages
