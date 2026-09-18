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

# `flatpak build-update-repo --gpg-sign` shells out to gpg without requesting
# loopback pinentry itself, so on a headless CI runner (no real tty) it fails
# with "Pinentry: Inappropriate ioctl for device" instead of prompting.
# Work around it by presetting the passphrase directly into gpg-agent so no
# pinentry interaction happens at all -- but the preset is a *cache entry*
# with a TTL (default 10 min), and this script spends hours building flatpaks
# before it signs anything. Presetting up front (as an earlier version did)
# meant the entry had long expired by signing time; so the preset itself is
# deferred to preset_passphrase, called right before signing.
cat > "${gnupg_home}/gpg-agent.conf" <<'EOF'
allow-loopback-pinentry
allow-preset-passphrase
default-cache-ttl 86400
max-cache-ttl 86400
EOF
gpgconf --kill gpg-agent
preset_bin=$(find /usr/lib* /usr/libexec* -name gpg-preset-passphrase -print -quit 2>/dev/null || true)
if [ -z "${preset_bin}" ]; then
    echo "could not find gpg-preset-passphrase on this runner" >&2
    exit 1
fi

# Presets every keygrip on the key (primary + all subkeys, since we don't
# know upfront which one signing will actually use).
preset_passphrase() {
    gpg --with-keygrip --list-secret-keys --with-colons | awk -F: '/^grp/{print $10}' | \
        while read -r keygrip; do
            "${preset_bin}" --preset "${keygrip}" <<< "${FLATPAK_GPG_PASSWORD}"
        done
}

for name in "${flatpak_names[@]}"; do
    card="flatpaks/${name}"
    echo "=== Building ${card} ==="
    venv/bin/ludos build --force --flatpak "${card}" YaguareteOS.yml
    # Mount, export, and unmount must happen inside the SAME `buildah unshare`
    # invocation: the rootless overlay mount from `podman image mount` only
    # resolves within that unshared user/mount namespace. Splitting it across
    # separate `buildah unshare` calls (mount in one, export in another)
    # leaves `flatpak build-export` looking at what it sees as an empty
    # directory -- it fails with "Build directory ... not initialized" even
    # though files/ and metadata are really there, confirmed against
    # flatpak's own source (flatpak-builtins-build-export.c just checks
    # g_file_query_exists on files/ and metadata under the given path).
    image="localhost/flatpaks:${name}" repo_dir="${repo_dir}" \
        buildah unshare bash -c '
            set -euo pipefail
            mnt=$(podman image mount "${image}")
            flatpak build-export --no-update-summary "${repo_dir}" "${mnt}" stable
            podman image unmount "${image}"
        '
done

# `flatpak build-export` above does not sign the app commits, and
# `build-update-repo --gpg-sign` below signs only the summary. Clients with
# GPG verification on (the yaguarete.flatpakrepo default) check each commit's
# own signature too, and refuse to install with "GPG verification enabled,
# but no signatures found" -- found on real hardware, not in CI. Refs are
# read from the filesystem because `ostree refs` chokes on the empty
# refs/remotes directory that git doesn't preserve in the gh-pages clone.
echo "=== Signing app commits ==="
preset_passphrase
while IFS=/ read -r app_id arch branch; do
    flatpak build-sign \
        --gpg-sign="${gpg_fingerprint}" \
        --gpg-homedir="${gnupg_home}" \
        --arch="${arch}" \
        "${repo_dir}" "${app_id}" "${branch}" \
        || { echo "failed to sign ${app_id}/${arch}/${branch}" >&2; exit 1; }
done < <(find "${repo_dir}/refs/heads/app" -type f -printf '%P\n')

# Static deltas matter here: a classic ostree repo is fetched one HTTP request
# per object, and installing a single KDE app from scratch cost ~6500 requests
# (measured with the real flatpak client). Installing the six ISO apps in one
# go from the same runner got HTTP 429 from GitHub Pages and failed the ISO
# build. With deltas the same install is ~30 requests. Costs ~46 MB of repo.
echo "=== Signing and updating the repo summary ==="
preset_passphrase
flatpak build-update-repo \
    --generate-static-deltas \
    --gpg-sign="${gpg_fingerprint}" \
    --gpg-homedir="${gnupg_home}" \
    "${repo_dir}"

# Same check a client does: a GPG-verified pull of every app ref against our
# vendored public key, so an unsigned or wrongly-signed publish fails here
# instead of on someone's machine.
echo "=== Verifying like a client (GPG-verified pull of every app ref) ==="
verify_dir=$(mktemp -d)
ostree init --repo="${verify_dir}" --mode=archive
ostree --repo="${verify_dir}" remote add \
    --gpg-import=cards/base/atomic/keys/yaguarete-gpg.pub.asc verify "file://${repo_dir}"
verify_failed=0
while read -r ref; do
    if ! ostree --repo="${verify_dir}" pull verify "${ref}"; then
        echo "GPG-verified pull failed for ${ref}" >&2
        verify_failed=1
    fi
done < <(find "${repo_dir}/refs/heads/app" -type f -printf 'app/%P\n')
rm -rf "${verify_dir}"
if [ "${verify_failed}" -ne 0 ]; then
    echo "refusing to publish: at least one app ref is not client-verifiable" >&2
    exit 1
fi

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
