# ADR-0006: Use Tag-Triggered Runtime Releases

Status: Accepted

## Context

The BiodiverseR runtime project distributes versioned runtime packages
through GitHub Releases.

Runtime releases need to:

- Have a clear and reproducible version identifier.
- Be associated with a specific point in repository history.
- Support automated build and release workflows.
- Be suitable for use by `releases.json`.

A mechanism is required to determine when a runtime release should be
created.

## Decision

Runtime releases shall be triggered by Git tags.

Creating and pushing a version tag initiates the runtime release
workflow.

Example:

```bash
git tag v0.2.0
git push origin v0.2.0
```

Release workflows listen for tags matching:

```yaml
on:
  push:
    tags:
      - 'v*'
```

The tag version becomes the runtime release version and is used when
naming release assets.

Example:

```text
BiodiverseR_windows_x64_v0.2.0.zip
BiodiverseR_macos_arm64_v0.2.0.zip
BiodiverseR_linux_x64_v0.2.0.zip
```

## Rationale

Git tags provide a simple and widely understood mechanism for
identifying release versions.

Using tags:

- Creates a clear association between source code and runtime releases.
- Makes releases reproducible.
- Supports automation of build and publishing workflows.
- Provides a natural source for release version numbers.
- Reduces the risk of manual versioning errors.

## Consequences

### Positive

- Release versions are explicitly defined.
- Runtime releases can be reproduced from a specific repository state.
- Release automation can be driven directly from Git events.
- Release asset versions align naturally with repository tags.
- Simplifies release management.

### Negative

- Releases depend on correct tag creation.
- Mistakenly pushed tags may trigger unwanted release workflows.
- Tag management becomes part of the release process.

## Alternatives Considered

### Manual release creation

Rejected.

This requires additional manual steps and increases the risk of human
error.

### Release branches

Rejected.

Release branches add complexity and do not provide a straightforward
version identifier for runtime assets.

### Workflow dispatch with a manually supplied version

Rejected.

This requires the version number to be entered separately from source
control and risks inconsistencies between code and release artifacts.

## Related Decisions

- Runtime build configuration is managed through
  `.github/runtime-config.yml`.
- Runtime installation and startup are validated through end-to-end CI
  testing.
- CI artifacts are identified using source commit SHAs.
- Release artifacts use version-based naming derived from Git tags.
