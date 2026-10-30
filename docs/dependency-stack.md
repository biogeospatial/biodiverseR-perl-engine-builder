# Dependency Stack

This document describes the major dependencies used to build and package BiodiverseR runtimes.

It is intended to help maintainers understand:

- Runtime build requirements.
- Platform-specific dependency differences.
- Build-time and runtime dependency relationships.
- Areas that are frequently involved in build failures.

## Overview

The BiodiverseR runtime depends on a number of upstream projects and Perl
modules.

At a high level:

```text
BiodiverseR Runtime
        ↓
    Biodiverse
        ↓
 Geo::GDAL::FFI
        ↓
 Alien libraries
        ↓
 GDAL / PROJ / GEOS
        ↓
 System libraries
```

## Runtime Dependency Releases

Runtime build workflows resolve their Perl distribution and dependencies
from the upstream `biodiverse-runtime-dependencies` repository's
`releases.json`. The selected channel points to a release, whose
platform-specific URL and SHA-256 checksum identify the archive.

The default channel is `development`, which is currently the only
populated channel. The Windows, macOS and Linux manual CI workflows allow
selecting `development`, `testing` or `stable`; a channel without a
published release or platform artifact fails with a clear error.

Downloaded archives are checksum-verified before extraction. On Windows,
the Strawberry Perl distribution is loaded from the archive's `perl`
directory. If an archive includes Carton-managed libraries under
`local/lib/perl5`, the platform workflow adds both that directory and its
architecture-specific subdirectory to `PERL5LIB`.

The upstream metadata is available at:

```text
https://raw.githubusercontent.com/biogeospatial/biodiverse-runtime-dependencies/main/releases.json
```

## Windows

### Major Components

```text
Strawberry Perl
PDL
GDAL
PROJ
GEOS
Geo::GDAL::FFI
Biodiverse dependencies
```

## macOS

The macOS workflow extracts the selected prebuilt Perl distribution and
its bundled dependencies instead of building Perl with perlbrew.

### System Dependencies

Installed using:

```bash
brew install gsl
brew install sqlite
brew install gdal
```

### Major Components

```text
Perl
PDL
Geo::GDAL::FFI
Alien::gdal
Alien::proj
Alien::geos::af
GDAL
PROJ
GEOS
```

## Linux

The Linux validation workflow downloads and uses the selected prebuilt
Perl distribution and verifies the bundled PDL modules.

### Status

Linux runtime support is currently under development.

The final dependency stack may differ from Windows and macOS.

### Expected Major Components

```text
Perl
PDL
Geo::GDAL::FFI
Alien::gdal
Alien::proj
Alien::geos::af
GDAL
PROJ
GEOS
```

## Geo::GDAL::FFI Stack

### Purpose

```text
Geo::GDAL::FFI
```

provides access to GDAL functionality used by Biodiverse.

### Dependency Chain

```text
Geo::GDAL::FFI
    ↓
Alien::gdal
    ↓
Alien::proj
    ↓
Alien::geos::af
    ↓
GDAL
PROJ
GEOS
```

### Build Characteristics

The stack is bundled in the upstream platform archives instead of being
rebuilt during every runtime packaging workflow. Its dependency baseline
is maintained in `biodiverse-runtime-dependencies`.

## PAR::Packer

### Purpose

```text
PAR::Packer
```

creates standalone runtime executables.

Examples:

```text
BiodiverseR.exe
BiodiverseR
```

The runtime executable distributed through GitHub Releases is generated
using PAR::Packer.

## PDL

### Purpose

```text
PDL
```

(Perl Data Language) provides numerical and scientific computing
capabilities required by Biodiverse.

### Additional Component

```text
PDL::GSL::CDF
```

is included in the prebuilt runtime dependency archive selected by the
release channel.

## Runtime Build Dependencies

The runtime build process currently depends on:

```text
Perl
PDL
PAR::Packer
Geo::GDAL::FFI
Biodiverse
BiodiverseR
```

### Build Sequence

```text
Resolve runtime dependency channel
        ↓
Download and verify platform archive
        ↓
Extract prebuilt Perl and dependencies
        ↓
Install Biodiverse dependencies
        ↓
Run Biodiverse tests
        ↓
Install BiodiverseR dependencies
        ↓
Run BiodiverseR tests
        ↓
Build runtime executable
```

Perl versions and dependency archive URLs are defined by the selected
release channel in the upstream release manifest.

## Related Documents

```text
docs/runtime-architecture.md
docs/release-process.md
docs/troubleshooting.md
docs/adr/
```
