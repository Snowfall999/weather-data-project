import requests
from datetime import datetime
import json  # <-- On importe le module JSON

# Variables globales
api_key = "2174404ed8b12ca6f8b753503e7bd6d6"
city_name = "abidjan"
root_url = "https://api.openweathermap.org/data/2.5/weather"
url = f"{root_url}?q={city_name}&appid={api_key}&units=metric&lang=fr"

def fetch_weather():
    try:
        response = requests.get(url)
        response.raise_for_status()
        print("Réponse API reçue avec succès.")
        return response.json()
    except requests.RequestException as e:
        print(f"Erreur lors de la récupération des données météo : {e}")
        return None

def extract_fetch_weather(data):
    if not data:
        print("Aucune donnée disponible.")
        return None

    try:
        dt_object = datetime.fromtimestamp(data['dt'])
        date = dt_object.date().isoformat()   
        heure = dt_object.time().isoformat()
        temp = data['main']['temp']
        pressure = data['main']['pressure']
        humidity = data['main']['humidity']
        wind = data['wind']['speed']
        description = data.get('weather', [{}])[0].get('description', None)



        return {
            "ville": city_name,
            "heure": heure ,
            "date": date,
            "temperature": temp,
            "pression": pressure,
            "humidite": humidity,
            "vent": wind,
            "description":description,
        }

    except KeyError as e:
        print(f"Erreur de lecture des données : {e}")
        return None

# Exécution
if __name__ == "__main__":
    data = fetch_weather()
    weather_info = extract_fetch_weather(data)

    if weather_info:
        # Affichage sous forme de JSON bien formaté
        print(json.dumps(weather_info, indent=4, ensure_ascii=False))
