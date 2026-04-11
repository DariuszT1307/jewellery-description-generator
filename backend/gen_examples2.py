"""
Generator przykładów biżuterii – poprawne formy gramatyczne:
 - po "z naturalnym" → narzędnik (cel)  np. "z naturalnym ametystem"
 - po "dla"          → dopełniacz        np. "dla Ryb, Wodnika"
 - po "naturalny"    → mianownik         np. "naturalny ametyst"
"""
import json
import os

BASE = r"c:\Users\HP\Desktop\Etsy Ilonka\jewellery-description-generator\backend\knowledge_base\examples\bracelet"

STONES = {
    "agat_01": {
        "stone": "agat",
        "cel":   "agatem",        # narzędnik: "z naturalnym agatem"
        "name":  "Agat",          # mianownik: "naturalny Agat"
        "title": "Bransoletka z agatem w miedzianym splocie",
        "main_feature": "ochrony i stabilności",
        "short_stone": "**Agat** chroni przed negatywną energią i pomaga zachować stabilność w trudnych chwilach.",
        "bullets": [
            "Chroni przed negatywną energią i negatywnymi wpływami otoczenia",
            "Stabilizuje emocje i pomaga odzyskać wewnętrzną równowagę",
            "Uziemia i daje poczucie bezpieczeństwa i zakorzenienia",
        ],
        "zodiaki_gen": "Bliźniąt, Koziorożca, Strzelca",   # dopełniacz po "dla"
        "zodiaki_nom": "Bliźnięta, Koziorożec, Strzelec",  # mianownik (info)
        "meta_focuses": ["duchowy / ochronny", "prezent / ochrona i siła", "estetyczny / naturalny wzór", "handmade / rzemiosło"],
        "meta_tones":  ["stabilny, uziemiający", "troskliwy, wspierający", "wyrazisty, naturalny", "autentyczny, rzemieślniczy"],
    },
    "ametyst_01": {
        "stone": "ametyst",
        "cel":   "ametystem",
        "name":  "Ametyst",
        "title": "Bransoletka z ametystem w miedzianym splocie",
        "main_feature": "spokoju i intuicji",
        "short_stone": "**Ametyst** uspokaja myśli, łagodzi napięcie i lęk oraz wspiera medytację i uważność.",
        "bullets": [
            "Uspokaja gonitwę myśli i łagodzi napięcie oraz lęk",
            "Wspiera medytację, uważność i wyciszenie umysłu",
            "Pogłębia intuicję i otwiera na wyższe postrzeganie",
        ],
        "zodiaki_gen": "Ryb, Wodnika, Koziorożca",
        "zodiaki_nom": "Ryby, Wodnik, Koziorożec",
        "meta_focuses": ["duchowy / medytacyjny", "prezent / spokój i wyciszenie", "estetyczny / fiolet i lawenda", "handmade / rzemiosło"],
        "meta_tones":  ["spokojny, refleksyjny", "troskliwy, wyciszający", "subtelny, estetyczny", "autentyczny, rzemieślniczy"],
    },
    "awenturyn_01": {
        "stone": "awenturyn",
        "cel":   "awenturynem",
        "name":  "Awenturyn",
        "title": "Bransoletka z awenturynem w miedzianym splocie",
        "main_feature": "szczęścia i nowych możliwości",
        "short_stone": "**Awenturyn** przyciąga szczęście, otwiera na nowe możliwości i wspiera podejmowanie odważnych decyzji.",
        "bullets": [
            "Przyciąga dobre zbieżności i sprzyja szczęśliwym okazjom",
            "Otwiera na zmiany i nowe możliwości w życiu",
            "Wspiera podejmowanie decyzji z optymizmem i otwartością",
        ],
        "zodiaki_gen": "Byka, Raka, Wagi",
        "zodiaki_nom": "Byk, Rak, Waga",
        "meta_focuses": ["duchowy / szczęście i otwartość", "prezent / nowe możliwości", "estetyczny / zielony połysk", "handmade / rzemiosło"],
        "meta_tones":  ["optymistyczny, otwarty", "radosny, wspierający", "żywy, naturalny", "autentyczny, rzemieślniczy"],
    },
    "jadeit_01": {
        "stone": "jadeit",
        "cel":   "jadeitem",
        "name":  "Jadeit",
        "title": "Bransoletka z jadeitem w miedzianym splocie",
        "main_feature": "harmonii i serca",
        "short_stone": "**Jadeit** harmonizuje emocje, przynosi wewnętrzny spokój i wspiera życie w zgodzie ze sobą.",
        "bullets": [
            "Harmonizuje emocje i przynosi spokój serca",
            "Wspiera życie w zgodzie ze sobą i z innymi",
            "Przyciąga dobrobyt i pomaga budować harmonijne relacje",
        ],
        "zodiaki_gen": "Byka, Wagi, Koziorożca",
        "zodiaki_nom": "Byk, Waga, Koziorożec",
        "meta_focuses": ["duchowy / harmonia i dobrobyt", "prezent / spokój i harmonia", "estetyczny / zieleń jadeitu", "handmade / rzemiosło"],
        "meta_tones":  ["spokojny, harmonijny", "troskliwy, harmonijny", "delikatny, naturalny", "autentyczny, rzemieślniczy"],
    },
    "karneol_01": {
        "stone": "karneol",
        "cel":   "karneolem",
        "name":  "Karneol",
        "title": "Bransoletka z karneolem w miedzianym splocie",
        "main_feature": "energii i twórczości",
        "short_stone": "**Karneol** pobudza energię, motywację i kreatywność – idealny dla twórczych dusz szukających impulsu do działania.",
        "bullets": [
            "Pobudza energię życiową i motywację do działania",
            "Rozbudza kreatywność i pomaga przełamać twórczy zastój",
            "Aktywuje czakrę sakralną i dodaje witalności",
        ],
        "zodiaki_gen": "Raka, Lwa, Byka",
        "zodiaki_nom": "Rak, Lew, Byk",
        "meta_focuses": ["duchowy / twórczość i witalność", "prezent / energia i motywacja", "estetyczny / ciepły pomarańcz", "handmade / rzemiosło"],
        "meta_tones":  ["energiczny, motywujący", "radosny, energiczny", "ciepły, wyrazisty", "autentyczny, rzemieślniczy"],
    },
    "krysztal_gorski_01": {
        "stone": "kryształ górski",
        "cel":   "kryształem górskim",
        "name":  "Kryształ górski",
        "title": "Bransoletka z kryształem górskim w miedzianym splocie",
        "main_feature": "oczyszczenia i wzmocnienia",
        "short_stone": "**Kryształ górski** wzmacnia intencje, oczyszcza energię i poprawia jasność myślenia – kamień universalny.",
        "bullets": [
            "Wzmacnia intencje i cele, które w niego włożysz",
            "Oczyszcza energię i przestrzeń wokół siebie",
            "Poprawia jasność myślenia i wspiera koncentrację",
        ],
        "zodiaki_gen": None,  # universalny
        "zodiaki_nom": None,
        "zodiaki_footer_custom": "Kryształ górski pasuje do każdego znaku – jeśli czujesz przyciąganie, to jest dla Ciebie.",
        "zodiaki_dk_custom": "Kryształ górski pasuje do każdego znaku zodiaku.",
        "meta_focuses": ["duchowy / oczyszczenie i intencja", "prezent / universalny wybór", "estetyczny / surowy kryształ", "handmade / rzemiosło"],
        "meta_tones":  ["jasny, intencjonalny", "otwarty, universalny", "czysty, przejrzysty", "autentyczny, rzemieślniczy"],
    },
    "lapis_lazuli_01": {
        "stone": "lapis lazuli",
        "cel":   "lapis lazuli",     # nieodmienny
        "name":  "Lapis lazuli",
        "title": "Bransoletka z lapis lazuli w miedzianym splocie",
        "main_feature": "mądrości i komunikacji",
        "short_stone": "**Lapis lazuli** wspiera komunikację, pewność siebie i autentyczne wyrażanie prawdy.",
        "bullets": [
            "Wspiera szczere wyrażanie siebie i odwagę w komunikacji",
            "Wzmacnia pewność siebie i pomaga mówić wprost",
            "Pogłębia intuicję i otwiera na wewnętrzną mądrość",
        ],
        "zodiaki_gen": "Strzelca, Ryb, Wagi",
        "zodiaki_nom": "Strzelec, Ryby, Waga",
        "meta_focuses": ["duchowy / mądrość i komunikacja", "prezent / autentyczność i prawda", "estetyczny / kobalt i piryt", "handmade / rzemiosło"],
        "meta_tones":  ["głęboki, ekspresyjny", "autentyczny, szczery", "wyrazisty, królewski", "autentyczny, rzemieślniczy"],
    },
    "tygrysie_oko_01": {
        "stone": "tygrysie oko",
        "cel":   "tygrysim okiem",
        "name":  "Tygrysie oko",
        "title": "Bransoletka z tygrysim okiem w miedzianym splocie",
        "main_feature": "odwagi i działania",
        "short_stone": "**Tygrysie oko** wzmacnia siłę woli i determinację, pomaga podejmować decyzje bez wahania.",
        "bullets": [
            "Wzmacnia siłę woli i determinację w działaniu",
            "Pomaga podejmować decyzje i przełamywać wewnętrzne bloki",
            "Daje impuls do ruszenia z miejsca i realizacji celów",
        ],
        "zodiaki_gen": "Lwa, Koziorożca, Barana",
        "zodiaki_nom": "Lew, Koziorożec, Baran",
        "meta_focuses": ["duchowy / odwaga i działanie", "prezent / siła i determinacja", "estetyczny / efekt kociego oka", "handmade / rzemiosło"],
        "meta_tones":  ["energiczny, pewny siebie", "motywujący, silny", "wyrazisty, dynamiczny", "autentyczny, rzemieślniczy"],
    },
}

