# Releasing YaguareteOS

Two channels, one image:

| Channel | Moves when | Followed by |
|---|---|---|
| `ghcr.io/lobinuxsoft/yaguareteos:test` | every merge to `master` that touches the image (`build.yml`) | testing devices (`bootc switch`) |
| `ghcr.io/lobinuxsoft/yaguareteos:stable` | someone runs `promote.yml` | every installed system (the ISO's kickstart points here) |

A release is a promotion of a build that was already tested on hardware. The
ISO is built from the promoted image, so image, GitHub Release and ISO always
describe the same thing.

## 1. Promote `:test` to `:stable`

```bash
gh workflow run promote.yml
```

Takes a few minutes (registry-side copy, no rebuild). It:

- reads the digest, version and commit from the `:test` labels;
- refuses to continue unless `:test` carries a valid cosign signature;
- copies it to `:stable` and `:stable-<version>` and signs both;
- creates the GitHub Release `stable-<version>` targeting that commit.

Two builds on the same day share the version label. If `:stable-<version>`
already points at a different digest the next free suffix is used
(`20260919-2`). Re-running over an unchanged `:test` changes nothing.

Installed systems pick it up with the **Update System** launcher or
`sudo bootc upgrade`.

## 2. Build the ISO (optional per release)

An ISO only matters for a fresh install; installed systems update through
`bootc`. Skip this step for most releases.

```bash
gh workflow run build-iso.yml                      # latest stable release
gh workflow run build-iso.yml -f version=20260919  # a specific one
```

The artifact is `yaguareteos-<version>-iso` (ISO plus `-CHECKSUM`) and
**expires after 7 days**: publish promptly or rebuild.

## 3. Publish to archive.org (from a workstation)

```bash
scripts/publish_isos.sh --dry-run   # download and verify only
scripts/publish_isos.sh
```

archive.org throttles long transfers (~15 MiB/s at first, under 1 MiB/s after
two hours), so this is deliberately not a CI job. The script downloads the
artifact, verifies its checksum, uploads, waits for archive.org to index it,
checks that the download answers `206`, appends the link to the GitHub Release
and deletes the local copy.

- Item identifier: `yaguareteos-stable-<version>`.
- Every item ships the ISO, its `-CHECKSUM` and `__ia_thumb.png`
  (`docs/assets/archive_thumb.png`), with full metadata.
- The scratch dir defaults to `/var/mnt/DATA/_yaguarete_iso` and `TMPDIR` is
  pointed there: `/tmp` is a RAM-backed tmpfs on Bazzite and fails at ~6 GB.
- Requires `gh` authenticated, `ia` configured (`pip install internetarchive
  && ia configure`), `jq`, `curl`.

## 4. Point the site at the new item

Update the download URL on the website (issue #3) and the README, and verify
it before committing:

```bash
curl -sI -r 0-1023 "https://archive.org/download/<identifier>/<iso>" | head -1
# expect: HTTP/1.1 206 Partial Content
```

## Known gap

The kickstart tracks `ostree-unverified-registry:...:stable`, so installed
systems do not verify the cosign signature on update. Moving to
`ostree-image-signed` touches `installer/`, needs a new image build and a new
ISO, and is deliberately left until this cycle has been validated end to end.
