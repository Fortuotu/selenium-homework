"""Ülesanne 3 - Nuppudele klõpsamine.

Vajutab nuppu "Add Element" 5 korda ja kustutab seejärel kõik lisatud
elemendid ühekaupa.
"""

from selenium.webdriver.common.by import By

from driver_setup import loo_draiver

KORDI = 5


def main():
    draiver = loo_draiver()
    try:
        draiver.get("https://the-internet.herokuapp.com/add_remove_elements/")

        lisa_nupp = draiver.find_element(By.CSS_SELECTOR, "button[onclick='addElement()']")
        for i in range(1, KORDI + 1):
            lisa_nupp.click()
            print(f"Vajutasin 'Add Element' {i}. korda")

        lisatud = draiver.find_elements(By.CLASS_NAME, "added-manually")
        print(f"\nLehel on nüüd {len(lisatud)} 'Delete' nuppu")
        assert len(lisatud) == KORDI, f"Oodati {KORDI} nuppu, aga leiti {len(lisatud)}"

        # Iga kustutamise järel otsime nupud uuesti, sest vana viide muutub kehtetuks.
        while True:
            nupud = draiver.find_elements(By.CLASS_NAME, "added-manually")
            if not nupud:
                break
            nupud[0].click()
            print(f"Kustutasin ühe elemendi, alles on {len(nupud) - 1}")

        alles = draiver.find_elements(By.CLASS_NAME, "added-manually")
        assert not alles, f"Kõik elemendid ei kustutatud, alles on {len(alles)}"
        print("\nKõik lisatud elemendid on kustutatud.")
    finally:
        draiver.quit()


if __name__ == "__main__":
    main()
