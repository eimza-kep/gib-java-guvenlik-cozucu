#!/usr/bin/env bash
# ==============================================================================
# GİB & UYAP Java Güvenlik Engeli (Exception Site List) Çözücü - macOS & Linux
# ==============================================================================
set -e

echo "=== GİB & UYAP Java Güvenlik Engeli Çözücü (macOS & Linux) ==="

OS_NAME="$(uname -s)"
if [ "$OS_NAME" = "Darwin" ]; then
    SEC_DIR="$HOME/Library/Application Support/Oracle/Java/Deployment/security"
    CACHE_DIR="$HOME/Library/Caches/Oracle/Java/Deployment/cache"
else
    SEC_DIR="$HOME/.java/deployment/security"
    CACHE_DIR="$HOME/.java/deployment/cache"
fi

mkdir -p "$SEC_DIR"
EXC_FILE="$SEC_DIR/exception.sites"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Python ortamı varsa gelişmiş normalizasyon ve preset desteği ile çalıştır
if command -v python3 >/dev/null 2>&1; then
    python3 "$SCRIPT_DIR/java_security.py" "$@"
elif command -v python >/dev/null 2>&1; then
    python "$SCRIPT_DIR/java_security.py" "$@"
else
    echo "[!] Python bulunamadı. Temel GİB/UYAP siteleri doğrudan ekleniyor..."
    cat << 'EOF' >> "$EXC_FILE"
https://uyap.gov.tr
https://avukat.uyap.gov.tr
https://vatandas.uyap.gov.tr
https://kurum.uyap.gov.tr
https://intvd.gib.gov.tr
https://ivd.gib.gov.tr
https://dijital.gib.gov.tr
https://edefter.gov.tr
https://efatura.gov.tr
https://ebildirge.sgk.gov.tr
https://medula.sgk.gov.tr
https://mersis.gtb.gov.tr
https://kamusm.bilgem.tubitak.gov.tr
EOF
    sort -u "$EXC_FILE" -o "$EXC_FILE"
    echo "[OK] Temel siteler eklendi: $EXC_FILE"

    if [ "$1" = "--clear-cache" ] || [ "$2" = "--clear-cache" ]; then
        if [ -d "$CACHE_DIR" ]; then
            rm -rf "${CACHE_DIR:?}"/*
            echo "[OK] Java önbelleği temizlendi."
        fi
    fi
fi
