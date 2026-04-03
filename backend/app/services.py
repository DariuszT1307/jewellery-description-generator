from .schemas import GenerateRequest, GenerateResponse


def build_prompt(request: GenerateRequest) -> str:
    return (
        f"Generate a product description for handmade jewelry.\n"
        f"Product Name: {request.productName}\n"
        f"Product Type: {request.productType}\n"
        f"Stone: {request.stone}\n"
        f"Keywords: {request.keywords or 'natural, handmade'}\n"
        f"Notes: {request.notes or 'No additional notes'}\n"
        f"Images: {len(request.images) if request.images else 0} files\n"
        f"Response format: JSON with title, shortDescription, bullets, longDescription, specs.\n"
        f"Focus on native Polish language, concise and descriptive tone.\n"
    )


def _label_product_type(product_type: str) -> str:
    mapping = {
        "necklace": "Naszyjnik",
        "ring": "Pierścionek",
        "bracelet": "Bransoletka",
        "earrings": "Kolczyki",
    }
    return mapping.get(product_type.lower(), product_type.capitalize())


def _label_stone(stone: str) -> str:
    mapping = {
        "amethyst": "Ametyst",
        "rose_quartz": "Kwarc różowy",
        "citrine": "Cytryn",
        "clear_quartz": "Kwarc przejrzysty",
        "obsidian": "Obsydian",
        "lapis_lazuli": "Lazuryt",
        "malachite": "Malachit",
        "tourmaline": "Turmalin",
    }
    return mapping.get(stone.lower(), stone.capitalize())


def call_openai(prompt: str, request: GenerateRequest) -> dict:
    # TODO: w przyszłości podpiąć realne OpenAI API
    product_label = _label_product_type(request.productType)
    stone_label = _label_stone(request.stone)

    title = f"{request.productName} – {stone_label} w {product_label}"
    short = (
        f"Odnajdź swój wewnętrzny spokój. Ta ręcznie wykonana {product_label.lower()} "
        f"łączy stabilizującą moc {stone_label.lower()} z kunsztowną oprawą. "
        "Materiały tworzą harmonijną całość, która wspiera energię i ochronę."
    )

    bullets = [
        f"Intencja: {request.keywords or 'Spokój, uziemienie, ochrona energetyczna'}.",
        f"Materiały: naturalny {stone_label.lower()}, miedź, regulowany sznurek.",
        "Prezent z intencją: Idealny upominek dla osoby potrzebującej balansu i stabilizacji.",
    ]

    long_description = (
        f"{product_label} z {stone_label}-miedziany talizman stabilizacji. "
        "Wybierz biżuterię, która wspiera Twoją wewnętrzną harmonię. "
        "To autorski projekt wire wrapping. Każde wygięcie miedzianego drutu "
        "poprowadzone z intencją ochrony, tworząc bezpieczną przestrzeń dla Twojej energii.\n"
        "Właściwości Twojego Talizmanu:\n"
        f"{stone_label}: Nazywany kamieniem równowagi. Jego energia pomaga w stabilizacji aury, "
        "eliminuje negatywne wibracje i buduje poczucie bezpieczeństwa.\n"
        "Moc miedzi i kontakt ze skórą: miedź usuwa blokady energetyczne, uziemia i pozwala korzystać z właściwości kamienia.\n"
        "Unikatowe rękodzieło: artystyczny splot miedzi nadaje surowy charakter. \n"
        "Zodiak i intuicja: idealne dla Byka, Bliźniąt, Skorpiona, Panny, ale intuicja jest najważniejsza.\n"
        "Dlaczego to dobry prezent: uniwersalny, regulowany, pełen intencji."
    )

    specs = {
        "Kamień": stone_label,
        "Metal": "Czysta miedź (nielakierowana, patynowana)",
        "Rozmiar": "Uniwersalny (regulowane zapięcie przesuwne)",
    }

    if request.images:
        specs["Ilość zdjęć"] = f"{len(request.images)} plików"

    # symulowane dane jak od modelu
    return {
        "title": title,
        "shortDescription": short,
        "bullets": bullets,
        "longDescription": long_description,
        "specs": specs,
    }


def parse_model_output(model_data: dict, request: GenerateRequest) -> GenerateResponse:
    return GenerateResponse(
        title=model_data["title"],
        shortDescription=model_data["shortDescription"],
        bullets=model_data["bullets"],
        longDescription=model_data["longDescription"],
        specs=model_data["specs"],
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
    prompt = build_prompt(request)
    model_data = call_openai(prompt, request)
    response = parse_model_output(model_data, request)
    validate_output(response)
    return response
