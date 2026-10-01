# Troubleshooting

This document captures issues encountered during development and maintenance of the BiodiverseR runtime build and release process.

## Runtime Startup

### Runtime fails to start

#### Symptoms

```text
Failed to connect to 127.0.0.1
```

or

```text
Waiting for server to start
```

followed by startup failure.

#### Checks

Verify that the runtime executable starts manually:

```bash
/path/to/BiodiverseR daemon -l http://127.0.0.1:3001
```

Verify that the runtime responds:

```bash
curl http://127.0.0.1:3001/api\_key
```

#### Possible Causes

- Runtime executable failed during startup.
- Runtime dependencies are missing.
- Runtime port is already in use.
- Runtime installation is incomplete.

---

### Runtime port already in use

#### Symptoms

```text
Address already in use
```

#### Checks

Identify processes using the port:

```bash
lsof -i :3001
```

Terminate stale runtime processes if necessary.

---

## Runtime Installation

### Wrong runtime downloaded

#### Symptoms

Unexpected executable type or startup failures.

#### Checks

Verify:

```json
releases.json
```

contains the correct platform-specific metadata.

Verify that:

```text
windows
macos
linux
```

entries resolve to the expected release asset URLs.

#### Resolution

Check:

```r
get_release_metadata()
```

and ensure platform-specific metadata is being selected correctly.

---

### Runtime executable not found after extraction

#### Symptoms

```text
Downloaded archive does not contain exactly one BiodiverseR
```

#### Checks

Verify archive contents:

```bash
unzip -l runtime.zip
```

Confirm:

```text
BiodiverseR
```

exists within the archive.

Verify executable naming matches the expected platform.

---

### Runtime executable lacks execute permissions

#### Symptoms

```text
Permission denied
```

when starting the runtime.

#### Resolution

Ensure permissions are applied after extraction:

```r
Sys.chmod(executable, mode = "0755")
```

---

## GDAL / Geo::GDAL::FFI

### Imath/half.h not found

#### Symptoms

```text
fatal error: 'Imath/half.h' file not found
```

during:

```text
Alien::gdal
```

or:

```text
Geo::GDAL::FFI
```

installation.

#### Checks

Verify Homebrew packages:

```bash
brew list | grep -E 'gdal|openexr|imath'
```

Locate header:

```bash
find /opt/homebrew -name half.h
```

Expected location:

```text
/opt/homebrew/include/Imath/half.h
```

#### Resolution

Configure the build environment to use Homebrew include paths:

```bash
export PKG_CONFIG_PATH=/opt/homebrew/lib/pkgconfig
export CMAKE_PREFIX_PATH=/opt/homebrew

export CPPFLAGS="-I/opt/homebrew/include"
export CFLAGS="-I/opt/homebrew/include"
export CXXFLAGS="-I/opt/homebrew/include"
```

---

### Geo::GDAL::FFI build is very slow

#### Symptoms

```text
Install Geo::GDAL::FFI
```

takes a significant amount of time.

#### Notes

The majority of build time may be spent building:

```text
Alien::gdal
Alien::proj
Alien::geos::af
Geo::GDAL::FFI
```

This is a performance issue rather than a functional issue.

#### Future Investigation

- Improve dependency caching.
- Investigate prebuilt runtime dependencies.
- Investigate alternatives to rebuilding GDAL-related dependencies on every run.

---

### Intermittent Alien::FFI failures

#### Symptoms

```text
Installing Alien::FFI failed
```

or

```text
Module 'Alien::FFI' is not installed
```

#### Notes

Intermittent failures have been observed on GitHub-hosted macOS runners.

The issue does not appear to be consistently reproducible.

#### Recommended Diagnostics

On failure, capture:

```text
~/.cpanm/work
```

and:

```text
~/.cpanm
```

for inspection.

---

## GitHub Actions

### Perl cache not restored

#### Symptoms

```text
Cache not found for input keys:
perlbrew--macOS
```

#### Checks

Verify cache configuration:

```yaml
key: perlbrew-${{ env.PERL_VERSION }}-${{ runner.os }}
```

Verify cache save step reports:

```text
Cache saved with key:
```

#### Notes

Cache misses do not affect correctness but increase build duration.

---

### Release asset not attached to GitHub Release

#### Symptoms

Tag exists but release asset is missing.

#### Checks

Verify workflow contains:

```yaml
uses: softprops/action-gh-release
```

Verify workflow permissions:

```yaml
permissions:
  contents: write
```

Verify the tag was created after the release publishing workflow changes were merged.

---

## Release Process

### Release exists but runtime asset missing

#### Symptoms

GitHub Release contains only:

```text
Source code (zip)
Source code (tar.gz)
```

#### Possible Causes

- Release asset upload step did not run.
- The workflow was triggered from a tag created before release publishing support existed.
- Release publishing step failed.

#### Checks

Inspect workflow steps:

```text
Package release artifact
Upload release artifact
Upload release asset
```

---

## Useful Commands

### Test runtime API

```bash
curl http://127.0.0.1:3001/api\_key
```

### Check GDAL installation

```bash
gdalinfo --version
```

### Locate Imath headers

```bash
find /opt/homebrew -name half.h
```

### Check active runtime processes

```bash
lsof -i :3001
```

### Verify release tags

```bash
git tag
```

### Publish a test release

```bash
git tag v0.2.0-test
git push origin v0.2.0-test
```

