from dotenv import load_dotenv
load_dotenv()  # ładuje backend/.env

import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .schemas import GenerateRequest, GenerateResponse, StonesResponse
from .services import generate_description as generate_description_service
from .knowledge_service import get_all_stones

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Jewellery Description Generator - Backend MVP",
    version="0.1.0",
    description="Mock API that accepts product form and returns a generated description.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev mode: akceptuj wszystkie origin, żeby preflight CORS nie blokował
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Backend is running"}


@app.get("/stones", response_model=StonesResponse)
def list_stones():
    try:
        stones = get_all_stones()
        return StonesResponse(stones=stones)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/generate", response_model=GenerateResponse)
def generate_description(request: GenerateRequest):
    logger.info("POST /generate | request: %s", request.dict())
    try:
        response = generate_description_service(request)
    except ValueError as exc:
        logger.error("ValueError w /generate: %s", exc)
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        logger.exception("Nieoczekiwany błąd w /generate")
        raise HTTPException(status_code=500, detail=str(exc))

    return JSONResponse(status_code=200, content=response.dict())

