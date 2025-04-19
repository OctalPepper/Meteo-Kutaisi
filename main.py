import requests
from bs4 import BeautifulSoup
from metar import Metar

# URL de la page METAR
url = "https://www.bigorre.org/aero/meteo/ugko/fr"

# En-têtes pour la requête HTTP
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

# Récupération de la page
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# Extraction du code METAR
metar_text = soup.find('code').get_text()

# Parsing du code METAR
report = Metar.Metar(metar_text)

# Extraction des informations
vent_direction = report.wind_dir.value()
vent_vitesse = report.wind_speed.value()
qnh = report.press.value()
# Note : Le QFE n'est généralement pas inclus dans le METAR

# Formatage du message
message = f"""**Bilan météo UGKO**

**Vent :** {vent_direction}° à {vent_vitesse} kt
**QNH :** {qnh} hPa
"""

# Envoi du message à Discord
WEBHOOK_URL = "https://discord.com/api/webhooks/..."
data = {"content": message}
requests.post(WEBHOOK_URL, json=data)
