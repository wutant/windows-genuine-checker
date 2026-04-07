@echo off
setlocal

echo ================================
echo Build Windows Genuine Checker EXE
echo ================================

where py >nul 2>nul
if %errorlevel% neq 0 (
  echo [ERROR] ไม่พบ Python launcher (py)
  echo กรุณาติดตั้ง Python for Windows ก่อน
  pause
  exit /b 1
)

py -m pip install --upgrade pip
py -m pip install pyinstaller

py -m PyInstaller ^
  --noconfirm ^
  --onefile ^
  --windowed ^
  --name "WindowsGenuineChecker" ^
  --icon "assets\icons\app-icon.ico" ^
  --add-data "assets\fonts\Sarabun-Regular.ttf;assets\fonts" ^
  --add-data "assets\fonts\Sarabun-Bold.ttf;assets\fonts" ^
  --add-data "assets\icons\app-icon.ico;assets\icons" ^
  --add-data "assets\icons\app-icon.png;assets\icons" ^
  "windows_genuine_checker.py"

echo.
echo เสร็จแล้ว
echo ไฟล์ EXE อยู่ที่ dist\WindowsGenuineChecker.exe
pause
