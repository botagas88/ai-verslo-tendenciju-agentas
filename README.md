# AI Verslo Tendencijų Agentas

Paprastas Python projektas, kuris **imituoja** verslo tendencijų rinkimą ir į failą `business_ideas.txt` įrašo tekstinę ataskaitą su **3 verslo idėjomis**.

Šis agentas nenaudoja mokamo AI API ir neskenuoja interneto. Tendencijos ir idėjos parenkamos iš projekte esančio sąrašo (pagal datą, kad tą pačią dieną rezultatas būtų toks pat).

## Kaip paleisti vietoje

Reikia [Python 3.10+](https://www.python.org/downloads/). Papildomų bibliotekų diegti nereikia.

```bash
python main.py
```

Windows PowerShell:

```powershell
python main.py
```

Po paleidimo atsiras (arba atsinaujins) `business_ideas.txt`. Konsolėje pamatysite tą pačią ataskaitą.

## Projekto failai

| Failas | Paskirtis |
| --- | --- |
| `main.py` | Agentas: tendencijos + 3 idėjos + ataskaita |
| `business_ideas.txt` | Sugeneruota ataskaita (sukuriama paleidus skriptą) |
| `.github/workflows/daily-report.yml` | Automatinis paleidimas GitHub |

## Kaip įkelti į GitHub ir paleisti automatiškai

### 1. Įdiekite Git (jei dar nėra)

1. Atsisiųskite: https://git-scm.com/download/win  
2. Įdiekite su numatytaisiais nustatymais.  
3. Uždarykite ir vėl atidarykite terminalą.

Patikra:

```powershell
git --version
```

### 2. Sukurkite GitHub paskyrą ir tuščią repozitoriją

1. Prisijunkite: https://github.com  
2. **New repository**  
3. Pavadinimas, pvz. `ai-verslo-tendenciju-agentas`  
4. Palikite **Public** (Actions su nemokamu limitu viešoms repo veikia paprasčiau)  
5. **Nepažymėkite** README, `.gitignore` ar licencijos – failai jau yra projekte  
6. Sukurkite repozitoriją ir nukopijuokite URL (`https://github.com/JUSU-VARDAS/ai-verslo-tendenciju-agentas.git`)

### 3. Nusiųskite šį projektą

PowerShell, projekto aplanke `C:\Users\rimvy\ai-verslo-tendenciju-agentas`:

```powershell
git init
git add .
git commit -m "Pirmas AI Verslo Tendencijų Agento įkėlimas"
git branch -M main
git remote add origin https://github.com/JUSU-VARDAS/ai-verslo-tendenciju-agentas.git
git push -u origin main
```

Pakeiskite `JUSU-VARDAS` savo GitHub vartotojo vardu. Pirmą kartą GitHub paprašys prisijungti (naršyklė arba Personal Access Token).

Jei `git` vis dar nerandamas, įdiekite Git ir paleiskite komandas iš naujo.

### 4. Nustatykite automatinį veikimą (GitHub Actions)

Projekte jau yra workflow failas `.github/workflows/daily-report.yml`. Jis:

- kasdien **06:00 UTC** paleidžia `python main.py`
- atnaujina `business_ideas.txt` ir, jei failas pasikeitė, padaro commit į `main`

Ką padaryti jums:

1. GitHub repo atidarykite skirtuką **Actions**  
2. Jei GitHub klausia, įjunkite Actions šiai repozitorijai  
3. Palikite workflow **Kasdienė verslo ataskaita** įjungtą  

Rankinis testas (nelaukiant kitos dienos):

1. **Actions** → **Kasdienė verslo ataskaita**  
2. **Run workflow** → **Run workflow**  
3. Palaukite, kol job'as taps žalias  
4. Patikrinkite, ar `business_ideas.txt` atsirado / atsinaujino repozitorijoje  

Planiniai (`schedule`) paleidimai GitHub kartais vėluoja keliomis minutėmis. Viešose repo Actions paprastai įjungiami automatiškai; privačiose – patikrinkite **Settings → Actions → General**.

### 5. Jei push nepavyksta dėl teisių

Workflow turi `permissions: contents: write`. Jei commit vis tiek nepavyksta:

**Settings → Actions → General → Workflow permissions** → **Read and write permissions** → išsaugokite.

## Pastabos

- Tai mokomasis pavyzdys, ne finansinis ar teisinis patarimas.  
- Norėdami tikrų naujienų, vėliau galite prijungti naujienų API ar AI modelį – dabar sąmoningai palikta paprasta imitacija.
