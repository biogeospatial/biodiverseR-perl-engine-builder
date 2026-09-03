# BiodiverseR Runtime Releases

This repository hosts runtime packages and release metadata used by BiodiverseR.

The repository currently distributes Windows runtimes and is designed to support additional platforms in future releases. BiodiverseR uses the release manifest maintained in this repository to discover, download, verify and install the appropriate runtime version for the user's platform.

Most users will never need to interact with this repository directly. Instead, BiodiverseR automatically downloads, verifies, installs and manages the required runtime when needed.

## Purpose

BiodiverseR relies on a local server process that provides access to Biodiverse functionality through an HTTP API.

To simplify installation, pre-built runtime packages are distributed through this repository. BiodiverseR automatically:

1. Checks the release manifest for the latest available runtime version.
2. Downloads the corresponding release package from GitHub.
3. Verifies the package using a SHA-256 checksum.
4. Installs the runtime into a per-version cache location.
5. Launches the runtime when required.

This removes the need for end users to install Perl or build Biodiverse from source.

## Runtime Behaviour

The runtime supports multiple concurrent server instances. BiodiverseR typically starts the server on an automatically selected available port, allowing multiple R sessions to run independently on the same machine.

## Release Manifest

The repository root contains a JSON manifest describing available runtime releases.

Example:

```json
{
  "current": "v0.1.0-alpha",
  "releases": {
    "v0.1.0-alpha": {
      "url": "https://github.com/biogeospatial/biodiverseR-perl-engine-builder/releases/download/v0.1.0-alpha/BiodiverseR_win_aaf20ba.zip",
      "sha256": "c4c95ce7f60de5aef0f425579d38b845752db91ff8009c061247a431413ab54a"
    }
  }
}
```

### Manifest Fields

#### `current`

The version BiodiverseR should treat as the default runtime.

```json
{
  "current": "v0.1.0-alpha"
}
```

#### `releases`

A collection of available runtime versions and their associated metadata.

```json
{
  "releases": {
    "v0.1.0-alpha": {
      ...
    }
  }
}
```

#### `url`

The download location of the release package.

```json
{
  "url": "https://github.com/.../BiodiverseR_win_aaf20ba.zip"
}
```

#### `sha256`

The SHA-256 checksum used to verify package integrity before installation.

```json
{
  "sha256": "c4c95ce7f60de5aef0f425579d38b845752db91ff8009c061247a431413ab54a"
}
```

If the downloaded package does not match the published checksum, BiodiverseR will reject the download and abort installation.

## Automatic Installation

When BiodiverseR requires a runtime, it performs the following steps:

1. Read the release manifest.
2. Determine the version specified by the `current` field.
3. Check whether that version is already installed locally.
4. If the runtime is not installed, download the associated release package.
5. Verify the package checksum.
6. Extract the runtime into a version-specific cache directory.
7. Reuse the cached runtime in future sessions.

To avoid race conditions, BiodiverseR uses an installation lock so that only one R session installs a particular runtime version at a time.

## Runtime Installation

BiodiverseR installs runtimes into platform-specific user cache locations.

The exact location depends on the operating system and BiodiverseR version.

Current Windows installations use a location similar to:

```text
%LOCALAPPDATA%\BiodiverseR\runtime\<version>\
```

For example:

```text
C:\Users\username\AppData\Local\BiodiverseR\runtime\v0.1.0-alpha\
```

If `LOCALAPPDATA` is unavailable, BiodiverseR falls back to:

```text
%APPDATA%
```

## Runtime Package Requirements

Each runtime package must:

- Contain the server runtime for the target platform.
- Include all required runtime dependencies.
- Be downloadable from the URL listed in the release manifest.
- Match the published SHA-256 checksum.

Current Windows releases are distributed as ZIP archives containing the `BiodiverseR.exe` runtime executable.

## Publishing a New Release

When publishing a new runtime release:

1. Build the runtime package.
2. Create a GitHub Release.
3. Upload the package as a release asset.
4. Calculate the SHA-256 checksum of the package.
5. Add a new release entry to the manifest.
6. Update the `current` field if the new release should become the default version.
7. Commit and push the updated manifest.

## Relationship to BiodiverseR

This repository serves as the distribution point for BiodiverseR runtimes.

BiodiverseR uses the release manifest as the authoritative source for:

- The current runtime version.
- Download locations for runtime packages.
- Package integrity verification using SHA-256 checksums.

The runtime is downloaded and managed automatically by BiodiverseR and normally requires no user intervention.

## License

See the repository license file for licensing information.
