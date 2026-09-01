"""Ülesanne 2 - Leia mitu elementi.

Avab quotes.toscrape.com, leiab esimeselt lehelt kõik tsitaadid (klass "text")
ja prindib need välja koos autoritega.
"""

from selenium.webdriver.common.by import By

from driver_setup import loo_draiver


def main():
    draiver = loo_draiver()
    try:
        draiver.get("https://quotes.toscrape.com")

        tsitaadid = draiver.find_elements(By.CLASS_NAME, "text")
        autorid = draiver.find_elements(By.CLASS_NAME, "author")

        print(f"Leidsin {len(tsitaadid)} tsitaati:\n")
        for nr, (tsitaat, autor) in enumerate(zip(tsitaadid, autorid), start=1):
            print(f"{nr}. {tsitaat.text}")
            print(f"   - {autor.text}\n")
    finally:
        draiver.quit()


if __name__ == "__main__":
    main()
