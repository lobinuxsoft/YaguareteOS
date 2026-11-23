import re
import urllib.error
import urllib.request

REPO = "https://github.com/elripalda/RecompLauncher"

# The releases Atom feed lists tags newest first and, unlike api.github.com,
# is not subject to the anonymous 60 req/h limit shared by CI runner IPs.
with urllib.request.urlopen(f"{REPO}/releases.atom", timeout=30) as resp:
    feed = resp.read().decode()

tags = re.findall(r"<id>tag:github\.com,2008:Repository/\d+/([^<]+)</id>", feed)
if not tags:
    raise SystemExit("no releases found in the RecompLauncher feed")

# A release just published may still be uploading its assets: fall back to
# the previous tag instead of failing the build.
for tag in tags[:3]:
    url = f"{REPO}/releases/download/{tag}/RecompLauncher_{tag.removeprefix('v')}_amd64.deb"
    try:
        with urllib.request.urlopen(url, timeout=120) as resp, \
                open("/tmp/recomplauncher.deb", "wb") as f:
            f.write(resp.read())
        print(f"RecompLauncher {tag}")
        break
    except urllib.error.HTTPError as err:
        if err.code != 404:
            raise
else:
    raise SystemExit(f"no amd64 .deb in the latest releases: {tags[:3]}")
