#!/usr/bin/env python3

import argparse
import os
import sys
from pathlib import Path


def runtime_perl_library_paths(perl_root: Path, runtime_root: Path) -> list[Path]:
    lib_root = perl_root / "lib"
    config_files = [
        path
        for path in lib_root.rglob("Config.pm")
        if (path.parent / "Config_heavy.pl").is_file()
    ]
    if len(config_files) != 1:
        raise ValueError(
            "Expected exactly one Perl Config.pm with a matching Config_heavy.pl "
            f"under '{lib_root}', found {len(config_files)}."
        )

    config_dir = config_files[0].parent
    version_dir = config_dir.parent
    arch_name = config_dir.name
    paths = [config_dir, version_dir]

    site_perl = lib_root / "site_perl"
    if site_perl.is_dir():
        for site_version in sorted(site_perl.iterdir()):
            if not site_version.is_dir():
                continue
            site_arch = site_version / arch_name
            if site_arch.is_dir():
                paths.append(site_arch)
            paths.append(site_version)

    local_lib = runtime_root / "local" / "lib" / "perl5"
    if local_lib.is_dir():
        paths.append(local_lib)
        local_arch = local_lib / arch_name
        if local_arch.is_dir():
            paths.append(local_arch)

    return paths


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Configure library paths for an extracted Perl runtime."
    )
    parser.add_argument("--perl-root", required=True, type=Path)
    parser.add_argument("--runtime-root", required=True, type=Path)
    parser.add_argument("--github-env", required=True, type=Path)
    args = parser.parse_args()

    try:
        paths = runtime_perl_library_paths(args.perl_root, args.runtime_root)
        existing_perl5lib = os.environ.get("PERL5LIB")
        if existing_perl5lib:
            paths.extend(Path(path) for path in existing_perl5lib.split(os.pathsep) if path)

        with args.github_env.open("a", encoding="utf-8", newline="\n") as environment:
            environment.write(f"PERL5LIB={os.pathsep.join(map(str, paths))}\n")
    except (OSError, ValueError) as error:
        parser.error(f"Could not configure extracted Perl runtime: {error}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
