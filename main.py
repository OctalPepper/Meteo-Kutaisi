import requests
from bs4 import BeautifulSoup
from metar import Metar

# Paramètres
url = "https://www.bigorre.org/aero/meteo/ugko/fr"
headers = {"User-Agent": "Mozilla/5.0"}
webhook_url = "https://discord.com/api/webhooks/..."  # Ton webhook ici

# Récupérer la page
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# Chercher un bloc contenant du METAR (on cherche une ligne commençant par 'UGKO')
metar_text = None
for tag in soup.find_all(text=True):
    if tag.strip().startswith("UGKO") and len(tag.strip()) > 30:
        metar_text = tag.strip()
        break

if metar_text:
    try:
        metar_obj = Metar.Metar(metar_text)
        vent = f"{metar_obj.wind_dir.value()}° à {metar_obj.wind_speed.value()} kt"
        qnh = f"{metar_obj.press.value()} hPa"
        ciel = metar_obj.sky_conditions() or "Non disponible"
        piste = "Non précisée dans le METAR"
        
        message = f"""**Bilan météo UGKO**

**Vent :** {vent}
**Ciel :** {ciel}
**QNH :** {qnh}
**Piste en service :** {piste}
"""
    except Exception as e:
        message = f"Erreur lors de l'analyse du METAR : {e}"
else:
    message = "Impossible de récupérer le METAR sur la page."

# Envoi à Discord
requests.post(webhook_url, json={"content": message})
