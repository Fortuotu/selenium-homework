"""Ülesanne 6 - 5 oma automaattesti.

Käivitamine:  pytest test_ulesanne6.py -v

Iga test avab vajaliku veebilehe ise ja fixture sulgeb brauseri testi lõpus,
seega on testid üksteisest sõltumatud.
"""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from driver_setup import loo_draiver


@pytest.fixture
def draiver():
    """Annab igale testile värske brauseri ja sulgeb selle lõpus."""
    d = loo_draiver()
    yield d
    d.quit()


def test_dropdown_valik(draiver):
    """Rippmenüüst valiku tegemine ja valitud väärtuse kontrollimine."""
    draiver.get("https://the-internet.herokuapp.com/dropdown")

    rippmenuu = Select(draiver.find_element(By.ID, "dropdown"))
    assert len(rippmenuu.options) == 3, "Rippmenüüs peaks olema 3 valikut"

    rippmenuu.select_by_visible_text("Option 2")

    assert rippmenuu.first_selected_option.text == "Option 2"
    assert rippmenuu.first_selected_option.get_attribute("value") == "2"


def test_dunaamiline_element(draiver):
    """Dünaamiliselt ilmuva elemendi ootamine ja kontrollimine."""
    draiver.get("https://the-internet.herokuapp.com/dynamic_loading/2")

    draiver.find_element(By.CSS_SELECTOR, "#start button").click()

    # Tekst "Hello World!" luuakse lehele alles paari sekundi pärast.
    tulemus = WebDriverWait(draiver, 15).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@id='finish']/h4"))
    )
    assert tulemus.text == "Hello World!"

    # Laadimisriba peab olema selleks hetkeks ära peidetud.
    assert not draiver.find_element(By.ID, "loading").is_displayed()


def test_sisselogimise_voog(draiver):
    """Mitmesammuline voog: avaleht -> login-vorm -> nupp -> tulemuse kontroll."""
    draiver.get("https://quotes.toscrape.com")
    assert draiver.find_elements(By.LINK_TEXT, "Logout") == [], "Ei tohiks veel sisse logitud olla"

    # 1. samm: navigeerimine menüülingi kaudu
    draiver.find_element(By.LINK_TEXT, "Login").click()
    assert draiver.current_url.endswith("/login")

    # 2. samm: vormi täitmine
    draiver.find_element(By.NAME, "username").send_keys("ott")
    draiver.find_element(By.NAME, "password").send_keys("parool123")

    # 3. samm: nupule vajutamine
    draiver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

    # 4. samm: tulemuse kontrollimine
    logout = WebDriverWait(draiver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Logout"))
    )
    assert logout.is_displayed(), "Pärast sisselogimist peaks ilmuma 'Logout' link"
    assert draiver.find_elements(By.LINK_TEXT, "Login") == [], "'Login' link peaks kaduma"


def test_tabelist_andmete_leidmine(draiver):
    """Tabelist konkreetse rea andmete leidmine ja kontrollimine."""
    draiver.get("https://the-internet.herokuapp.com/tables")

    read = draiver.find_elements(By.CSS_SELECTOR, "#table1 tbody tr")
    assert len(read) == 4, "Tabelis peaks olema 4 rida"

    # Otsime XPathiga rea, mille perekonnanimi on "Doe", ja loeme sealt "Due" veeru.
    summa = draiver.find_element(
        By.XPATH, "//table[@id='table1']//tr[td[1]='Doe']/td[4]"
    ).text
    assert summa == "$100.00", f"Doe võlg peaks olema $100.00, aga on {summa}"

    # Kontrollime ka, et igal real on kõik 6 veergu täidetud.
    for rida in read:
        lahtrid = rida.find_elements(By.TAG_NAME, "td")
        assert len(lahtrid) == 6
        assert lahtrid[2].text.strip() != "", "E-posti veerg ei tohiks olla tühi"


def test_sildi_jargi_filtreerimine(draiver):
    """Mitme elemendi oleku kontroll: filtreerimine sildi järgi."""
    draiver.get("https://quotes.toscrape.com")

    silt = "humor"
    draiver.find_element(By.LINK_TEXT, silt).click()
    assert f"/tag/{silt}/" in draiver.current_url

    tsitaadid = draiver.find_elements(By.CLASS_NAME, "quote")
    assert len(tsitaadid) > 0, "Filtreeritud lehel peab olema vähemalt üks tsitaat"

    # Igal lehel oleval tsitaadil peab see silt küljes olema.
    for tsitaat in tsitaadid:
        sildid = [s.text for s in tsitaat.find_elements(By.CLASS_NAME, "tag")]
        assert silt in sildid, f"Tsitaadil puudub silt '{silt}', sildid olid {sildid}"
