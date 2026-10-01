# ADR-0004: Use yq for Runtime Configuration

Status: Accepted

## Context

The BiodiverseR runtime build workflows load configuration values from
`.github/runtime-config.yml`.

A mechanism is required to read configuration values from YAML and make
them available to GitHub Actions workflows.

Several approaches were considered, including embedding configuration
directly in workflows, using Python with PyYAML, and using a dedicated
YAML processing tool.

## Decision

Use `yq` to read values from `.github/runtime-config.yml` and export
them to the GitHub Actions environment.

Example:

```bash
echo "PERL_VERSION=$(yq -r '.perl_version' .github/runtime-config.yml)" >> "$GITHUB_ENV"
```

Runtime build workflows shall use `yq` when loading configuration from
`runtime-config.yml`.

## Rationale

`yq` is designed specifically for querying and processing YAML files.

Using `yq` provides:

- A simple and readable workflow implementation.
- Native support for YAML.
- No requirement for custom parsing logic.
- No dependency on Python packages such as PyYAML.
- Consistent behaviour across runtime build workflows.

The GitHub-hosted runners used for runtime builds already provide
`yq`, allowing workflows to consume runtime configuration without
additional setup.

## Consequences

### Positive

- Removes the need for custom Python scripts.
- Eliminates dependency on PyYAML.
- Reduces workflow complexity.
- Keeps runtime configuration logic concise and easy to understand.
- Works naturally with YAML-based configuration files.

### Negative

- Workflows depend on the availability of `yq`.
- Contributors unfamiliar with `yq` may need to learn its query syntax.

## Alternatives Considered

### Store values directly in workflows

Rejected.

This duplicates configuration and works against the goal of using a
shared runtime configuration file.

### Use Python and PyYAML

Rejected.

Although functional, this introduces an unnecessary dependency on
PyYAML and requires more code to perform simple configuration lookups.

### Use shell parsing tools

Rejected.

YAML is more complex than line-oriented configuration formats and is
not reliably parsed using tools such as `grep`, `awk`, or `sed`.

## Related Decisions

- Runtime build configuration is managed through
  `.github/runtime-config.yml`.
- Runtime installation and startup are validated through end-to-end CI
  testing.
- Platform-specific runtime settings may be used where required by
  platform tooling or compatibility constraints.
