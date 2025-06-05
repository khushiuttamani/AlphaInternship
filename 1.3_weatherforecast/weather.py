import requests
import os
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env file

def get_weather(city, api_key):
    base_url = "https://api.openweathermap.org/data/2.5/weather" #api for weather
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        main = data['main']
        weather = data['weather'][0]
        wind = data['wind']

        # print the description of the required place
        print(f"\nWeather in {city.title()}:")  
        print(f"Description: {weather['description'].title()}")
        print(f"Temperature: {main['temp']} °C")
        print(f"Feels Like: {main['feels_like']} °C")
        print(f"Humidity: {main['humidity']}%")
        print(f"Wind Speed: {wind['speed']} m/s")
    else:
        print("City not found or API request failed.")

def main():
    api_key = os.getenv("OPENWEATHER_API_KEY")  # get API key from .env
    if not api_key:
        print("API key not found. Please set it in the .env file.")
        return
    
    city = input("Enter city name: ")
    get_weather(city, api_key)

if __name__ == "__main__":
    main()