FILENAMES = [
    "desc_01_spiritual.json",
    "desc_02_gift.json",
    "desc_03_aesthetic.json",
    "desc_04_handmade.json",
]

AUDIENCES = [
    "osoby szukające wsparcia energetycznego i duchowej siły",
    "osoby szukające wyjątkowego, znaczącego prezentu",
    "osoby ceniące estetykę naturalnych materiałów i ręczne rzemiosło",
    "osoby doceniające ręcznie robioną biżuterię z naturalnych materiałów",
]

# Intro dla shortDescription – po "z naturalnym" → narzędnik (cel)
SHORT_INTROS = [
    "Ręcznie robiona bransoletka z naturalnym {cel}. Lekka i wygodna w noszeniu, pasuje do różnych stylizacji. Miedź działa antybakteryjnie i wzmacnia działanie kamienia.",
    "Ręcznie robiona bransoletka z naturalnym {cel} – wyjątkowy prezent dla niej. Lekka i wygodna w noszeniu. Miedź działa antybakteryjnie i wzmacnia działanie kamienia.",
    "Ręcznie robiona bransoletka z naturalnym {cel}. Biżuteria boho do casualowych i eleganckich stylizacji. Miedź działa antybakteryjnie i wzmacnia działanie kamienia.",
    "Ręcznie robiona bransoletka z naturalnym {cel} – 100% handmade, wire wrapping. Pasuje do różnych stylizacji. Miedź działa antybakteryjnie i wzmacnia działanie kamienia.",
]

