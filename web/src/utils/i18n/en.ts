import type { Translations } from './types';

const en: Translations = {
  meta: {
    pageTitle:
      'YaguareteOS — Anatase-based KDE distribution for dev and gaming',
    ogTitle: 'YaguareteOS — KDE for dev and gaming on top of Anatase',
    description:
      'YaguareteOS is a bootable Linux distribution, a fork of Anatase (Fedora Atomic / bootc), aimed at development and handheld gaming. Native controller/TDP/RGB daemon, firmware-validated VRAM slider, atomic updates and signed by our own CI.',
  },
  hero: {
    titlePrefix: 'Yaguarete',
    titleSuffix: 'OS',
    subTitle:
      'Handheld-first KDE distribution, a fork of Anatase. HHD (Handheld Daemon) native for controller/TDP/RGB, a VRAM slider validated by the firmware right from HHD\'s own panel, our own apps (Yryvu, Tatu) and a gamescope+Steam Gamemode session. Image-based with bootc, atomic updates, signed by our own CI.',
    primaryBtn: 'Read the README',
    primaryBtnUrl: 'https://github.com/lobinuxsoft/YaguareteOS#readme',
  },
  variants: {
    title: 'One image, every piece of hardware',
    subTitle:
      'No variant to pick: one image covers handhelds, desktops, laptops, HTPCs and NVIDIA hardware. Always built and signed from the same source tree.',
    upstreamLabel: 'Upstream',
    downloadLabel: 'Download ISO',
    pendingNote: 'ISO in preparation — the release pipeline hasn\'t published the first one yet',
    cosignNote:
      'Stable releases are signed with cosign. Verify the signature against cosign.pub before installing — instructions in the README.',
    cards: [
      {
        name: 'yaguareteos',
        tag: 'Desktop, laptop, handheld, HTPC — AMD, Intel and NVIDIA',
        description:
          'A single image. AMD/Intel graphics stack out of the box, proprietary NVIDIA drivers included for hardware that needs them. Plasma Desktop, Plasma Mobile and Gamemode (gamescope + Steam) sessions on the same boot.',
        upstream: 'anatase:stable',
      },
    ],
  },
  stack: {
    title: 'Anatase underneath, dev and gaming on top',
    subTitle:
      'We inherit the Anatase gaming stack — Steam (Flatpak), gamescope, GameMode, MangoHud, recent Mesa, native HHD — and layer on what we need for daily dev work and for squeezing a handheld. Image-based with bootc: every update is atomic, rollback is one command.',
    features: [
      {
        heading: 'Gaming-ready',
        content:
          'Steam (Flatpak), GameMode, gamescope and MangoHud preconfigured in the Gamemode session. Recent Mesa/AMD. Native HHD (Handheld Daemon): controller, TDP and RGB out of the box on handhelds like the OneXFly.',
        svg: 'rocket',
      },
      {
        heading: 'Our own handheld tooling',
        content:
          'An HHD plugin to move the firmware\'s own VRAM carveout (kernel-validated, not a GTT workaround) right from the handheld\'s settings panel, no terminal needed. Curated ujust recipes for Decky Loader, Eden, Antigravity, Claude Code and our own apps.',
        svg: 'puzzle',
      },
      {
        heading: 'Atomic and immutable',
        content:
          'Image-based on Fedora Atomic with bootc. Every update is a full signed image. Instant rollback if anything breaks.',
        svg: 'frame',
      },
      {
        heading: 'Dev-friendly',
        content:
          'A terminal that arrives configured: kitty with zsh, a Powerlevel10k prompt and FiraCode Nerd Font with ligatures, in one command. Claude Code and Antigravity one `ujust` away. Toolbox, distrobox and devcontainer first-class. KDE Plasma desktop. Spanish-first defaults, es-AR locale.',
        svg: 'tools',
      },
    ],
  },
  faq: {
    title: 'Frequently asked questions',
    subTitle:
      'What YaguareteOS is, how to install it, and how it relates to Anatase and the Fedora Atomic ecosystem.',
    items: [
      {
        question: 'Is YaguareteOS just Anatase with a new logo?',
        answer:
          'No. On top of Anatase we add: our own HHD plugin to move the VRAM carveout from the handheld\'s panel (validated by the firmware/kernel), our own installers for our own apps — Yryvu and Tatu — curated ujust recipes for third-party software like Eden, Antigravity, Claude Code or Decky Loader, our own identity and art (logos, wallpapers, Plymouth, KDE theme), and our own pipeline signed with cosign over our own container registry.',
      },
      {
        question: 'What is the handheld VRAM slider?',
        answer:
          'On an AMD APU the firmware exposes a fixed set of VRAM carveout sizes (512 MB to 32 GB on the OneXFly, for example). Our HHD plugin shows it as a direct selector in the handheld\'s panel: pick the level, confirm, and the system reboots to apply it — no terminal, no BIOS trip. The firmware itself always validates the value.',
      },
      {
        question: 'Do I need a separate variant for NVIDIA?',
        answer:
          'No. It\'s a single image: proprietary NVIDIA drivers are already included, activated when the kernel detects the NVIDIA module loaded.',
      },
      {
        question: 'How do I rebase from another bootc system?',
        answer:
          'Verify the signature with cosign against our public key, then run sudo bootc switch ghcr.io/lobinuxsoft/yaguareteos:stable and reboot. The previous deployment stays on disk as a rollback target. Full step-by-step instructions live in the README.',
      },
      {
        question: 'When will downloadable ISOs be available?',
        answer:
          'Not yet. The pipeline that publishes each :stable promotion as a GitHub Release plus an archive.org item is under construction. Until then, the install path is bootc switch over an existing Fedora Atomic system.',
      },
      {
        question: 'Where will stable releases live?',
        answer:
          'Each :stable promotion will produce a GitHub Release plus a dated archive.org item. The container registry already serves :stable, :testing and :unstable channels for bootc users; the dated tags pin a specific build.',
      },
    ],
  },
};

export default en;
