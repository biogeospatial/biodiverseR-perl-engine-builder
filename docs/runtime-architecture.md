# Runtime Architecture

## Overview

This repository builds and publishes runtime packages used by
BiodiverseR.

The runtime allows BiodiverseR users to access Biodiverse functionality
from R without needing to install Perl, Biodiverse, or the associated
dependency stack manually.

BiodiverseR communicates with the runtime through a local HTTP API.
The runtime starts a local Biodiverse server process and BiodiverseR
uses that server to perform biodiversity analyses from within R.

Runtime packages are built, tested, packaged, published and later
downloaded automatically by BiodiverseR when required.

## Repository Relationships

The runtime ecosystem currently consists of four primary repositories:

```text
Biodiverse
BiodiverseR
biodiverse-runtime-dependencies
biodiverseR-perl-engine-builder
```

### Biodiverse

Provides the underlying biodiversity analysis functionality.

### BiodiverseR

Provides the R interface used by end users.

### biodiverse-runtime-dependencies

Builds and publishes pre-built Perl runtime dependency archives for
Windows, macOS and Linux. Its `releases.json` manifest maps release
channels to platform-specific download URLs and SHA-256 checksums.

### biodiverseR-perl-engine-builder

Downloads and verifies the selected platform archive, then builds, tests,
packages and publishes the BiodiverseR runtime.

## Runtime Lifecycle

The high-level runtime lifecycle is:

```text
Runtime dependency release
    ↓
Upstream releases.json
    ↓
Select channel and platform
    ↓
Download and verify Perl runtime
    ↓
Build and package BiodiverseR runtime
    ↓
Builder GitHub Release and releases.json
    ↓
BiodiverseR
    ↓
R User
```

## Runtime Execution Model

Runtime execution follows the model:

```text
R User
    ↓
BiodiverseR
    ↓
Local HTTP API
    ↓
Runtime
    ↓
Biodiverse
```

The runtime acts as a bridge between R and Biodiverse.

This architecture allows BiodiverseR to provide Biodiverse functionality
without requiring users to install Perl or Biodiverse directly.

## Runtime Distribution

Published runtime archives are described in:

```text
releases.json
```

BiodiverseR uses this manifest to locate the correct runtime for the
current platform.

The builder's Perl runtime inputs are selected separately from the
upstream `biodiverse-runtime-dependencies` `releases.json` manifest.

## Runtime Selection

BiodiverseR follows the model:

```text
Runtime available?
    Yes -> Use packaged runtime
    No  -> Use bundled Perl script
```

This allows packaged runtimes to be introduced incrementally for
different platforms without changing runtime startup logic.

## Supported Platforms

Current platform identifiers are:

```text
windows
macos
linux
```

Each runtime release may contain platform-specific runtime packages.

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

## Runtime Configuration

Runtime build configuration is managed through:

```text
.github/runtime-config.yml
```

Configuration is divided into:

```text
globals
```

Shared settings used across all platforms.

Examples:

- Biodiverse branch
- BiodiverseR branch
- Runtime test configuration

and:

```text
platforms
```

Platform-specific configuration.

Examples:

- Perl version
- Build environment settings
- Platform-specific paths

## Build Workflows

### windows.yml

Builds and validates the Windows runtime.

### macos-runtime.yml

Reusable workflow that:

- Builds the macOS runtime.
- Runs runtime validation tests.
- Packages runtime artifacts.
- Supports CI and release builds.

### macos-ci.yml

Invokes the reusable macOS workflow for:

- Pull requests
- Manual workflow runs

### releases.yml

Triggers on Git tags and invokes runtime build
