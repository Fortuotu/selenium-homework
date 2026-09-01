"""Ülesanne 1 - Ava Google ja sisesta otsing.

Avab brauseri, läheb Google'i avalehele, otsib minu nime ja teeb tulemustest
kuvatõmmise faili screenshots/minu_otsing.png.

Nagu juhendi lk 4 kirjeldab, tuvastab Google automatiseeritud brauseri kiiresti ja
paneb ette CAPTCHA "I'm not a robot". Sel juhul salvestab skript tõendina CAPTCHA
kuvatõmmise ja teeb sama otsingu uuesti DuckDuckGos, mis on juhendis pakutud
leebem variant. Nii jääb minu_otsing.png-i alati päris otsingutulemustega pilt.
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


def main():
    os.makedirs(KAUST, exist_ok=True)
    draiver = loo_draiver()
    try:
        # 1. katse: Google, nagu ülesandes nõutud.
        otsi(draiver, "https://www.google.com")
        if draiver.find_elements(By.ID, "search"):
            draiver.save_screenshot(KUVATOMMIS)
            print("Google'i otsingutulemused salvestatud:", KUVATOMMIS)
            return

        draiver.save_screenshot(CAPTCHA_KUVATOMMIS)
        print(
            "Google tuvastas roboti ja näitas CAPTCHA-t (vt juhendi lk 4).\n"
            f"Salvestasin selle tõendiks: {CAPTCHA_KUVATOMMIS}\n"
            "Teen sama otsingu DuckDuckGos, mis on juhendis pakutud leebem variant."
        )

        # 2. katse: DuckDuckGo ei blokeeri Seleniumi.
        otsi(draiver, "https://duckduckgo.com")
        tulemused = draiver.find_elements(By.CSS_SELECTOR, "[data-testid='result']")
        draiver.save_screenshot(KUVATOMMIS)
        print(f"DuckDuckGo leidis {len(tulemused)} tulemust")
        print("Otsingutulemused salvestatud:", KUVATOMMIS)
    finally:
        draiver.quit()


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
