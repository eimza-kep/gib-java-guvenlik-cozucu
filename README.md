# GİB, UYAP & MERSİS Java Güvenlik Engeli Çözücü ☕🛡️

[![Python CI](https://github.com/eimza-kep/gib-java-guvenlik-cozucu/actions/workflows/ci.yml/badge.svg)](https://github.com/eimza-kep/gib-java-guvenlik-cozucu/actions)
[![Lisans: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform: Win | Mac | Linux](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-blue.svg)](https://github.com)
[![Blog](https://img.shields.io/badge/Rehber-UYAP%20Teknik%20Destek-red.svg)](https://uyap-teknik-destek.pages.dev/)

GİB (e-Beyanname, e-Fatura, e-Defter, İnteraktif Vergi Dairesi), UYAP (Avukat, Vatandaş, Kurum Portalları), DYS, SGK e-Bildirge ve MERSİS'e giriş yaparken karşılaşılan **"Application Blocked by Java Security"**, **"Your security settings have blocked an application from running with an out-of-date or expired version of Java"** ve sertifika engellerini otomatik olarak `exception.sites` dosyasına ekleyerek çözen açık kaynaklı yardımcı araçtır.

---

## ✨ Öne Çıkan Özellikler

* ⚡ **Otomatik İstisna Yapılandırması:** 30'dan fazla resmi devlet portalını (`.gov.tr`) tek komutla güvenli siteler listesine ekler.
* 🧹 **Java Önbellek Temizleme:** `--clear-cache` parametresi ile bozulmuş JAR dosyalarını ve eski sertifika önbelleklerini temizler.
* 💾 **Güvenli Yedekleme:** Değişiklik öncesinde mevcut `exception.sites` dosyasının zaman damgalı yedeğini alır.
* 🖥️ **Çoklu Platform:** Windows (`%APPDATA%\Sun\Java`), macOS (`~/Library/Application Support/Oracle/Java`) ve Linux (`~/.java`) dizinlerini otomatik tanır.
* 📋 **Site Yönetimi:** `--list` ile kayıtlı siteleri listeleme, `--remove` ile site çıkarma olanağı.

---

## 🚀 Hızlı Başlangıç

### 1. Tek Komutla Tüm Resmi Portalları Ekleme
```bash
python java_security.py
```

### 2. Java Önbelleğini Temizleme ve Listeleme
```bash
# Önbellek temizleme
python java_security.py --clear-cache

# Kayıtlı siteleri listeleme
python java_security.py --list
```

### 3. Özel URL Ekleme veya Çıkarma
```bash
python java_security.py --add https://ozel-portal.gov.tr
python java_security.py --remove https://eski-portal.gov.tr
```

### 4. Windows PowerShell İle Doğrudan Çalıştırma
```powershell
powershell -ExecutionPolicy Bypass -File .\Fix-JavaSecurity.ps1
```

---

## 🔗 E-Dönüşüm Açık Kaynak Ekosistemi

Bu araç [eimza-kep](https://github.com/eimza-kep) organizasyonunun açık kaynak e-dönüşüm araçları ekosisteminin bir parçasıdır:

* 🇹🇷 **[awesome-turkiye-e-donusum](https://github.com/eimza-kep/awesome-turkiye-e-donusum):** Türkiye E-Dönüşüm kütüphane, mevzuat ve araçlar listesi.
* 🛠️ **[uyap-editor-hizli-onarim](https://github.com/eimza-kep/uyap-editor-hizli-onarim):** UYAP Doküman Editörü açılmama ve Java bellek aşımı onarım aracı.
* 🩺 **[akilli-kart-surucu-teshis](https://github.com/eimza-kep/akilli-kart-surucu-teshis):** Akıllı kart okuyucu ve sürücü teşhis aracı.
* 📊 **[gib-edefter-berat-xml-dogrulayici](https://github.com/eimza-kep/gib-edefter-berat-xml-dogrulayici):** GİB e-Defter ve berat doğrulama aracı.

---

## 📚 İlgili Teknik Rehberler
* 📄 [GİB ve UYAP Java Security Application Blocked Hatası Kesin Çözümü](https://uyap-teknik-destek.pages.dev/yazilar/java-security-exception-sites-ekleme-rehberi.html)
* 📄 [UYAP Editör Donma ve Bellek Aşımı Sorunları Nasıl Düzeltilir?](https://uyap-teknik-destek.pages.dev/yazilar/uyap-editor-donma-ve-bellek-hatalari.html)
* 📄 [e-Beyanname ve e-Bildirge Girişinde Karşılaşılan Java Sorunları](https://mali-muhur-merkezi.pages.dev/yazilar/e-beyanname-ve-ebildirge-java-hatalari.html)

---

## ⚖️ Lisans

Bu proje [MIT Lisansı](LICENSE) ile lisanslanmıştır.