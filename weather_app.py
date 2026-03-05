#-------Weather App-------

"""
    A CLI-based application that fetches and displays
    real-time weather data using OpenWeatherMap API.
    
    Functionality:
        - Sends a GET request to OpenWeatherMap API
        - Parses the JSON response
        - Extracts city, country, temperature, humidity, weather condition, wind speed
        - Prints a nicely formatted weather report
        - Handles errors like city not found or network issues 
"""
import requests 
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv() 

def get_weather(city_name, api_key):
    
    """
    Fetch weather data from OpenWeatherMap API.

    Parameters:
        city_name (str): Name of the city.
        api_key (str): API key for authentication.
    """
    
    base_url = "https://api.openweathermap.org/data/2.5/weather"   # OpenWeatherMap endpoint
    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric" 
    }

    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json() 
        
        # Check API response
        if data.get("cod") != 200:
            print(f"Error: {data.get('message', 'City not found')}")
            return 
        
        # Extract weather details safely 
        city = data["name"]
        country = data["sys"]["country"]
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        condition = data["weather"][0]["description"]
        wind_speed = data["wind"]["speed"]

        # Display formatted weather report
        print("\n----- Weather Report -----")
        print(f"City: {city}, {country}")
        print(f"Temperature: {temperature}°C")
        print(f"Condition: {condition.capitalize()}")
        print(f"Humidity: {humidity}%")
        print(f"Wind Speed: {wind_speed} m/s")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")


def main():
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        print("API key not found. Make sure you added it to .env")
        return
    
    print("=== Welcome to Weather App ===")

    while True:
        city_name = input("\nEnter city name (or press Enter to exit): ").strip()

        if city_name == "":
            print("\nThank you for using Weather App 🌤")
            break

        get_weather(city_name, api_key)

# --- Run main Program --- 
       
if __name__ == "__main__":
    main()