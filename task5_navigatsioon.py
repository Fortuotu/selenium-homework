"""Ülesanne 5 - Navigatsioon.

Avab the-internet.herokuapp.com, klõpsab lingil "Checkboxes", märgib mõlemad
kastid ära ja läheb siis Seleniumi abil brauseris tagasi eelmisele lehele.
"""

from selenium.webdriver.common.by import By

from driver_setup import loo_draiver

AVALEHT = "https://the-internet.herokuapp.com/"


def main():
    draiver = loo_draiver()
    try:
        draiver.get(AVALEHT)
        print("Avasin avalehe:", draiver.current_url)

        draiver.find_element(By.LINK_TEXT, "Checkboxes").click()
        print("Klõpsasin lingil 'Checkboxes', olen nüüd:", draiver.current_url)

        kastid = draiver.find_elements(By.CSS_SELECTOR, "#checkboxes input[type='checkbox']")
        print(f"Leidsin {len(kastid)} märkeruutu")
        for nr, kast in enumerate(kastid, start=1):
            if not kast.is_selected():
                kast.click()
                print(f"  Märkeruut {nr} sai linnukese")
            else:
                print(f"  Märkeruut {nr} oli juba märgitud")

        assert all(kast.is_selected() for kast in kastid), "Kõik kastid ei ole märgitud"
        print("Mõlemad kastid on nüüd märgitud.")

        draiver.back()
        print("Läksin tagasi, olen nüüd:", draiver.current_url)
        assert draiver.current_url.rstrip("/") == AVALEHT.rstrip("/")
        print("Tagasi avalehel - ülesanne tehtud.")
    finally:
        draiver.quit()


if __name__ == "__main__":
    main()
