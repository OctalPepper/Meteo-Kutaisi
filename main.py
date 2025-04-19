import requests
from bs4 import BeautifulSoup

WEBHOOK_URL = "https://discord.com/api/webhooks/..."

def get_meteo_ugko():
    url = "https://www.bigorre.org/aero/meteo/ugko/fr"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    def find_value(label):
        row = soup.find("td", string=label)
        if row:
            next_td = row.find_next_sibling("td")
            if next_td:
                return next_td.text.strip()
        return "Non disponible"

    vent = find_value("Vent")
    couverture = find_value("Couverture nuageuse")
    qnh = find_value("QNH")
    qfe = find_value("QFE")
    piste = find_value("Piste en service")

    message = f"""**Bilan météo UGKO**

**Vent :** {vent}
**Couverture nuageuse :** {couverture}
**QNH :** {qnh}
**QFE :** {qfe}
**Piste en service :** {piste}
"""

    return message

def send_to_discord(message):
    data = {
        "content": message
    }
    requests.post(WEBHOOK_URL, json=data)

if __name__ == "__main__":
    meteo = get_meteo_ugko()
    send_to_discord(meteo)
