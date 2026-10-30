import tempfile
import unittest
from pathlib import Path

from scripts.configure_perl_runtime import runtime_perl_library_paths


class RuntimePerlLibraryPathsTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.runtime_root = Path(self.temporary_directory.name)
        self.perl_root = self.runtime_root / "perl" / "perl-5.38.4"
        self.arch_name = "darwin-2level"

        config_directory = (
            self.perl_root / "lib" / "5.38.4" / self.arch_name
        )
        config_directory.mkdir(parents=True)
        (config_directory / "Config.pm").touch()
        (config_directory / "Config_heavy.pl").touch()

    def test_includes_core_site_and_carton_library_directories(self):
        site_version = self.perl_root / "lib" / "site_perl" / "5.38.4"
        (site_version / self.arch_name).mkdir(parents=True)
        local_lib = self.runtime_root / "local" / "lib" / "perl5"
        (local_lib / self.arch_name).mkdir(parents=True)

        paths = runtime_perl_library_paths(self.perl_root, self.runtime_root)

        self.assertEqual(
            paths,
            [
                self.perl_root / "lib" / "5.38.4" / self.arch_name,
                self.perl_root / "lib" / "5.38.4",
                site_version / self.arch_name,
                site_version,
                local_lib,
                local_lib / self.arch_name,
            ],
        )

    def test_allows_missing_optional_site_and_carton_directories(self):
        paths = runtime_perl_library_paths(self.perl_root, self.runtime_root)

        self.assertEqual(
            paths,
            [
                self.perl_root / "lib" / "5.38.4" / self.arch_name,
                self.perl_root / "lib" / "5.38.4",
            ],
        )

    def test_rejects_archive_without_perl_config(self):
        (self.perl_root / "lib" / "5.38.4" / self.arch_name / "Config.pm").unlink()

        with self.assertRaisesRegex(ValueError, "Expected exactly one Perl Config.pm"):
            runtime_perl_library_paths(self.perl_root, self.runtime_root)


if __name__ == "__main__":
    unittest.main()
