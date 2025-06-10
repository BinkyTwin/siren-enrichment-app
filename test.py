import requests
import urllib.parse

BASE_URL = "https://recherche-entreprises.api.gouv.fr"
TERME    = "Abdelatif Djeddou"
CP       = "93350"
PER_PAGE = 5

def recherche_filtrée(api_base, terme, code_postal, per_page=5):
    q   = urllib.parse.quote(terme, safe="")
    # On utilise code_postal (snake_case) et non codePostal
    url = (
        f"{api_base}/search"
        f"?q={q}"
        f"&code_postal={code_postal}"
        f"&per_page={per_page}"
    )
    r = requests.get(url)
    print("> URL appelée :", r.request.url)
    print("> Status       :", r.status_code)
    r.raise_for_status()

    results = r.json().get("results", [])
    if not results:
        print(f"> Aucun résultat pour « {terme} » dans le {code_postal}")
        return None

    premier = results[0]
    siren   = premier.get("siren", "<siren absent>")
    nom     = (
        premier.get("denomination")
        or premier.get("denominationUniteLegale")
        or premier.get("nom_raison_sociale")
        or premier.get("nom_complet")
        or "<nom inconnu>"
    )
    siege_cp = premier.get("siege", {}).get("code_postal", "<CP inconnu>")
    print(f"> Match filtré → SIREN: {siren}  |  Nom : {nom}  |  CP du siège : {siege_cp}")
    return premier

if __name__ == "__main__":
    recherche_filtrée(BASE_URL, TERME, CP, PER_PAGE)
