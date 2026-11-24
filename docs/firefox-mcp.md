# Firefox MCP

`yaguarete-firefox-mcp` runs Mozilla's [Firefox MCP server](https://github.com/mozilla/firefox-mcp)
(v0.11.0) over stdio, inside bubblewrap, against the image's Firefox.

## Client config

```json
{ "mcpServers": { "firefox": { "command": "yaguarete-firefox-mcp" } } }
```

No keys, tokens or cookies are needed or read. `YAGUARETE_FIREFOX_MCP_PRESET`
(`slim` by default, `basic` or `developer`) widens the tool set; `basic` adds
`evaluate_script`, downloads and extension install.

`YAGUARETE_FIREFOX_MCP_PERSIST=1` keeps one profile in `~/.firefox-mcp/profile-*`
between sessions, so a site you sign into by hand stays signed in:

```json
{ "mcpServers": { "firefox": { "command": "yaguarete-firefox-mcp",
  "env": { "YAGUARETE_FIREFOX_MCP_PERSIST": "1" } } } }
```

Sign into that profile only the sites the agent needs: any page it visits
can try prompt injection against the accounts signed in there. Passwords are
never saved (`signon.rememberSignons=false`), session cookies are. Delete
`~/.firefox-mcp/profile-*` to sign everything out. Files to upload (e.g. a
CV) must live under `~/.firefox-mcp`; the sandbox sees nothing else in `$HOME`.

## What the sandbox gives

- The image's Firefox RPM, never the user's Flatpak Firefox or its profile;
  `-no-remote` keeps it from attaching to a running browser.
- By default a fresh temporary profile per session: no logins, no saved passwords.
  Sign in by hand in the window if a task needs it; it is gone when the session ends.
- `/usr` and `/etc` read-only, `$HOME` and `/tmp` empty and throwaway; only
  `~/.firefox-mcp` (0700) is writable. The caller's environment is cleared.
- Telemetry, Normandy/studies, Safe Browsing, captive-portal, region and
  remote-settings fetches are disabled by pref; network body collection is off.

## Known limitations

- **Loopback ports without a token.** geckodriver (HTTP), Marionette and the
  BiDi WebSocket listen on random `127.0.0.1` ports while a session runs.
  They check Host/Origin but have no token, so another process of the same
  user can attach. The network namespace is shared so pages can load.
- **Network is open.** The browser reaches whatever the agent navigates to;
  no egress filter. Page content can carry prompt injection.
- **Bundled SDK advisories.** The dist bundles `@modelcontextprotocol/sdk`
  1.29.0 and zod 3.25.76. Their advisories cover HTTP transports, OAuth and
  experimental tasks (not reachable over stdio) and a zod DoS on oversized
  client input. Fixed upstream only by a new firefox-mcp release.
- **No request limits** beyond what the MCP SDK and Firefox enforce.
- **Persistent profile is a standing session.** With `PERSIST=1` the signed-in
  accounts are reachable by every page the agent opens, across sessions.
- **Upstream is pre-1.0** and moves fast (weekly releases); pins are bumped by hand.
