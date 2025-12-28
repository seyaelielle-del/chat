import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import io

# --- Fonction pour récupérer la météo ---
def get_weather(city):
    api_key = 'b6096ab338cc41f7bc2141327253010'  # Remplace par ta clé API WeatherAPI
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        location = data['location']['name']
        country = data['location']['country']
        temperature = data['current']['temp_c']
        condition = data['current']['condition']['text']
        icon_url = "https:" + data['current']['condition']['icon']
        humidity = data['current']['humidity']
        wind_speed = data['current']['wind_kph']

        return {
            "location": location,
            "country": country,
            "temperature": temperature,
            "condition": condition,
            "icon": icon_url,
            "humidity": humidity,
            "wind_speed": wind_speed
        }

    except requests.exceptions.RequestException as req_err:
        return {"error": f"Erreur de connexion : {req_err}"}
    except KeyError:
        return {"error": "Ville introuvable ou données incomplètes."}


# --- Fonction pour afficher la météo dans l'interface ---
def afficher_meteo():
    city = entry_city.get().strip()
    if not city:
        messagebox.showwarning("Attention", "Veuillez entrer le nom d'une ville.")
        return

    data = get_weather(city)

    # Nettoyage
    for widget in frame_result.winfo_children():
        widget.destroy()

    if "error" in data:
        label_error = tk.Label(frame_result, text=data["error"], fg="red", font=("Arial", 12, "bold"), bg="#E3F2FD")
        label_error.pack()
        return

    # --- Affichage du lieu ---
    label_place = tk.Label(frame_result, text=f"{data['location']}, {data['country']}", 
                           font=("Arial", 16, "bold"), bg="#E3F2FD", fg="#0D47A1")
    label_place.pack(pady=5)

    # --- Icône météo ---
    icon_response = requests.get(data['icon'])
    icon_image = Image.open(io.BytesIO(icon_response.content))
    icon_image = icon_image.resize((100, 100))
    icon_photo = ImageTk.PhotoImage(icon_image)

    label_icon = tk.Label(frame_result, image=icon_photo, bg="#E3F2FD")
    label_icon.image = icon_photo
    label_icon.pack(pady=5)

    # --- Détails météo ---
    label_temp = tk.Label(frame_result, text=f"{data['temperature']}°C", font=("Arial", 30, "bold"), bg="#E3F2FD")
    label_temp.pack()

    label_cond = tk.Label(frame_result, text=data['condition'], font=("Arial", 14), bg="#E3F2FD")
    label_cond.pack(pady=2)

    label_humid = tk.Label(frame_result, text=f"💧 Humidité : {data['humidity']}%", font=("Arial", 12), bg="#E3F2FD")
    label_humid.pack()

    label_vent = tk.Label(frame_result, text=f"🌬️ Vent : {data['wind_speed']} km/h", font=("Arial", 12), bg="#E3F2FD")
    label_vent.pack()


# --- Création de la fenêtre principale ---
root = tk.Tk()
root.title("🌤️ Météo en Direct")
root.geometry("500x600")
root.config(bg="#E3F2FD")

# --- Titre ---
label_title = tk.Label(root, text="🌦️ Application Météo", font=("Arial", 20, "bold"), bg="#2196F3", fg="white", pady=15)
label_title.pack(fill=tk.X)

# --- Zone de saisie ---
frame_input = tk.Frame(root, bg="#E3F2FD")
frame_input.pack(pady=20)

label_city = tk.Label(frame_input, text="Ville :", font=("Arial", 13), bg="#E3F2FD")
label_city.grid(row=0, column=0, padx=5)

entry_city = tk.Entry(frame_input, font=("Arial", 13), width=25)
entry_city.grid(row=0, column=1, padx=5)

btn_search = tk.Button(frame_input, text="🔍 Rechercher", font=("Arial", 12, "bold"), bg="#1976D2", fg="white",
                       command=afficher_meteo)
btn_search.grid(row=0, column=2, padx=5)

# --- Cadre pour afficher les résultats ---
frame_result = tk.Frame(root, bg="#E3F2FD")
frame_result.pack(pady=20)

# --- Message par défaut ---
label_defaut = tk.Label(frame_result, text="Entrez une ville pour voir la météo ☀️", 
                        font=("Arial", 13), bg="#E3F2FD", fg="#555")
label_defaut.pack()

# --- Bouton Quitter ---
btn_quit = tk.Button(root, text="❌ Quitter", font=("Arial", 12, "bold"), bg="#E53935", fg="white",
                     command=root.destroy)
btn_quit.pack(pady=20)

root.mainloop()
