# BiodiverseR Runtime Releases

This repository builds, tests, packages and publishes runtime releases
used by BiodiverseR.

The runtime allows BiodiverseR users to access Biodiverse functionality
from R without requiring a separate Perl or Biodiverse installation.

Most users will never interact with this repository directly. Instead,
BiodiverseR automatically downloads, verifies, installs and manages the
appropriate runtime when required.

## Purpose

BiodiverseR communicates with a local runtime process through an HTTP
API.

To simplify installation, pre-built runtime packages are distributed
through this repository.

When required, BiodiverseR automatically:

1. Checks the release manifest for the current runtime version.
2. Determines the runtime package appropriate for the current platform.
3. Downloads the runtime package from GitHub Releases.
4. Verifies the package using a SHA-256 checksum.
5. Installs the runtime into a version-specific cache location.
6. Starts the runtime and establishes communication through the local
   API.

This removes the need for end users to install Perl or build Biodiverse
from source.

## Supported Platforms

Current runtime support includes:

- Windows
- macOS ARM64 (Apple Silicon)

Linux runtime support is under development.

## Documentation

Additional documentation is available in:

- `docs/runtime-architecture.md`
- `docs/release-process.md`
- `docs/troubleshooting.md`
- `docs/glossary.md`
- `docs/dependency-stack.md`
- `docs/adr/`

## Runtime Behaviour

The runtime supports multiple concurrent server instances.

BiodiverseR typically starts the server on an automatically selected
available port, allowing multiple R sessions to run independently on
the same machine.

## Release Manifest

The repository root contains a JSON manifest describing available
runtime releases.

The release workflow maintains this file automatically when new runtime
releases are published.

New releases are added automatically to the manifest, but do not
automatically become the default runtime version.

File:

```text
releases.json
```

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

### Manifest Fields

#### `current`

The runtime version BiodiverseR should use by default.

Publishing a runtime release and promoting a runtime release are separate
actions. New releases are added to the manifest automatically, while the
`current` value is updated independently once a release has been
validated.

Example:

```json
{
  "current": "v0.2.0"
}
```

#### `releases`

A collection of runtime versions and their associated platform metadata.

Example:

```json
{
  "releases": {
    "v0.2.0": {
      "windows": { ... },
      "macos": { ... },
      "linux": { ... }
    }
  }
}
```

#### Platform Entries

Each platform entry contains:

```json
{
  "url": "...",
  "sha256": "..."
}
```

where:

- `url` is the runtime package download location.
- `sha256` is the checksum used to verify package integrity.

Current platform identifiers are:

```text
windows
macos
linux
```

## Manifest Compatibility

The release manifest currently supports both:

### Legacy Format

```json
{
  "url": "...",
  "sha256": "..."
}
```

### Platform-Specific Format

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

New runtime releases should use platform-specific metadata.

Legacy metadata is retained for compatibility with previously released
versions of BiodiverseR.

## Automatic Installation

When BiodiverseR requires a runtime it performs the following steps:

1. Check whether the required runtime version is already installed.
2. Reuse the runtime if it already exists locally.
3. Download the runtime if required.
4. Verify the package checksum.
5. Extract the runtime into a version-specific cache directory.
6. Start the runtime when needed.
7. Reuse the installed runtime for future sessions.

To avoid race conditions, BiodiverseR uses an installation lock so that
only one R session installs a particular runtime version at a time.

## Runtime Installation Locations

Runtimes are installed into platform-specific user cache locations.

Examples include:

### Windows

```text
%LOCALAPPDATA%\BiodiverseR\runtime\\
```

Example:

```text
C:\Users\username\AppData\Local\BiodiverseR\runtime\v0.2.0\
```

### macOS

```text
~/Library/Application Support/BiodiverseR/runtime//
```

## Runtime Package Requirements

Each runtime package must:

- Contain the Biodiverse runtime executable for the target platform.
- Include all required runtime dependencies.
- Be downloadable from the URL defined in the release manifest.
- Match the published SHA-256 checksum.

Typical runtime package names include:

```text
BiodiverseR_windows_x64_v0.2.0.zip
BiodiverseR_macos_arm64_v0.2.0.zip
BiodiverseR_linux_x64_v0.2.0.zip
```

## CI Artifacts vs Release Assets

### CI Artifacts

Generated during development and CI validation.

Examples:

```text
BiodiverseR_win_d2ddf75
BiodiverseR_macos_arm64_d2ddf75
```

CI artifacts are identified using the source commit SHA and are intended
for testing and traceability.

### Release Assets

Generated from version tags.

Examples:

```text
BiodiverseR_windows_x64_v0.2.0.zip
BiodiverseR_macos_arm64_v0.2.0.zip
```

Release assets are intended for distribution and installation by
BiodiverseR users.

## Release Workflow

Runtime releases are created from Git tags.

Example:

```bash
git tag v0.2.0
git push origin v0.2.0
```

The automated release workflow:

1. Builds the runtime.
2. Runs validation tests.
3. Packages the runtime archive.
4. Generates release metadata and SHA256 checksums.
5. Creates or updates the GitHub Release.
6. Uploads runtime release assets.
7. Updates `releases.json`.
8. Commits and publishes metadata updates.

See:

```text
docs/release-process.md
```

for detailed release instructions.

## Relationship to BiodiverseR

This repository serves as the distribution point for BiodiverseR
runtimes.

BiodiverseR uses the release manifest as the authoritative source for:

- The current runtime version.
- Runtime package download locations.
- Runtime package checksum verification.

Runtime installation and management are normally performed
automatically by BiodiverseR and require no user intervention.

## Current Status

- Windows runtime build: complete
- macOS ARM64 runtime build: complete
- Linux runtime build: in progress
- Automated runtime release workflow: complete
- Automated GitHub Release publication: complete
- Automated SHA256 generation: complete
- Automated `releases.json` updates: complete

## License

See the repository license file for licensing information.
