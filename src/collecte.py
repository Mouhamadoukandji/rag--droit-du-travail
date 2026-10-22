from bs4 import BeautifulSoup
from pathlib import Path
import time
import requests

BASE = "https://www.service-public.gouv.fr"
ENTETES = {"User-Agent": "rag-droit-du-travail (projet etudiant ; contact : kandjifallou114@gmail.com)"}
CACHE = Path("../data/raw/html")

def load_html(director):
    file = CACHE / (director.strip("/").replace("/", "_") + ".html")
    if file.exists():
        print("File {} exist".format(file))
        return file.read_text(encoding="utf-8")
    response = requests.get(BASE + "/" + director, headers=ENTETES, timeout=30)
    response.raise_for_status()
    file.write_text(response.text, encoding="utf-8")
    time.sleep(1.5)
    print(file.read_text(encoding="utf-8"))
    return response.text


from urllib.parse import urlparse

def extract_all_link(html, prefixe, selecteur="a[href]"):
    soupe = BeautifulSoup(html, "lxml")
    liens = set()
    for a in soupe.select(selecteur):
        chemin = urlparse(a["href"]).path
        if chemin.startswith(prefixe):
            liens.add(chemin)
    return liens

subject = load_html("particuliers/vosdroits/N19806")

sub_subject = extract_all_link(subject, "/particuliers/vosdroits/N",
                         'a[data-test="href-lien-dossier"]')
print(sub_subject)


# 2. Fiches de chaque sous-thème
fiches = set()

for n in sub_subject:
    print('je fais le test')
    print(n)
    fiches |=(extract_all_link(load_html(n.lstrip("/")),"/particuliers/vosdroits/F", 'a[data-test="href-lien-fiche"]'))
    print(fiches)

# 3. Téléchargement de toutes les fiches
for f in sorted(fiches):
    load_html(f)
