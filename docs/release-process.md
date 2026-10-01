# Releasing BiodiverseR Runtimes

This document describes the process for publishing new BiodiverseR runtime releases.

## Overview

Runtime releases are published through GitHub Releases and described in
`releases.json`.

Each release may contain platform-specific runtime packages, including:

- Windows
- macOS
- Linux

BiodiverseR uses `releases.json` to determine which runtime version
should be downloaded and installed.

## Current Release Process

Runtime releases are created from Git tags.

Example:

```bash
git tag v0.2.0
git push origin v0.2.0
```

The release workflow:

1. Builds the runtime package.
2. Creates a runtime archive.
3. Creates or updates the GitHub Release.
4. Uploads the runtime archive as a release asset.

## Release Workflow

### 1. Ensure CI Is Passing

Confirm that all relevant runtime workflows are succeeding.

Current workflows include:

- Windows
- macOS
- Linux

### 2. Create a Release Tag

Create and push a version tag:

```bash
git tag v0.2.0
git push origin v0.2.0
```

### 3. Verify Release Build

The release workflow should:

- Build the runtime.
- Run runtime validation tests.
- Package the runtime archive.
- Publish the release asset.

### 4. Verify Release Asset

Confirm that a GitHub Release has been created and that the expected
runtime archive has been attached.

Example:

```text
BiodiverseR_macos_arm64_v0.2.0.zip
```

### 5. Update releases.json

Update the release manifest to reference the new runtime release.

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

### 6. Verify Installation

Confirm that BiodiverseR can:

- Download the runtime.
- Verify the checksum.
- Install successfully.
- Start the runtime.
- Create and use a `basedata` object.

## Release Manifest

Runtime release metadata is stored in:

```text
releases.json
```

The manifest contains:

```json
{
  "current": "v0.2.0"
}
```

which identifies the runtime release BiodiverseR should use by default.

### Platform Metadata

Each release contains platform-specific entries.

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

## Manifest Compatibility

The release manifest currently retains the legacy top-level `url` and
`sha256` fields for backward compatibility with previously released
versions of BiodiverseR.

Older versions expect:

```json
{
  "url": "...",
  "sha256": "..."
}
```

Newer versions use platform-specific metadata:

```json
{
  "windows": { ... },
  "macos": { ... },
  "linux": { ... }
}
```

The BiodiverseR runtime metadata loader supports both formats.

## Runtime Package Naming

Runtime packages should use the following naming convention:

```text
BiodiverseR___.zip
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

The version component must exactly match the Git tag used to create the
release.

## CI Artifacts vs Release Assets

CI artifacts and release assets serve different purposes.

### CI Artifacts

Generated during normal CI runs.

Example:

```text
BiodiverseR_macos_arm64_d2ddf75
```

CI artifacts are identified using the source commit SHA and are intended
for development, testing and traceability.

### Release Assets

Generated from version tags.

Example:

```text
BiodiverseR_macos_arm64_v0.2.0.zip
```

Release assets are intended for distribution and installation by
BiodiverseR users.

## Future Automation

The release workflow currently:

1. Builds runtime packages.
2. Creates GitHub Releases.
3. Uploads release assets.

Planned future enhancements include:

1. Automatic SHA-256 generation.
2. Automatic updates to `releases.json`.
3. Expanded multi-platform release automation.
4. Additional runtime validation and release checks.

## Current Status

- Windows runtime build: complete
- macOS ARM64 runtime build: complete
- macOS x86_64 runtime build: planned
- Linux runtime build: in progress
- Automated macOS release workflow: complete
- Automated `releases.json` updates: planned

