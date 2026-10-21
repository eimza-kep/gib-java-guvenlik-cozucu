#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GİB & UYAP Java Güvenlik Engeli (Exception Site List) Çözücü v1.3
================================================================
Windows, macOS ve Linux üzerinde Java deployment "Application Blocked by Security Settings"
hatalarını çözmek için resmi GİB, UYAP, SGK, MERSİS, Kamu SM, Belediye ve Baro portallarını
güvenli istisna listesine (exception.sites) otomatik olarak ekler, URL normalizasyonu yapar
ve önbellek temizler.

Yazar: E-İmza & Dijital Dönüşüm Portalı (https://uyapteknikdestek.site/)
Lisans: MIT
"""

import os
import sys
import shutil
import argparse
from datetime import datetime
from pathlib import Path

# Force UTF-8 stdout
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

OFFICIAL_SITES = [
    # SGK
    "https://ebildirge.sgk.gov.tr",
    "https://kesenek.sgk.gov.tr",
    "https://medula.sgk.gov.tr",
    # Adalet Bakanlığı / UYAP & DYS
    "https://uyap.gov.tr",
    "https://uyap.adalet.gov.tr",
    "https://avukat.uyap.gov.tr",
    "https://vatandas.uyap.gov.tr",
    "https://kurum.uyap.gov.tr",
    "https://bilirkisi.uyap.gov.tr",
    "https://uzlasmacilar.uyap.gov.tr",
    "https://icra.uyap.gov.tr",
    "https://portal.uyap.gov.tr",
    "https://dys.adalet.gov.tr",
    "https://e-satis.uyap.gov.tr",
    "https://uets.ptt.gov.tr",
    "https://etebligat.ptt.gov.tr",
    # Gelir İdaresi Başkanlığı (GİB)
    "https://intvd.gib.gov.tr",
    "https://ivd.gib.gov.tr",
    "https://dijital.gib.gov.tr",
    "https://etebligat.gib.gov.tr",
    "https://edefter.gov.tr",
    "https://efatura.gov.tr",
    "https://earsiv.efatura.gov.tr",
    "https://earsivportal.efatura.gov.tr",
    "https://ebelge.gib.gov.tr",
    "https://vedop.gib.gov.tr",
    "https://ebeyanname.gib.gov.tr",
    # Tapu Kadastro & Web Tapu
    "https://webtapu.tkgm.gov.tr",
    # Ticaret & MERSİS & KİK
    "https://mersis.gtb.gov.tr",
    "https://mersis.ticaret.gov.tr",
    "https://ekap.kik.gov.tr",
    # Kamu SM & E-Devlet
    "https://kamusm.bilgem.tubitak.gov.tr",
    "https://nes.kamusm.gov.tr",
    "https://giris.turkiye.gov.tr",
    "https://www.turkiye.gov.tr"
]

PRESETS = {
    "belediye": [
        "https://ebelediye.ibb.gov.tr",
        "https://ebelediye.ankara.bel.tr",
        "https://ebelediye.izmir.bel.tr",
        "https://ebelediye.bursa.bel.tr",
        "https://ebelediye.antalya.bel.tr",
        "https://ebelediye.konya.bel.tr",
        "https://ebelediye.gaziantep.bel.tr",
        "https://e-imar.ibb.gov.tr",
        "https://imar.ankara.bel.tr"
    ],
    "baro": [
        "https://uhap.com.tr",
        "https://portal.barobirlik.org.tr",
        "https://ubap.barobirlik.org.tr",
        "https://istanbulbarosu.org.tr",
        "https://ankarabarosu.org.tr"
    ]
}

def normalize_url(entry):
    """
    Java Exception Site List formatına uygun şekilde URL veya domaini normalize eder.
    - Protokol belirtilmemişse (ör. 'belediye.gov.tr' veya 'intranet:8443') hem https hem http döner.
    - URL sonundaki gereksiz eğik çizgileri (slash) ve boşlukları temizler.
    - Port numarasını korur (ör. https://belediye.gov.tr:8443).
    """
    entry = entry.strip()
    if not entry or entry.startswith("#"):
        return []

    # Wildcard prefix temizleme (*.belediye.gov.tr -> belediye.gov.tr)
    if entry.startswith("*."):
        entry = entry[2:]

    if not (entry.startswith("http://") or entry.startswith("https://") or entry.startswith("file:///")):
        return [f"https://{entry.rstrip('/')}", f"http://{entry.rstrip('/')}"]

    return [entry.rstrip("/")]

def load_sites_from_file(file_path):
    """Metin dosyasından site listesini okur, yorum satırlarını eler ve normalize eder."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Dosya bulunamadı: {file_path}")

    sites = []
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            cleaned = line.strip()
            if cleaned and not cleaned.startswith("#"):
                normalized = normalize_url(cleaned)
                sites.extend(normalized)
    return sites

def get_java_security_path():
    """Java deployment security dizinini platforma göre belirler."""
    if sys.platform == "win32":
        appdata = os.environ.get("APPDATA")
        if not appdata:
            appdata = str(Path.home() / "AppData" / "Roaming")
        return Path(appdata) / "Sun" / "Java" / "Deployment" / "security"
    elif sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / "Oracle" / "Java" / "Deployment" / "security"
    else:  # Linux / Unix
        return Path.home() / ".java" / "deployment" / "security"

def get_java_cache_path():
    """Java geçici önbellek dizinini belirler."""
    if sys.platform == "win32":
        local_app = os.environ.get("LOCALAPPDATA")
        if not local_app:
            local_app = str(Path.home() / "AppData" / "Local")
        return Path(local_app) / "Sun" / "Java" / "Deployment" / "cache"
    elif sys.platform == "darwin":
        return Path.home() / "Library" / "Caches" / "Oracle" / "Java" / "Deployment" / "cache"
    else:
        return Path.home() / ".java" / "deployment" / "cache"

def load_existing_sites(exception_file):
    if not exception_file.exists():
        return []
    try:
        with open(exception_file, "r", encoding="utf-8", errors="ignore") as f:
            lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]
            return lines
    except Exception as e:
        print(f"[!] Dosya okuma hatası: {e}")
        return []

