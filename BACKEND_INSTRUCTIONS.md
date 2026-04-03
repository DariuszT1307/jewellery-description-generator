# BACKEND_INSTRUCTIONS

## Cel tego pliku
Ten plik definiuje zasady budowy backendu dla aplikacji generującej opisy produktów biżuterii handmade.

Backend ma być prosty, przewidywalny i łatwy do rozwijania.
Backend NIE ma być rozbudowaną platformą AI.
Backend NIE ma być systemem wieloagentowym.
Backend ma obsługiwać jeden kontrolowany workflow.

---

## Główny cel backendu
Backend ma pełnić rolę warstwy pośredniej między frontendem a OpenAI API.

Backend odpowiada za:
1. przyjęcie danych z frontendu,
2. podstawową walidację wejścia,
3. zbudowanie kontrolowanego promptu dla modelu,
4. wywołanie OpenAI API,
5. walidację odpowiedzi modelu,
6. zwrócenie stabilnego JSON do frontendu.

Najważniejsza zasada:
AI nie może być wywoływane bezpośrednio z frontendu.
Cała logika przygotowania danych i kontroli odpowiedzi ma być po stronie backendu.

---

## Filozofia backendu
Backend ma być:
- prosty,
- czytelny,
- mały,
- łatwy do testowania,
- łatwy do rozbudowy etapami.

Preferuj:
- małe kroki,
- małą liczbę plików,
- prostą strukturę,
- jasne nazwy funkcji,
- przewidywalne zachowanie.

Unikaj:
- overengineeringu,
- architektury enterprise na start,
- zbędnych warstw,
- abstrakcji "na zapas",
- mikroserwisów,
- skomplikowanego dependency injection,
- repozytoriów, fabryk i wzorców, jeśli nie są jeszcze potrzebne.

---

## Stack technologiczny
Preferowany stack:
- Python
- FastAPI
- Pydantic

Na obecnym etapie:
- bez bazy SQL
- bez Redis
- bez Celery
- bez cache
- bez kolejki
- bez ORM
- bez async komplikacji, jeśli nie jest konieczne

---

## Aktualny zakres backendu
Na obecnym etapie backend ma obsługiwać tylko jeden główny endpoint:

`POST /generate`

Ten endpoint:
- przyjmuje dane produktu,
- buduje prompt,
- wywołuje OpenAI,
- odbiera odpowiedź,
- waliduje wynik,
- zwraca JSON do frontendu.

Nie dodawaj innych endpointów, jeśli nie zostało to wyraźnie zlecone.

---

## Zakres odpowiedzialności backendu

### Backend MA robić:
- odbierać request z frontendu,
- walidować wymagane pola,
- budować jeden przewidywalny prompt,
- wywoływać OpenAI API,
- parsować odpowiedź,
- walidować strukturę i podstawową jakość outputu,
- zwracać stabilny response JSON.

### Backend NIE MA jeszcze robić:
- logowania,
- kont użytkowników,
- przechowywania historii,
- uploadu plików do storage,
- rozbudowanej autoryzacji,
- pracy na wielu modelach,
- retrieval z vector database,
- file_search,
- automatycznego wybierania wielu workflow,
- asynchronicznych kolejek zadań,
- skomplikowanego pipeline orchestration.

---

## Główny workflow backendu

### Krok 1
Odbierz request JSON z frontendu.

### Krok 2
Zweryfikuj podstawowe pola wejściowe.

### Krok 3
Zbuduj kontrolowany prompt dla modelu.

### Krok 4
Wywołaj OpenAI API.

### Krok 5
Odbierz odpowiedź modelu.

### Krok 6
Spróbuj sparsować odpowiedź do ustalonego JSON.

### Krok 7
Zweryfikuj output:
- kompletność pól,
- poprawność struktury,
- brak zakazanych fraz.

### Krok 8
Zwróć odpowiedź do frontendu.

Backend ma zawsze działać w tej kolejności.

---

## Architektura backendu
Na obecnym etapie preferowana jest minimalna struktura:

```text
backend/
  app/
    main.py
    schemas.py
    services.py

Jesli kod zacznie byc zbyt duzy przejdz do 

backend/
  app/
    main.py
    schemas.py
    prompt_builder.py
    openai_client.py
    validator.py