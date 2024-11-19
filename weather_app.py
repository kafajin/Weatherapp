import tkinter as tk
from PIL import Image, ImageTk
import requests

# Funktion för att hämta väderdata från WeatherAPI
def get_weather(city):
    api_key = "e7a0b031073b46cab8003547241911"  # Ersätt med din egen API-nyckel
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no"
    
    # Skicka begäran till API:et
    response = requests.get(url)
    data = response.json()
    
    # Om begäran inte lyckades, returnera None
    if response.status_code != 200:
        return None
    else:
        # Hämta väderinformation från svaret
        temperature = data['current']['temp_c']
        condition = data['current']['condition']['text']
        wind_speed = data['current']['wind_kph']
        icon = data['current']['condition']['icon']
        return temperature, condition, wind_speed, icon

# Funktion för att uppdatera väderinformationen i GUI
def show_weather():
    city = city_entry.get()  # Hämta användarens input från textfältet
    weather_data = get_weather(city)

    if weather_data is None:
        result_label.config(text="Stad inte hittad.", fg="red")
        weather_icon_label.config(image="")  # Ta bort bilden om ingen stad hittas
        window.config(bg="#FFCCCB")  # Färga fönstret rött för fel
    else:
        temperature, condition, wind_speed, icon = weather_data
        result_label.config(text=f"Temperatur: {temperature}°C\nVäder: {condition}\nVindhastighet: {wind_speed} km/h", fg="black")
        
        # Ladda och visa väderikon
        weather_icon_url = f"http:{icon}"  # API:n ger väderikonens URL
        weather_icon = Image.open(requests.get(weather_icon_url, stream=True).raw)  # Ladda ikonen med Pillow
        weather_icon = ImageTk.PhotoImage(weather_icon)
        weather_icon_label.config(image=weather_icon)
        weather_icon_label.image = weather_icon  # För att hålla referensen till bilden
        
        # Uppdatera bakgrund och design beroende på väderförhållandena
        if 'sunny' in condition.lower():
            window.config(bg="#FFD700")  # Soligt - Gul bakgrund
            result_label.config(fg="black")
            background_label.config(image=sunny_bg)  # Solig bakgrund
        elif 'rain' in condition.lower():
            window.config(bg="#00BFFF")  # Regnigt - Blå bakgrund
            result_label.config(fg="white")
            background_label.config(image=rainy_bg)  # Regnig bakgrund
        elif 'cloud' in condition.lower():
            window.config(bg="#B0C4DE")  # Molnigt - Ljusblå bakgrund
            result_label.config(fg="black")
            background_label.config(image=cloudy_bg)  # Molnig bakgrund
        elif 'wind' in condition.lower():
            window.config(bg="#ADD8E6")  # Vindigt - Blå bakgrund
            result_label.config(fg="black")
            background_label.config(image=windy_bg)  # Vindt bakgrund
        else:
            window.config(bg="#FFFFFF")  # Standard bakgrund för okänt väder
            result_label.config(fg="black")
            background_label.config(image=default_bg)  # Standard bakgrund

# Skapa huvudfönster för appen
window = tk.Tk()
window.title("Väderapp")

# Lägg till bilder för bakgrunder (sol, regn, moln, vind etc.)
sunny_bg = Image.open("Weather.pics/sunny_background.png.jpg")
sunny_bg = ImageTk.PhotoImage(sunny_bg)

rainy_bg = Image.open("Weather.pics/rainy_background.png.jpg")
rainy_bg = ImageTk.PhotoImage(rainy_bg)

cloudy_bg = Image.open("Weather.pics/cloudy_background.png.jpg")
cloudy_bg = ImageTk.PhotoImage(cloudy_bg)

windy_bg = Image.open("Weather.pics/windy_background.png.jpg")
windy_bg = ImageTk.PhotoImage(windy_bg)

default_bg = Image.open("Weather.pics/default_background.png.jpg")
default_bg = ImageTk.PhotoImage(default_bg)

# Lägg till en bakgrundsbild i fönstret
background_label = tk.Label(window, image=default_bg)
background_label.place(relwidth=1, relheight=1)

# Ställ in fönstrets storlek
window.geometry("400x400")

# Lägg till en rubrik
header_label = tk.Label(window, text="Väderapplikation", font=("Helvetica", 16, "bold"), bg="white", fg="black")
header_label.pack(pady=10)

# Etikett för stad
city_label = tk.Label(window, text="Ange stad:", font=("Arial", 12), bg="white", fg="black")
city_label.pack(pady=5)

# Textfält för att skriva in stad
city_entry = tk.Entry(window, font=("Arial", 12), width=20)
city_entry.pack(pady=5)

# Knapp för att hämta väderinformation
search_button = tk.Button(window, text="Hämta Väder", font=("Arial", 12), bg="black", fg="white", command=show_weather)
search_button.pack(pady=10)

# Etikett för att visa väderinformation
result_label = tk.Label(window, text="", font=("Arial", 14), bg="white", fg="black")
result_label.pack(pady=10)

# Etikett för att visa väderikon
weather_icon_label = tk.Label(window, bg="white")
weather_icon_label.pack(pady=10)

# Starta GUI:t
window.mainloop()