def apply_sites(target_dir=None, custom_sites=None, presets=None):
    sec_dir = Path(target_dir) if target_dir else get_java_security_path()
    sec_dir.mkdir(parents=True, exist_ok=True)
    exception_file = sec_dir / "exception.sites"

    existing = load_existing_sites(exception_file)

    # Yedekleme
    if exception_file.exists() and len(existing) > 0:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = sec_dir / f"exception.sites.bak_{timestamp}"
        try:
            shutil.copy2(exception_file, backup_file)
        except Exception:
            pass

    sites_to_add = list(OFFICIAL_SITES)

    if presets:
        preset_list = ["belediye", "baro"] if presets == "all" else ([presets] if isinstance(presets, str) else presets)
        for p in preset_list:
            if p.lower() in PRESETS:
                sites_to_add.extend(PRESETS[p.lower()])

    if custom_sites:
        for s in custom_sites:
            normalized = normalize_url(s)
            sites_to_add.extend(normalized)

    merged = list(existing)
    added_count = 0
    for site in sites_to_add:
        cleaned = site.strip()
        if cleaned and cleaned not in merged:
            merged.append(cleaned)
            added_count += 1

    with open(exception_file, "w", encoding="utf-8") as f:
        f.write("# Java Exception Site List - Generated by gib-java-guvenlik-cozucu v1.3\n")
        f.write(f"# Updated: {datetime.now().isoformat()}\n")
        for s in merged:
            f.write(s + "\n")

    return added_count, len(merged)

def remove_site(target_dir, site_url):
    sec_dir = Path(target_dir) if target_dir else get_java_security_path()
    exception_file = sec_dir / "exception.sites"
    existing = load_existing_sites(exception_file)
    target = site_url.strip().lower()

    new_list = [s for s in existing if s.lower() != target]
    removed = len(existing) - len(new_list)

    if removed > 0:
        with open(exception_file, "w", encoding="utf-8") as f:
            f.write("# Java Exception Site List - Updated\n")
            for s in new_list:
                f.write(s + "\n")
    return removed, len(new_list)

