# ADR-0008: Use a Shared Cross-Platform Runtime Dependency Repository

## Status

Proposed

## Context

The current macOS runtime workflow builds a large dependency stack during CI, including Perl and geospatial dependencies such as:

- Geo::GDAL::FFI
- Alien::gdal
- Alien::proj
- Alien::geos::af

These dependencies contribute significantly to runtime build duration and increase workflow complexity.

Windows runtime builds already use a pre-built portable Perl environment distributed through a dedicated runtime repository. This avoids rebuilding the dependency stack on every workflow execution and provides a reproducible runtime environment.

Issue #19 investigates whether a similar approach should be adopted for macOS and Linux. 【1-df6f76】

## Decision

A single shared repository will be used to build and distribute runtime dependencies for all supported platforms.

The repository will:

- Build platform-specific runtime dependency stacks for Windows, macOS and Linux.
- Use a single release version stream across all platforms.
- Publish platform-specific runtime dependency artifacts as part of a single release.
- Maintain a single `releases.json` metadata file describing available runtime dependency releases.
- Support runtime dependency version selection using runtime metadata and configuration overrides.

The repository may be named:

```text
biodiverse-runtime-dependencies
```

A tag will trigger builds for all supported platforms:

```text
Tag v1.2.0
    ↓
Build Windows runtime dependencies
    ↓
Build macOS runtime dependencies
    ↓
Build Linux runtime dependencies
    ↓
Create release
    ↓
Update releases.json
```

The `biodiverseR-perl-engine-builder` repository will consume versioned runtime dependency releases rather than building the complete runtime dependency stack during every CI execution.

New runtime dependency releases will be added automatically to `releases.json`, but will not automatically become the current default version.

Promotion of a release to the current default version remains a separate action.

The runtime builder workflows will download and package pre-built runtime dependency releases rather than constructing runtime dependencies from source during every build.

Runtime selection and version management will continue to be controlled through runtime metadata and configuration files.

## Rationale

Building runtime dependencies during every CI run:

- Increases workflow duration.
- Rebuilds the same dependency stack repeatedly.
- Introduces additional opportunities for transient build failures.
- Couples dependency maintenance to runtime packaging workflows.

Using pre-built runtime dependency releases:

- Reduces CI build times.
- Improves reproducibility.
- Allows runtime dependencies to be tested independently.
- Separates runtime maintenance from application packaging.
- Aligns macOS and Linux runtime distribution with the existing Windows approach.
- Provides a single source of truth for runtime dependency releases.
- Simplifies release management by maintaining a single version stream across platforms.

Example workflow:

```text
Create runtime dependency release
    ↓
Add release to releases.json
    ↓
Test using metadata override
    ↓
Promote by updating current
```

## Consequences

### Positive

- Reduced CI build times.
- Improved build reproducibility.
- Runtime environments can be tested independently of packaging workflows.
- Runtime dependency updates become separate from application packaging changes.
- Consistent runtime versioning across platforms.
- Simplified runtime packaging workflows.
- A single runtime dependency version can be referenced across all supported platforms.
- Only one `releases.json` file needs to be maintained.
- Development and testing workflows remain consistent with existing runtime release workflows.

### Negative

- An additional repository requires maintenance.
- Runtime dependency releases become a prerequisite for runtime packaging releases.
- Release coordination becomes more important.
- Additional storage is required for runtime artifacts.
- A platform-specific fix may require a new cross-platform dependency release.

### Neutral

- Runtime metadata remains the mechanism used to select runtime versions.
- Platform-specific runtime build processes may continue to differ internally.
- Existing runtime installation and validation workflows remain applicable.

## Alternatives Considered

### Option 1: Continue building all dependencies during CI

#### Pros

- Simple architecture.
- No additional runtime repository.

#### Cons

- Long CI build times.
- Repeated rebuilding of the same dependency stack.
- Reduced reproducibility.

### Option 2: Build platform-specific portable runtimes within this repository

#### Pros

- Reduced build times.
- Improved reproducibility.

#### Cons

- Additional release management.
- Larger runtime artifacts.
- Runtime dependency maintenance remains coupled to packaging workflows.

### Option 3: Use separate runtime repositories for each platform

Examples:

```text
biodiverse-runtime-windows
biodiverse-runtime-macos
biodiverse-runtime-linux
```

#### Pros

- Platforms can evolve independently.
- Runtime releases can be published separately.

#### Cons

- Multiple version streams must be managed.
- Multiple metadata files must be maintained.
- Runtime packaging workflows must coordinate versions across repositories.
- Additional operational complexity.
- Inconsistent testing and promotion workflows across platforms.

## Related

- Issue #19: Investigate Portable Runtime Strategy for macOS and Linux 【1-df6f76】
- ADR-0002: Platform-Specific Perl Versions
- ADR-0006: Use Tag Triggered Runtime Releases
- ADR-0007: Use Platform-Specific Runtime Release Metadata
