# GİB & UYAP Java Güvenlik Engeli Çözücü ☕🛡️

[![Lisans: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform: Windows](https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011-blue.svg)](https://microsoft.com)
[![PowerShell](https://img.shields.io/badge/PowerShell-5.1%2B%20%7C%207%2B-blueviolet.svg)](https://github.com/PowerShell/PowerShell)
[![Blog](https://img.shields.io/badge/Rehber-E--%C4%B0mza%20Blog-22c55e.svg)](https://eimza-kep.github.io/eimza-blog/)

Gelir İdaresi Başkanlığı (**GİB e-Arşiv, e-Defter, e-Beyanname**), **UYAP (Avukat/Vatandaş/Bilirkişi)**, **MERSİS**, **EKAP** ve **SGK Medula** portallarında e-imza ile giriş yaparken veya belge imzalarken karşılaşılan meşhur:

> **"Your security settings have blocked an untrusted application from running"**  
> veya  
> **"Application Blocked by Deployment Rule Set / Java Security"**

hatasını **tek tıkla** kalıcı olarak çözen açık kaynaklı otomatik yapılandırma aracıdır.

---

## 🚀 Hızlı Kullanım (1 Tıkla Çözüm)

### Yöntem 1: Dosyayı İndirip Çalıştırma
1. Bu repoyu yeşil **`Code > Download ZIP`** butonundan indirin (veya [Releases](../../releases) kısmından alın).
2. ZIP içerisindeki **`fix-java.bat`** dosyasına **çift tıklayın**.
3. Betik gerekli tüm kamu portallarını Java Güvenilir Siteler listesine ekleyecek ve eski Java önbelleğini temizleyecektir.
4. Tarayıcınızı veya UYAP Editörünü yeniden başlatın. Artık imzalama ekranınız sorunsuz açılacaktır!

### Yöntem 2: PowerShell ile Doğrudan Çalıştırma
PowerShell terminalinizi açıp şu komutu yapıştırın:
```powershell
irm https://raw.githubusercontent.com/eimza-kep/gib-java-guvenlik-cozucu/main/Fix-JavaSecurity.ps1 | iex
```

### Yöntem 3: Gelişmiş Komut Satırı Seçenekleri
```powershell
# Mevcut güvenilen siteleri listeleme
.\Fix-JavaSecurity.ps1 -ListSites

# Kendi özel portalınızı da listeye ekleme
.\Fix-JavaSecurity.ps1 -CustomSites "https://otomasyon.kurumunuz.gov.tr"

# Önceki güvenlik yapılandırmasını geri yükleme
.\Fix-JavaSecurity.ps1 -RestoreBackup
```

---

## 📋 Otomatik Eklenen Resmi Portallar

Betik çalıştırıldığında `%APPDATA%\Sun\Java\Deployment\security\exception.sites` dosyasına şu güvenilir kamu adreslerini ekler:

| Kurum / Portal | Adres | Kullanım Amacı |
| :--- | :--- | :--- |
| **GİB e-Arşiv / e-Belge** | `https://earsivportal.gib.gov.tr` | Fatura kesme, e-Arşiv portal girişi |
| **GİB e-Defter Portalı** | `https://edefter.gov.tr` | e-Defter beratı imzalama ve yükleme |
| **GİB e-Beyanname** | `https://ebilgi.gib.gov.tr` | Beyanname gönderme ve sorgulama |
| **İnteraktif Vergi Dairesi** | `https://dijital.gib.gov.tr` | Yeni Dijital Vergi Dairesi işlemleri |
| **UYAP Avukat Portalı** | `https://avukat.uyap.gov.tr` | Dava açma, evrak gönderme, e-duruşma |
| **UYAP Vatandaş Portalı** | `https://vatandas.uyap.gov.tr` | Dosya sorgulama ve e-imzalı evrak alma |
| **MERSİS (Ticaret Bak.)** | `https://mersis.ticaret.gov.tr` | Şirket kuruluşu, ana sözleşme imzalama |
| **EKAP (Kamu İhale)** | `https://ekap.kik.gov.tr` | Kamu ihale teklifi verme ve e-imza |
| **SGK Medula** | `https://medula.sgk.gov.tr` | Hekim ve eczane e-reçete onaylama |
| **Web Tapu** | `https://webtapu.tkgm.gov.tr` | Tapu devir, ipotek ve başvuru işlemleri |
| **TÜBİTAK Kamu SM** | `https://kamusm.bilgem.tubitak.gov.tr` | Sertifika ve PIN kilit çözme işlemleri |

---

## 🛠️ Manuel Olarak Nasıl Yapılır?

Eğer betik çalıştırmak istemiyorsanız aynı işlemi elle şu adımlarla yapabilirsiniz:
1. Windows Başlat menüsüne **"Configure Java"** yazıp açın.
2. Üst menüden **"Security" (Güvenlik)** sekmesine geçin.
3. En alttaki **"Edit Site List..." (Site Listesini Düzenle)** butonuna tıklayın.
4. **"Add" (Ekle)** diyerek yukarıdaki tablodaki adresleri tek tek yapıştırın.
5. **OK** ve **Apply** butonlarına basarak kaydedin.

---

## 📖 İlgili Kılavuzlar ve Teknik Yazılar

Daha fazla e-dönüşüm, mali mühür ve e-imza hata çözümleri için resmi blogumuzu ziyaret edebilirsiniz:

---

## ⚖️ Lisans

Bu proje [MIT Lisansı](LICENSE) kapsamında tamamen ücretsiz ve açık kaynaklıdır. Ticari veya bireysel olarak dilediğiniz gibi kullanabilir ve dağıtabilirsiniz.

### 📚 İlgili Rehber ve Çözümler
* 📄 [UYAP Doküman Editörü (.udf) Açılmıyor Sorununda Java Bellek Ayarı](https://uyap-teknik-destek.pages.dev/yazilar/uyap-dokuman-editoru-udf-acilmiyor-java-bellek-ayari.html)
* 📄 [e-Defter Berat Yükleme Gününde Mali Mühür Çalışmazsa Ne Yapılır?](https://mali-muhur-merkezi.pages.dev/yazilar/e-defter-berat-gunu-mali-muhur-calismazsa-cozum.html)
* 📄 [GİB e-Arşiv Portaldan Fatura Kestikten Sonra İptal Süresi Kaç Gündür?](https://efatura-atolyesi.pages.dev/yazilar/gib-e-arsiv-fatura-iptal-suresi-kac-gun.html)
* 📄 [Elektronik İmza Nedir? Islak İmza Yerine Hangi Alanlarda Kullanılır?](https://eimza-kep.github.io/eimza-blog/posts/elektronik-imza-nedir-hangi-alanlarda-kullanilir.html)