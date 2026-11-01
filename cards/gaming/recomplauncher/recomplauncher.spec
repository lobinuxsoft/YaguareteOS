# Hand-packaged: upstream ships no RPM spec. RecompLauncher is a Tauri 2
# (Rust + static HTML/JS, no npm build step -- frontendDist points straight
# at ui/) desktop app, so this builds the Rust side only with plain cargo.
#
# Fedora does not package the Tauri/wry/webkit2gtk-rs ecosystem, so most of
# Cargo.lock's crates resolve from Fedora's own rust-* packages via the usual
# dynamic BuildRequires (%%cargo_generate_buildrequires), and the ~60 crates
# Fedora lacks are pinned individually from crates.io below and patched in
# via [patch.crates-io], the same technique steamos-manager.spec uses for its
# own gaps. keyboard-types needs two incompatible major versions at once
# (global-hotkey wants 0.7, muda/tauri want 0.8); [patch] can only name a
# crate once, so those two are placed directly into cargo's local registry
# instead, where multiple versions are expected to coexist.

%global cargo_install_lib 0
%global debug_package %{nil}
# version_no_tilde just drops the "~"; upstream's own tag keeps the dash
# (v0.90.0-beta.6), so track it separately for Source0/%%autosetup.
%global tag 0.90.0-beta.6

Name:           recomplauncher
Version:        0.90.0~beta.6
Release:        1%{?dist}
Summary:        Launcher for PC recomps (native PC ports of console games)

License:        GPL-3.0-or-later

URL:            https://github.com/elripalda/RecompLauncher
Source0:        %{url}/archive/refs/tags/v%{tag}/recomplauncher-%{tag}.tar.gz

