import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.validate_catalog import CATALOG_PATH, discover_artifacts, validate_catalog, validate_zip


class CatalogTest(unittest.TestCase):
    def test_full_catalog_and_hashes(self):
        self.assertEqual([], validate_catalog(check_hashes=True))

    def test_all_legacy_artifacts_are_discovered(self):
        self.assertEqual(15, len(discover_artifacts()))

    def test_catalog_inventory_is_explicit(self):
        catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
        self.assertEqual({"case_count": 10, "artifact_count": 15}, catalog["inventory"])

    def test_zip_rejects_windows_style_parent_traversal(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "unsafe.zip"
            with zipfile.ZipFile(path, "w") as zipped:
                zipped.writestr(r"..\outside.txt", b"unsafe")
            artifact = {
                "archive": {
                    "member_count": 1,
                    "compressed_size_bytes": path.stat().st_size,
                    "uncompressed_size_bytes": 6,
                }
            }
            errors = validate_zip(path, artifact, "fixture")
            self.assertTrue(any("unsafe archive member path" in error for error in errors))

    def test_zip_rejects_windows_drive_path(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "unsafe.zip"
            with zipfile.ZipFile(path, "w") as zipped:
                zipped.writestr(r"C:\outside.txt", b"unsafe")
            artifact = {
                "archive": {
                    "member_count": 1,
                    "compressed_size_bytes": path.stat().st_size,
                    "uncompressed_size_bytes": 6,
                }
            }
            errors = validate_zip(path, artifact, "fixture")
            self.assertTrue(any("unsafe archive member path" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
