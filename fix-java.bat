@echo off
chcp 65001 >nul
title GIB & UYAP Java Guvenlik Engeli Cozucu
echo =================================================================
echo  GIB, UYAP, E-Defter Java Guvenlik Engeli Cozucu Calistiriliyor...
echo =================================================================
echo.

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0Fix-JavaSecurity.ps1"

echo.
pause
