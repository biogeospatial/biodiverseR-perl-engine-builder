# releases.json Schema

This document defines the structure and semantics of the runtime dependency metadata file.

The metadata file is the authoritative source of information about:

- Runtime dependency release channels.
- Available runtime dependency releases.
- Platform-specific artifacts.
- Artifact verification checksums.

See ADR-0004 and ADR-0008 for the architectural decisions behind this design.

## Overview

Runtime dependency metadata is stored in:

```text
releases.json
```

Example:

```json
{
  "channels": {
    "stable": "v1.0.0",
    "testing": "v1.1.0",
    "development": "v1.2.0"
  },

  "releases": {
    "v1.0.0": {
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

## Top-Level Structure

The metadata file contains two top-level sections:

```json
{
  "channels": {},
  "releases": {}
}
```

### channels

Maps channel names to release versions.

Example:

```json
{
  "channels": {
    "stable": "v1.0.0",
    "testing": "v1.1.0",
    "development": "v1.2.0"
  }
}
```

### releases

Stores metadata for each published release.

Example:

```json
{
  "releases": {
    "v1.0.0": {}
  }
}
```

Release keys must match the Git tag used to create the release.

## Channels

Channels provide stable references to release versions.

Current channels:

```text
stable
testing
development
```

### stable

The recommended release for general use.

Example:

```json
{
  "stable": "v1.0.0"
}
```

### testing

A release undergoing validation prior to promotion.

Example:

```json
{
  "testing": "v1.1.0"
}
```

### development

A release intended for active development and experimentation.

Example:

```json
{
  "development": "v1.2.0"
}
```

## Release Entries

Each release entry contains platform-specific artifact metadata.

Example:

```json
{
  "v1.0.0": {
    "windows": {},
    "macos": {},
    "linux": {}
  }
}
```

The release identifier must exactly match the associated Git tag.

Example:

```text
Git tag: v1.0.0

Release entry:
"v1.0.0"
```

## Platform Metadata

Each platform entry contains:

```json
{
  "url": "...",
  "sha256": "..."
}
```

### url

The download URL for the runtime dependency artifact.

Example:

```json
{
  "url": "https://github.com/org/repo/releases/download/v1.0.0/artifact.zip"
}
```

### sha256

SHA256 checksum used to verify artifact integrity.

Example:

```json
{
  "sha256": "f2617270e45914f0951afd5e3ae66515f6e234f372dee77b61abb231df59eac1"
}
```

## Supported Platforms

Current platform identifiers:

```text
windows
macos
linux
```

Example:

```json
{
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
```

## Resolution Process

Consumers resolve runtime dependency releases using metadata.

Example:

```text
Channel
    ↓
Release
    ↓
Platform
    ↓
Artifact
```

For example:

```text
stable
    ↓
v1.0.0
    ↓
macos
    ↓
download URL
```

## Release Lifecycle

Publishing a release adds metadata to the `releases` section.

Example:

```text
Create release
    ↓
Update releases.json
```

Promotion updates a channel reference.

Example:

Before:

```json
{
  "channels": {
    "stable": "v1.0.0",
    "testing": "v1.1.0"
  }
}
```

After:

```json
{
  "channels": {
    "stable": "v1.1.0",
    "testing": "v1.1.0"
  }
}
```

No release is modified during promotion.

Only channel assignments change.

## Validation Rules

Release metadata must satisfy the following rules:

### Rule 1

Every channel must reference an existing release.

Valid:

```json
{
  "channels": {
    "stable": "v1.0.0"
  },
  "releases": {
    "v1.0.0": {}
  }
}
```

Invalid:

```json
{
  "channels": {
    "stable": "v1.0.0"
  },
  "releases": {}
}
```

### Rule 2

Every release identifier must correspond to a published Git tag.

Example:

```text
v1.0.0
```

### Rule 3

Every published artifact should provide:

```json
{
  "url": "...",
  "sha256": "..."
}
```

### Rule 4

Consumers should ignore unknown fields.

This allows the schema to evolve without breaking compatibility.

Example:

```json
{
  "released": "2026-10-10",
  "notes": "Initial release"
}
```

## Future Schema Extensions

Future releases may introduce additional fields.

Potential examples include:

```json
{
  "released": "2026-10-10"
}
```

```json
{
  "notes": "GDAL upgrade"
}
```

```json
{
  "supported_platforms": []
}
```

```json
{
  "minimum_runtime_version": "1.0.0"
}
```

Consumers should ignore unrecognised fields.

## Example Complete Metadata File

```json
{
  "channels": {
    "stable": "v1.0.0",
    "testing": "v1.1.0",
    "development": "v1.2.0"
  },

  "releases": {
    "v1.0.0": {
      "windows": {
        "url": "https://example/windows.zip",
        "sha256": "..."
      },

      "macos": {
        "url": "https://example/macos.zip",
        "sha256": "..."
      },

      "linux": {
        "url": "https://example/linux.zip",
        "sha256": "..."
      }
    }
  }
}
```
