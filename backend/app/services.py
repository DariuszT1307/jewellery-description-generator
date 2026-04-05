from dotenv import load_dotenv
from pathlib import Path

# override=True — .env zawsze nadpisuje zmienne systemowe
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path, override=True)

import json
import logging
import os

from openai import OpenAI

from .schemas import GenerateRequest, GenerateResponse
from .knowledge_service import get_context

logger = logging.getLogger(__name__)


def _get_client() -> OpenAI:
    """Tworzy klienta OpenAI z aktualnym kluczem z env."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Brak OPENAI_API_KEY w pliku .env")
    return OpenAI(api_key=api_key)


def _format_stone_data(stone_data: dict) -> str:
    m = stone_data.get("metaphysical", {})
    color = stone_data.get("color", {})
    return "\n".join(filter(None, [
        f"Kamień: {stone_data.get('name', '')} ({stone_data.get('name_en', '')})",
        f"Kolor: {color.get('primary', '')}",
        f"Chakry: {', '.join(m.get('chakra', []))}",
        f"Znaczenie: {', '.join(m.get('meaning', []))}",
        f"Działanie: {m.get('healing', '')}",
        f"Znaki zodiaku: {', '.join(stone_data.get('zodiac', []))}",
        f"Słowa kluczowe: {', '.join(stone_data.get('keywords', []))}",
    ]))


def _format_examples(examples: list[dict]) -> str:
    parts = []
    for i, ex in enumerate(examples, 1):
        out = ex.get("output", {})
        meta = ex.get("_meta", {})
        parts.append(
            f"--- PRZYKŁAD {i} (focus: {meta.get('focus', '')}) ---\n"
            f"Tytuł: {out.get('title', '')}\n"
            f"Krótki opis:\n{out.get('shortDescription', '')}\n"
            f"Długi opis:\n{out.get('longDescription', '')}"
        )
    return "\n\n".join(parts)


def build_prompt(request: GenerateRequest, context: dict) -> tuple[str, str]:
    stone_data = context.get("stone_data") or {}
    examples = context.get("examples") or []

    system = (
        "Jesteś ekspertem od copywritingu biżuterii handmade na Etsy. "
        "Piszesz wyłącznie po polsku. Styl naturalny, konkretny, bez ogólników. "
        "Znasz właściwości kamieni i ich znaczenie energetyczne. "
        "Odpowiadasz TYLKO czystym JSON bez markdown."
    )

    sections = []

    sections.append(
        "## DANE PRODUKTU\n"
        f"Typ: {request.productType}\n"
        f"Nazwa: {request.productName}\n"
        f"Kamień: {request.stone}"
        + (f"\nSłowa kluczowe: {request.keywords}" if request.keywords else "")
        + (f"\nNotatki: {request.notes}" if request.notes else "")
    )

    if stone_data:
        sections.append(f"## DANE KAMIENIA\n{_format_stone_data(stone_data)}")

    if examples:
        sections.append(f"## PRZYKŁADY (wzorzec stylu i struktury)\n{_format_examples(examples)}")

    sections.append(
        "## ZASADY\n"
        "1. Tytuł: 'Bransoletka z [kamień w NARZĘDNIKU]' — np. 'z ametystem', NIE 'z ametystu'\n"
        "2. shortDescription: dokładnie 3 zdania oddzielone \\n:\n"
        "   (1) 'Miedziana bransoletka z [kamień] – miedź wykazuje właściwości antybakteryjne i przeciwzapalne, w biżuterii wzmacnia działanie kamieni.'\n"
        "   (2) '[Kamień] to kamień [cechy], [działanie].'\n"
        "   (3) 'Dla: [znaki zodiaku], ale pasuje każdemu, jeśli rezonuje.'\n"
        "3. longDescription: sekcje oddzielone \\n\\n w kolejności:\n"
        "   intro → talizman → 'Właściwości miedzi' → 'Szczegóły produktu' → 'Dla kogo' → 'Styl' → uwaga o kolorach\n"
        "4. Styl zawsze kończy się: 'Kolory na zdjęciach mogą się różnić, ponieważ miedź jest wrażliwa na światło i nawet zmiana otoczenia i tła wpływa na jej odcień.'\n"
        "5. bullets: 5 punktów, konkretnych, bez gwiazdek"
    )

    sections.append(
        "## FORMAT ODPOWIEDZI\n"
        + json.dumps({
            "title": "string",
            "shortDescription": "string — 3 zdania oddzielone \\n",
            "bullets": ["string x5"],
            "longDescription": "string — sekcje oddzielone \\n\\n",
            "specs": {
                "materiał": "miedź",
                "kamień": "string",
                "wykonanie": "ręczne, wire wrapping",
                "obwód": "ok. 17 cm (możliwość dopasowania)"
            }
        }, ensure_ascii=False, indent=2)
        + "\n\nWygeneruj opis. Odpowiedz TYLKO czystym JSON."
    )

    return system, "\n\n".join(sections)


def call_openai(system_prompt: str, user_prompt: str) -> dict:
    response = _get_client().chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.7,
        response_format={"type": "json_object"},
    )
    return json.loads(response.choices[0].message.content)


def parse_model_output(model_data: dict, request: GenerateRequest) -> GenerateResponse:
    # Szukamy specs pod różnymi możliwymi nazwami kluczy
    specs = (
        model_data.get("specs")
        or model_data.get("szczegoly")
        or model_data.get("szczegóły")
        or model_data.get("details")
        or {
            "materiał": "miedź",
            "kamień": request.stone,
            "wykonanie": "ręczne, wire wrapping",
            "obwód": "ok. 17 cm (możliwość dopasowania)",
        }
    )
    if not isinstance(specs, dict):
        specs = {"materiał": "miedź", "kamień": request.stone}

    return GenerateResponse(
        title=model_data.get("title", ""),
        shortDescription=model_data.get("shortDescription", ""),
        bullets=model_data.get("bullets", []),
        longDescription=model_data.get("longDescription", ""),
        specs=specs,
        source=request,
        status="completed",
    )


def validate_output(response: GenerateResponse) -> None:
    if not response.title.strip():
        raise ValueError("title is empty")
    if not response.shortDescription.strip():
        raise ValueError("shortDescription is empty")
    if not response.bullets or not all(b.strip() for b in response.bullets):
        raise ValueError("bullets are invalid")
    if not response.longDescription.strip():
        raise ValueError("longDescription is empty")
    if not isinstance(response.specs, dict):
        raise ValueError("specs must be a dict")


def generate_description(request: GenerateRequest) -> GenerateResponse:
    context = get_context(request.productType, request.stone)
    system_prompt, user_prompt = build_prompt(request, context)
    logger.info(
        "Prompt zbudowany | kamień: %s | przykłady: %d | stone_data: %s",
        request.stone,
        len(context.get("examples", [])),
        "tak" if context.get("stone_data") else "nie",
    )
    model_data = call_openai(system_prompt, user_prompt)
    logger.info("Odpowiedź modelu — klucze: %s", list(model_data.keys()))
    response = parse_model_output(model_data, request)
    validate_output(response)
    return response