# Sekcja „dla kogo" – {zdk} to "Bransoletka dla {dopełniacz}."
DLA_KOGO = [
    "{zdk}\nDoskonały prezent dla niej – na urodziny, rocznicę, Dzień Matki lub po prostu tak.\nBiżuteria boho pasująca do casualowych i eleganckich stylizacji.",
    "{zdk}\nDoskonały prezent dla niej – szczególnie dla kogoś, kto ceni naturalne kamienie i ręczne rzemiosło.\nBiżuteria boho pasująca do casualowych i eleganckich stylizacji.",
    "{zdk}\nDoskonały prezent dla niej – na każdą okazję.\nBiżuteria boho z naturalnych kamieni, pasująca zarówno do stylizacji codziennych, jak i eleganckich.",
    "{zdk}\nDoskonały prezent dla niej – każda bransoletka jest jedyna w swoim rodzaju.\nBiżuteria boho wykonana w 100% ręcznie.",
]


def zodiaki_footer(d):
    if d.get("zodiaki_footer_custom"):
        return d["zodiaki_footer_custom"]
    return f"Bransoletka dla {d['zodiaki_gen']}, ale jeśli czujesz przyciąganie – to jest dla Ciebie."


def zodiaki_dk(d):
    if d.get("zodiaki_dk_custom"):
        return d["zodiaki_dk_custom"]
    return f"Bransoletka dla {d['zodiaki_gen']}."


