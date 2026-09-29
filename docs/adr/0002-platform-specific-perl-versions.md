# ADR-0002: Platform-Specific Perl Versions

Status: Accepted

## Context

The BiodiverseR runtime builders support multiple operating systems,
including Windows, macOS and Linux.

A decision was needed on whether all platforms should use the same Perl
version or whether platform-specific Perl versions are acceptable.

The Windows runtime currently uses Strawberry Perl 5.38.4.1.

## Decision

Platform-specific Perl versions may be used where required.

The Windows runtime uses Strawberry Perl 5.38.4.1 because it matches
the dependency stack used to build the Biodiverse GUI.

Runtime builders are not required to use identical Perl versions across
all platforms.

## Rationale

The primary objective is compatibility and stability of the runtime build
environment.

Using the same Perl version as the Biodiverse GUI dependency stack on
Windows helps align runtime builds with the existing Biodiverse build
environment and reduces the risk of incompatibilities.

Consistency across platforms is desirable, but compatibility and build
stability take precedence over strict Perl version parity.

## Consequences

### Positive

- Runtime builders can use the most appropriate Perl version for each
  platform.
- Windows runtime builds remain aligned with the Biodiverse GUI build
  environment.
- Platform-specific compatibility issues can be addressed without
  forcing changes on other platforms.

### Negative

- Runtime builders may use different Perl versions.
- Platform-specific build configurations must be documented.
- Shared runtime configuration must support platform-specific settings.

## Alternatives Considered

### Use the same Perl version on all platforms

Rejected.

There is no requirement that runtime builders use identical Perl
versions, and platform-specific compatibility requirements may justify
different versions.

## Related Decisions

- Runtime build configuration is managed through
  `.github/runtime-config.yml`.
- Runtime installation and startup are validated through end-to-end CI
  testing.
