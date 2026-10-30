#!/usr/bin/env python3

import argparse
import json
import os
import re
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

MANIFEST_URL = (
    "https://raw.githubusercontent.com/"
    "biogeospatial/biodiverse-runtime-dependencies/main/releases.json"
)
CHANNELS = ("development", "testing", "stable")
PLATFORMS = ("windows", "macos", "linux")


def resolve_runtime_dependency(
    manifest: object, channel: str, platform: str
) -> dict[str, str]:
    if channel not in CHANNELS:
        raise ValueError(
            f"Unsupported runtime dependency channel '{channel}'. "
            f"Choose one of: {', '.join(CHANNELS)}"
        )
    if platform not in PLATFORMS:
        raise ValueError(
            f"Unsupported runtime dependency platform '{platform}'. "
            f"Choose one of: {', '.join(PLATFORMS)}"
        )
    if not isinstance(manifest, dict):
        raise ValueError("The release manifest must be a JSON object.")

    channels = manifest.get("channels")
    releases = manifest.get("releases")
    if not isinstance(channels, dict) or not isinstance(releases, dict):
        raise ValueError("The release manifest must contain channels and releases objects.")

    version = channels.get(channel)
    if not isinstance(version, str) or not version.strip():
        raise ValueError(f"The '{channel}' channel does not reference a release.")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._+-]*", version):
        raise ValueError(f"The '{channel}' channel contains an invalid release version.")

    release = releases.get(version)
    if not isinstance(release, dict):
        raise ValueError(
            f"The '{channel}' channel references missing release '{version}'."
        )

    artifact = release.get(platform)
    if not isinstance(artifact, dict):
        raise ValueError(
            f"Release '{version}' has no '{platform}' artifact metadata."
        )

    url = artifact.get("url")
    if not isinstance(url, str) or not url.strip():
        raise ValueError(
            f"Release '{version}' has no download URL for '{platform}'."
        )
    parsed_url = urlparse(url)
    if parsed_url.scheme != "https" or not parsed_url.netloc or any(
        character in url for character in "\r\n"
    ):
        raise ValueError(
            f"Release '{version}' has an invalid HTTPS download URL for '{platform}'."
        )

    sha256 = artifact.get("sha256")
    if not isinstance(sha256, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", sha256):
        raise ValueError(
            f"Release '{version}' has an invalid SHA-256 checksum for '{platform}'."
        )

    return {
        "version": version,
        "url": url,
        "sha256": sha256.lower(),
    }


def load_manifest(manifest_path: Path | None) -> object:
    if manifest_path is not None:
        return json.loads(manifest_path.read_text(encoding="utf-8"))

    request = Request(
        MANIFEST_URL,
        headers={"Accept": "application/json", "User-Agent": "biodiverseR-runtime-builder"},
    )
    with urlopen(request, timeout=30) as response:
        return json.loads(response.read())


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Resolve a platform artifact from the runtime dependency manifest."
    )
    parser.add_argument("--channel", required=True, choices=CHANNELS)
    parser.add_argument("--platform", required=True, choices=PLATFORMS)
    parser.add_argument(
        "--manifest",
        type=Path,
        help="Read a local manifest instead of fetching the upstream manifest.",
    )
    parser.add_argument(
        "--github-env",
        type=Path,
        default=Path(os.environ["GITHUB_ENV"]) if "GITHUB_ENV" in os.environ else None,
        help="Append resolved values to a GitHub Actions environment file.",
    )
    args = parser.parse_args()

    try:
        dependency = resolve_runtime_dependency(
            load_manifest(args.manifest), args.channel, args.platform
        )
    except (HTTPError, URLError, TimeoutError, OSError, json.JSONDecodeError, ValueError) as error:
        parser.error(f"Could not resolve runtime dependency: {error}")

    values = {
        "RUNTIME_DEPENDENCY_CHANNEL": args.channel,
        "RUNTIME_DEPENDENCY_VERSION": dependency["version"],
        "RUNTIME_DEPENDENCY_URL": dependency["url"],
        "RUNTIME_DEPENDENCY_SHA256": dependency["sha256"],
    }
    output = "".join(f"{key}={value}\n" for key, value in values.items())
    if args.github_env is None:
        sys.stdout.write(output)
    else:
        with args.github_env.open("a", encoding="utf-8", newline="\n") as environment:
            environment.write(output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
