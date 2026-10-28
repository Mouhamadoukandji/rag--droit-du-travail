from pathlib import Path
from bs4 import BeautifulSoup

DIRECTORY = Path("../data/raw/html")


def extract_data(directory: Path):
    all_information = {}
    for file in directory.rglob("*.html"):
        if "particuliers_vosdroits_F" in file.name:
            soup = BeautifulSoup(file.open(), features="html.parser")
            all_information["title"] = soup.select_one('h1[data-test="titre-page"]')
            all_information["url"] = soup.select_one('link[rel="canonical"]')["href"]
            fil_ariane = soup.select('ol[data-test="ol-filDAriane"] li')
            for a in fil_ariane:
                print(a.get_text())
            for k in all_information.keys():
                if k == "title":
                    print("titre :", all_information[k].get_text())
                else: print("url :", all_information["url"])

    return 0

print(extract_data(DIRECTORY))
