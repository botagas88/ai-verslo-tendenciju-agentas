"""AI Verslo Tendencijų Agentas – imituoja tendencijų rinkimą ir sugeneruoja ataskaitą."""

import sys
from datetime import datetime
from pathlib import Path
from random import Random

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

OUTPUT_FILE = Path(__file__).resolve().parent / "business_ideas.txt"

TRENDS = [
    {
        "pavadinimas": "Dirbtinis intelektas mažame versle",
        "aprasymas": "Įmonės vis dažniau naudoja AI klientų aptarnavimui, turinio kūrimui ir procesų automatizavimui.",
    },
    {
        "pavadinimas": "Tvarumas ir antrinis naudojimas",
        "aprasymas": "Vartotojai renkasi produktus su mažesniu poveikiu aplinkai ir aiškia kilmės istorija.",
    },
    {
        "pavadinimas": "Sveikata ir prevencija namuose",
        "aprasymas": "Auga susidomėjimas miego, streso ir mitybos stebėsena be dažnų vizitų pas specialistus.",
    },
    {
        "pavadinimas": "Vietinis e. prekybos patogumas",
        "aprasymas": "Pirkėjai nori greito pristatymo, paprasto grąžinimo ir asmeninių rekomendacijų.",
    },
    {
        "pavadinimas": "Nuotolinis darbas ir hibridinės komandos",
        "aprasymas": "Mažos komandos ieško paprastų įrankių, kurie pakeistų brangias įmonių sistemas.",
    },
    {
        "pavadinimas": "Mokymasis visą gyvenimą",
        "aprasymas": "Profesionalai ieško trumpų, praktinių kursų, pritaikytų konkrečiai specialybei.",
    },
]

IDEA_TEMPLATES = [
    {
        "pavadinimas": "AI asistentas vietiniams verslams",
        "santrauka": "Paprasta paslauga, kuri automatiškai atsako į klientų žinutes, sudaro kainos pasiūlymus ir primena apie užsakymus.",
        "kodel": "Mažos įmonės nori AI naudos, bet neturi laiko ir biudžeto kurti savų sistemų.",
        "pirmas_zingsnis": "Pasirinkti vieną nišą (pvz. grožio salonai) ir paleisti 5 klientų bandomąją versiją.",
    },
    {
        "pavadinimas": "Tvaraus pakartotinio naudojimo rinka",
        "santrauka": "Platforma, kurioje gyventojai ir smulkūs gamintojai parduoda atnaujintus daiktus su aiškia būklės informacija.",
        "kodel": "Antrinė rinka auga, bet pirkėjai vis dar bijo kokybės rizikos.",
        "pirmas_zingsnis": "Pradėti nuo vienos kategorijos (baldai arba elektronika) ir vietinio miesto.",
    },
    {
        "pavadinimas": "Namų sveikatos ataskaitų rinkinys",
        "santrauka": "Prenumerata: nešiojamas jutiklis + savaitinė ataskaita su paprastais veiksmais miegui ir energijai gerinti.",
        "kodel": "Žmonės nori prevencijos, bet nesupranta žalių duomenų iš programėlių.",
        "pirmas_zingsnis": "Sukurtį PDF ataskaitos šabloną ir išbandyti su 20 pažįstamų.",
    },
    {
        "pavadinimas": "Vietinių parduotuvių greito atsiėmimo tinklas",
        "santrauka": "Bendras užsakymo langas kelioms kaimynystės parduotuvėms su atsiėmimu per 2 valandas.",
        "kodel": "Klientai nori greičio kaip didžiosiose platformose, bet palaiko vietinį verslą.",
        "pirmas_zingsnis": "Surinkti 8 parduotuves viename rajone ir paleisti WhatsApp / paprastą svetainę.",
    },
    {
        "pavadinimas": "Hibridinės komandos „vieno langelio“ įrankis",
        "santrauka": "Lengva lenta užduotims, sutarčių šablonams ir savaitės ataskaitoms, skirta 3–15 žmonių komandoms.",
        "kodel": "Didelės sistemos per sudėtingos, o lentelės greitai virsta chaosu.",
        "pirmas_zingsnis": "Apklausti 10 smulkių agentūrų, kokių 3 funkcijų joms iš tikrųjų reikia.",
    },
    {
        "pavadinimas": "Trumpi praktiniai kursai specialistams",
        "santrauka": "4 savaičių programos (pvz. buhalteriams, meistrams, restoranams) su namų darbais ir grįžtamuoju ryšiu.",
        "kodel": "Bendri kursai per platūs; žmonės moka už konkretų rezultatą darbe.",
        "pirmas_zingsnis": "Paruošti vieną kursą, parduoti jį už išankstinę kainą ir patobulinti pagal atsiliepimus.",
    },
]


def collect_trends(rng: Random) -> list[dict]:
    """Imituoja viešų šaltinių peržiūrą ir grąžina 3 tendencijas."""
    return rng.sample(TRENDS, k=3)


def pick_ideas(rng: Random) -> list[dict]:
    """Parenka 3 verslo idėjas pagal dienos sėklą, kad ataskaita būtų kartojama tą pačią dieną."""
    return rng.sample(IDEA_TEMPLATES, k=3)


def build_report(trends: list[dict], ideas: list[dict], generated_at: datetime) -> str:
    lines = [
        "AI VERSLO TENDENCIJŲ AGENTAS",
        "Tekstinė ataskaita",
        f"Sugeneruota: {generated_at.strftime('%Y-%m-%d %H:%M')}",
        "",
        "Ši ataskaita IMITUOJA tendencijų rinkimą (nėra gyvo interneto skenavimo).",
        "Idėjos skirtos inspiracijai, ne investavimo ar verslo patarimui.",
        "",
        "=" * 60,
        "PASTEBĖTOS TENDENCIJOS",
        "=" * 60,
        "",
    ]

    for index, trend in enumerate(trends, start=1):
        lines.append(f"{index}. {trend['pavadinimas']}")
        lines.append(f"   {trend['aprasymas']}")
        lines.append("")

    lines.extend(
        [
            "=" * 60,
            "3 VERSLO IDĖJOS",
            "=" * 60,
            "",
        ]
    )

    for index, idea in enumerate(ideas, start=1):
        lines.append(f"{index}. {idea['pavadinimas']}")
        lines.append(f"   Santrauka: {idea['santrauka']}")
        lines.append(f"   Kodėl dabar: {idea['kodel']}")
        lines.append(f"   Pirmas žingsnis: {idea['pirmas_zingsnis']}")
        lines.append("")

    lines.append("Pabaiga.")
    return "\n".join(lines) + "\n"


def main() -> None:
    generated_at = datetime.now()
    rng = Random(generated_at.strftime("%Y-%m-%d"))
    trends = collect_trends(rng)
    ideas = pick_ideas(rng)
    report = build_report(trends, ideas, generated_at)
    OUTPUT_FILE.write_text(report, encoding="utf-8")
    print(f"Ataskaita įrašyta: {OUTPUT_FILE}")
    print(report)


if __name__ == "__main__":
    main()
