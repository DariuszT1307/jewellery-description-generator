from typing import List, Optional
from pydantic import BaseModel, Field, constr

class ImageMeta(BaseModel):
    name: constr(min_length=1)
    size: int = Field(..., ge=0)
    type: constr(min_length=1)

class GenerateRequest(BaseModel):
    productType: constr(min_length=1)
    stone: constr(min_length=1)
    productName: constr(min_length=1)
    keywords: Optional[str] = None
    notes: Optional[str] = None
    images: Optional[List[ImageMeta]] = None

class GenerateResponse(BaseModel):
    title: str
    shortDescription: str
    bullets: List[str]
    longDescription: str
    specs: dict
    source: GenerateRequest
    status: str = "success"