# Crates Fedora does not package (see the dynamic-buildrequires note above).
Source10:        https://crates.io/api/v1/crates/atk/0.18.2/download#/atk-0.18.2.crate
Source11:        https://crates.io/api/v1/crates/atk-sys/0.18.2/download#/atk-sys-0.18.2.crate
Source12:        https://crates.io/api/v1/crates/cfb/0.14.0/download#/cfb-0.14.0.crate
Source13:        https://crates.io/api/v1/crates/compression-codecs/0.4.46/download#/compression-codecs-0.4.46.crate
Source14:        https://crates.io/api/v1/crates/compression-core/0.4.34/download#/compression-core-0.4.34.crate
Source15:        https://crates.io/api/v1/crates/discord-rich-presence/1.1.0/download#/discord-rich-presence-1.1.0.crate
Source16:        https://crates.io/api/v1/crates/dom_query/0.28.0/download#/dom_query-0.28.0.crate
Source17:        https://crates.io/api/v1/crates/embed-resource/3.0.12/download#/embed-resource-3.0.12.crate
Source18:        https://crates.io/api/v1/crates/filetime_creation/0.2.0/download#/filetime_creation-0.2.0.crate
Source19:        https://crates.io/api/v1/crates/gdk/0.18.2/download#/gdk-0.18.2.crate
Source20:        https://crates.io/api/v1/crates/gdk-sys/0.18.2/download#/gdk-sys-0.18.2.crate
Source21:        https://crates.io/api/v1/crates/gdkwayland-sys/0.18.2/download#/gdkwayland-sys-0.18.2.crate
Source22:        https://crates.io/api/v1/crates/gdkx11/0.18.2/download#/gdkx11-0.18.2.crate
Source23:        https://crates.io/api/v1/crates/gdkx11-sys/0.18.2/download#/gdkx11-sys-0.18.2.crate
Source24:        https://crates.io/api/v1/crates/gilrs/0.11.2/download#/gilrs-0.11.2.crate
Source25:        https://crates.io/api/v1/crates/gilrs-core/0.6.8/download#/gilrs-core-0.6.8.crate
Source26:        https://crates.io/api/v1/crates/global-hotkey/0.8.0/download#/global-hotkey-0.8.0.crate
Source27:        https://crates.io/api/v1/crates/gtk/0.18.2/download#/gtk-0.18.2.crate
Source28:        https://crates.io/api/v1/crates/gtk-sys/0.18.2/download#/gtk-sys-0.18.2.crate
Source29:        https://crates.io/api/v1/crates/gtk3-macros/0.18.2/download#/gtk3-macros-0.18.2.crate
Source30:        https://crates.io/api/v1/crates/http-range/0.1.6/download#/http-range-0.1.6.crate
Source31:        https://crates.io/api/v1/crates/ico/0.6.0/download#/ico-0.6.0.crate
Source32:        https://crates.io/api/v1/crates/infer/0.22.0/download#/infer-0.22.0.crate
Source33:        https://crates.io/api/v1/crates/javascriptcore-rs/1.1.2/download#/javascriptcore-rs-1.1.2.crate
Source34:        https://crates.io/api/v1/crates/javascriptcore-rs-sys/1.1.1/download#/javascriptcore-rs-sys-1.1.1.crate
Source35:        https://crates.io/api/v1/crates/json-patch/4.2.0/download#/json-patch-4.2.0.crate
Source36:        https://crates.io/api/v1/crates/jsonptr/0.7.1/download#/jsonptr-0.7.1.crate
Source37:        https://crates.io/api/v1/crates/keyboard-types/0.7.0/download#/keyboard-types-0.7.0.crate
Source38:        https://crates.io/api/v1/crates/keyboard-types/0.8.3/download#/keyboard-types-0.8.3.crate
Source39:        https://crates.io/api/v1/crates/libappindicator/0.9.0/download#/libappindicator-0.9.0.crate
Source40:        https://crates.io/api/v1/crates/libappindicator-sys/0.9.0/download#/libappindicator-sys-0.9.0.crate
Source41:        https://crates.io/api/v1/crates/lzma-rust/0.1.7/download#/lzma-rust-0.1.7.crate
Source42:        https://crates.io/api/v1/crates/muda/0.20.0/download#/muda-0.20.0.crate
Source43:        https://crates.io/api/v1/crates/nt-time/0.8.1/download#/nt-time-0.8.1.crate
Source44:        https://crates.io/api/v1/crates/qrcode/0.14.1/download#/qrcode-0.14.1.crate
Source45:        https://crates.io/api/v1/crates/serialize-to-javascript/0.1.2/download#/serialize-to-javascript-0.1.2.crate
Source46:        https://crates.io/api/v1/crates/serialize-to-javascript-impl/0.1.2/download#/serialize-to-javascript-impl-0.1.2.crate
Source47:        https://crates.io/api/v1/crates/sevenz-rust/0.6.1/download#/sevenz-rust-0.6.1.crate
Source48:        https://crates.io/api/v1/crates/soup3/0.5.0/download#/soup3-0.5.0.crate
Source49:        https://crates.io/api/v1/crates/soup3-sys/0.5.0/download#/soup3-sys-0.5.0.crate
Source50:        https://crates.io/api/v1/crates/static_vcruntime/3.0.0/download#/static_vcruntime-3.0.0.crate
Source51:        https://crates.io/api/v1/crates/tao/0.37.2/download#/tao-0.37.2.crate
Source52:        https://crates.io/api/v1/crates/tauri/2.12.5/download#/tauri-2.12.5.crate
Source53:        https://crates.io/api/v1/crates/tauri-build/2.7.4/download#/tauri-build-2.7.4.crate
Source54:        https://crates.io/api/v1/crates/tauri-codegen/2.7.4/download#/tauri-codegen-2.7.4.crate
Source55:        https://crates.io/api/v1/crates/tauri-macros/2.7.4/download#/tauri-macros-2.7.4.crate
Source56:        https://crates.io/api/v1/crates/tauri-plugin/2.7.2/download#/tauri-plugin-2.7.2.crate
Source57:        https://crates.io/api/v1/crates/tauri-plugin-dialog/2.8.3/download#/tauri-plugin-dialog-2.8.3.crate
Source58:        https://crates.io/api/v1/crates/tauri-plugin-fs/2.7.1/download#/tauri-plugin-fs-2.7.1.crate
Source59:        https://crates.io/api/v1/crates/tauri-plugin-global-shortcut/2.4.1/download#/tauri-plugin-global-shortcut-2.4.1.crate
Source60:        https://crates.io/api/v1/crates/tauri-plugin-notification/2.7.0/download#/tauri-plugin-notification-2.7.0.crate
Source61:        https://crates.io/api/v1/crates/tauri-plugin-opener/2.7.2/download#/tauri-plugin-opener-2.7.2.crate
Source62:        https://crates.io/api/v1/crates/tauri-plugin-single-instance/2.5.4/download#/tauri-plugin-single-instance-2.5.4.crate
Source63:        https://crates.io/api/v1/crates/tauri-runtime/2.12.2/download#/tauri-runtime-2.12.2.crate
Source64:        https://crates.io/api/v1/crates/tauri-runtime-wry/2.12.3/download#/tauri-runtime-wry-2.12.3.crate
Source65:        https://crates.io/api/v1/crates/tauri-utils/2.10.2/download#/tauri-utils-2.10.2.crate
Source66:        https://crates.io/api/v1/crates/tauri-winres/0.3.7/download#/tauri-winres-0.3.7.crate
Source67:        https://crates.io/api/v1/crates/tray-icon/0.25.1/download#/tray-icon-0.25.1.crate
Source68:        https://crates.io/api/v1/crates/unrar/0.5.8/download#/unrar-0.5.8.crate
Source69:        https://crates.io/api/v1/crates/unrar_sys/0.5.8/download#/unrar_sys-0.5.8.crate
Source70:        https://crates.io/api/v1/crates/urlpattern/0.6.0/download#/urlpattern-0.6.0.crate
Source71:        https://crates.io/api/v1/crates/webkit2gtk/2.0.2/download#/webkit2gtk-2.0.2.crate
Source72:        https://crates.io/api/v1/crates/webkit2gtk-sys/2.0.2/download#/webkit2gtk-sys-2.0.2.crate
Source73:        https://crates.io/api/v1/crates/wry/0.57.1/download#/wry-0.57.1.crate

