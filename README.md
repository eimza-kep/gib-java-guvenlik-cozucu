# GİB, UYAP & MERSİS Java Güvenlik Engeli Çözücü & DRS Paketleyici ☕🛡️

[![Python CI](https://github.com/eimza-kep/gib-java-guvenlik-cozucu/actions/workflows/ci.yml/badge.svg)](https://github.com/eimza-kep/gib-java-guvenlik-cozucu/actions)
[![Lisans: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform: Win | Mac | Linux](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-blue.svg)](https://github.com)
[![Enterprise: Java DRS](https://img.shields.io/badge/Enterprise-Deployment%20Rule%20Set-orange.svg)](java_security.py)
[![Blog](https://img.shields.io/badge/Rehber-UYAP%20Teknik%20Destek-red.svg)](https://uyapteknikdestek.site/)

GİB (e-Beyanname, e-Fatura, e-Defter, İnteraktif Vergi Dairesi), UYAP (Avukat, Vatandaş, Kurum Portalları), DYS, SGK e-Bildirge, MERSİS, E-Belediye ve Baro portallarına giriş yaparken karşılaşılan **"Application Blocked by Java Security"**, **"Your security settings have blocked an application from running with an out-of-date or expired version of Java"** ve sertifika engellerini otomatik çözen; büyük hukuk büroları ve kurumsal firmalar için **Java Deployment Rule Set (DRS)** paketleri üreten açık kaynaklı güvenlik aracı.

---

## ✨ Öne Çıkan Özellikler (v1.4)

* 🏢 **Kurumsal Deployment Rule Set (DRS) Desteği:** `--generate-drs` ile her bilgisayara tek tek istisna girmek yerine tüm ağda güvenlik uyarılarını kaldıran `DeploymentRuleSet.jar` üretir.
* ⚡ **Otomatik İstisna Yapılandırması:** 35'ten fazla resmi devlet portalını (`.gov.tr`) tek komutla güvenli siteler listesine (`exception.sites`) ekler.
* 🏛️ **Hazır Portal Paketleri (`--preset`):** Büyükşehir belediyeleri e-belediye/e-imar sistemleri (`belediye`), Türkiye Barolar Birliği ve UHAP portalları (`baro`) için tek parametreyle genişletme.
* 📁 **Toplu Dosyadan Aktarma (`--file`):** Kurumsal intranet, özel port ve yerel alan adlarını metin dosyasından toplu içe aktarma desteği.
* 🌐 **Akıllı URL Normalizasyonu:** Protokol (`https://` ve `http://`) eksikliklerini otomatik tamamlama, özel portları (`:8443`, `:8080`) koruma ve wildcard temizleme.
* 🧹 **Java Önbellek Temizleme:** `--clear-cache` parametresi ile bozulmuş JAR dosyalarını ve eski sertifika önbelleklerini temizler.
* 💾 **Güvenli Yedekleme:** Değişiklik öncesinde mevcut `exception.sites` dosyasının zaman damgalı yedeğini alır.
* 🖥️ **Çoklu Platform:** Windows (`%APPDATA%\Sun\Java`), macOS (`~/Library/Application Support/Oracle/Java`) ve Linux (`~/.java`) dizinlerini otomatik tanır.

---

## 🛠️ Kurulum ve Yerel Geliştirme (Local Setup)

### Sistem Gereksinimleri
- Python 3.8 veya üzeri
- `git`
- (İsteğe bağlı) DRS paketlerini kurumsal imzalamak için Java JDK (`keytool` ve `jarsigner`)

### 1. Depoyu Klonlama ve Çalışma Ortamı
```bash
# Depoyu klonlayın
git clone https://github.com/eimza-kep/gib-java-guvenlik-cozucu.git
cd gib-java-guvenlik-cozucu

# Sanal ortam (virtualenv) oluşturma ve aktifleştirme (Opsiyonel)
python -m venv venv
# Linux/macOS:
source venv/bin/activate
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
```

### 2. Birim Testleri Çalıştırma
```bash
python test_security.py
```
veya `unittest` keşif mekanizmasıyla:
```bash
python -m unittest discover -v
```

---

## 🏢 Kurumsal Ağ Dağıtımı: Java Deployment Rule Set (DRS)

Büyük hukuk bürolarında, bankalarda ve muhasebe departmanlarında yüzlerce istemciye tek tek `exception.sites` yapılandırmak yerine Oracle / OpenJDK **Deployment Rule Set (DRS)** mimarisi kullanılır.

### 1. Kurumsal DRS Paketi Oluşturma
```bash
python java_security.py --generate-drs ./DeploymentRuleSet.jar
```

### 2. Paketi Kurumsal Sertifikanızla İmzalama
Java DRS mimarisi, kural setinin güvenilir bir kurum sertifikasıyla imzalanmasını şart koşar:
```bash
jarsigner -keystore <sirket_sertifikasi.jks> ./DeploymentRuleSet.jar <alias>
```
*(Test ortamları için `--self-sign` parametresi ile otomatik kendinden imzalı paket de üretebilirsiniz).*

### 3. GPO / Intune ile Merkezi Dağıtım Yolları:

| İşletim Sistemi | Hedef DRS Konumu |
|:---|:---|
| **Windows** | `C:\Windows\Sun\Java\Deployment\DeploymentRuleSet.jar` |
| **macOS** | `/Library/Application Support/Oracle/Java/Deployment/DeploymentRuleSet.jar` |
| **Linux** | `/etc/.java/deployment/DeploymentRuleSet.jar` |

*Sistemdeki DRS durumunu kontrol etmek için:*
```bash
python java_security.py --drs-info
```

---

## 🚀 Bireysel Kullanım Senaryoları (Exception Sites)

### 1. Temel Kullanım (Tüm Resmi Portalları Tek Komutla Ekleme)
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
powershell -ExecutionPolicy Bypass -File .\Fix-JavaSecurity.ps1 -Preset all -ClearCache
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
