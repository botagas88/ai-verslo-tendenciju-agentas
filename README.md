# AI Verslo Tendencijų Agentas

Python projektas, kuris **renka realias AI / verslo naujienas** (RSS ir DuckDuckGo), **analizuoja jas su OpenAI arba Claude** ir įrašo trumpą įžvalgų ataskaitą į `business_ideas.txt`. Jei sukonfigūruotas SMTP, ataskaitą galima gauti **el. paštu**.

## Kaip paleisti vietoje

Reikia [Python 3.10+](https://www.python.org/downloads/).

```powershell
cd C:\Users\rimvy\ai-verslo-tendenciju-agentas
python -m pip install -r requirements.txt
copy .env.example .env
```

Užpildykite `.env`:

1. `OPENAI_API_KEY` (arba `ANTHROPIC_API_KEY`, jei naudojate Claude)
2. El. paštui (nebūtina): `SMTP_*`, `EMAIL_FROM`, `EMAIL_TO`

Gmail: įjunkite dviejų žingsnių patvirtinimą ir sukurkite [programos slaptažodį](https://support.google.com/accounts/answer/185833). `SMTP_PASSWORD` turi būti tas 16 simbolių slaptažodis, ne įprastas Gmail slaptažodis.

```powershell
python main.py
```

Po paleidimo atsinaujins `business_ideas.txt`. Konsolėje pamatysite tą pačią ataskaitą. Jei el. paštas sukonfigūruotas, laiškas išsiunčiamas gavėjui.

## Projekto failai

| Failas | Paskirtis |
| --- | --- |
| `main.py` | Naujienos + AI analizė + el. paštas |
| `requirements.txt` | Python bibliotekos |
| `.env.example` | Slaptažodžių ir raktų šablonas (be tikrų reikšmių) |
| `.env` | Jūsų raktai (nekeliamas į Git) |
| `business_ideas.txt` | Sugeneruota ataskaita |
| `.github/workflows/daily-report.yml` | Automatinis paleidimas GitHub |

## GitHub Actions

Workflow kasdien **06:00 UTC** paleidžia `python main.py`, atnaujina `business_ideas.txt` ir, jei pasikeitė, padaro commit.

**Settings → Secrets and variables → Actions** pridėkite:

| Secret | Privaloma |
| --- | --- |
| `OPENAI_API_KEY` | Taip (arba `ANTHROPIC_API_KEY`) |
| `SMTP_HOST` | Tik jei norite el. pašto |
| `SMTP_PORT` | Tik jei norite el. pašto (pvz. `587`) |
| `SMTP_USER` | Tik jei norite el. pašto |
| `SMTP_PASSWORD` | Tik jei norite el. pašto |
| `EMAIL_FROM` | Tik jei norite el. pašto |
| `EMAIL_TO` | Tik jei norite el. pašto |

Rankinis testas: **Actions** → **Kasdienė verslo ataskaita** → **Run workflow**.

Jei Actions commit nepavyksta: **Settings → Actions → General → Workflow permissions** → **Read and write permissions**.

## Pastabos

- Tai mokomasis įrankis, ne finansinis ar teisinis patarimas.
- Naujienų šaltiniai ir AI modelis gali kisti; jei paieška laikinai nepavyksta, agentas vis tiek bando kitus šaltinius.