BuildRequires:  cargo-rpm-macros >= 24
BuildRequires:  cargo
BuildRequires:  rust
BuildRequires:  rust-packaging
BuildRequires:  desktop-file-utils
BuildRequires:  pkgconfig(webkit2gtk-4.1)
BuildRequires:  pkgconfig(javascriptcoregtk-4.1)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(libsoup-3.0)
BuildRequires:  pkgconfig(appindicator3-0.1)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(glib-2.0)

Requires:       webkit2gtk4.1
Requires:       gtk3
Requires:       libsoup3
Requires:       libappindicator-gtk3

%description
RecompLauncher finds, installs, updates and starts PC recomps (native PC
ports of console games, made by their own developers) from each
developer's GitHub releases. It ships no game files; every game needs the
user's own copy. On Linux it can hand games off to Steam's Proton,
GE-Proton, umu-launcher or Wine.

%prep
%autosetup -n RecompLauncher-%{tag}
cd src-tauri
%cargo_prep
mkdir -p vendor
install -dm0755 "vendor/atk-0.18.2"
tar -xzf %{SOURCE10} --strip-components=1 -C "vendor/atk-0.18.2"
install -dm0755 "vendor/atk-sys-0.18.2"
tar -xzf %{SOURCE11} --strip-components=1 -C "vendor/atk-sys-0.18.2"
install -dm0755 "vendor/cfb-0.14.0"
tar -xzf %{SOURCE12} --strip-components=1 -C "vendor/cfb-0.14.0"
install -dm0755 "vendor/compression-codecs-0.4.46"
tar -xzf %{SOURCE13} --strip-components=1 -C "vendor/compression-codecs-0.4.46"
install -dm0755 "vendor/compression-core-0.4.34"
tar -xzf %{SOURCE14} --strip-components=1 -C "vendor/compression-core-0.4.34"
install -dm0755 "vendor/discord-rich-presence-1.1.0"
tar -xzf %{SOURCE15} --strip-components=1 -C "vendor/discord-rich-presence-1.1.0"
install -dm0755 "vendor/dom_query-0.28.0"
tar -xzf %{SOURCE16} --strip-components=1 -C "vendor/dom_query-0.28.0"
install -dm0755 "vendor/embed-resource-3.0.12"
tar -xzf %{SOURCE17} --strip-components=1 -C "vendor/embed-resource-3.0.12"
install -dm0755 "vendor/filetime_creation-0.2.0"
tar -xzf %{SOURCE18} --strip-components=1 -C "vendor/filetime_creation-0.2.0"
install -dm0755 "vendor/gdk-0.18.2"
tar -xzf %{SOURCE19} --strip-components=1 -C "vendor/gdk-0.18.2"
install -dm0755 "vendor/gdk-sys-0.18.2"
tar -xzf %{SOURCE20} --strip-components=1 -C "vendor/gdk-sys-0.18.2"
install -dm0755 "vendor/gdkwayland-sys-0.18.2"
tar -xzf %{SOURCE21} --strip-components=1 -C "vendor/gdkwayland-sys-0.18.2"
install -dm0755 "vendor/gdkx11-0.18.2"
tar -xzf %{SOURCE22} --strip-components=1 -C "vendor/gdkx11-0.18.2"
install -dm0755 "vendor/gdkx11-sys-0.18.2"
tar -xzf %{SOURCE23} --strip-components=1 -C "vendor/gdkx11-sys-0.18.2"
install -dm0755 "vendor/gilrs-0.11.2"
tar -xzf %{SOURCE24} --strip-components=1 -C "vendor/gilrs-0.11.2"
install -dm0755 "vendor/gilrs-core-0.6.8"
tar -xzf %{SOURCE25} --strip-components=1 -C "vendor/gilrs-core-0.6.8"
install -dm0755 "vendor/global-hotkey-0.8.0"
tar -xzf %{SOURCE26} --strip-components=1 -C "vendor/global-hotkey-0.8.0"
install -dm0755 "vendor/gtk-0.18.2"
tar -xzf %{SOURCE27} --strip-components=1 -C "vendor/gtk-0.18.2"
install -dm0755 "vendor/gtk-sys-0.18.2"
tar -xzf %{SOURCE28} --strip-components=1 -C "vendor/gtk-sys-0.18.2"
install -dm0755 "vendor/gtk3-macros-0.18.2"
tar -xzf %{SOURCE29} --strip-components=1 -C "vendor/gtk3-macros-0.18.2"
install -dm0755 "vendor/http-range-0.1.6"
tar -xzf %{SOURCE30} --strip-components=1 -C "vendor/http-range-0.1.6"
install -dm0755 "vendor/ico-0.6.0"
tar -xzf %{SOURCE31} --strip-components=1 -C "vendor/ico-0.6.0"
install -dm0755 "vendor/infer-0.22.0"
tar -xzf %{SOURCE32} --strip-components=1 -C "vendor/infer-0.22.0"
install -dm0755 "vendor/javascriptcore-rs-1.1.2"
tar -xzf %{SOURCE33} --strip-components=1 -C "vendor/javascriptcore-rs-1.1.2"
install -dm0755 "vendor/javascriptcore-rs-sys-1.1.1"
tar -xzf %{SOURCE34} --strip-components=1 -C "vendor/javascriptcore-rs-sys-1.1.1"
install -dm0755 "vendor/json-patch-4.2.0"
tar -xzf %{SOURCE35} --strip-components=1 -C "vendor/json-patch-4.2.0"
install -dm0755 "vendor/jsonptr-0.7.1"
tar -xzf %{SOURCE36} --strip-components=1 -C "vendor/jsonptr-0.7.1"
install -dm0755 "vendor/libappindicator-0.9.0"
tar -xzf %{SOURCE39} --strip-components=1 -C "vendor/libappindicator-0.9.0"
install -dm0755 "vendor/libappindicator-sys-0.9.0"
tar -xzf %{SOURCE40} --strip-components=1 -C "vendor/libappindicator-sys-0.9.0"
install -dm0755 "vendor/lzma-rust-0.1.7"
tar -xzf %{SOURCE41} --strip-components=1 -C "vendor/lzma-rust-0.1.7"
install -dm0755 "vendor/muda-0.20.0"
tar -xzf %{SOURCE42} --strip-components=1 -C "vendor/muda-0.20.0"
install -dm0755 "vendor/nt-time-0.8.1"
tar -xzf %{SOURCE43} --strip-components=1 -C "vendor/nt-time-0.8.1"
install -dm0755 "vendor/qrcode-0.14.1"
tar -xzf %{SOURCE44} --strip-components=1 -C "vendor/qrcode-0.14.1"
install -dm0755 "vendor/serialize-to-javascript-0.1.2"
tar -xzf %{SOURCE45} --strip-components=1 -C "vendor/serialize-to-javascript-0.1.2"
install -dm0755 "vendor/serialize-to-javascript-impl-0.1.2"
tar -xzf %{SOURCE46} --strip-components=1 -C "vendor/serialize-to-javascript-impl-0.1.2"
install -dm0755 "vendor/sevenz-rust-0.6.1"
tar -xzf %{SOURCE47} --strip-components=1 -C "vendor/sevenz-rust-0.6.1"
install -dm0755 "vendor/soup3-0.5.0"
tar -xzf %{SOURCE48} --strip-components=1 -C "vendor/soup3-0.5.0"
install -dm0755 "vendor/soup3-sys-0.5.0"
tar -xzf %{SOURCE49} --strip-components=1 -C "vendor/soup3-sys-0.5.0"
install -dm0755 "vendor/static_vcruntime-3.0.0"
tar -xzf %{SOURCE50} --strip-components=1 -C "vendor/static_vcruntime-3.0.0"
install -dm0755 "vendor/tao-0.37.2"
tar -xzf %{SOURCE51} --strip-components=1 -C "vendor/tao-0.37.2"
install -dm0755 "vendor/tauri-2.12.5"
tar -xzf %{SOURCE52} --strip-components=1 -C "vendor/tauri-2.12.5"
install -dm0755 "vendor/tauri-build-2.7.4"
tar -xzf %{SOURCE53} --strip-components=1 -C "vendor/tauri-build-2.7.4"
install -dm0755 "vendor/tauri-codegen-2.7.4"
tar -xzf %{SOURCE54} --strip-components=1 -C "vendor/tauri-codegen-2.7.4"
install -dm0755 "vendor/tauri-macros-2.7.4"
tar -xzf %{SOURCE55} --strip-components=1 -C "vendor/tauri-macros-2.7.4"
install -dm0755 "vendor/tauri-plugin-2.7.2"
tar -xzf %{SOURCE56} --strip-components=1 -C "vendor/tauri-plugin-2.7.2"
install -dm0755 "vendor/tauri-plugin-dialog-2.8.3"
tar -xzf %{SOURCE57} --strip-components=1 -C "vendor/tauri-plugin-dialog-2.8.3"
install -dm0755 "vendor/tauri-plugin-fs-2.7.1"
tar -xzf %{SOURCE58} --strip-components=1 -C "vendor/tauri-plugin-fs-2.7.1"
install -dm0755 "vendor/tauri-plugin-global-shortcut-2.4.1"
tar -xzf %{SOURCE59} --strip-components=1 -C "vendor/tauri-plugin-global-shortcut-2.4.1"
install -dm0755 "vendor/tauri-plugin-notification-2.7.0"
tar -xzf %{SOURCE60} --strip-components=1 -C "vendor/tauri-plugin-notification-2.7.0"
install -dm0755 "vendor/tauri-plugin-opener-2.7.2"
tar -xzf %{SOURCE61} --strip-components=1 -C "vendor/tauri-plugin-opener-2.7.2"
install -dm0755 "vendor/tauri-plugin-single-instance-2.5.4"
tar -xzf %{SOURCE62} --strip-components=1 -C "vendor/tauri-plugin-single-instance-2.5.4"
install -dm0755 "vendor/tauri-runtime-2.12.2"
tar -xzf %{SOURCE63} --strip-components=1 -C "vendor/tauri-runtime-2.12.2"
install -dm0755 "vendor/tauri-runtime-wry-2.12.3"
tar -xzf %{SOURCE64} --strip-components=1 -C "vendor/tauri-runtime-wry-2.12.3"
install -dm0755 "vendor/tauri-utils-2.10.2"
tar -xzf %{SOURCE65} --strip-components=1 -C "vendor/tauri-utils-2.10.2"
install -dm0755 "vendor/tauri-winres-0.3.7"
tar -xzf %{SOURCE66} --strip-components=1 -C "vendor/tauri-winres-0.3.7"
install -dm0755 "vendor/tray-icon-0.25.1"
tar -xzf %{SOURCE67} --strip-components=1 -C "vendor/tray-icon-0.25.1"
install -dm0755 "vendor/unrar-0.5.8"
tar -xzf %{SOURCE68} --strip-components=1 -C "vendor/unrar-0.5.8"
install -dm0755 "vendor/unrar_sys-0.5.8"
tar -xzf %{SOURCE69} --strip-components=1 -C "vendor/unrar_sys-0.5.8"
install -dm0755 "vendor/urlpattern-0.6.0"
tar -xzf %{SOURCE70} --strip-components=1 -C "vendor/urlpattern-0.6.0"
install -dm0755 "vendor/webkit2gtk-2.0.2"
tar -xzf %{SOURCE71} --strip-components=1 -C "vendor/webkit2gtk-2.0.2"
install -dm0755 "vendor/webkit2gtk-sys-2.0.2"
tar -xzf %{SOURCE72} --strip-components=1 -C "vendor/webkit2gtk-sys-2.0.2"
install -dm0755 "vendor/wry-0.57.1"
tar -xzf %{SOURCE73} --strip-components=1 -C "vendor/wry-0.57.1"

