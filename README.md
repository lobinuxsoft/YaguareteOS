# YaguareteOS

[![License: AGPL v3](https://img.shields.io/badge/license-AGPLv3-blue.svg)](LICENSE)

YaguareteOS is an immutable, bootc-based image for handhelds, desktops, laptops, and HTPCs. It is a rebrand and fork of [Anatase](https://github.com/anatase-org/anatase) — this repository replaces Anatase's identity, branding, and defaults with YaguareteOS's own, per the permission Anatase's own license grants for exactly this ("fork Anatase and replace the identity card with your type and marks"). The underlying build mechanism (`ludos`, `cards/`, `chunks.yml`) is used as-is.

- **Smaller, more stable, and universal**. One image covers handhelds, desktops, laptops, HTPCs, and Nvidia devices. Installs and updates fast, without functionality loss.
- **Compliance, Security, Provenance**. Packages are either sourced from Fedora or built in this repository, so fixes ship fast and no unaccounted changes sneak in.
- **Handheld-first**: HHD (Handheld Daemon) ships natively — controller, TDP, and RGB support out of the box, unlike Bazzite 44+ which dropped it for InputPlumber/OpenGamepadUI.
- **Argentine cultural identity** — Guaraní naming (Yaguareté), Spanish-first defaults, `es-AR` locale, native wallpapers. *Cultural*, not governmental.

> **Estado (2026-09-08):** branding cosmético (logos, wallpapers, os-release,
> KDE, Gamemode, zsh) ya rebrandeado — ver commit `d906fd6`. Sin build-test
> todavía (`ludos build YaguareteOS.yml` nunca corrió sobre esto). Llaves de
> firma propias (cosign, GPG, MOK) generadas pero no conectadas a
> `ludos.yml`/`cards/base/atomic/card.yml` todavía. Publicación: build vía
> `ludos` local, push/firma vía herramientas estándar (skopeo + `cosign sign
> --key`) a un paquete GHCR propio, no el pipeline S3 propio de Anatase — ver
> `cards/base/atomic/` para lo que sigue sin tocar (llaves, Flatpak runtime).

## Installation

*Pendiente: todavía no publicamos un ISO propio. Por ahora, para reproducir localmente:*

```bash
ludos build YaguareteOS.yml
```

### Secure boot

MOK CA propia generada (2026-09-08, cosign/GPG/MOK), todavía sin conectar al
build. Hasta que eso esté armado, el procedimiento de enrolado sigue siendo
el que documentaba Anatase (MOK Management al primer arranque), pero con
llaves que van a cambiar antes de esto ser instalable de verdad.

## Overview
> [!TIP]
> YaguareteOS uses three sessions. You can switch between them on the login screen, by opening the drop-down on the bottom left of the screen.
>
> To select a default one, in desktop mode **Settings** -> **Login Screen** -> **Automatically Log in ✔️ as user:** your user -> **with session:** your session
>
> **Do not tick "Login again immediately after logging off" or you will get stuck in Gamemode**

### Plasma Desktop
YaguareteOS uses KDE Plasma as its desktop. Preinstalls Ark (Archive Manager), Filelight (Disk Usage Analyzer), Kate (Text Editor), and Okular (Document Viewer).

### Plasma Mobile
YaguareteOS also offers Plasma Mobile for tablet-like devices, such as handhelds and two-in-ones. Includes a Chromium based browser with working GPU acceleration, Spotify & 720p Netflix support, and a built-in adblocker.

### Gamemode
A SteamOS-style gaming session, gamescope + Steam (Flatpak) direct, with HHD for controller/TDP/RGB and a patched `steamos-manager` (Valve's own) as backend. Intuitive to touch, lighter than a full desktop session, with proper lock/login screens.

### Access the Linux world with Spaces
Typing `arch`, `fedora`, `ubuntu`, or `kali` in a terminal switches to that distribution's packages, both terminal and desktop, with a permission system controlling what's shared with the host.

## Roadmap

Inherited from Anatase's own mechanism, evaluated selectively for YaguareteOS's own needs (see project notes, not tracked here yet):
 * Rebrand cards (identity, KDE theme, wallpapers, Plymouth) — **fase 3, en curso**
 * Revive `hhd-vram` (GTT control) as a native HHD plugin — YaguareteOS already had this working before Bazzite dropped HHD
 * Evaluate TDP write correctness on Strix Point APUs vs. our own validated clamping logic
 * Everything else Anatase tracks upstream (SLSA3, ARM image, TPM attestation) — adopt as it lands, no divergence unless needed

## Contributing

YaguareteOS is a personal project; same policy as upstream Anatase — issues/suggestions welcome, no external contributions accepted at this time.

## License

A copy of the files in this repository is provided to you under the terms of [GNU Affero General Public License v3.0 or later](LICENSE). Exceptions: `.patch` files carry the license of their respective project solely, and files with an SPDX license header carry that license solely.

**Credits**: this repository is a fork of [Anatase](https://github.com/anatase-org/anatase) by Antheas Kapenekakis, used and modified under the terms of the AGPLv3. The `ludos` build tool is also his, vendored here as a submodule under the same license. YaguareteOS's own marks, branding, and configuration are separate from Anatase's identity, per the license terms Anatase itself grants for forks that replace the identity card.
