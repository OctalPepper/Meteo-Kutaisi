import requests
from bs4 import BeautifulSoup

# Ton URL webhook Discord
WEBHOOK_URL = "https://discord.com/api/webhooks/1362851767494250797/NZA_R2SPfK9ijEukU07cAZGDLM-Q26IBpdu2Hpei4SMVAElc8x-MC4zdK-STeQ1fuyUZ"

def get_meteo_ugko():
    url = "https://www.bigorre.org/aero/meteo/ugko/fr"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    def find_value(label):
        row = soup.find("td", string=label)
        if row:
            return row.find_next_sibling("td").text.strip()
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
