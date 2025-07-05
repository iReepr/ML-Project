import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

headers = {
    "User-Agent": "Mozilla/5.0"
}

def chercher_profil_joueur(nom_joueur):
    url = f"https://www.transfermarkt.com/schnellsuche/ergebnis/schnellsuche?query={nom_joueur.replace(' ', '+')}"
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    lien = soup.select_one("a.spielprofil_tooltip")
    if lien:
        return "https://www.transfermarkt.com" + lien.get("href").split("?")[0]
    td = soup.find("td", class_="hauptlink")
    if td and td.find("a"):
        return "https://www.transfermarkt.com" + td.find("a").get("href")
    return None

def extract_end_contract(profil_url):
    r = requests.get(profil_url, headers=headers)
    if r.status_code != 200:
        return None
    soup = BeautifulSoup(r.text, "html.parser")

    divs = soup.select("span.data-header__label")
    for div in divs:
        if "Contract expires" in div.text:
            date_str = div.text.strip().split(":")[-1].strip()
            try:
                return datetime.strptime(date_str, "%b %d, %Y")
            except ValueError:
                try:
                    return datetime.strptime(date_str, "%B %d, %Y")
                except ValueError:
                    pass

    imgs = soup.find_all("img", alt=True)
    for img in imgs:
        alt = img["alt"]
        alt_match = re.search(r"(\w+ \d{1,2}, \d{4})", alt)
        if alt_match:
            date_str = alt_match.group(1)
            for fmt in ("%b %d, %Y", "%B %d, %Y"):
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    continue
    return None

def get_contrat_info(nom_joueur, date_reference):
    url = chercher_profil_joueur(nom_joueur)
    if not url:
        return f"Joueur introuvable : {nom_joueur}"

    print(f"Profil trouvé : {url}")
    fin_contrat = extract_end_contract(url)
    if not fin_contrat:
        return f"Aucune date de fin de contrat trouvée pour {nom_joueur}"

    date_ref = datetime.strptime(date_reference, "%Y-%m-%d")
    delta = fin_contrat - date_ref
    annees_restantes = delta.days // 365
    mois_restants = (delta.days % 365) // 30
    return f"Contrat se termine le {fin_contrat.strftime('%d/%m/%Y')} → Il reste {annees_restantes} an(s) et {mois_restants} mois à la date du {date_reference}"

if __name__ == "__main__":
    url = chercher_profil_joueur("Dean Huijsen")
    if url:
        print(f"Profil trouvé : {url}")
        fin_contrat = extract_end_contract(url)
        if fin_contrat:
            print(f"Date de fin de contrat : {fin_contrat.strftime('%d/%m/%Y')}")
        else:
            print("Aucune date de fin de contrat trouvée.")
    else:
        print("Joueur introuvable.")
