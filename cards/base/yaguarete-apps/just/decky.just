# YaguareteOS — install Decky Loader (Steam plugin loader).
#
# Source: the official fast-install command from the README at
# github.com/SteamDeckHomebrew/decky-loader (verified against the repo
# directly). Decky injects into Steam over its CEF remote-debugging port
# at runtime -- it does not care which Steam build is running (native,
# Flathub, or our own org.anatase.Steam), only that Steam is installed
# and gets restarted afterwards.

_decky_install_url := "https://github.com/SteamDeckHomebrew/decky-installer/releases/latest/download/install_release.sh"

# Install Decky Loader (Steam plugin loader)
[group("yaguarete")]
install-decky:
    #!/usr/bin/bash
    set -euo pipefail
    source /usr/libexec/yaguarete/emu-helpers.sh

    yg_info "Decky Loader — install"
    yg_check_internet
    yg_check_disk 200

    script=$(mktemp --suffix=.sh)
    yg_download "{{ _decky_install_url }}" "$script"

    echo
    yg_info "First lines of the installer (review before executing):"
    echo "──────────────────────────────────────────────────────────────"
    head -40 "$script"
    echo "──────────────────────────────────────────────────────────────"
    yg_info "Full script saved at $script ($(wc -l < "$script") lines, $(wc -c < "$script") bytes)."
    echo

    yg_confirm "Run the installer?" || {
        yg_warn "Aborted. The script stays at $script — inspect and run it manually if you want."
        exit 0
    }

    sh "$script"
    rm -f "$script"

    echo
    yg_ok "Decky Loader installer finished."
    yg_info "Close Steam completely (including the system tray icon) and open it again."
    yg_info "Decky lives in the Quick Access menu (the ... button), not in the library."
    yg_pause

# Uninstall Decky Loader
[group("yaguarete")]
remove-decky:
    #!/usr/bin/bash
    set -euo pipefail
    source /usr/libexec/yaguarete/emu-helpers.sh
    yg_warn "About to remove ~/homebrew (Decky binary, plugins and their data)."
    yg_confirm "Continue?" || { yg_info "Aborted."; exit 0; }
    yg_sudo systemctl disable --now plugin_loader 2>/dev/null || true
    rm -rf "$HOME/homebrew"
    yg_ok "Decky Loader removed."