def make_short(d, idx):
    intro = SHORT_INTROS[idx].format(cel=d["cel"])
    return "\n\n".join([
        d["title"],
        intro,
        d["short_stone"],
        f"Doskonały prezent dla niej.\n{zodiaki_footer(d)}",
    ])


def make_long(d, idx):
    b = d["bullets"]
    zdk = zodiaki_dk(d)
    dk = DLA_KOGO[idx].format(zdk=zdk)
    name_lower = d["name"].lower()
    return "\n\n".join([
        f"Ręcznie robiona bransoletka z naturalnym {d['cel']} i miedzią. Biżuteria boho wykonana techniką wire wrapping.",
        f"**Miedź** – naturalny przewodnik energii\n- Działa antybakteryjnie i przeciwzapalnie\n- Wzmacnia działanie kamieni\n- Wspiera organizm",
        f"**{d['name']}** – kamień {d['main_feature']}\n- {b[0]}\n- {b[1]}\n- {b[2]}",
        f"**Materiał:** czysta miedź, naturalny {name_lower}\n**Rozmiar:** obwód ok. 17 cm z możliwością regulacji\n**Wykonanie:** 100% ręcznie robiony\n**Technika:** wire wrapping",
        dk,
        "❣️ Kolory na zdjęciach mogą się różnić w zależności od ustawień monitora. Miedź reaguje na światło i otoczenie, co wpływa na jej odcień.",
    ])


# ---------- GENERUJ PRZYKŁADY 1-KAMIENNE ----------
count = 0
for stone_key, d in STONES.items():
    for i, fname in enumerate(FILENAMES):
        fpath = os.path.join(BASE, stone_key, fname)
        obj = {
            "_meta": {
                "focus": d["meta_focuses"][i],
                "tone":  d["meta_tones"][i],
                "target_audience": AUDIENCES[i],
            },
            "input": {
                "productType": "bransoletka",
                "stone": d["stone"],
                "productName": f"Miedziana bransoletka z {d['cel']}",
            },
            "output": {
                "title":            d["title"],
                "shortDescription": make_short(d, i),
                "longDescription":  make_long(d, i),
            },
        }
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)
        count += 1

print(f"Jednokamieniowe: {count} plikow")

# ---------- GENERUJ PRZYKŁADY 2-KAMIENNE ----------

# Lookup main_feature by stone name
def get_main_feature(stone_name):
    for d in STONES.values():
        if d["stone"] == stone_name:
            return d["main_feature"]
    return "właściwości"


