import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# App title
st.set_page_config(page_title="Weather App", page_icon="🌦", layout="centered")
st.title("Real Time Weather")

# Input for city
city = st.text_input("Enter city / village / town name:")

#OpenWeatherMap API Key
api_key = "8dab5f0f631db014b3e42244f70b6c8e"
geo_url = "http://api.openweathermap.org/geo/1.0/direct"
weather_url = "http://api.openweathermap.org/data/2.5/weather"

if st.button("Get Weather"):
    if city:
        try:
            # Step 1: Get latitude & longitude from Geocoding API
            geo_params = {'q': city, 'limit': 1, 'appid': api_key}
            geo_response = requests.get(geo_url, params=geo_params)
            geo_data = geo_response.json()

            if not geo_data:
                st.error("❌ Location not found. Please check the spelling.")
            else:
                lat = geo_data[0]['lat']
                lon = geo_data[0]['lon']
                location_name = geo_data[0]['name']
                country = geo_data[0]['country']

                # Step 2: Get weather data using lat & lon
                weather_params = {'lat': lat, 'lon': lon, 'appid': api_key, 'units': 'metric'}
                response = requests.get(weather_url, params=weather_params)
                data = response.json()

                # Extract weather details
                weather = data['weather'][0]['description'].title()
                temp = data['main']['temp']
                feels_like = data['main']['feels_like']
                humidity = data['main']['humidity']
                wind_speed = data['wind']['speed']

                # Weather icon
                icon_code = data['weather'][0]['icon']
                icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
                icon_data = requests.get(icon_url).content
                icon_img = Image.open(BytesIO(icon_data))

                # Display results
                st.image(icon_img, width=100)
                st.subheader(f"{location_name}, {country}")
                st.write(f"🌡 **Temperature:** {temp}°C (Feels like {feels_like}°C)")
                st.write(f"☁ **Weather:** {weather}")
                st.write(f"💧 **Humidity:** {humidity}%")
                st.write(f"🌬 **Wind Speed:** {wind_speed} m/s")

        except Exception as e:
            st.error(f"⚠ Unable to fetch data: {e}")
    else:
        st.warning("Please enter a location name.")