cat >> .cargo/config.toml << EOF

[patch.crates-io]
atk = { path = "vendor/atk-0.18.2" }
atk-sys = { path = "vendor/atk-sys-0.18.2" }
cfb = { path = "vendor/cfb-0.14.0" }
compression-codecs = { path = "vendor/compression-codecs-0.4.46" }
compression-core = { path = "vendor/compression-core-0.4.34" }
discord-rich-presence = { path = "vendor/discord-rich-presence-1.1.0" }
dom_query = { path = "vendor/dom_query-0.28.0" }
embed-resource = { path = "vendor/embed-resource-3.0.12" }
filetime_creation = { path = "vendor/filetime_creation-0.2.0" }
gdk = { path = "vendor/gdk-0.18.2" }
gdk-sys = { path = "vendor/gdk-sys-0.18.2" }
gdkwayland-sys = { path = "vendor/gdkwayland-sys-0.18.2" }
gdkx11 = { path = "vendor/gdkx11-0.18.2" }
gdkx11-sys = { path = "vendor/gdkx11-sys-0.18.2" }
gilrs = { path = "vendor/gilrs-0.11.2" }
gilrs-core = { path = "vendor/gilrs-core-0.6.8" }
global-hotkey = { path = "vendor/global-hotkey-0.8.0" }
gtk = { path = "vendor/gtk-0.18.2" }
gtk-sys = { path = "vendor/gtk-sys-0.18.2" }
gtk3-macros = { path = "vendor/gtk3-macros-0.18.2" }
http-range = { path = "vendor/http-range-0.1.6" }
ico = { path = "vendor/ico-0.6.0" }
infer = { path = "vendor/infer-0.22.0" }
javascriptcore-rs = { path = "vendor/javascriptcore-rs-1.1.2" }
javascriptcore-rs-sys = { path = "vendor/javascriptcore-rs-sys-1.1.1" }
json-patch = { path = "vendor/json-patch-4.2.0" }
jsonptr = { path = "vendor/jsonptr-0.7.1" }
libappindicator = { path = "vendor/libappindicator-0.9.0" }
libappindicator-sys = { path = "vendor/libappindicator-sys-0.9.0" }
lzma-rust = { path = "vendor/lzma-rust-0.1.7" }
muda = { path = "vendor/muda-0.20.0" }
nt-time = { path = "vendor/nt-time-0.8.1" }
qrcode = { path = "vendor/qrcode-0.14.1" }
serialize-to-javascript = { path = "vendor/serialize-to-javascript-0.1.2" }
serialize-to-javascript-impl = { path = "vendor/serialize-to-javascript-impl-0.1.2" }
sevenz-rust = { path = "vendor/sevenz-rust-0.6.1" }
soup3 = { path = "vendor/soup3-0.5.0" }
soup3-sys = { path = "vendor/soup3-sys-0.5.0" }
static_vcruntime = { path = "vendor/static_vcruntime-3.0.0" }
tao = { path = "vendor/tao-0.37.2" }
tauri = { path = "vendor/tauri-2.12.5" }
tauri-build = { path = "vendor/tauri-build-2.7.4" }
tauri-codegen = { path = "vendor/tauri-codegen-2.7.4" }
tauri-macros = { path = "vendor/tauri-macros-2.7.4" }
tauri-plugin = { path = "vendor/tauri-plugin-2.7.2" }
tauri-plugin-dialog = { path = "vendor/tauri-plugin-dialog-2.8.3" }
tauri-plugin-fs = { path = "vendor/tauri-plugin-fs-2.7.1" }
tauri-plugin-global-shortcut = { path = "vendor/tauri-plugin-global-shortcut-2.4.1" }
tauri-plugin-notification = { path = "vendor/tauri-plugin-notification-2.7.0" }
tauri-plugin-opener = { path = "vendor/tauri-plugin-opener-2.7.2" }
tauri-plugin-single-instance = { path = "vendor/tauri-plugin-single-instance-2.5.4" }
tauri-runtime = { path = "vendor/tauri-runtime-2.12.2" }
tauri-runtime-wry = { path = "vendor/tauri-runtime-wry-2.12.3" }
tauri-utils = { path = "vendor/tauri-utils-2.10.2" }
tauri-winres = { path = "vendor/tauri-winres-0.3.7" }
tray-icon = { path = "vendor/tray-icon-0.25.1" }
unrar = { path = "vendor/unrar-0.5.8" }
unrar_sys = { path = "vendor/unrar_sys-0.5.8" }
urlpattern = { path = "vendor/urlpattern-0.6.0" }
webkit2gtk = { path = "vendor/webkit2gtk-2.0.2" }
webkit2gtk-sys = { path = "vendor/webkit2gtk-sys-2.0.2" }
wry = { path = "vendor/wry-0.57.1" }
EOF
install -dm0755 "%{cargo_registry}/keyboard-types-0.7.0"
tar -xzf %{SOURCE37} --strip-components=1 -C "%{cargo_registry}/keyboard-types-0.7.0"
echo '{"files":{},"package":""}' > "%{cargo_registry}/keyboard-types-0.7.0/.cargo-checksum.json"

