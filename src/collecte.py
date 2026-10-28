from bs4 import BeautifulSoup
from pathlib import Path
import time
import requests
from urllib.parse import urlparse

BASE = "https://www.service-public.gouv.fr"
ENTETES = {"User-Agent": "rag-droit-du-travail (projet etudiant ; contact : kandjifallou114@gmail.com)"}
CACHE = Path("../data/raw/html")

def load_html(director):
    file = CACHE / (director.strip("/").replace("/", "_") + ".html")
    if file.exists():
        print("File {} exist".format(file))
        return file.read_text(encoding="utf-8")
    response = requests.get(BASE + director, headers=ENTETES, timeout=30)
    response.raise_for_status()
    file.write_text(response.text, encoding="utf-8")
    time.sleep(1.5)
    return response.text




def extract_all_link(html, prefixe, selecteur="a[href]"):
    soupe = BeautifulSoup(html, "lxml")
    liens = set()
    for a in soupe.select(selecteur):
        chemin = urlparse(a["href"]).path
        if chemin.startswith(prefixe):
            if prefixe == "/particuliers/vosdroits/F":
                load_html(chemin)
                continue
            else: liens.add(chemin)
    return liens



def extract_fact_sheets(subject_collection):
    fact_sheets = set()
    for n in subject_collection:
        fact_sheets |=(extract_all_link(load_html(n),"/particuliers/vosdroits/F", 'div[data-test="div-content-fiche"] a[href]'))
    for f in sorted(fact_sheets):
        load_html(f)
    return fact_sheets


subject = load_html("/particuliers/vosdroits/N19611")
sub_subject = extract_all_link(subject, "/particuliers/vosdroits/N", 'div[data-test="div-content-fiche"] a[href]')
fact_sheet = extract_all_link(subject, "/particuliers/vosdroits/F", 'div[data-test="div-content-fiche"] a[href]')


extract_fact_sheets(sub_subject)