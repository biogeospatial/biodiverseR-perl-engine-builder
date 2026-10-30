import unittest

from scripts.resolve_runtime_dependency import resolve_runtime_dependency


class ResolveRuntimeDependencyTests(unittest.TestCase):
    def setUp(self):
        self.manifest = {
            "channels": {
                "stable": "v1.0.0",
                "testing": "v1.1.0",
                "development": "v1.2.0",
            },
            "releases": {
                "v1.0.0": self.release(),
                "v1.1.0": self.release(),
                "v1.2.0": self.release(),
            },
        }

    @staticmethod
    def release():
        return {
            platform: {
                "url": f"https://github.com/example/runtime/{platform}.zip",
                "sha256": "a" * 64,
            }
            for platform in ("windows", "macos", "linux")
        }

    def test_resolves_each_channel_and_platform(self):
        for channel, version in (
            ("stable", "v1.0.0"),
            ("testing", "v1.1.0"),
            ("development", "v1.2.0"),
        ):
            for platform in ("windows", "macos", "linux"):
                with self.subTest(channel=channel, platform=platform):
                    result = resolve_runtime_dependency(
                        self.manifest, channel, platform
                    )

                    self.assertEqual(result["version"], version)
                    self.assertEqual(
                        result["url"],
                        f"https://github.com/example/runtime/{platform}.zip",
                    )
                    self.assertEqual(result["sha256"], "a" * 64)

    def test_rejects_empty_channel(self):
        self.manifest["channels"]["stable"] = ""

        with self.assertRaisesRegex(ValueError, "does not reference a release"):
            resolve_runtime_dependency(self.manifest, "stable", "windows")

    def test_rejects_unsupported_channel(self):
        with self.assertRaisesRegex(ValueError, "Unsupported runtime dependency channel"):
            resolve_runtime_dependency(self.manifest, "preview", "windows")

    def test_rejects_missing_release(self):
        self.manifest["channels"]["stable"] = "v9.9.9"

        with self.assertRaisesRegex(ValueError, "references missing release"):
            resolve_runtime_dependency(self.manifest, "stable", "windows")

    def test_rejects_missing_platform(self):
        del self.manifest["releases"]["v1.0.0"]["macos"]

        with self.assertRaisesRegex(ValueError, "no 'macos' artifact metadata"):
            resolve_runtime_dependency(self.manifest, "stable", "macos")

    def test_rejects_invalid_url_or_checksum(self):
        artifact = self.manifest["releases"]["v1.0.0"]["windows"]
        artifact["url"] = "http://example.com/runtime.zip"

        with self.assertRaisesRegex(ValueError, "invalid HTTPS download URL"):
            resolve_runtime_dependency(self.manifest, "stable", "windows")

        artifact["url"] = "https://example.com/runtime.zip"
        artifact["sha256"] = "not-a-checksum"
        with self.assertRaisesRegex(ValueError, "invalid SHA-256 checksum"):
            resolve_runtime_dependency(self.manifest, "stable", "windows")


if __name__ == "__main__":
    unittest.main()
