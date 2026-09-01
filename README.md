# Seleniumi kodutöö

Seleniumi ülesannete lahendused (Python + Selenium WebDriver).

## Ülesannete lahendused

| Ülesanne | Fail | Mida teeb |
|----------|------|-----------|
| 1 – Ava Google ja sisesta otsing | `task1_google_otsing.py` | Otsib nime "Ott Saluvere" ja salvestab kuvatõmmise `screenshots/minu_otsing.png` |
| 2 – Leia mitu elementi | `task2_tsitaadid.py` | Leiab kõik tsitaadid lehelt quotes.toscrape.com ja prindib need koos autoritega |
| 3 – Nuppudele klõpsamine | `task3_lisa_eemalda.py` | Vajutab "Add Element" 5 korda ja kustutab siis kõik elemendid ühekaupa |
| 4 – Vormitäitmine | `task4_vormitaitmine.py` | Logib sisse kasutajaga `tomsmith` ja kontrollib teadet "You logged into a secure area!" |
| 5 – Navigatsioon | `task5_navigatsioon.py` | Klõpsab lingil "Checkboxes", märgib mõlemad kastid ja läheb brauseris tagasi |
| 6 – 5 oma automaattesti | `test_ulesanne6.py` | Viis iseseisvat pytest-testi (vt allpool) |

Kaustad:

* `screenshots/` – ülesande 1 kuvatõmmised
* `valjund/` – iga ülesande terminali väljund

## Paigaldamine

```
py -m pip install -r requirements.txt
```

Vaja on ka **chromedriver**-it, mis vastab sinu Chrome'i versioonile, ja see peab olema
PATH-is (vt juhendi 2. samm). Kontroll:

```
chromedriver --version
```

## Käivitamine

Ülesanded 1–5 on tavalised skriptid:

```
py task1_google_otsing.py
py task2_tsitaadid.py
py task3_lisa_eemalda.py
py task4_vormitaitmine.py
py task5_navigatsioon.py
```

Ülesande 6 testid käivitatakse pytestiga:

```
pytest test_ulesanne6.py -v
```

### Valikulised seadistused

Kõik failid kasutavad ühist abifunktsiooni `driver_setup.loo_draiver()`. Selle käitumist
saab muuta keskkonnamuutujatega:

* `BROWSER=firefox` – kasutab Chrome'i asemel Firefoxi (vajab `geckodriver`-it)
* `HEADLESS=1` – ei ava nähtavat brauseriakent

Näiteks Linuxis:

```
BROWSER=firefox HEADLESS=1 pytest test_ulesanne6.py -v
```

## Märkus Google'i kohta (ülesanne 1)

Nagu juhendis lk 4 kirjas, tuvastab Google automatiseeritud brauseri üsna kiiresti ja
paneb ette CAPTCHA "I'm not a robot". Täpselt nii ka juhtus – vt tõendit
`screenshots/google_captcha.png`.

Skript proovib seetõttu esimesena ikkagi Google'it, nagu ülesandes nõutud, ja teeb siis
sama otsingu **DuckDuckGos**, mis on juhendis endas pakutud leebem variant. Nii jääb
faili `screenshots/minu_otsing.png` alati päris otsingutulemustega pilt. Kui Google
mingil masinal siiski läbi laseb, salvestatakse `minu_otsing.png` kohe Google'i
tulemustest ja DuckDuckGot ei kasutata.

Kui käivitad skripti nähtava brauseriga (ilma `HEADLESS=1`), siis CAPTCHA korral
skript **peatub ja ootab**: lahenda "I'm not a robot" brauseriaknas ära ja vajuta
terminalis Enter. Seejärel salvestab skript kuvatõmmise Google'i päris tulemustest.
Kui vajutad kohe Enter, minnakse edasi DuckDuckGole.

Otsingumootori saab ka ise valida keskkonnamuutujaga `OTSINGUMOOTOR`:

```
OTSINGUMOOTOR=duckduckgo py task1_google_otsing.py   # jäta Google'i katse vahele
OTSINGUMOOTOR=google py task1_google_otsing.py       # ainult Google, ilma varulahenduseta
```

## Ülesande 6 testid

| Test | Eesmärk | Kasutatud leidmismeetodid |
|------|---------|---------------------------|
| `test_dropdown_valik` | Rippmenüüst valiku tegemine ja valitud väärtuse kontroll | `By.ID` |
| `test_dunaamiline_element` | Dünaamiliselt ilmuva elemendi ootamine (`WebDriverWait`) | `By.CSS_SELECTOR`, `By.XPATH` |
| `test_sisselogimise_voog` | Mitmesammuline voog: navigeerimine → vormi täitmine → nupp → tulemuse kontroll | `By.LINK_TEXT`, `By.NAME`, `By.CSS_SELECTOR` |
| `test_tabelist_andmete_leidmine` | Tabelist konkreetse rea andmete leidmine ja kontroll | `By.XPATH`, `By.CSS_SELECTOR` |
| `test_sildi_jargi_filtreerimine` | Mitme elemendi oleku kontroll pärast filtreerimist | `By.LINK_TEXT`, `By.CLASS_NAME` |

Iga test avab veebilehe ise ja sulgeb brauseri lõpus (pytest fixture `draiver`), seega on
testid üksteisest sõltumatud.
