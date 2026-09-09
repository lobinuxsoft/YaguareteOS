# YaguareteOS — install EmuDeck (emulation frontend + RetroArch/standalone
# emulator manager).
#
# Source: the official Linux installer documented at
# https://emudeck.github.io/how-to-install-emudeck/linux/ (verified
# against the page directly, not a mirror). Runs as the user, everything
# lands under $HOME; the script itself drives a GUI (zenity/whiptail) for
# the rest of the setup once it starts.

_emudeck_install_url := "https://raw.githubusercontent.com/dragoonDorise/EmuDeck/main/install.sh"

# Install EmuDeck (emulation frontend + emulator manager)
[group("yaguarete")]
install-emudeck:
    #!/usr/bin/bash
    set -euo pipefail
    source /usr/libexec/yaguarete/emu-helpers.sh

    yg_info "EmuDeck — install"
    yg_check_internet
    yg_check_disk 500

    script=$(mktemp --suffix=.sh)
    yg_download "{{ _emudeck_install_url }}" "$script"

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

    bash "$script"
    rm -f "$script"
    yg_ok "EmuDeck installer finished — follow its own GUI for emulator selection and ROM paths."
    yg_pause

# Uninstall EmuDeck (ROMs and saves are never touched by this)
[group("yaguarete")]
remove-emudeck:
    #!/usr/bin/bash
    set -euo pipefail
    source /usr/libexec/yaguarete/emu-helpers.sh
    yg_warn "About to remove ~/.config/EmuDeck and ~/.emudeck (emulator configs only)."
    yg_warn "Your ROMs and saves are never touched by this — remove them yourself if wanted."
    yg_confirm "Continue?" || { yg_info "Aborted."; exit 0; }
    rm -rf "$HOME/.config/EmuDeck" "$HOME/.emudeck"
    yg_ok "EmuDeck configuration removed. Emulators installed via Flatpak/AppImage are untouched — remove those individually."
