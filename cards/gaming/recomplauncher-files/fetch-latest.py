import json
import urllib.request

req = urllib.request.Request(
    "https://api.github.com/repos/elripalda/RecompLauncher/releases",
    headers={"Accept": "application/vnd.github+json"},
)
with urllib.request.urlopen(req, timeout=30) as resp:
    releases = json.load(resp)

release = next(r for r in releases if not r["draft"])
asset = next(a for a in release["assets"] if a["name"].endswith("_amd64.deb"))

with urllib.request.urlopen(asset["browser_download_url"], timeout=120) as resp, \
        open("/tmp/recomplauncher.deb", "wb") as f:
    f.write(resp.read())
