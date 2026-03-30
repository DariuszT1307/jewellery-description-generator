from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .schemas import GenerateRequest, GenerateResponse

app = FastAPI(
    title="Jewellery Description Generator - Backend MVP",
    version="0.1.0",
    description="Mock API that accepts product form and returns a generated description.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174", "http://127.0.0.1:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Backend is running"}


def normalize_product_type(product_type: str) -> str:
    mapping = {
        "necklace": "Naszyjnik",
        "ring": "Pierścionek",
        "bracelet": "Bransoletka",
        "earrings": "Kolczyki",
    }
    return mapping.get(product_type.lower(), product_type.capitalize())


def stone_label(stone: str) -> str:
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


@app.post("/generate", response_model=GenerateResponse)
def generate_description(request: GenerateRequest):
    product_type_label = normalize_product_type(request.productType)
    stone_label_text = stone_label(request.stone)

    title = f"{request.productName} – {stone_label_text} w {product_type_label}"

    short_description_text = (
        f"Odnajdź swój wewnętrzny spokój. Ta ręcznie wykonana {product_type_label.lower()} "
        f"łączy stabilizującą moc {stone_label_text.lower()} z kunsztowną oprawą. "
        "Materiały tworzą harmonijną całość, która wspiera energię i ochronę." 
    )

    bullets = [
        f"Intencja: {request.keywords or 'Spokój, uziemienie, ochrona energetyczna'}.",
        f"Materiały: naturalny {stone_label_text.lower()}, miedź, regulowany sznurek.",
        "Prezent z intencją: Idealny upominek dla osoby potrzebującej balansu i stabilizacji.",
    ]

    long_description = (
        f"{product_type_label} z {stone_label_text}-miedziany talizman stabilizacji. "
        "Wybierz biżuterię, która wspiera Twoją wewnętrzną harmonię. "
        "To autorski projekt wire wrapping. Każde wygięcie miedzianego drutu "
        "poprowadzone z intencją ochrony, tworząc bezpieczną przestrzeń dla Twojej energii.\n"
        "Właściwości Twojego Talizmanu:\n"
        f"{stone_label_text}: Nazywany kamieniem równowagi. Jego energia pomaga w stabilizacji aury, "
        "eliminuje negatywne wibracje i buduje poczucie bezpieczeństwa.\n"
        "Moc miedzi i kontakt ze skórą: miedź usuwa blokady energetyczne, uziemia i pozwala korzystać z właściwości kamienia.\n"
        "Unikatowe rękodzieło: artystyczny splot miedzi nadaje surowy charakter. \n"
        "Zodiak i intuicja: idealne dla Byka, Bliźniąt, Skorpiona, Panny, ale intuicja jest najważniejsza.\n"
        "Dlaczego to dobry prezent: uniwersalny, regulowany, pełen intencji."
    )

    specs = {
        "Kamień": stone_label_text,
        "Metal": "Czysta miedź (nielakierowana, patynowana)",
        "Rozmiar": "Uniwersalny (regulowane zapięcie przesuwne)",
    }

    if request.images:
        specs["Ilość zdjęć"] = f"{len(request.images)} plików"

    response = GenerateResponse(
        title=title,
        shortDescription=short_description_text,
        bullets=bullets,
        longDescription=long_description,
        specs=specs,
        source=request,
        status="completed",
    )

    return JSONResponse(status_code=200, content=response.dict())

