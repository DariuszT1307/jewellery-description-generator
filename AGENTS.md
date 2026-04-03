# INSTRUCTIONS

## Rola agenta
Pomagasz budować aplikację do generowania opisów produktów biżuterii handmade.

Aplikacja docelowo składa się z:
- frontendu webowego
- backendu API
- logiki generowania opisów
- integracji z bazą wiedzy
- później integracji z OpenAI API

To NIE jest chatbot.
To NIE jest system multi-agentowy.
To jest jedna aplikacja z jednym kontrolowanym workflow.

---

## Główny cel
Zbudować prostą, przewidywalną i łatwą do rozwijania aplikację.

Priorytety:
1. poprawne działanie
2. prostota
3. czytelność
4. łatwość rozbudowy później

---

## Główna filozofia projektu

Zawsze preferuj:
- prostsze rozwiązania
- małe kroki
- czytelny kod
- minimalny zakres na dany etap
- przewidywalny workflow

Unikaj:
- overengineeringu
- zbyt wczesnej abstrakcji
- budowania funkcji "na zapas"
- tworzenia architektury większej niż potrzebna

---

## Zasada etapów

Projekt realizujemy etapami.

### Etap 1
Frontend MVP:
- jedna strona
- jeden formularz
- upload zdjęć
- podgląd payloadu

### Etap 2
Backend MVP:
- instrukcje zwiazane z backendem sprawdz w BACKEND_INSTRUCTIONS.md
- proste API
- przyjęcie danych z formularza
- walidacja wejścia
- mock odpowiedź

### Etap 3
Integracja frontend + backend

### Etap 4
Warstwa danych:
- baza wiedzy o kamieniach
- przykładowe opisy
- polityki i instrukcje

### Etap 5
Integracja z OpenAI API

### Etap 6
Walidacja i dopracowanie workflow

Nie pomijaj etapów.
Nie wdrażaj późniejszych etapów bez wyraźnej potrzeby.

---

## Zasady dla frontendu

Frontend ma być:
- prosty
- czytelny
- beginner-friendly
- oparty na React
- napisany w JavaScript, nie TypeScript

Frontend na obecnym etapie:
- nie zawiera logiki AI
- nie zawiera backendowej logiki biznesowej
- nie zawiera routingu wielu stron
- nie zawiera global state management
- nie zawiera skomplikowanej architektury

Dopuszczalne:
- useState
- prosty formularz
- upload plików
- payload preview
- lekki refactor

---

## Zasady dla backendu

Backend ma być:
- prosty
- przewidywalny
- oparty na Pythonie
- łatwy do testowania
- łatwy do rozbudowy

Preferowany stack backendowy:
- Python
- FastAPI

Backend na etapie MVP ma:
- udostępniać proste endpointy HTTP
- przyjmować dane z frontendu
- zwracać JSON
- zawierać prostą walidację
- na początku zwracać mock odpowiedzi

Backend na początku NIE ma:
- skomplikowanej autoryzacji
- bazy danych SQL
- kolejek
- cache
- mikroserwisów
- asynchronicznej architektury
- złożonych warstw domenowych

---

## Docelowy workflow aplikacji

1. Użytkownik otwiera frontend
2. Wypełnia formularz
3. Dodaje opcjonalne zdjęcia
4. Frontend buduje request
5. Frontend wysyła request do backendu
6. Backend waliduje dane
7. Backend pobiera odpowiedni kontekst z lokalnej bazy wiedzy
8. Backend buduje wejście dla modelu
9. Backend generuje odpowiedź
10. Backend zwraca wynik JSON
11. Frontend pokazuje wynik użytkownikowi

Na początku można mockować kroki 7-10.

---

## Baza wiedzy i dane

Docelowo aplikacja będzie korzystać z lokalnej, uporządkowanej bazy plików.

Dane będą podzielone na:
- stones/
- examples/
- policies/
- schemas/

Na początku nie buduj pełnej logiki odczytu tych danych, jeśli aktualny etap tego nie wymaga.

---

## Zasady implementacji backendu

Jeśli pracujesz nad backendem:
- zaczynaj od najprostszego endpointu
- utrzymuj małą liczbę plików
- nie komplikuj struktury katalogów
- zwracaj JSON
- waliduj wymagane pola
- rozdzielaj kod dopiero wtedy, gdy faktycznie robi się zbyt duży

Na start preferowana struktura:

```text
backend/
  app/
    main.py
    schemas.py
    services.py