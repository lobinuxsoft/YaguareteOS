import type { Translations } from './types';

const es: Translations = {
  meta: {
    pageTitle:
      'YaguareteOS — Distro KDE basada en Anatase, orientada al desarrollo y el gaming',
    ogTitle: 'YaguareteOS — KDE para dev y gaming sobre Anatase',
    description:
      'YaguareteOS es una distribución Linux booteable, fork de Anatase (Fedora Atomic / bootc), orientada al desarrollo y el gaming en handhelds. Daemon de mando/TDP/RGB nativo, slider de VRAM validado por firmware, actualizaciones atómicas y firmada en nuestra propia CI.',
  },
  hero: {
    titlePrefix: 'Yaguarete',
    titleSuffix: 'OS',
    subTitle:
      'Distro KDE handheld-first, fork de Anatase. HHD (Handheld Daemon) nativo para mando/TDP/RGB, slider de VRAM validado por el firmware desde el propio panel de HHD, apps propias (Yryvu, Tatu) y sesión Gamemode gamescope+Steam. Image-based con bootc, actualizaciones atómicas, firmada en nuestra propia CI.',
    primaryBtn: 'Leer el README',
    primaryBtnUrl: 'https://github.com/lobinuxsoft/YaguareteOS#readme',
  },
  variants: {
    title: 'Una sola imagen, todo el hardware',
    subTitle:
      'Sin variantes que elegir: una imagen cubre handhelds, desktops, laptops, HTPCs y hardware NVIDIA. Se construye y firma siempre del mismo árbol.',
    upstreamLabel: 'Base upstream',
    downloadLabel: 'Descargar ISO',
    pendingNote: 'ISO en preparación para esta release',
    cosignNote:
      'Las releases stable se publican firmadas con cosign. Verificá la firma contra cosign.pub antes de instalar — instrucciones en el README.',
    cards: [
      {
        name: 'yaguareteos',
        tag: 'Desktop, laptop, handheld y HTPC — AMD, Intel y NVIDIA',
        description:
          'Imagen única. Stack de gráficos AMD/Intel de fábrica, drivers NVIDIA propietarios incluidos cuando el hardware los necesita. Sesiones Plasma Desktop, Plasma Mobile y Gamemode (gamescope + Steam) en el mismo boot.',
        upstream: 'anatase:stable',
        downloadUrl:
          'https://archive.org/download/yaguareteos-stable-20261019/yaguareteos-20261019-x86_64.iso',
      },
    ],
  },
  stack: {
    title: 'Anatase por debajo, dev y gaming arriba',
    subTitle:
      'Heredamos el stack de gaming de Anatase — Steam (Flatpak), gamescope, GameMode, MangoHud, Mesa al día, HHD nativo — y le agregamos lo que necesitamos para el dev cotidiano y para exprimir un handheld. Image-based con bootc: cada update es atómico, rollback en un comando.',
    features: [
      {
        heading: 'Gaming-ready',
        content:
          'Steam (Flatpak), GameMode, gamescope y MangoHud preconfigurados en la sesión Gamemode. Mesa/AMD recientes. HHD (Handheld Daemon) nativo: mando, TDP y RGB out of the box en handhelds como la OneXFly.',
        svg: 'rocket',
      },
      {
        heading: 'Herramientas propias para handheld',
        content:
          'Plugin de HHD para mover el carveout de VRAM del firmware (validado por el kernel, no un workaround de GTT) directo desde el panel de ajustes del handheld, sin terminal. Recetas ujust curadas para Decky Loader, Eden, Antigravity, Claude Code y nuestras propias apps.',
        svg: 'puzzle',
      },
      {
        heading: 'Atómico e inmutable',
        content:
          'Image-based sobre Fedora Atomic con bootc. Cada update es una imagen completa firmada. Rollback inmediato si algo falla.',
        svg: 'frame',
      },
      {
        heading: 'Dev-friendly',
        content:
          'Terminal lista de fábrica: kitty con zsh, prompt Powerlevel10k y FiraCode Nerd Font con ligatures, en un comando. Claude Code y Antigravity a un `ujust`. Toolbox, distrobox y devcontainer first-class. KDE Plasma como escritorio. Defaults en español, locale es-AR.',
        svg: 'tools',
      },
    ],
  },
  faq: {
    title: 'Preguntas frecuentes',
    subTitle:
      'Qué es YaguareteOS, cómo se instala, y cómo se relaciona con Anatase y el ecosistema Fedora Atomic.',
    items: [
      {
        question: '¿YaguareteOS es Anatase con otro logo?',
        answer:
          'No. Sumamos sobre Anatase: un plugin de HHD propio para mover el carveout de VRAM desde el panel del handheld (validado por el firmware/kernel), instaladores propios para nuestras apps —Yryvu y Tatu— y recetas ujust curadas para software de terceros como Eden, Antigravity, Claude Code o Decky Loader, identidad y arte propios (logos, wallpapers, Plymouth, tema KDE) y pipeline propio firmado con cosign sobre nuestro propio registro de contenedores.',
      },
      {
        question: '¿Qué es el slider de VRAM para handhelds?',
        answer:
          'En una APU AMD el firmware expone un conjunto fijo de tamaños de carveout de VRAM (por ejemplo 512 MB a 32 GB en la OneXFly). Nuestro plugin de HHD lo muestra como un selector directo en el panel del handheld: elegís el nivel, confirmás y el sistema reinicia para aplicarlo — sin terminal, sin tocar el BIOS a mano. El valor siempre lo valida el propio firmware.',
      },
      {
        question: '¿Necesito elegir una variante para NVIDIA?',
        answer:
          'No. Es una sola imagen: los drivers NVIDIA propietarios ya están incluidos, se activan cuando el kernel detecta el módulo NVIDIA cargado.',
      },
      {
        question: '¿Cómo hago rebase desde otro sistema bootc?',
        answer:
          'Verificá la firma con cosign contra nuestra clave pública, después corré sudo bootc switch ghcr.io/lobinuxsoft/yaguareteos:stable y reiniciá. El deployment previo queda en disco como target de rollback. Instrucciones paso a paso completas viven en el README.',
      },
      {
        question: '¿Cuándo va a haber ISOs descargables?',
        answer:
          'Ya está disponible la primera. Cada promoción a :stable produce un GitHub Release más un item en archive.org con la ISO x86_64. El botón de descarga de la sección de arriba apunta directo a la última publicada. Para usuarios bootc, el rebase sigue siendo directo: sudo bootc switch ghcr.io/lobinuxsoft/yaguareteos:stable.',
      },
      {
        question: '¿Dónde viven las releases stable?',
        answer:
          'Cada promoción a :stable produce un GitHub Release más un item con fecha en archive.org (identificador yaguareteos-stable-<YYYYMMDD>). El registro de contenedores sirve los canales :stable, :testing y :unstable para usuarios bootc; los tags con fecha pinean una build específica.',
      },
    ],
  },
};

export default es;
