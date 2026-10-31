%global debug_package %{nil}

Name:           yaguarete-qwen-code-desktop-placeholder
Version:        1
Release:        1%{?dist}
Summary:        Satisfies ludos's "specs must contain at least one item"
# Qwen Code Desktop repacks QwenLM's own .deb directly (see card.yaml's
# files/postprocess); it has nothing to build from an RPM spec. ludos's
# FlatpakCard model requires a non-empty `specs:` regardless, so this
# builds an intentionally empty package that nothing lists under
# `packages:` and nothing in `files:` ever references.
License:        MIT
BuildArch:      noarch

%description
Empty placeholder package. Exists only so this card.yaml validates.

%files

%changelog
