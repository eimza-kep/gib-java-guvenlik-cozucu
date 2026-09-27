import unittest
import tempfile
import shutil
from pathlib import Path
from java_security import apply_sites, load_existing_sites, remove_site, OFFICIAL_SITES

class TestJavaSecurity(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_apply_sites_initial(self):
        added, total = apply_sites(target_dir=self.test_dir)
        self.assertEqual(added, len(OFFICIAL_SITES))
        self.assertEqual(total, len(OFFICIAL_SITES))

        exc_file = Path(self.test_dir) / "exception.sites"
        self.assertTrue(exc_file.exists())
        loaded = load_existing_sites(exc_file)
        self.assertEqual(len(loaded), len(OFFICIAL_SITES))

    def test_apply_sites_idempotent(self):
        apply_sites(target_dir=self.test_dir)
        # Running again should add 0 new sites
        added, total = apply_sites(target_dir=self.test_dir)
        self.assertEqual(added, 0)
        self.assertEqual(total, len(OFFICIAL_SITES))

    def test_custom_site_and_remove(self):
        custom = ["https://custom-portal.gov.tr"]
        added, total = apply_sites(target_dir=self.test_dir, custom_sites=custom)
        self.assertEqual(total, len(OFFICIAL_SITES) + 1)
        
        # Test removal
        rem, remaining = remove_site(self.test_dir, "https://custom-portal.gov.tr")
        self.assertEqual(rem, 1)
        self.assertEqual(remaining, len(OFFICIAL_SITES))

if __name__ == "__main__":
    unittest.main()
