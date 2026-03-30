# PROJECT_PLAN

## Nazwa projektu
Generator opisów produktów biżuterii handmade

## Główny cel projektu
Zbudować prostą, przewidywalną aplikację webową do generowania opisów produktów dla sklepu internetowego z ręcznie robioną biżuterią.

Aplikacja ma wspierać jeden kontrolowany workflow:
1. użytkownik podaje dane produktu,
2. system dobiera kontekst,
3. system generuje opis produktu,
4. użytkownik otrzymuje gotowy wynik.

To NIE jest chatbot.  
To NIE jest system multi-agentowy.  
To NIE jest uniwersalny asystent AI.  

To jest aplikacja do jednego, konkretnego zadania: generowania opisów produktów.

---

## Kontekst biznesowy
Sklep sprzedaje ręcznie robioną biżuterię z drutu i kamieni.

Docelowo opisy produktów mają być tworzone na podstawie:
- wiedzy o kamieniach,
- przykładowych opisów już używanych w sklepie,
- zasad stylu marki,
- zasad SEO,
- zasad compliance / bezpieczeństwa treści,
- opcjonalnych zdjęć referencyjnych.

Opisy mają być:
- spójne stylistycznie,
- przewidywalne,
- użyteczne marketingowo,
- zgodne z ustalonym tonem marki,

---

## Główna filozofia projektu
Projekt ma być budowany etapami.

Priorytety:
1. działanie,
2. prostota,
3. przewidywalność,
4. czytelność,
5. łatwość rozbudowy później.

Należy unikać:
- overengineeringu,
- budowania funkcji “na zapas”,
- nadmiernej abstrakcji,
- skomplikowanej architektury na starcie,
- zbyt wczesnego dzielenia projektu na wiele warstw i modułów.

---

## Zakres całego systemu
System docelowo składa się z 4 głównych części:

### 1. Frontend
Strona webowa z formularzem do wpisywania danych produktu.

### 2. Backend
API przyjmujące dane z frontendu, przygotowujące kontekst i zwracające wygenerowany wynik.

### 3. Lokalna baza wiedzy
Uporządkowany zbiór plików z:
- wiedzą o kamieniach,
- przykładami opisów,
- politykami i zasadami.

### 4. Warstwa AI
Logika generowania opisu produktu na podstawie danych wejściowych i kontekstu.

---

# ETAPY REALIZACJI

## Etap 1 — Frontend MVP
Na początku budujemy tylko prosty frontend.

### Cel etapu
Stworzyć jedną stronę z formularzem wejściowym.

### Frontend MVP ma umożliwiać:
- wybór typu produktu,
- wybór kamienia,
- wpisanie nazwy roboczej,
- dodanie opcjonalnych słów / motywów,
- dodanie opcjonalnych notatek,
- wrzucenie zdjęć referencyjnych,
- kliknięcie przycisku „Generuj”,
- zobaczenie payloadu lub mock odpowiedzi.

### Zakres etapu
W ZAKRESIE:
- React
- jedna strona
- jeden formularz
- local state (`useState`)
- upload zdjęć
- podgląd wybranych plików
- przycisk submit
- prosty preview payloadu / odpowiedzi

POZA ZAKRESEM:
- logowanie
- backend
- integracja z OpenAI
- baza danych
- routing wielu stron
- panel admina
- historia generacji
- deploy produkcyjny

---

## Etap 2 — Backend MVP
Po gotowym frontendzie budujemy prosty backend.

### Cel etapu
Stworzyć bardzo prosty backend API, który:
- przyjmie dane z formularza,
- zweryfikuje wejście,
- zwróci mock odpowiedź JSON.

### Backend MVP ma:
- działać lokalnie,
- mieć jeden główny endpoint,
- przyjmować request JSON,
- zwracać response JSON.

### Preferowana technologia
- Python
- FastAPI

### Główny endpoint
`POST /generate`

### Zakres backend MVP
W ZAKRESIE:
- prosty serwer API,
- endpoint `POST /generate`,
- podstawowa walidacja danych,
- mock odpowiedź,
- struktura kodu łatwa do dalszej rozbudowy.

POZA ZAKRESEM:
- autoryzacja,
- baza SQL,
- kolejki,
- cache,
- mikroserwisy,
- zaawansowana architektura,
- upload plików do storage,
- integracja z OpenAI na tym etapie.

---

## Etap 3 — Integracja frontend + backend
Po zbudowaniu frontend MVP i backend MVP należy je połączyć.

### Cel etapu
Zamiast lokalnego mocka frontend ma wysyłać request do backendu.

### Etap obejmuje:
- wywołanie `POST /generate` z frontendu,
- obsługę loading state,
- obsługę odpowiedzi JSON,
- wyświetlenie wyniku na stronie.

---

## Etap 4 — Baza wiedzy
Po działającej integracji frontend-backend budujemy bazę wiedzy.

### Cel etapu
Przygotować uporządkowaną lokalną strukturę plików, z której backend będzie pobierał kontekst.

### Baza wiedzy ma zawierać:
- wiedzę o kamieniach,
- przykładowe opisy produktów,
- reguły stylu marki,
- reguły SEO,
- zasady compliance,
- schematy wejścia i wyjścia.

### Proponowana struktura
```text
knowledge_base/
  stones/
    akwamaryn/
      stone.json
    ametyst/
      stone.json

  examples/
    bracelet/
      akwamaryn_01/
        input.json
        short_description.md
        long_description.md
        seo.json
        image_notes.md
        images/

  policies/
    brand_voice.md
    seo_rules.md
    compliance.md
    output_rules.md
    forbidden_phrases.md

  schemas/
    product_input.schema.json
    product_output.schema.json
    stone.schema.json
    example.schema.json