DUAL = [
    {
        "folder": "ametyst_krysztal_gorski_01",
        "fname": "desc_01.json",
        "stone1": "ametyst",      "cel1": "ametystem",       "name1": "Ametyst",
        "stone2": "kryształ górski", "cel2": "kryształem górskim", "name2": "Kryształ górski",
        "title": "Bransoletka z ametystem i kryształem górskim w miedzianym splocie",
        "focus": "duchowy / spokój i jasność umysłu",
        "tone": "spokojny, klarowny",
        "short_intro": "Ręcznie robiona bransoletka z naturalnym ametystem i kryształem górskim. Biżuteria boho łącząca dwie komplementarne energie: wyciszenie i jasność. Miedź wzmacnia działanie obu kamieni.",
        "stone1_short": "**Ametyst** uspokaja myśli, łagodzi napięcie i wspiera medytację.",
        "stone2_short": "**Kryształ górski** wzmacnia intencje, oczyszcza energię i poprawia jasność myślenia.",
        "synergia_short": "**Połączenie ametystu i kryształu górskiego** – ametyst wycisza umysłowy szum, kryształ górski wyostrza to, co zostaje. Razem: spokój i klarowność w jednym.",
        "zodiaki_footer": "Bransoletka dla Ryb, Wodnika, Koziorożca, ale jeśli czujesz przyciąganie – to jest dla Ciebie.",
        "stone1_bullets": ["Uspokaja gonitwę myśli i łagodzi napięcie", "Wspiera medytację i uważność", "Pogłębia intuicję"],
        "stone2_bullets": ["Wzmacnia intencje i cele", "Oczyszcza energię i przestrzeń", "Poprawia jasność myślenia"],
        "synergia_long": "**Połączenie ametystu i kryształu górskiego** działa dwuetapowo: ametyst wycisza to, co przeszkadza – stres, gonienie myśli – a kryształ górski wzmacnia to, co zostaje po wyciszeniu. Nie tępa cisza, lecz świadomy spokój, z którego możesz działać wyraźnie.",
        "dla_kogo": "Bransoletka dla Ryb, Wodnika, Koziorożca.\nDoskonały prezent dla niej – na urodziny, Dzień Matki lub dla kogoś, kto dużo myśli i potrzebuje chwili oddechu.\nBiżuteria boho pasująca do casualowych i eleganckich stylizacji.",
        "materialy": "czysta miedź, naturalny ametyst, kryształ górski",
        "stone1_main": "spokoju i intuicji",
        "stone2_main": "oczyszczenia i wzmocnienia",
    },
    {
        "folder": "karneol_lapis_lazuli_01",
        "fname": "desc_01.json",
        "stone1": "karneol",    "cel1": "karneolem",    "name1": "Karneol",
        "stone2": "lapis lazuli", "cel2": "lapis lazuli", "name2": "Lapis lazuli",
        "title": "Bransoletka z karneolem i lapis lazuli w miedzianym splocie",
        "focus": "duchowy / energia i autentyczne wyrażanie siebie",
        "tone": "energiczny, autentyczny",
        "short_intro": "Ręcznie robiona bransoletka z naturalnym karneolem i lapis lazuli. Biżuteria boho łącząca energię twórczości z siłą autentycznej komunikacji. Miedź wzmacnia działanie obu kamieni.",
        "stone1_short": "**Karneol** pobudza energię, motywację i kreatywność.",
        "stone2_short": "**Lapis lazuli** wspiera komunikację, pewność siebie i autentyczne wyrażanie prawdy.",
        "synergia_short": "**Połączenie karneolu i lapis lazuli** – karneol daje energię i odwagę do działania, lapis lazuli nadaje jej kierunek i głos. Dla osób, które mają coś do powiedzenia i chcą mieć siłę, by to zrobić.",
        "zodiaki_footer": "Bransoletka dla Raka, Lwa, Byka, Strzelca, Ryb i Wagi, ale jeśli czujesz przyciąganie – to jest dla Ciebie.",
        "stone1_bullets": ["Pobudza energię życiową i motywację", "Rozbudza kreatywność i pomaga przełamać twórczy zastój", "Aktywuje witalność i chęć do działania"],
        "stone2_bullets": ["Wspiera szczere wyrażanie siebie", "Wzmacnia pewność siebie w komunikacji", "Pogłębia intuicję i otwiera na mądrość"],
        "synergia_long": "**Połączenie karneolu i lapis lazuli** zamyka pętlę twórczego wyrażenia: karneol zapala energię i daje odwagę do działania, lapis lazuli kieruje ją ku autentycznemu wyrażeniu siebie. Razem – nie tylko motywacja, ale też jasność co do tego, co naprawdę chcesz powiedzieć i stworzyć.",
        "dla_kogo": "Bransoletka dla Raka, Lwa, Byka, Strzelca, Ryb i Wagi.\nDoskonały prezent dla niej – szczególnie dla artystek, twórczyń, nauczycielek lub każdej osoby zaczynającej nowy projekt.\nBiżuteria boho pasująca do casualowych i eleganckich stylizacji.",
        "materialy": "czysta miedź, naturalny karneol, lapis lazuli",
        "stone1_main": "energii i twórczości",
        "stone2_main": "mądrości i komunikacji",
    },
    {
        "folder": "awenturyn_tygrysie_oko_01",
        "fname": "desc_01.json",
        "stone1": "awenturyn",    "cel1": "awenturynem",    "name1": "Awenturyn",
        "stone2": "tygrysie oko", "cel2": "tygrysim okiem", "name2": "Tygrysie oko",
        "title": "Bransoletka z awenturynem i tygrysim okiem w miedzianym splocie",
        "focus": "duchowy / nowe możliwości i skuteczne działanie",
        "tone": "optymistyczny, zdecydowany",
        "short_intro": "Ręcznie robiona bransoletka z naturalnym awenturynem i tygrysim okiem. Biżuteria boho łącząca kamień okazji z kamieniem działania. Miedź wzmacnia działanie obu kamieni.",
        "stone1_short": "**Awenturyn** przyciąga szczęście, otwiera na nowe możliwości i wspiera podejmowanie odważnych decyzji.",
        "stone2_short": "**Tygrysie oko** wzmacnia siłę woli i determinację, pomaga podejmować decyzje bez wahania.",
        "synergia_short": "**Połączenie awenturynu i tygrysiego oka** – awenturyn otwiera oczy na okazje, tygrysie oko daje determinację, żeby je wykorzystać zanim znikną. Razem: widzisz i działasz.",
        "zodiaki_footer": "Bransoletka dla Byka, Raka, Wagi, Lwa, Koziorożca i Barana, ale jeśli czujesz przyciąganie – to jest dla Ciebie.",
        "stone1_bullets": ["Przyciąga dobre zbieżności i sprzyja szczęśliwym okazjom", "Otwiera na zmiany i nowe możliwości", "Wspiera optymizm i podejmowanie decyzji"],
        "stone2_bullets": ["Wzmacnia siłę woli i determinację", "Pomaga podejmować decyzje bez wahania", "Daje impuls do ruszenia z miejsca"],
        "synergia_long": "**Połączenie awenturynu i tygrysiego oka** tworzy dynamiczny duet: awenturyn sprawia, że okazje są lepiej widoczne i łatwiej je rozpoznać, tygrysie oko daje wolę i determinację, żeby z nich skorzystać. Dla kogoś, kto ma dużo pomysłów, ale często je odkłada – to połączenie mówi: teraz.",
        "dla_kogo": "Bransoletka dla Byka, Raka, Wagi, Lwa, Koziorożca i Barana.\nDoskonały prezent dla niej – dla kogoś gotowego na nowy etap lub zmieniającego kierunek życia.\nBiżuteria boho pasująca do casualowych i eleganckich stylizacji.",
        "materialy": "czysta miedź, naturalny awenturyn, tygrysie oko",
        "stone1_main": "szczęścia i nowych możliwości",
        "stone2_main": "odwagi i działania",
    },
]


