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
import sys
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
        if otsi_ja_salvesta(draiver, GOOGLE):
            return

        # Google blokeeris. Kui brauser on nähtav, saab kasutaja CAPTCHA ise lahendada.
        if oota_captcha_lahendamist(draiver):
            return

        if valik == "google":
            print("Google ei andnud tulemusi ja varulahendus on välja lülitatud.")
            return

        # Salvestame CAPTCHA tõendiks ja läheme DuckDuckGole.
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
    return salvesta_tulemused(draiver, url)


def salvesta_tulemused(draiver, url):
    """Salvestab kuvatõmmise, kui lehel on päris otsingutulemused."""
    tulemused = draiver.find_elements(*TULEMUSTE_VALIJA[url])
    if not tulemused:
        print("Otsingutulemusi ei leitud.")
        return False

    draiver.save_screenshot(KUVATOMMIS)
    print(f"Leidsin {len(tulemused)} tulemust")
    print("Kuvatõmmis salvestatud:", KUVATOMMIS)
    return True


def oota_captcha_lahendamist(draiver):
    """Ootab, kuni kasutaja CAPTCHA ise ära lahendab, ja kontrollib siis tulemusi.

    Töötab ainult nähtava brauseriga käsurealt (HEADLESS=1 korral pole midagi
    lahendada). Tagastab True, kui pärast lahendamist olid tulemused olemas.
    """
    if os.environ.get("HEADLESS") == "1" or not sys.stdin.isatty():
        return False

    print(
        "\nGoogle näitab CAPTCHA-t 'I'm not a robot'.\n"
        "Lahenda see brauseriaknas ja vajuta siis siin Enter, et skript jätkaks\n"
        "(või vajuta lihtsalt Enter, et minna edasi DuckDuckGole)."
    )
    input()

    return salvesta_tulemused(draiver, GOOGLE)


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


# Google'i küpsiseteate nuppude id-d ("Nõustu kõigiga" ja "Keeldu kõigist").
KUPSISENUPUD = [
    (By.ID, "L2AGLb"),
    (By.ID, "W0wltc"),
    (By.XPATH, "//button[contains(., 'Nõustu kõigiga')]"),
    (By.XPATH, "//button[contains(., 'Accept all')]"),
]


def noustu_kupsistega(draiver):
    """Sulgeb küpsiste nõusolekuteate, kui see otsingukasti ette jääb.

    Ilma selleta jääb skript Google'i lehel "Enne Google'i avamist" akna taha kinni.
    """
    for asukoht in KUPSISENUPUD:
        for nupp in draiver.find_elements(*asukoht):
            if not nupp.is_displayed():
                continue
            # Tavaline klõps ei pruugi ülekattel mõjuda, seega klõpsame JavaScriptiga.
            draiver.execute_script("arguments[0].click();", nupp)
            print("Sulgesin küpsiste nõusolekuteate.")
            time.sleep(2)
            return


if __name__ == "__main__":
    main()
