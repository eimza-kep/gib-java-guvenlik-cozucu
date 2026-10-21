# GİB, UYAP & MERSİS Java Güvenlik Engeli Çözücü ☕🛡️

[![Python CI](https://github.com/eimza-kep/gib-java-guvenlik-cozucu/actions/workflows/ci.yml/badge.svg)](https://github.com/eimza-kep/gib-java-guvenlik-cozucu/actions)
[![Lisans: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform: Win | Mac | Linux](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-blue.svg)](https://github.com)
[![Blog](https://img.shields.io/badge/Rehber-UYAP%20Teknik%20Destek-red.svg)](https://uyapteknikdestek.site/)

GİB (e-Beyanname, e-Fatura, e-Defter, İnteraktif Vergi Dairesi), UYAP (Avukat, Vatandaş, Kurum Portalları), DYS, SGK e-Bildirge, MERSİS, E-Belediye ve Baro portallarına giriş yaparken karşılaşılan **"Application Blocked by Java Security"**, **"Your security settings have blocked an application from running with an out-of-date or expired version of Java"** ve sertifika engellerini otomatik olarak `exception.sites` dosyasına ekleyerek çözen açık kaynaklı yardımcı araçtır.

---

## ✨ Öne Çıkan Özellikler

* ⚡ **Otomatik İstisna Yapılandırması:** 30'dan fazla resmi devlet portalını (`.gov.tr`) tek komutla güvenli siteler listesine ekler.
* 🏛️ **Hazır Portal Paketleri (`--preset`):** Büyükşehir belediyeleri e-belediye/e-imar sistemleri (`belediye`), Türkiye Barolar Birliği ve UHAP portalları (`baro`) için tek parametreyle genişletme.
* 📁 **Toplu Dosyadan Aktarma (`--file`):** Kurumsal intranet, özel port ve yerel alan adlarını metin dosyasından toplu içe aktarma desteği.
* 🌐 **Akıllı URL Normalizasyonu:** Protokol (`https://` ve `http://`) eksikliklerini otomatik tamamlama, özel portları (`:8443`, `:8080`) koruma ve wildcard temizleme.
* 🧹 **Java Önbellek Temizleme:** `--clear-cache` parametresi ile bozulmuş JAR dosyalarını ve eski sertifika önbelleklerini temizler.
* 💾 **Güvenli Yedekleme:** Değişiklik öncesinde mevcut `exception.sites` dosyasının zaman damgalı yedeğini alır.
* 🖥️ **Çoklu Platform:** Windows (`%APPDATA%\Sun\Java`), macOS (`~/Library/Application Support/Oracle/Java`) ve Linux (`~/.java`) dizinlerini otomatik tanır.
* 📋 **Site Yönetimi:** `--list` ile kayıtlı siteleri listeleme, `--remove` ile site çıkarma olanağı.

---

## 🛠️ Kurulum ve Ortam Hazırlığı

Projeyi yerel ortamınızda çalıştırmak için ek bir harici kütüphane (pip) bağımlılığı gerekmez; standart Python 3.8+ kütüphaneleriyle doğrudan çalışır.

```bash
# Depoyu klonlayın
git clone https://github.com/eimza-kep/gib-java-guvenlik-cozucu.git
cd gib-java-guvenlik-cozucu

# Testleri çalıştırın
python -m unittest test_security.py
```

---

## 🚀 Kullanım Senaryoları

### 1. Temel Kullanım (Tüm Resmi Portalları Ekleme)
```bash
python java_security.py
```

### 2. Hazır Belediye ve Baro Paketlerini Dahil Etme
```bash
# Büyükşehir e-belediye ve e-imar portallarını ekle
python java_security.py --preset belediye

# Türkiye Barolar Birliği (UHAP/UBAP) portallarını ekle
python java_security.py --preset baro

# Hem resmi kamu, hem belediye hem de baroları topluca ekle
python java_security.py --preset all
```

### 3. Dış Metin Dosyasından Toplu Aktarım (`--file`)
Kurumsal intranet veya özel portalların listesini içeren bir dosya oluşturun (`siteler.txt`):
```text
# Kurumsal İntranet ve Özel Portlar
https://intranet.adalet.gov.tr:8443
portal.belediye.gov.tr
https://ebys.universite.edu.tr:8080
```
Ve tek komutla içe aktarın:
```bash
python java_security.py --file siteler.txt
```

### 4. Java Önbelleğini Temizleme ve Listeleme
```bash
# Önbellek temizleme
python java_security.py --clear-cache

# Kayıtlı siteleri listeleme
python java_security.py --list

# JSON formatında çıktı alma
python java_security.py --list --json
```

### 5. Özel URL Ekleme veya Çıkarma
```bash
python java_security.py --add https://ozel-portal.gov.tr:8443
python java_security.py --remove https://eski-portal.gov.tr
```

---

## 💻 İşletim Sistemi Betikleri

### Windows PowerShell Tek Tıkla Onarım
```powershell
powershell -ExecutionPolicy Bypass -File .\Fix-JavaSecurity.ps1
```
*Hazır paket ile:*
```powershell
powershell -ExecutionPolicy Bypass -File .\Fix-JavaSecurity.ps1 -Preset all
```

### macOS ve Linux Bash Başlatıcı
```bash
chmod +x fix-java.sh
./fix-java.sh --preset all --clear-cache
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
* 📄 [GİB ve UYAP Java Security Application Blocked Hatası Kesin Çözümü](https://uyapteknikdestek.site/yazilar/java-security-exception-sites-ekleme-rehberi.html)
* 📄 [UYAP Editör Donma ve Bellek Aşımı Sorunları Nasıl Düzeltilir?](https://uyapteknikdestek.site/yazilar/uyap-editor-donma-ve-bellek-hatalari.html)
* 📄 [e-Beyanname ve e-Bildirge Girişinde Karşılaşılan Java Sorunları](https://malimuhur.site/yazilar/e-beyanname-ve-ebildirge-java-hatalari.html)

---

## ⚖️ Lisans

Bu proje [MIT Lisansı](LICENSE) ile lisanslanmıştır.