install -dm0755 "%{cargo_registry}/keyboard-types-0.8.3"
tar -xzf %{SOURCE38} --strip-components=1 -C "%{cargo_registry}/keyboard-types-0.8.3"
echo '{"files":{},"package":""}' > "%{cargo_registry}/keyboard-types-0.8.3/.cargo-checksum.json"


%generate_buildrequires
cd src-tauri
%cargo_generate_buildrequires

%build
cd src-tauri
%cargo_build

%install
cd src-tauri
install -Dm0755 target/rpm/recomplauncher %{buildroot}%{_bindir}/recomplauncher

install -Dm0644 icons/128x128.png \
    %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/recomplauncher.png

install -Dm0644 /dev/stdin %{buildroot}%{_datadir}/applications/recomplauncher.desktop << EOF
[Desktop Entry]
Type=Application
Name=RecompLauncher
Comment=One home for PC recomps
Exec=recomplauncher
Icon=recomplauncher
Categories=Game;
EOF

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/recomplauncher.desktop

%files
%license LICENSE
%{_bindir}/recomplauncher
%{_datadir}/applications/recomplauncher.desktop
%{_datadir}/icons/hicolor/128x128/apps/recomplauncher.png

%changelog
* Sun Nov 01 2026 YaguareteOS <noreply@yaguarete.os> - 0.90.0~beta.6-1
- Initial package, built from upstream's v0.90.0-beta.6 tag.
