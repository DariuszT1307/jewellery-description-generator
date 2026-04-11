# Jewellery Description Generator — Instrukcja uruchomienia

Aplikacja generuje opisy biżuterii na Etsy za pomocą AI (ChatGPT).

---

## Wymagania (zainstaluj raz)

### 1. Python 3.10 lub nowszy

1. Wejdź na stronę: **https://www.python.org/downloads/**
2. Pobierz i uruchom instalator
3. **WAŻNE:** zaznacz opcję **"Add Python to PATH"** przed kliknięciem Install

Sprawdź instalację — otwórz wiersz poleceń (`Win + R` → wpisz `cmd` → Enter) i wpisz:
```
python --version
```
Powinno pojawić się np. `Python 3.12.0`

---

### 2. Node.js (wersja LTS)

1. Wejdź na stronę: **https://nodejs.org/**
2. Kliknij duży przycisk **"Download Node.js (LTS)"**
3. Uruchom instalator i kliknij Next do końca

Sprawdź instalację:
```
node --version
```
Powinno pojawić się np. `v22.0.0`

---

## Pierwsze uruchomienie — sklonuj projekt

### Opcja A: Przez Git (jeśli masz zainstalowanego Git)
```
git clone https://github.com/TwojeRepo/jewellery-description-generator.git
```

### Opcja B: Pobierz jako ZIP
1. Wejdź na stronę projektu na GitHub
2. Kliknij zielony przycisk **Code** → **Download ZIP**
3. Wypakuj archiwum w wybranym miejscu na dysku

---

## Konfiguracja klucza API

Klucz OpenAI jest już skonfigurowany w pliku `backend/.env`.  
Jeśli chcesz go zmienić (np. po wygaśnięciu):

1. Otwórz plik `backend/.env` w Notatniku
2. Zmień wartość po znaku `=`:
   ```
   OPENAI_API_KEY=sk-proj-TwojNowyKlucz
   ```
3. Zapisz plik

---

## Uruchomienie aplikacji

### Jeden dubel-klik!

Kliknij dwa razy na plik **`start.bat`** w głównym folderze projektu.

Otworzy się kilka okien — to normalne:
- **Okno "Backend - FastAPI"** — serwer API (nie zamykaj go)
- **Okno terminala** — frontend (nie zamykaj go)
- **Przeglądarka** z aplikacją otwarta automatycznie

> Przy **pierwszym uruchomieniu** instalacja pakietów npm może potrwać kilka minut.

---

## Jak korzystać z aplikacji

1. Wpisz nazwę produktu i opis kamieni / materiałów
2. Kliknij **"Generuj opis"**
3. Poczekaj kilka sekund — AI wygeneruje opis
4. Skopiuj gotowy tekst i wklej na Etsy

---

## Zatrzymanie aplikacji

Aby zatrzymać aplikację:

1. **Frontend** — kliknij w okno terminala i naciśnij `Ctrl + C`
2. **Backend** — zamknij okno **"Backend - FastAPI"** (kliknij X)

Lub po prostu zamknij oba okna terminala.

---

## Adresy aplikacji

| Usługa | Adres |
|--------|-------|
| Aplikacja (frontend) | http://localhost:5173 |
| API (backend) | http://localhost:8000 |
| Dokumentacja API | http://localhost:8000/docs |

---

## Rozwiązywanie problemów

**"Python nie jest zainstalowany"**
→ Zainstaluj Python ze strony python.org, pamiętaj o "Add to PATH"

**"Node.js nie jest zainstalowany"**
→ Zainstaluj Node.js ze strony nodejs.org

**"Brak pliku backend\.env"**
→ Skontaktuj się z Dariuszem — potrzebny jest plik z kluczem API

**Przeglądarka się nie otworzyła**
→ Ręcznie wejdź na adres: http://localhost:5173

**Backend nie startuje (błąd w oknie FastAPI)**
→ Sprawdź czy klucz API w `backend/.env` jest poprawny

---

*Aplikacja stworzona przez Dariusza T.*
