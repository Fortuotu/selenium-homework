"""Ühine abifunktsioon Seleniumi veebidraiveri loomiseks.

Vaikimisi kasutatakse Chrome'i (nagu ülesande juhendis).
Keskkonnamuutujatega saab käitumist muuta:
    BROWSER=firefox   -> kasuta Chrome'i asemel Firefoxi
    HEADLESS=1        -> ära ava nähtavat brauseriakent
"""

import os
import shutil

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService


def loo_draiver():
    """Loob ja tagastab seadistatud WebDriveri."""
    brauser = os.environ.get("BROWSER", "chrome").lower()
    headless = os.environ.get("HEADLESS", "") == "1"

    if brauser == "firefox":
        valikud = webdriver.FirefoxOptions()
        if headless:
            valikud.add_argument("-headless")
        draiver = webdriver.Firefox(
            options=valikud, service=FirefoxService(_draiveri_tee("geckodriver"))
        )
    else:
        valikud = webdriver.ChromeOptions()
        if headless:
            valikud.add_argument("--headless=new")
        draiver = webdriver.Chrome(
            options=valikud, service=ChromeService(_draiveri_tee("chromedriver"))
        )

    # Aknasuurus on fikseeritud, et kuvatõmmised oleksid alati ühesugused.
    draiver.set_window_size(1920, 1080)
    # Väike automaatne ootamine, kui element pole veel lehele jõudnud.
    draiver.implicitly_wait(5)
    return draiver


def _draiveri_tee(nimi):
    """Otsib draiveri PATH-ist (juhendi 2. samm).

    Kui seda seal pole, tagastame None ja Selenium proovib selle ise leida.
    """
    return shutil.which(nimi)
