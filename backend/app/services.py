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
        lines = [f"--- PRZYKŁAD {i} (focus: {meta.get('focus', '')}) ---"]
        lines.append(f"Tytuł: {out.get('title', '')}")
        if out.get("shortDescription"):
            lines.append(f"shortDescription:\n{out['shortDescription']}")
        if out.get("longDescription"):
            lines.append(f"longDescription:\n{out['longDescription']}")
        parts.append("\n".join(lines))
    return "\n\n".join(parts)


_WYMIARY = {
    "bracelet":  "obwód ok. 17 cm z możliwością regulacji",
    "bransoletka": "obwód ok. 17 cm z możliwością regulacji",
    "necklace":  "długość łańcuszka ok. 45 cm, można skrócić",
    "naszyjnik": "długość łańcuszka ok. 45 cm, można skrócić",
    "earrings":  "długość ok. 4 cm",
    "kolczyki":  "długość ok. 4 cm",
    "ring":      "rozmiar do ustalenia przy zamówieniu",
    "pierścionek": "rozmiar do ustalenia przy zamówieniu",
}


def _wymiar(product_type: str) -> str:
    return _WYMIARY.get(product_type.lower(), "rozmiar do ustalenia przy zamówieniu")


def _build_prompt_single(request: GenerateRequest, stone_data: dict, examples: list[dict]) -> tuple[str, str]:
    """Prompt dla produktu z jednym kamieniem."""
    system = (
        "Jesteś copywriterem biżuterii handmade na Etsy. Piszesz po polsku. "
        "Styl: konkretny, sprzedażowy, bez patosu. "
        "Wplatasz naturalne słowa kluczowe SEO (ręcznie robiony, biżuteria boho, "
        "wire wrapping, prezent dla niej, naturalne kamienie). "
        "Odpowiadasz TYLKO czystym JSON bez żadnego markdown."
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

    wymiar = _wymiar(request.productType)

    sections.append(
        "## ZASADY\n"
        "\n"
        "GRAMATYKA:\n"
        "- Po 'z naturalnym' → narzędnik: 'z naturalnym ametystem' NIE 'z naturalnego ametystu'\n"
        "- Po 'dla' → dopełniacz: 'dla Ryb, Wodnika, Koziorożca' NIE 'dla Ryby, Wodnik'\n"
        "- W specyfikacji 'naturalny [kamień]' → mianownik: 'naturalny ametyst'\n"
        "\n"
        "TYTUŁ: '[Typ] z [kamień NARZĘDNIK] w miedzianym splocie'\n"
        "   Przykład: 'Bransoletka z ametystem w miedzianym splocie'\n"
        "\n"
        "SHORT DESCRIPTION — 4 akapity oddzielone pustą linią:\n"
        "   (1) Nagłówek = tytuł produktu\n"
        "   (2) 'Ręcznie robiona [typ] z naturalnym [kamień NARZĘDNIK]. Lekki/a i wygodny/a w noszeniu, "
        "pasuje do różnych stylizacji. Miedź działa antybakteryjnie i wzmacnia działanie kamienia.'\n"
        "   (3) '**[Nazwa kamienia]** [właściwości – 1 zdanie].'\n"
        "   (4) 'Doskonały prezent dla niej.' + nowa linia + "
        "'[Typ] dla [znaki zodiaku DOPEŁNIACZ], ale jeśli czujesz przyciąganie – to jest dla Ciebie.'\n"
        "\n"
        "LONG DESCRIPTION — 6 sekcji oddzielonych pustą linią:\n"
        "   (1) Opis produktu (1-2 zdania): "
        "'Ręcznie robiony/a [typ] z naturalnym [kamień NARZĘDNIK] i miedzią. "
        "Biżuteria boho wykonana techniką wire wrapping.'\n"
        "   (2) Sekcja miedzi z nagłówkiem i 3 bulletami:\n"
        "       '**Miedź** – naturalny przewodnik energii'\n"
        "       '- Działa antybakteryjnie i przeciwzapalnie'\n"
        "       '- Wzmacnia działanie kamieni'\n"
        "       '- Wspiera organizm'\n"
        "   (3) Sekcja kamienia z nagłówkiem i 3 bulletami:\n"
        "       '**[Nazwa kamienia]** – kamień [główna właściwość]'\n"
        "       '- [właściwość 1]'\n"
        "       '- [właściwość 2]'\n"
        "       '- [właściwość 3]'\n"
        "   (4) Specyfikacja (każde pole w osobnej linii):\n"
        f"       '**Materiał:** czysta miedź, naturalny [kamień MIANOWNIK]'\n"
        f"       '**Rozmiar:** {wymiar}'\n"
        "       '**Wykonanie:** 100% ręcznie robiony'\n"
        "       '**Technika:** wire wrapping'\n"
        "   (5) Dla kogo i prezent (3 linie):\n"
        "       '[Typ] dla [znaki DOPEŁNIACZ].'\n"
        "       'Doskonały prezent dla niej – na urodziny, rocznicę, Dzień Matki lub po prostu tak.'\n"
        "       'Biżuteria boho pasująca do casualowych i eleganckich stylizacji.'\n"
        "   (6) '❣️ Kolory na zdjęciach mogą się różnić w zależności od ustawień monitora. "
        "Miedź reaguje na światło i otoczenie, co wpływa na jej odcień.'"
    )

    sections.append(
        "## FORMAT ODPOWIEDZI\n"
        + json.dumps({
            "title": "np. 'Bransoletka z ametystem w miedzianym splocie'",
            "shortDescription": "nagłówek\n\nRęcznie robiona...\n\n**Kamień** właściwości\n\nDoskonały prezent...\nBransoletka dla Ryb...",
            "longDescription": "Ręcznie robiona...\n\n**Miedź**...\n- bullet\n\n**Kamień**...\n- bullet\n\n**Materiał:**...\n\nBransoletka dla...\n\n❣️ Kolory...",
        }, ensure_ascii=False, indent=2)
        + "\n\nWygeneruj opis. Odpowiedz TYLKO czystym JSON."
    )

    return system, "\n\n".join(sections)


def _build_prompt_dual(
    request: GenerateRequest,
    stone_data: dict,
    stone2_data: dict,
    examples: list[dict],
) -> tuple[str, str]:
    """Prompt dla produktu z dwoma kamieniami."""
    system = (
        "Jesteś copywriterem biżuterii handmade na Etsy. Piszesz po polsku. "
        "Styl: konkretny, sprzedażowy, bez patosu. "
        "Wplatasz naturalne słowa kluczowe SEO (ręcznie robiony, biżuteria boho, "
        "wire wrapping, prezent dla niej, naturalne kamienie). "
        "Synergię kamieni opisujesz konkretnie – co użytkownik czuje i zyskuje, NIE ogólniki. "
        "Odpowiadasz TYLKO czystym JSON bez żadnego markdown."
    )

    sections = []

    sections.append(
        "## DANE PRODUKTU\n"
        f"Typ: {request.productType}\n"
        f"Nazwa: {request.productName}\n"
        f"Kamień 1: {request.stone}\n"
        f"Kamień 2: {request.stone2}"
        + (f"\nSłowa kluczowe: {request.keywords}" if request.keywords else "")
        + (f"\nNotatki: {request.notes}" if request.notes else "")
    )

    stone_sections = []
    if stone_data:
        stone_sections.append(f"KAMIEŃ 1:\n{_format_stone_data(stone_data)}")
    if stone2_data:
        stone_sections.append(f"KAMIEŃ 2:\n{_format_stone_data(stone2_data)}")
    if stone_sections:
        sections.append("## DANE KAMIENI\n" + "\n\n".join(stone_sections))

    if examples:
        sections.append(f"## PRZYKŁADY (wzorzec stylu i struktury)\n{_format_examples(examples)}")

    wymiar = _wymiar(request.productType)

    sections.append(
        "## ZASADY\n"
        "\n"
        "GRAMATYKA:\n"
        "- Po 'z naturalnym' → narzędnik: 'z naturalnym ametystem i kryształem górskim'\n"
        "- Po 'dla' → dopełniacz: 'dla Ryb, Wodnika'\n"
        "- W specyfikacji → mianownik: 'naturalny ametyst, kryształ górski'\n"
        "\n"
        "TYTUŁ: '[Typ] z [kamień1 NARZĘDNIK] i [kamień2 NARZĘDNIK] w miedzianym splocie'\n"
        "\n"
        "SHORT DESCRIPTION — 6 akapitów oddzielonych pustą linią:\n"
        "   (1) Nagłówek = tytuł\n"
        "   (2) 'Ręcznie robiona [typ] z naturalnym [kamień1 NARZĘDNIK] i [kamień2 NARZĘDNIK]. "
        "Biżuteria boho łącząca [opis połączenia]. Miedź wzmacnia działanie obu kamieni.'\n"
        "   (3) '**[Kamień1]** [właściwości – 1 zdanie].'\n"
        "   (4) '**[Kamień2]** [właściwości – 1 zdanie].'\n"
        "   (5) '**Połączenie [kamień1] i [kamień2]** – [konkretna synergia: co razem dają, "
        "NIE: 'tworzą harmonię', TAK: 'ametyst wycisza szum, kryształ wyostrza to co zostaje'].'\n"
        "   (6) 'Doskonały prezent dla niej.' + nowa linia + "
        "'[Typ] dla [znaki obu kamieni DOPEŁNIACZ bez duplikatów], ale jeśli czujesz przyciąganie – to jest dla Ciebie.'\n"
        "\n"
        "LONG DESCRIPTION — 7 sekcji oddzielonych pustą linią:\n"
        "   (1) 'Ręcznie robiona [typ] z naturalnym [kamień1 NARZĘDNIK] i [kamień2 NARZĘDNIK] oraz miedzią. "
        "Biżuteria boho wykonana techniką wire wrapping.'\n"
        "   (2) Miedź z 3 bulletami (jak w szablonie jednokamieniowym)\n"
        "   (3) Kamień1 z nagłówkiem i 3 bulletami\n"
        "   (4) Kamień2 z nagłówkiem i 3 bulletami\n"
        "   (5) '**Połączenie [kamień1] i [kamień2]** [2-3 zdania konkretnej synergii].'\n"
        f"   (6) Specyfikacja: '**Materiał:** czysta miedź, naturalny [kamień1 MIANOWNIK], [kamień2 MIANOWNIK]' "
        f"+ '**Rozmiar:** {wymiar}' + '**Wykonanie:** 100% ręcznie robiony' + '**Technika:** wire wrapping'\n"
        "   (7) Dla kogo (3 linie) + '❣️ Kolory...'\n"
        "\n"
        "SYNERGIA: konkretna – opisz co użytkownik zyskuje nosząc oba kamienie jednocześnie."
    )

    sections.append(
        "## FORMAT ODPOWIEDZI\n"
        + json.dumps({
            "title": "np. 'Bransoletka z ametystem i kryształem górskim w miedzianym splocie'",
            "shortDescription": "nagłówek\n\nRęcznie robiona...\n\n**Kamień1**\n\n**Kamień2**\n\n**Połączenie**\n\nDoskonały prezent...\nBransoletka dla...",
            "longDescription": "Ręcznie robiona...\n\n**Miedź**...\n- bullet\n\n**Kamień1**...\n- bullet\n\n**Kamień2**...\n- bullet\n\n**Połączenie**...\n\n**Materiał:**...\n\nBransoletka dla...\n\n❣️ Kolory...",
        }, ensure_ascii=False, indent=2)
        + "\n\nWygeneruj opis. Odpowiedz TYLKO czystym JSON."
    )

    return system, "\n\n".join(sections)


def build_prompt(request: GenerateRequest, context: dict) -> tuple[str, str]:
    stone_data = context.get("stone_data") or {}
    stone2_data = context.get("stone2_data") or {}
    examples = context.get("examples") or []

    if request.stone2 and stone2_data:
        return _build_prompt_dual(request, stone_data, stone2_data, examples)
    return _build_prompt_single(request, stone_data, examples)


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
    return GenerateResponse(
        title=model_data.get("title", ""),
        shortDescription=model_data.get("shortDescription", ""),
        longDescription=model_data.get("longDescription", ""),
        source=request,
        status="completed",
    )


def validate_output(response: GenerateResponse) -> None:
    if not response.title.strip():
        raise ValueError("title is empty")
    if not response.shortDescription.strip():
        raise ValueError("shortDescription is empty")
    if not response.longDescription.strip():
        raise ValueError("longDescription is empty")


def generate_description(request: GenerateRequest) -> GenerateResponse:
    context = get_context(request.productType, request.stone, request.stone2)
    system_prompt, user_prompt = build_prompt(request, context)
    logger.info(
        "Prompt zbudowany | kamień: %s | kamień2: %s | przykłady: %d | stone_data: %s",
        request.stone,
        request.stone2 or "—",
        len(context.get("examples", [])),
        "tak" if context.get("stone_data") else "nie",
    )
    model_data = call_openai(system_prompt, user_prompt)
    logger.info("Odpowiedź modelu — klucze: %s", list(model_data.keys()))
    response = parse_model_output(model_data, request)
    validate_output(response)
    return response
