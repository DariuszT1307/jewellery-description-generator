@echo off
chcp 65001 >nul
title Jewellery Description Generator

:: ============================================================
::  Kolory (ANSI - dziala w Windows 10+ i Windows Terminal)
:: ============================================================
set "GREEN=[92m"
set "YELLOW=[93m"
set "RED=[91m"
set "CYAN=[96m"
set "RESET=[0m"

echo.
echo %CYAN%============================================================%RESET%
echo %CYAN%   Jewellery Description Generator - Uruchamianie...%RESET%
echo %CYAN%============================================================%RESET%
echo.

:: ============================================================
::  Sprawdz Python
:: ============================================================
echo %YELLOW%[1/5] Sprawdzam Python...%RESET%
python --version >nul 2>&1
if errorlevel 1 (
    echo %RED%[BLAD] Python nie jest zainstalowany!%RESET%
    echo %RED%       Pobierz ze strony: https://www.python.org/downloads/%RESET%
    echo %RED%       Pamietaj o zaznaczeniu "Add Python to PATH"%RESET%
    pause
    exit /b 1
)
for /f "tokens=*" %%v in ('python --version 2^>^&1') do echo %GREEN%[OK] %%v%RESET%

:: ============================================================
::  Sprawdz Node.js / npm
:: ============================================================
echo %YELLOW%[2/5] Sprawdzam Node.js...%RESET%
node --version >nul 2>&1
if errorlevel 1 (
    echo %RED%[BLAD] Node.js nie jest zainstalowany!%RESET%
    echo %RED%       Pobierz ze strony: https://nodejs.org/%RESET%
    pause
    exit /b 1
)
for /f "tokens=*" %%v in ('node --version 2^>^&1') do echo %GREEN%[OK] Node.js %%v%RESET%

:: ============================================================
::  Wczytaj OPENAI_API_KEY z backend/.env
:: ============================================================
echo %YELLOW%[3/5] Wczytuje klucz API...%RESET%
set "ENV_FILE=%~dp0backend\.env"

if not exist "%ENV_FILE%" (
    echo %RED%[BLAD] Brak pliku backend\.env !%RESET%
    echo %RED%       Stworz plik backend\.env z linia:%RESET%
    echo %RED%       OPENAI_API_KEY=sk-proj-...%RESET%
    pause
    exit /b 1
)

for /f "usebackq tokens=1,* delims==" %%a in ("%ENV_FILE%") do (
    set "KEY=%%a"
    set "VAL=%%b"
    :: Usun biale znaki z nazwy klucza
    set "KEY=%%a"
    if /i "%%a"=="OPENAI_API_KEY" (
        set "OPENAI_API_KEY=%%b"
    )
)

if "%OPENAI_API_KEY%"=="" (
    echo %RED%[BLAD] OPENAI_API_KEY nie znaleziony w backend\.env !%RESET%
    pause
    exit /b 1
)

:: Pokaz tylko poczatek klucza dla potwierdzenia (bezpieczenstwo)
set "KEY_PREVIEW=%OPENAI_API_KEY:~0,12%..."
echo %GREEN%[OK] Klucz API wczytany: %KEY_PREVIEW%%RESET%

:: ============================================================
::  Uruchom backend w tle
:: ============================================================
echo %YELLOW%[4/5] Uruchamiam backend (FastAPI)...%RESET%
cd /d "%~dp0backend"
start "Backend - FastAPI" cmd /k "title Backend ^& python -m uvicorn app.main:app --reload"
echo %GREEN%[OK] Backend uruchomiony w osobnym oknie%RESET%

:: ============================================================
::  Czekaj 3 sekundy
:: ============================================================
echo %YELLOW%      Czekam az backend sie uruchomi (3s)...%RESET%
timeout /t 3 /nobreak >nul

:: ============================================================
::  Uruchom frontend
:: ============================================================
echo %YELLOW%[5/5] Uruchamiam frontend (Vite / React)...%RESET%
cd /d "%~dp0frontend"

:: Sprawdz czy node_modules istnieje
if not exist "node_modules" (
    echo %YELLOW%      Instaluje pakiety npm (pierwsze uruchomienie)...%RESET%
    npm install
    if errorlevel 1 (
        echo %RED%[BLAD] npm install zakonczony bledem!%RESET%
        pause
        exit /b 1
    )
)

:: Uruchom frontend (w tym samym oknie - Ctrl+C zatrzyma)
echo.
echo %CYAN%============================================================%RESET%
echo %GREEN%  Aplikacja dziala!%RESET%
echo %GREEN%  Frontend: http://localhost:5173%RESET%
echo %GREEN%  Backend:  http://localhost:8000%RESET%
echo %GREEN%  API docs: http://localhost:8000/docs%RESET%
echo %CYAN%============================================================%RESET%
echo %YELLOW%  Nacisnij Ctrl+C aby zatrzymac frontend%RESET%
echo %YELLOW%  Zamknij okno "Backend - FastAPI" aby zatrzymac backend%RESET%
echo %CYAN%============================================================%RESET%
echo.

:: Otworz przegladarke po 4 sekundach (po starcie Vite)
start "" cmd /c "timeout /t 4 /nobreak >nul && start http://localhost:5173"

npm run dev
