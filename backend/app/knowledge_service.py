import json
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

KNOWLEDGE_BASE_DIR = Path(__file__).parent.parent / "knowledge_base"

# Foldery z danymi kamieni — nowe kamienie w stones/, ametyst legacy w katalogu głównym
STONE_DIRS = [
    KNOWLEDGE_BASE_DIR / "stones",
    KNOWLEDGE_BASE_DIR,  # fallback dla ametystu w knowledge_base/ametyst/
]

# Mapowanie nazw kamieni (PL/EN warianty) → nazwa folderu
STONE_FOLDER: dict[str, str] = {
    "amethyst": "ametyst",
    "ametyst": "ametyst",
    "jade": "jadeit",
    "jadeit": "jadeit",
    "agate": "agat",
    "agat": "agat",
    "tiger's eye": "tygrysie_oko",
    "tigers eye": "tygrysie_oko",
    "tygrysie oko": "tygrysie_oko",
    "tygrysie_oko": "tygrysie_oko",
    "carnelian": "karneol",
    "karneol": "karneol",
    "clear quartz": "krysztal_gorski",
    "clear_quartz": "krysztal_gorski",
    "kryształ górski": "krysztal_gorski",
    "krysztal_gorski": "krysztal_gorski",
    "kryształ gorski": "krysztal_gorski",
    "lapis lazuli": "lapis_lazuli",
    "lapis_lazuli": "lapis_lazuli",
    "lazuryt": "lapis_lazuli",
    "aventurine": "awenturyn",
    "awenturyn": "awenturyn",
    "rose quartz": "kwarc_rozowy",
    "rose_quartz": "kwarc_rozowy",
    "kwarc różowy": "kwarc_rozowy",
    "citrine": "cytryn",
    "cytryn": "cytryn",
    "obsidian": "obsydian",
    "obsydian": "obsydian",
    "malachite": "malachit",
    "malachit": "malachit",
    "tourmaline": "turmalin",
    "turmalin": "turmalin",
}

# Mapowanie typów produktów → nazwa folderu w examples/
PRODUCT_FOLDER: dict[str, str] = {
    "bracelet": "bracelet",
    "bransoletka": "bracelet",
    "necklace": "necklace",
    "naszyjnik": "necklace",
    "ring": "ring",
    "pierścionek": "ring",
    "earrings": "earrings",
    "kolczyki": "earrings",
}


def _stone_key(stone: str) -> str:
    return STONE_FOLDER.get(stone.lower().strip(), stone.lower().strip().replace(" ", "_"))


def _product_key(product_type: str) -> str:
    return PRODUCT_FOLDER.get(product_type.lower().strip(), product_type.lower().strip())


def _find_stone_file(folder_name: str) -> Optional[Path]:
    """Szuka stone.json w stones/{folder}/ lub knowledge_base/{folder}/."""
    for base in STONE_DIRS:
        candidate = base / folder_name / "stone.json"
        if candidate.exists():
            return candidate
    return None


def get_all_stones() -> list[dict]:
    """
    Zwraca listę wszystkich kamieni z knowledge_base.
    Przeszukuje knowledge_base/stones/ oraz knowledge_base/ (dla ametystu).
    Każdy wpis zawiera: value, label (PL), label_en.
    """
    found: dict[str, dict] = {}  # key=folder_name, deduplikacja

    search_dirs = [
        (KNOWLEDGE_BASE_DIR / "stones", True),   # nowe kamienie
        (KNOWLEDGE_BASE_DIR, False),              # legacy (ametyst)
    ]

    for base_dir, all_subdirs in search_dirs:
        if not base_dir.exists():
            continue
        for folder in sorted(base_dir.iterdir()):
            if not folder.is_dir():
                continue
            # W katalogu głównym knowledge_base pomijamy foldery bez stone.json
            stone_file = folder / "stone.json"
            if not stone_file.exists():
                continue
            folder_name = folder.name
            if folder_name in found:
                continue
            try:
                with stone_file.open(encoding="utf-8") as f:
                    data = json.load(f)
                found[folder_name] = {
                    "value": folder_name,
                    "label": data.get("name", folder_name.capitalize()),
                    "label_en": data.get("name_en", folder_name.capitalize()),
                }
            except (json.JSONDecodeError, OSError):
                logger.warning("Nie można wczytać stone.json: %s", stone_file)

    return sorted(found.values(), key=lambda s: s["label"])


def get_stone_data(stone: str) -> Optional[dict]:
    """Zwraca dane kamienia z pliku stone.json lub None jeśli nie znaleziono."""
    folder = _stone_key(stone)
    stone_file = _find_stone_file(folder)
    if not stone_file:
        logger.warning("Brak danych kamienia dla: %s (szukano folderu: %s)", stone, folder)
        return None
    with stone_file.open(encoding="utf-8") as f:
        return json.load(f)


def get_examples(product_type: str, stone: str, max_examples: int = 2) -> list[dict]:
    """
    Zwraca listę przykładowych opisów z knowledge_base/examples/{product}/{stone_*}/.
    """
    product_folder = _product_key(product_type)
    stone_prefix = _stone_key(stone)
    examples_root = KNOWLEDGE_BASE_DIR / "examples" / product_folder

    if not examples_root.exists():
        logger.info("Brak folderu przykładów: %s", examples_root)
        return []

    examples: list[dict] = []
    for subfolder in sorted(examples_root.iterdir()):
        if not subfolder.is_dir() or not subfolder.name.startswith(stone_prefix):
            continue
        for json_file in sorted(subfolder.glob("*.json")):
            try:
                with json_file.open(encoding="utf-8") as f:
                    examples.append(json.load(f))
                if len(examples) >= max_examples:
                    return examples
            except json.JSONDecodeError:
                logger.warning("Niepoprawny JSON w przykładzie: %s", json_file)

    return examples


def get_context(product_type: str, stone: str) -> dict:
    """Zwraca pełny kontekst (dane kamienia + przykłady) dla danego produktu."""
    return {
        "stone_data": get_stone_data(stone),
        "examples": get_examples(product_type, stone),
    }