def clear_java_cache():
    cache_dir = get_java_cache_path()
    if not cache_dir.exists():
        return False, "Java önbellek dizini bulunamadı veya zaten temiz."
    try:
        shutil.rmtree(cache_dir, ignore_errors=True)
        return True, "Java applet ve sertifika önbelleği başarıyla temizlendi."
    except Exception as e:
        return False, str(e)

def main():
    parser = argparse.ArgumentParser(description="GİB & UYAP Java Güvenlik Engeli Çözücü v1.3")
    parser.add_argument("--add", nargs="+", help="İstisna listesine eklenecek özel URL adresleri veya domainler")
    parser.add_argument("--file", help="İstisna listesine toplu eklenecek metin dosyası (her satıra bir URL/domain)")
    parser.add_argument("--preset", choices=["belediye", "baro", "all"], help="Hazır kamu/belediye portal paketlerini dahil eder")
    parser.add_argument("--remove", help="İstisna listesinden çıkarılacak URL")
    parser.add_argument("--list", action="store_true", help="Kayıtlı güvenli siteleri listele")
    parser.add_argument("--clear-cache", action="store_true", help="Java geçici dosya ve sertifika önbelleğini temizler")
    parser.add_argument("--target-dir", help="Özel Java security dizini")
    parser.add_argument("--json", action="store_true", help="JSON çıktısı ver")

    args = parser.parse_args()

    sec_dir = Path(args.target_dir) if args.target_dir else get_java_security_path()
    exc_file = sec_dir / "exception.sites"

    if args.clear_cache:
        success, msg = clear_java_cache()
        print(f"[{'OK' if success else 'INFO'}] {msg}")

    if args.remove:
        rem, total = remove_site(args.target_dir, args.remove)
        print(f"[+] '{args.remove}' kaldırıldı. Kalan site sayısı: {total}")
        return

    if args.list:
        sites = load_existing_sites(exc_file)
        if args.json:
            import json
            print(json.dumps({"path": str(exc_file), "sites": sites}, indent=2, ensure_ascii=False))
        else:
            print(f"Kayıtlı İstisna Siteleri ({len(sites)} Adet - {exc_file}):")
            for idx, s in enumerate(sites, 1):
                print(f"  {idx:2d}. {s}")
        return

    custom_sites = list(args.add) if args.add else []
    if args.file:
        try:
            file_sites = load_sites_from_file(args.file)
            custom_sites.extend(file_sites)
        except Exception as e:
            print(f"[HATA] Dosya okunamadı: {e}")
            sys.exit(1)

    # Varsayılan: Siteleri uygula
    added, total = apply_sites(target_dir=args.target_dir, custom_sites=custom_sites, presets=args.preset)

    if args.json:
        import json
        print(json.dumps({"added": added, "total": total, "path": str(exc_file)}, indent=2))
        return

    print("=" * 70)
    print("      GİB & UYAP JAVA GÜVENLİK İSTİSNA YAPILANDIRICISI v1.3")
    print("=" * 70)
    print(f"Yapılandırma Dosyası: {exc_file}")
    print(f"Yeni Eklenen Site:    {added} Adet")
    print(f"Toplam Güvenli Site:  {total} Adet")
    if args.preset:
        print(f"Uygulanan Paket:      {args.preset.upper()}")
    if args.file:
        print(f"İçe Aktarılan Dosya:  {args.file}")
    print("\n✅ GİB, UYAP, MERSİS, SGK ve ilgili portallar Java 'Application Blocked' engeli çözüldü!")
    print("💡 Tarayıcınızı ve Java uygulamanızı yeniden başlatarak giriş yapabilirsiniz.")
    print("=" * 70)

if __name__ == "__main__":
    main()
