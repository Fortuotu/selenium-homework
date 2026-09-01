"""Ülesanne 1 - Ava Google ja sisesta otsing.

Avab brauseri, otsib minu nime ja teeb tulemustest kuvatõmmise faili
screenshots/minu_otsing.png.

Nagu juhendi lk 4 kirjeldab, tuvastab Google automatiseeritud brauseri kiiresti ja
paneb ette CAPTCHA "I'm not a robot". Sel juhul salvestab skript tõendina CAPTCHA
kuvatõmmise ja teeb sama otsingu uuesti DuckDuckGos, mis on juhendis pakutud
leebem variant. Nii jääb minu_otsing.png-i alati päris otsingutulemustega pilt.

Keskkonnamuutujaga saab otsingumootori ka ise valida:
    OTSINGUMOOTOR=duckduckgo   -> jäta Google'i katse vahele
    OTSINGUMOOTOR=google       -> proovi ainult Google'it, ilma varulahenduseta
"""

import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from driver_setup import loo_draiver

OTSINGUSONA = "Ott Saluvere"
KAUST = "screenshots"
KUVATOMMIS = os.path.join(KAUST, "minu_otsing.png")
CAPTCHA_KUVATOMMIS = os.path.join(KAUST, "google_captcha.png")

GOOGLE = "https://www.google.com"
DUCKDUCKGO = "https://duckduckgo.com"

# Kuidas tuvastada, et lehel on päris otsingutulemused.
TULEMUSTE_VALIJA = {
    GOOGLE: (By.ID, "search"),
    DUCKDUCKGO: (By.CSS_SELECTOR, "[data-testid='result']"),
}


def main():
    os.makedirs(KAUST, exist_ok=True)
    valik = os.environ.get("OTSINGUMOOTOR", "").lower()
    draiver = loo_draiver()
    try:
        if valik == "duckduckgo":
            otsi_ja_salvesta(draiver, DUCKDUCKGO)
            return

        # Vaikimisi proovime Google'it, nagu ülesandes nõutud.
        if otsi_ja_salvesta(draiver, GOOGLE) or valik == "google":
            return

        # Google blokeeris - salvestame selle tõendiks ja läheme DuckDuckGole.
        draiver.save_screenshot(CAPTCHA_KUVATOMMIS)
        print(
            "Google tuvastas roboti ja näitas CAPTCHA-t (vt juhendi lk 4).\n"
            f"Salvestasin selle tõendiks: {CAPTCHA_KUVATOMMIS}\n"
            "Teen sama otsingu DuckDuckGos, mis on juhendis pakutud leebem variant."
        )
        otsi_ja_salvesta(draiver, DUCKDUCKGO)
    finally:
        draiver.quit()


def otsi_ja_salvesta(draiver, url):
    """Teeb otsingu ja salvestab kuvatõmmise. Tagastab True, kui tulemusi oli."""
    otsi(draiver, url)

    tulemused = draiver.find_elements(*TULEMUSTE_VALIJA[url])
    if not tulemused:
        print("Otsingutulemusi ei leitud.")
        return False

    draiver.save_screenshot(KUVATOMMIS)
    print(f"Leidsin {len(tulemused)} tulemust")
    print("Kuvatõmmis salvestatud:", KUVATOMMIS)
    return True


def otsi(draiver, url):
    """Avab otsingumootori avalehe ja sisestab otsingusõna."""
    draiver.get(url)
    time.sleep(2)
    noustu_kupsistega(draiver)

    # Nii Google'i kui DuckDuckGo otsingukastil on nimi "q".
    otsingukast = draiver.find_element(By.NAME, "q")
    otsingukast.send_keys(OTSINGUSONA)
    otsingukast.send_keys(Keys.RETURN)
    time.sleep(3)

    print(f"\nOtsisin '{OTSINGUSONA}' lehel {url}")
    print("Lehe pealkiri:", draiver.title)


def noustu_kupsistega(draiver):
    """Klõpsab küpsiste nõusoleku nupul, kui see on lehel olemas."""
    for tekst in ("Nõustun kõigiga", "Accept all", "Nõustu kõigiga"):
        nupud = draiver.find_elements(By.XPATH, f"//button[.//div[text()='{tekst}']]")
        if nupud:
            nupud[0].click()
            time.sleep(1)
            return


if __name__ == "__main__":
    main()
