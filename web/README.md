# YaguareteOS — landing source

Astro 6 + Tailwind 4 + GSAP + Lenis. Builds to <https://lobinuxsoft.github.io/YaguareteOS/>.

Forked from [ScrewFast](https://github.com/mearashadowfax/ScrewFast) (MIT). Brand colours, content, assets and copy are YaguareteOS.

## Local dev

Requires Node 20+ and `pnpm` (or `npm` / `yarn`, but the lockfile is pnpm).

```bash
cd web/
pnpm install
pnpm dev
```

Dev server runs at `http://localhost:4321/YaguareteOS/`.

## Build

```bash
pnpm build
```

Output to `web/dist/`. Includes `astro check` + post-process HTML minification.

## CI

`.github/workflows/pages.yml` builds + deploys on every push to `master` that touches `web/**`. Pages source is configured to **GitHub Actions** (not branch/folder).

## Migration note

Ported as-is from [`lobinuxsoft/yaguarete_os`](https://github.com/lobinuxsoft/yaguarete_os) (Bazzite-based, retired) — see [#3](https://github.com/lobinuxsoft/YaguareteOS/issues/3). Content and branding were updated for this repo's Anatase base; the Astro app itself (components, build, i18n setup) is unchanged.
