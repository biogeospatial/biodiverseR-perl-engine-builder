# ADR-0009: Separate Runtime Release Publication from Promotion

## Status

Proposed

## Context

Runtime releases are distributed using release metadata stored in `releases.json`.

The metadata currently contains:

- A list of available runtime releases.
- The current default runtime release.
- Platform-specific download URLs and checksums.

New runtime releases may require validation before being recommended as the default runtime for all users.

Examples include:

- Testing a newly built runtime release.
- Verifying runtime installation behaviour.
- Validating startup and integration tests.
- Evaluating platform-specific dependency changes.
- Investigating runtime issues before general adoption.

Automatically promoting newly published runtime releases to the default version would tightly couple release publication with runtime adoption and increase the risk of exposing users to unvalidated runtime changes.

## Decision

Publishing a runtime release and promoting a runtime release are separate actions.

Publishing a runtime release will:

```text
Create release
    ↓
Add release metadata to releases.json
```

Promoting a runtime release will:

```text
Update current in releases.json
```

A newly published release will be added to the list of available releases but will not automatically become the default runtime.

Example:

```json
{
  "current": "v1.0.0",
  "releases": {
    "v1.0.0": {},
    "v1.1.0": {}
  }
}
```

In this example:

- `v1.1.0` is available for testing.
- `v1.0.0` remains the default runtime.
- Promotion to `v1.1.0` occurs only after validation.

Runtime selection for testing will be performed using environment variable overrides that allow alternative runtime releases to be selected without modifying committed configuration files.

Example:

```text
Current release: v1.0.0
Test release:    v1.1.0

Set environment variable
    ↓
Test v1.1.0
    ↓
Remove environment variable
    ↓
Revert to v1.0.0
```

Promotion of a release to the current default version remains a separate action. Runtime releases can be validated prior to promotion using environment variable overrides.

## Rationale

Separating publication from promotion:

- Reduces risk when introducing new runtime releases.
- Supports testing and validation before adoption.
- Allows multiple runtime releases to coexist.
- Provides a clear rollback path.
- Aligns runtime management with staged release practices.
- Supports development and testing workflows without modifying the default runtime version.
- Supports testing of non-default runtime versions using environment variable overrides.
- Avoids temporary changes to committed configuration files during validation.

The preferred workflow is:

```text
Create runtime release
    ↓
Add release metadata
    ↓
Set environment variable override
    ↓
Validate runtime
    ↓
Promote release
```

rather than:

```text
Create runtime release
    ↓
Automatically become current
```

## Consequences

### Positive

- New releases can be tested before becoming the default runtime.
- Runtime publication and runtime adoption are independently controlled.
- Reduces the impact of release regressions.
- Simplifies rollback to a previously validated release.
- Supports parallel validation of multiple runtime releases.
- Improves confidence in runtime promotion decisions.
- Allows testing without modifying repository configuration.

### Negative

- Promoting a runtime becomes a separate maintenance action.
- Additional metadata updates may be required.
- Release management becomes a two-step process.

### Neutral

- All runtime releases remain available through `releases.json`.
- Existing runtime metadata structures remain valid.
- Runtime packaging and release workflows are unaffected.

## Alternatives Considered

### Option 1: Automatically promote newly published releases

#### Pros

- Simpler workflow.
- Fewer maintenance steps.

#### Cons

- Increased risk of exposing users to unvalidated releases.
- No opportunity for staged validation.
- More difficult rollback process.

### Option 2: Separate publication from promotion

#### Pros

- Supports release validation before adoption.
- Allows safe testing of new runtime releases.
- Provides clear promotion and rollback workflows.
- Enables environment variable based runtime selection for testing.

#### Cons

- Requires an explicit promotion step.

## Related

- ADR-0006: Use Tag Triggered Runtime Releases
- ADR-0007: Use Platform-Specific Runtime Release Metadata
- ADR-0008: Use a Shared Cross-Platform Runtime Dependency Repository
- Issue #13: Add Runtime Release Workflow
- Issue #19: Investigate Portable Runtime Strategy for macOS and Linux
