## Releasing BiodiverseR Runtimes

This document describes the process for publishing new BiodiverseR runtime releases.

### Overview

Runtime releases are published through GitHub Releases and described in `releases.json`.

Each release may contain platform-specific runtime packages, including:

- Windows
- macOS
- Linux

BiodiverseR uses `releases.json` to determine which runtime version should be downloaded and installed.

### Release Process

#### 1. Ensure CI Is Passing

Confirm that all runtime build workflows are succeeding:

- Windows
- macOS
- Linux

#### 2. Create a Release Tag

Create and push a version tag:

```bash
git tag v0.2.0
git push origin v0.2.0
```

#### 3. Build Runtime Packages

Build runtime packages for all supported platforms.

Examples:

```text
BiodiverseR_windows_x64.zip
BiodiverseR_macos.zip
BiodiverseR_linux_x64.zip
```

#### 4. Create a GitHub Release

Create a GitHub Release using the version tag.

Example:

```text
v0.2.0
```

#### 5. Upload Runtime Packages

Upload all platform runtime packages as release assets.

#### 6. Generate Checksums

Calculate SHA-256 checksums for all uploaded packages.

Example:

```bash
sha256sum BiodiverseR_windows_x64.zip
sha256sum BiodiverseR_macos.zip
sha256sum BiodiverseR_linux_x64.zip
```

#### 7. Update releases.json

Add release metadata and checksums.

Example:

```json
{
  "current": "v0.2.0",
  "releases": {
    "v0.2.0": {
      "windows": {
        "url": "...",
        "sha256": "..."
      },
      "macos": {
        "url": "...",
        "sha256": "..."
      },
      "linux": {
        "url": "...",
        "sha256": "..."
      }
    }
  }
}
```

#### 8. Commit Manifest Changes

Commit and push the updated manifest:

```bash
git add releases.json
git commit -m "Update release manifest for v0.2.0"
git push
```

#### 9. Verify Installation

Confirm that BiodiverseR can:

- Download the runtime.
- Verify the checksum.
- Install successfully.
- Start the runtime.

### Runtime Package Naming

Runtime packages should use the following naming convention:

```text
BiodiverseR_<platform>_<architecture>_<version>.zip
```

Examples:

```text
BiodiverseR_windows_x64_v0.2.0.zip
BiodiverseR_macos_arm64_v0.2.0.zip
BiodiverseR_macos_x86_64_v0.2.0.zip
BiodiverseR_linux_x64_v0.2.0.zip
```

If a universal macOS runtime is available:

```text
BiodiverseR_macos_universal_v0.2.0.zip
```

The version component must exactly match the Git tag used to create the release.

## Future Automation

The release workflow is expected to evolve toward:

1. Build runtime packages.
2. Create GitHub Releases.
3. Upload artifacts.
4. Calculate SHA-256 checksums.
5. Update `releases.json` automatically.

At that point, only tag creation should be required:

```bash
git tag v0.2.0
git push origin v0.2.0
```

### Current Status

- Windows runtime build: complete
- macOS ARM64 runtime build: in progress
- macOS x86_64 runtime build: in progress
- Linux runtime build: in progress
- Automated release workflow: planned
