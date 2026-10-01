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

The runtime ecosystem consists of three primary repositories:

```text
Biodiverse
    ↓
BiodiverseR
    ↓
biodiverseR-perl-engine-builder
```

### Biodiverse

Provides the underlying biodiversity analysis functionality.

### BiodiverseR

Provides the R interface used by end users.

BiodiverseR communicates with a local Biodiverse runtime through an
HTTP API and exposes Biodiverse functionality as R objects and methods.

BiodiverseR is responsible for:

- Detecting runtime availability.
- Downloading runtimes.
- Verifying runtime integrity.
- Installing runtimes.
- Starting runtimes.
- Communicating with runtimes.
- Exposing Biodiverse functionality to R users.

### biodiverseR-perl-engine-builder

Builds and publishes platform-specific runtime packages used by
BiodiverseR.

## Runtime Lifecycle

The high-level runtime lifecycle is:

```text
Git Tag
    ↓
Release Workflow
    ↓
Build Runtime
    ↓
Package Runtime
    ↓
GitHub Release
    ↓
releases.json
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

Triggers on Git tags and invokes runtime build workflows to publish
release assets.

### linux-test.yml

Provides Linux validation and testing.

## Runtime Validation

Runtime builds are validated using:

### Runtime Startup Test

Verifies that the packaged runtime executable starts successfully.

### Runtime Installation Test

Verifies that BiodiverseR can:

- Download the runtime.
- Install the runtime.
- Start the runtime.
- Create a `basedata` object.
- Communicate successfully with the runtime.

This provides an end-to-end validation of the user installation path.

## Architecture Decision Records

Important architectural decisions are documented in:

```text
docs/adr/
```

These records describe:

- Why decisions were made.
- Alternatives that were considered.
- Consequences of those decisions.

ADRs should be consulted when modifying runtime architecture,
configuration, release processes, or platform support.