def make_dual_short(d):
    return "\n\n".join([
        d["title"],
        d["short_intro"],
        d["stone1_short"],
        d["stone2_short"],
        d["synergia_short"],
        f"Doskonały prezent dla niej.\n{d['zodiaki_footer']}",
    ])


def make_dual_long(d):
    b1, b2 = d["stone1_bullets"], d["stone2_bullets"]
    return "\n\n".join([
        f"Ręcznie robiona bransoletka z naturalnym {d['cel1']} i {d['cel2']} oraz miedzią. Biżuteria boho wykonana techniką wire wrapping.",
        f"**Miedź** – naturalny przewodnik energii\n- Działa antybakteryjnie i przeciwzapalnie\n- Wzmacnia działanie kamieni\n- Wspiera organizm",
        f"**{d['name1']}** – kamień {d['stone1_main']}\n- {b1[0]}\n- {b1[1]}\n- {b1[2]}",
        f"**{d['name2']}** – kamień {d['stone2_main']}\n- {b2[0]}\n- {b2[1]}\n- {b2[2]}",
        d["synergia_long"],
        f"**Materiał:** {d['materialy']}\n**Rozmiar:** obwód ok. 17 cm z możliwością regulacji\n**Wykonanie:** 100% ręcznie robiony\n**Technika:** wire wrapping",
        d["dla_kogo"],
        "❣️ Kolory na zdjęciach mogą się różnić w zależności od ustawień monitora. Miedź reaguje na światło i otoczenie, co wpływa na jej odcień.",
    ])


for d in DUAL:
    fpath = os.path.join(BASE, d["folder"], d["fname"])
    obj = {
        "_meta": {
            "focus": d["focus"],
            "tone":  d["tone"],
            "target_audience": "osoby szukające biżuterii łączącej dwie energie",
            "stones": [d["stone1"], d["stone2"]],
        },
        "input": {
            "productType": "bransoletka",
            "stone":  d["stone1"],
            "stone2": d["stone2"],
            "productName": f"Miedziana bransoletka z {d['cel1']} i {d['cel2']}",
        },
        "output": {
            "title":            d["title"],
            "shortDescription": make_dual_short(d),
            "longDescription":  make_dual_long(d),
        },
    }
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    print(f"  2-kamienne: {d['folder']}/{d['fname']}")

print("Gotowe!")
