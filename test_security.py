import unittest
import tempfile
import shutil
from pathlib import Path
from java_security import (
    apply_sites,
    load_existing_sites,
    remove_site,
    normalize_url,
    load_sites_from_file,
    OFFICIAL_SITES,
    PRESETS
)

class TestJavaSecurity(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_normalize_url(self):
        # 1. Protokolsüz domain (https ve http üretmeli)
        res = normalize_url("belediye.gov.tr")
        self.assertEqual(res, ["https://belediye.gov.tr", "http://belediye.gov.tr"])

        # 2. Port bilgisi içeren URL
        res_port = normalize_url("https://intranet.adalet.gov.tr:8443/")
        self.assertEqual(res_port, ["https://intranet.adalet.gov.tr:8443"])

        # 3. Wildcard temizleme
        res_wildcard = normalize_url("*.ankara.bel.tr")
        self.assertEqual(res_wildcard, ["https://ankara.bel.tr", "http://ankara.bel.tr"])

        # 4. Yorum satırı ve boşluk
        self.assertEqual(normalize_url("# yorum"), [])
        self.assertEqual(normalize_url("   "), [])

    def test_load_sites_from_file(self):
        test_file = Path(self.test_dir) / "sites.txt"
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("# Kurumsal Siteler\n")
            f.write("https://portal.belediye.gov.tr:8443\n")
            f.write("\n")
            f.write("intranet.firma.local\n")

        sites = load_sites_from_file(test_file)
        self.assertIn("https://portal.belediye.gov.tr:8443", sites)
        self.assertIn("https://intranet.firma.local", sites)
        self.assertIn("http://intranet.firma.local", sites)

        with self.assertRaises(FileNotFoundError):
            load_sites_from_file(Path(self.test_dir) / "non_existing.txt")

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
        # İkinci çalıştırmada 0 yeni site eklenmeli
        added, total = apply_sites(target_dir=self.test_dir)
        self.assertEqual(added, 0)
        self.assertEqual(total, len(OFFICIAL_SITES))

    def test_apply_presets(self):
        # Belediye paketi
        added, total = apply_sites(target_dir=self.test_dir, presets="belediye")
        self.assertEqual(total, len(OFFICIAL_SITES) + len(PRESETS["belediye"]))

        # 'all' paketi
        added_all, total_all = apply_sites(target_dir=self.test_dir, presets="all")
        expected_total = len(OFFICIAL_SITES) + len(PRESETS["belediye"]) + len(PRESETS["baro"])
        self.assertEqual(total_all, expected_total)

    def test_custom_site_and_remove(self):
        custom = ["https://custom-portal.gov.tr"]
        added, total = apply_sites(target_dir=self.test_dir, custom_sites=custom)
        self.assertEqual(total, len(OFFICIAL_SITES) + 1)

        # Silme testi
        rem, remaining = remove_site(self.test_dir, "https://custom-portal.gov.tr")
        self.assertEqual(rem, 1)
        self.assertEqual(remaining, len(OFFICIAL_SITES))

if __name__ == "__main__":
    unittest.main()
