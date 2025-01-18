import tkinter as tk
from tkinter import messagebox
import requests
import geocoder
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()


# API keys
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
BASE_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"


# Color scheme
yellow = "#f18d00"
brown = "#180e00"
blue = "#4a80f5"
darkgray = "#101418"
white = "#ffffff"
black = "#000000"
lt_yellow = "#fadcb2"

# Function to fetch weather data
def get_weather_data(city):
    try:
        params = {
            "q": city,
            "appid": WEATHER_API_KEY,
            "units": "metric"
        }
        response = requests.get(BASE_WEATHER_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch weather data: {e}")
        return None

# Function to detect user location
def detect_location():
    try:
        location = geocoder.ip("me")
        if location.city:
            return location.city
        else:
            messagebox.showwarning("Warning", "Unable to detect location. Defaulting to Kolkata.")
            return "Kolkata"
    except Exception as e:
        messagebox.showerror("Error", f"Failed to detect location: {e}")
        return "Kolkata"

# Function to display weather data
def display_weather():
    city = city_entry.get() or detect_location()
    weather_data = get_weather_data(city)

    if weather_data:
        city_label.config(text=f"Weather in {weather_data['name']}")
        temp_label.config(text=f"Temperature: {weather_data['main']['temp']} °C")
        humidity_label.config(text=f"Humidity: {weather_data['main']['humidity']}%")
        wind_label.config(text=f"Wind Speed: {weather_data['wind']['speed']} m/s")

# GUI setup
root = tk.Tk()
root.title("Weather App")
root.geometry("700x400")
root.configure(bg=black)


# Header
header = tk.Label(root, text="Real-Time Weather", bg=black, fg=blue, font=("Helvetica", 18, "bold"))
header.pack(pady=20)

# Input frame
input_frame = tk.Frame(root, bg=blue)
input_frame.pack(pady=10)

city_label_input = tk.Label(input_frame, text="Enter City:", bg=blue, fg=black, font=("Helvetica", 12,"bold"))
city_label_input.grid(row=0, column=0, padx=10, pady=20)

city_entry = tk.Entry(input_frame, font=("Helvetica", 12), bg=white, fg=black, width=20)
city_entry.grid(row=0, column=1, padx=10)

search_button = tk.Button(input_frame, text="Get Weather", bg="#0d51e6", fg=white, font=("Helvetica", 12), command=display_weather)
search_button.grid(row=0, column=2, padx=10)

# Weather display frame
weather_frame = tk.Frame(root, bg=black)
weather_frame.pack(pady=20)

city_label = tk.Label(weather_frame, text="", bg=black, fg=blue, font=("Helvetica", 14, "bold"))
city_label.pack()

temp_label = tk.Label(weather_frame, text="", bg=black, fg=white, font=("Helvetica", 12))
temp_label.pack()

humidity_label = tk.Label(weather_frame, text="", bg=black, fg=white, font=("Helvetica", 12))
humidity_label.pack()

wind_label = tk.Label(weather_frame, text="", bg=black, fg=white, font=("Helvetica", 12))
wind_label.pack()

# Run the application
root.mainloop()
