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

## Windows

### Perl

```text
Strawberry Perl 5.38.4.1
```

Windows runtime builds currently use the same Perl version as the
Biodiverse GUI dependency stack.

See:

```text
ADR-0002: Platform-Specific Perl Versions
```

### Runtime Source

The Windows workflow downloads a pre-built portable runtime from:

```text
biodiverse-sp-portable
```

This portable runtime contains the majority of the required dependency
stack and avoids rebuilding large geospatial dependencies on every CI
run.

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

### Perl

```text
Perl 5.38.4
```

Installed using:

```text
perlbrew
```

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

### Build Environment

The macOS build relies on:

```text
PKG_CONFIG_PATH
CMAKE_PREFIX_PATH
CPPFLAGS
CFLAGS
CXXFLAGS
```

to ensure GDAL and related dependencies can locate Homebrew headers and
libraries.

### Known Issues

Historically, the following have caused build failures:

```text
Alien::gdal
Geo::GDAL::FFI
OpenEXR
Imath
```

Particularly:

```text
Imath/half.h not found
```

which was resolved by explicitly providing Homebrew include paths during
the build.

## Linux

### Perl

```text
Perl 5.38.4
```

(Current target version.)

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

This dependency stack is one of the longest-running parts of the macOS
build process and can dominate overall workflow execution time.

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

is currently installed as part of the runtime build process.

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
Install Perl
        ↓
Install PDL
        ↓
Install Geo::GDAL::FFI
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

## Platform-Specific Versions

Platform-specific versions are permitted where required for build
stability or compatibility.

The current configuration is defined in:

```text
.github/runtime-config.yml
```

See:

```text
ADR-0002: Platform-Specific Perl Versions
```

for the rationale.

## Related Documents

```text
docs/runtime-architecture.md
docs/release-process.md
docs/troubleshooting.md
docs/adr/
```

