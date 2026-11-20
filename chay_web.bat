@echo off
chcp 65001 >nul
rem Ban web (M12): dong goi game cho trinh duyet roi mo may chu cho ca Wi-Fi.
rem Dien thoai mo  http://<dia chi may nay>:8000/web/  (xem docs\WEB_BUILD.md)
cd /d %~dp0
python -m pip install -r server\requirements.txt
if errorlevel 1 (
  echo [LOI] Cai thu vien that bai. Hay chup man hinh cua so nay gui lai.
  pause
  exit /b 1
)
python tools\build_web.py serve
echo.
echo [!] May chu da dung. Neu ben tren co chu "Error" hoac "Traceback", hay chup man hinh gui lai.
pause
