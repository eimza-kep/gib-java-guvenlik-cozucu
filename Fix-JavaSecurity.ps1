<#
.SYNOPSIS
    GİB, UYAP, MERSİS ve Kamu Portalları İçin Java Güvenlik Engeli (Exception Site List) Otomatik Çözücü

.DESCRIPTION
    Bu betik, Windows üzerinde Java güvenlik ayarlarından dolayı engellenen GİB (Gelir İdaresi Başkanlığı),
    UYAP, MERSİS, EKAP, SGK Medula ve e-Devlet portallarını otomatik olarak Java Exception Site List
    (Güvenilen Siteler) listesine ekler ve önbelleği temizler.

.NOTES
    Yazar: E-İmza & Dijital Dönüşüm Portalı (https://uyap-teknik-destek.pages.dev/yazilar/uyap-dokuman-editoru-udf-acilmiyor-java-bellek-ayari.html)
    Lisans: MIT
#>

[CmdletBinding()]
param(
    [switch]$SkipCacheClear,
    [switch]$NoBackup,
    [switch]$ListSites,
    [switch]$RestoreBackup,
    [string[]]$CustomSites = @()
)

try {
    $OutputEncoding = [System.Text.Encoding]::UTF8
    [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
} catch {}

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "   GİB & UYAP Java Güvenlik Engeli Otomatik Çözücü v1.1         " -ForegroundColor Yellow
Write-Host "   E-İmza & Dijital Dönüşüm Destek Aracı                        " -ForegroundColor Gray
Write-Host "=================================================================`n" -ForegroundColor Cyan

# 1. Java Deployment Security Klasörünü Bul / Oluştur
$javaSecurityDir = Join-Path $env:APPDATA "Sun\Java\Deployment\security"
$exceptionFile = Join-Path $javaSecurityDir "exception.sites"

if (-not (Test-Path $javaSecurityDir)) {
    Write-Host "[+] Java yapılandırma dizini oluşturuluyor: $javaSecurityDir" -ForegroundColor White
    New-Item -ItemType Directory -Force -Path $javaSecurityDir | Out-Null
}

# 1.1 Restore Backup Modu
if ($RestoreBackup) {
    $backups = Get-ChildItem -Path $javaSecurityDir -Filter "exception.sites.bak_*" | Sort-Object LastWriteTime -Descending
    if ($backups.Count -gt 0) {
        $latestBackup = $backups[0].FullName
        Copy-Item -Path $latestBackup -Destination $exceptionFile -Force
        Write-Host "[OK] En son yedek başarıyla geri yüklendi: $($backups[0].Name)" -ForegroundColor Green
    } else {
        Write-Host "[!] Geri yüklenecek bir yedek dosyası bulunamadı." -ForegroundColor Yellow
    }
    exit 0
}

# 1.2 List Sites Modu
if ($ListSites) {
    if (Test-Path $exceptionFile) {
        $currentList = Get-Content $exceptionFile | Where-Object { -not [string]::IsNullOrWhiteSpace($_) }
        Write-Host "Güvenilen Siteler Listesi ($($currentList.Count) Adet):" -ForegroundColor Green
        foreach ($site in $currentList) {
            Write-Host "  - $site" -ForegroundColor White
        }
    } else {
        Write-Host "[i] Henüz yapılandırılmış bir exception.sites dosyası bulunmuyor." -ForegroundColor Yellow
    }
    exit 0
}


# 2. Eklenecek Resmi Portalların Listesi
$officialSites = @(
    "https://ebilgi.gib.gov.tr",
    "http://ebilgi.gib.gov.tr",
    "https://earsivportal.gib.gov.tr",
    "http://earsivportal.gib.gov.tr",
    "https://edefter.gov.tr",
    "https://e-beyanname.gib.gov.tr",
    "https://intvrg.gib.gov.tr",
    "https://dijital.gib.gov.tr",
    "https://uyap.gov.tr",
    "https://avukat.uyap.gov.tr",
    "https://vatandas.uyap.gov.tr",
    "https://kurum.uyap.gov.tr",
    "https://bilirkisi.uyap.gov.tr",
    "https://uzlastirmaci.uyap.gov.tr",
    "https://mersis.gtb.gov.tr",
    "https://mersis.ticaret.gov.tr",
    "https://ekap.kik.gov.tr",
    "https://medula.sgk.gov.tr",
    "https://webtapu.tkgm.gov.tr",
    "https://kamusm.bilgem.tubitak.gov.tr",
    "https://nesislemleri.kamusm.gov.tr",
    "https://e-devlet.turkiye.gov.tr",
    "https://turkiye.gov.tr",
    "https://portal.kamusm.gov.tr"
)

# 3. Mevcut exception.sites Dosyasını Oku ve Yedekle
$existingSites = @()
if (Test-Path $exceptionFile) {
    $existingSites = Get-Content $exceptionFile | Where-Object { -not [string]::IsNullOrWhiteSpace($_) }
    Write-Host "[i] Mevcut listede $($existingSites.Count) adet site bulundu." -ForegroundColor Gray

    if (-not $NoBackup -and $existingSites.Count -gt 0) {
        $backupPath = Join-Path $javaSecurityDir ("exception.sites.bak_{0}" -f (Get-Date -Format "yyyyMMdd_HHmmss"))
        Copy-Item -Path $exceptionFile -Destination $backupPath -Force
        Write-Host "[+] Güvenlik yedeği alındı: $(Split-Path $backupPath -Leaf)" -ForegroundColor DarkGray
    }
} else {
    Write-Host "[i] exception.sites dosyası ilk kez oluşturuluyor." -ForegroundColor Gray
}

# 4. Listeleri Birleştir ve Tekilleştir
$allSites = ($existingSites + $officialSites + $CustomSites) | 
            Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | 
            Select-Object -Unique

# 5. Dosyaya Yaz
try {
    $allSites | Set-Content -Path $exceptionFile -Encoding ASCII -Force
    Write-Host "`n[OK] Başarılı! Toplam $($allSites.Count) adet güvenilir kamu portalı Java listesine eklendi." -ForegroundColor Green
    Write-Host "     Dosya: $exceptionFile" -ForegroundColor DarkGray
} catch {
    Write-Host "`n[HATA] Dosyaya yazılamadı: $_" -ForegroundColor Red
    exit 1
}

# 6. Eski Java Önbelleğini Temizle (Opsiyonel ama Önemli)
if (-not $SkipCacheClear) {
    Write-Host "`n[*] Java geçici applet önbelleği taranıyor..." -ForegroundColor White
    $cacheDir = Join-Path $env:LOCALAPPDATA "Sun\Java\Deployment\cache"
    if (Test-Path $cacheDir) {
        try {
            Remove-Item "$cacheDir\*" -Recurse -Force -ErrorAction SilentlyContinue
            Write-Host "[OK] Eski Java önbelleği temizlendi. Tarayıcınız güncel portalları sorunsuz yükleyecek." -ForegroundColor Green
        } catch {
            Write-Host "[!] Bazı önbellek dosyaları kilitli olabilir, tarayıcınızı kapatıp tekrar deneyin." -ForegroundColor Yellow
        }
    }
}

Write-Host "`n=================================================================" -ForegroundColor Cyan
Write-Host " İŞLEM TAMAMLANDI!                                               " -ForegroundColor Green
Write-Host " Tarayıcınızı veya UYAP Editörünü yeniden başlatabilirsiniz.     " -ForegroundColor White
Write-Host " Daha fazla rehber için: https://uyap-teknik-destek.pages.dev/yazilar/uyap-dokuman-editoru-udf-acilmiyor-java-bellek-ayari.html " -ForegroundColor Cyan
Write-Host "=================================================================`n" -ForegroundColor Cyan
