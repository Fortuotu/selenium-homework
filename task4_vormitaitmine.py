"""Ülesanne 4 - Vormitäitmine.

Logib sisse lehel the-internet.herokuapp.com/login ja kontrollib, kas ilmub
teade "You logged into a secure area!".
"""

import sys

from selenium.webdriver.common.by import By

from driver_setup import loo_draiver

KASUTAJANIMI = "tomsmith"
PAROOL = "SuperSecretPassword!"
OODATUD_TEADE = "You logged into a secure area!"


def main():
    draiver = loo_draiver()
    try:
        draiver.get("https://the-internet.herokuapp.com/login")

        draiver.find_element(By.ID, "username").send_keys(KASUTAJANIMI)
        draiver.find_element(By.ID, "password").send_keys(PAROOL)
        draiver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        teade = draiver.find_element(By.ID, "flash").text
        print("Sisestasin kasutajanime:", KASUTAJANIMI)
        print("Lehe teade:", teade.replace("×", "").strip())
        print("Praegune URL:", draiver.current_url)

        if OODATUD_TEADE in teade:
            print(f"\nTEST ÕNNESTUS: leidsin oodatud teate '{OODATUD_TEADE}'")
            return 0

        print(f"\nTEST EBAÕNNESTUS: teadet '{OODATUD_TEADE}' ei leitud")
        return 1
    finally:
        draiver.quit()


if __name__ == "__main__":
    sys.exit(main())
