from fastapi import FastAPI
from fastapi.responses import JSONResponse

from .schemas import GenerateRequest, GenerateResponse

app = FastAPI(
    title="Jewellery Description Generator - Backend MVP",
    version="0.1.0",
    description="Mock API that accepts product form and returns a generated description.",
)

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Backend is running"}

@app.post("/generate", response_model=GenerateResponse)
def generate_description(request: GenerateRequest):
    description_items = [
        f"Produkt: {request.productName}",
        f"Typ: {request.productType}",
        f"Kamień: {request.stone}",
    ]

    if request.keywords:
        description_items.append(f"Słowa kluczowe: {request.keywords}")
    if request.notes:
        description_items.append(f"Notatki: {request.notes}")
    if request.images:
        description_items.append(f"Zdjęcia: {len(request.images)} plików")

    generated_description = (
        "Mockowy opis produktu na bazie danych wejściowych: "
        + "; ".join(description_items)
    )

    response = GenerateResponse(
        generatedDescription=generated_description,
        source=request,
        status="completed",
    )

    return JSONResponse(status_code=200, content=response.dict())
