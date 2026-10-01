# ADR-0005: Prioritise macOS ARM64 Runtime Support

Status: Accepted

## Context

The BiodiverseR runtime project aims to provide runtime support for
macOS.

An initial goal was to investigate support for both Apple Silicon
(ARM64) and older Intel (x86_64) macOS systems. Options considered
included:

- Building separate ARM64 and x86_64 runtimes.
- Building a universal macOS runtime supporting both architectures.
- Supporting ARM64 only initially.

During development, significant effort was required to address
compatibility issues associated with supporting older Intel-based
macOS systems. These issues increased complexity and slowed progress
towards delivering a working macOS runtime.

A decision was needed on whether to continue pursuing universal or Intel
support immediately, or focus on delivering a working runtime for Apple
Silicon systems first.

## Decision

Prioritise support for Apple Silicon (ARM64) macOS systems.

The runtime build process will initially target ARM64 only.

Support for Intel (x86_64) macOS systems and the possibility of a
universal macOS runtime will be evaluated in the future as separate
work.

## Rationale

Delivering a working runtime for Apple Silicon users provides immediate
value while reducing implementation complexity.

Attempting to solve ARM64 and Intel compatibility issues
simultaneously would delay delivery of macOS runtime support and
increase maintenance effort.

A phased approach allows:

- A working macOS runtime to be released sooner.
- Runtime installation and startup workflows to be validated.
- Release and distribution processes to be established.
- Future Intel or universal runtime support to be explored
  independently.

## Consequences

### Positive

- macOS runtime support can be delivered sooner.
- CI workflows are simpler.
- Runtime packaging and testing are less complex.
- Effort can be focused on a single supported architecture.

### Negative

- Older Intel-based Macs are not currently supported.
- Some users will be unable to use the runtime until Intel support is
  added.
- Additional work may be required in the future to support Intel or
  universal runtime builds.

## Alternatives Considered

### Support ARM64 and Intel simultaneously

Rejected.

Compatibility issues increased development effort and delayed delivery
of a working macOS runtime.

### Create a universal runtime immediately

Rejected.

The additional complexity was not justified for the initial release of
macOS runtime support.

### Support Intel only

Rejected.

Apple Silicon is the primary target platform and the development
environment used for runtime testing.

## Future Considerations

Future work may investigate:

- Dedicated Intel (x86_64) macOS runtime builds.
- Universal macOS runtime builds.
- Automated testing across multiple macOS architectures.

No decision has been made at this time regarding whether future macOS
runtime releases will use separate architecture-specific builds or a
universal runtime.

## Related Decisions

- Runtime build configuration is managed through
  `.github/runtime-config.yml`.
- Runtime installation and startup are validated through end-to-end CI
  testing.
- Runtime release artifacts are distributed separately from CI
  artifacts.
