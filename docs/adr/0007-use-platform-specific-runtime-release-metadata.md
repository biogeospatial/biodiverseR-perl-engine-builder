# ADR-0007: Use Platform-Specific Runtime Release Metadata

Status: Accepted

## Context

The BiodiverseR runtime project distributes pre-built runtime packages
through GitHub Releases.

The initial release manifest structure assumed a single runtime package
per release version.

Example:

```json
{
  "current": "v0.1.0-alpha",
  "releases": {
    "v0.1.0-alpha": {
      "url": "...",
      "sha256": "..."
    }
  }
}
```

As support expands to multiple operating systems, a release version may
contain multiple runtime packages, each with different download URLs and
checksums.

Examples include:

- Windows
- macOS ARM64
- Linux

Future releases may also include:

- macOS x86_64
- macOS universal
- Additional platform-specific variants

A release manifest structure is required that can represent multiple
runtime artifacts for a single release version.

## Decision

Use platform-specific metadata within each runtime release entry.

The release manifest structure shall be:

```json
{
  "current": "v0.2.0",
  "releases": {
    "v0.2.0": {
      "windows": {
        "url": "...",
        "sha256": "..."
      },
      "macos-arm64": {
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

The `current` field identifies the default runtime release version.

Platform-specific download information is stored under the corresponding
release version.

## Rationale

A platform-specific structure allows a single runtime release version to
contain multiple runtime artifacts.

This approach:

- Supports multiple operating systems.
- Supports future platform variants.
- Keeps release metadata grouped by release version.
- Allows independent checksums and download URLs for each platform.
- Avoids future changes to the manifest schema as additional platforms
  are added.

## Consequences

### Positive

- Supports multiple runtime artifacts per release.
- Scales to additional operating systems.
- Scales to additional architecture-specific builds.
- Keeps release metadata organised by version.
- Allows release automation to update metadata incrementally.

### Negative

- Release manifest structure becomes more complex.
- Runtime installation code must select the correct platform entry.

## Alternatives Considered

### Single artifact per release

Rejected.

This structure does not support multiple runtime packages associated
with the same release version.

### Separate manifest per platform

Rejected.

This increases maintenance effort and duplicates release information.

### Platform-first structure

Example:

```json
{
  "windows": {
    "current": "v0.2.0"
  },
  "macos-arm64": {
    "current": "v0.2.0"
  }
}
```

Rejected.

This makes it more difficult to understand which runtime artifacts belong
to the same release version.

## Related Decisions

- Runtime build configuration is managed through
  `.github/runtime-config.yml`.
- Runtime releases are triggered by Git tags.
- Platform-specific runtime settings may be used where required by
  platform tooling or compatibility constraints.
