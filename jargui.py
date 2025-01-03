import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import json
import speech_recognition as sr
import pyttsx3
import requests
import google.generativeai as genai
import wikipedia
import subprocess
import datetime
import math
import cv2
from PIL import Image, ImageTk
import io
import os
import logging
from requests.utils import quote
import numpy as np
import tempfile
import mss
import mss.tools
from google.ai.generativelanguage_v1beta.types import Blob
import re
from gtts import gTTS
from playsound import playsound
import webbrowser
import threading

# ----- Chargement des Configurations -----
CONFIG_FILE = "config.json"
COMMANDS_FILE = "commands.json"
RESPONSES_FILE = "responses.json"

def load_config():
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)

def load_commands():
    try:
        with open(COMMANDS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_commands(commands):
    with open(COMMANDS_FILE, "w", encoding="utf-8") as f:
        json.dump(commands, f, indent=4)

def load_responses():
    try:
        with open(RESPONSES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_responses(responses):
    with open(RESPONSES_FILE, "w", encoding="utf-8") as f:
        json.dump(responses, f, indent=4)

# ----- Configuration de l'API Gemini et de la synthèse vocale -----
config = load_config()
commands = load_commands()
responses = load_responses()

try:
    genai.configure(api_key=config.get("gemini_api_key"))
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
except Exception as e:
    print(f"Erreur lors de la configuration de l'API Gemini: {e}")
    model = None

engine = pyttsx3.init()
voices = engine.getProperty('voices')
try:
    engine.setProperty('voice', voices[config.get("voice_index", 0)].id)
except Exception as e:
    print(f"Erreur lors de la sélection de la voix: {e}")
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)

# ----- Variables Globales -----
mode = "standard"
llm_state = "idle"
camera = cv2.VideoCapture(0)
if not camera.isOpened():
    print("Erreur : Impossible d'ouvrir la caméra. Vérifiez qu'elle est connectée et accessible.")

# ----- Fonctions de Base -----

def speak(text):
    print(f"Texte envoyé à gTTS : {text}")
    text = re.sub(r'\*', '', text)
    tts = gTTS(text, lang='fr')
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
        tts.save(tmp_file.name)
        tmp_file_path = tmp_file.name
    playsound(tmp_file_path)
    os.remove(tmp_file_path)

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        if source is None:
            print("Erreur: Impossible d'accéder au microphone.")
            return ""
        #print("Écoute...") #Masqué ici
        try:
            audio = r.listen(source)
        except Exception as e:
           print(f"Erreur lors de l'écoute: {e}")
           return ""
        
    try:
        text = r.recognize_google(audio, language='fr-FR')
        #print(f"Vous avez dit : {text}") # on ne le print plus ici, on va le print si une command est reconnu
        return text.lower()
    except sr.UnknownValueError:
        #print("Je n'ai pas compris.")
        return ""
    except sr.RequestError:
        print("Erreur de connexion au service de reconnaissance vocale.")
        return ""

def launch_app(path):
    try:
        subprocess.Popen(path)
        speak(responses.get("app_launched", "Application lancée."))
    except Exception as e:
        speak(responses.get("app_error", "Erreur lors du lancement de l'application."))
        print(e)
        
def open_file(path):
    try:
        os.startfile(path)
        speak(responses.get("file_opened","Fichier ouvert"))
    except Exception as e:
        speak(responses.get("file_error","Erreur lors de l'ouverture du fichier"))
        print(e)
        
def take_note():
  speak(responses.get("note_prompt", "Que souhaitez-vous noter?"))
  note = get_audio()
  if note:
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = f"note_{timestamp}.txt"
    try:
        with open(filepath,"w",encoding="utf-8") as f:
           f.write(note)
        speak(responses.get("note_saved", f"Note enregistrée dans {filepath}"))
        
    except Exception as e:
        speak(responses.get("note_error","Erreur lors de la sauvegarde de la note"))
        print(e)

def get_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    speak(f"Il est {current_time}.")
    
def get_date():
    now = datetime.datetime.now()
    current_date = now.strftime("%d %B %Y")
    speak(f"Nous sommes le {current_date}.")

def calculate(query):
    try:
        # Retirer tous les caractères non numériques ou des opérations mathématiques
        query = re.sub(r'[^\d\s*\/+\-\.]', '', query)
        query = re.sub(r'\b(?:fois|multiplier|x)\b', '*', query)
        result = eval(query)
        speak(f"Le résultat est {result}")
    except Exception as e:
        speak(responses.get("calc_error", "Je n'ai pas compris le calcul."))
        print(e)
        
def ask_calculate():
   speak(responses.get("calculate_prompt","Quel calcul souhaitez-vous effectuer ?"))
   query = get_audio()
   if query:
        calculate(query)

def search_web(query, engine_type):
    try:
        if engine_type == "google":
            url = f"https://www.google.com/search?q={quote(query)}"
        elif engine_type == "youtube":
            url = f"https://www.youtube.com/results?search_query={quote(query)}"
        elif engine_type == "wikipedia":
             try:
                result = wikipedia.summary(quote(query), sentences=2, auto_suggest=False)
                speak(result)
                return
             except wikipedia.exceptions.PageError:
                speak(responses.get("wiki_notfound","Page introuvable sur Wikipedia"))
                return
        else:
            return
        
        webbrowser.open(url)
        speak(responses.get("search_done", f"Voici les résultats pour {query}."))
    except Exception as e:
        speak(responses.get("search_error", "Erreur lors de la recherche."))
        print(e)


# ----- Fonctions Mode Gemini -----

def gemini_mode_interaction():
    global llm_state
    listening = False
    while True:
      
        if llm_state == "idle":
            if not listening:
               print("Écoute...")
               listening = True
            speak(responses.get("gemini_idle", "Je suis prêt à discuter en mode Gemini."))
            llm_state = "listening"
        elif llm_state == "listening":
            if not listening:
              print("Écoute...")
              listening = True
            query = get_audio()
            if query == "":
              continue
            listening = False # réinitialiser la variable ici
            if "standard" in query:
                speak(responses.get("mode_standard","Je repasse en mode standard."))
                llm_state = "idle"
                return
            elif "screenshot" in query:
                speak(responses.get("screenshot_question", "Que souhaitez-vous faire avec la capture d'écran ?"))
                llm_state = "taking_screenshot"
                continue
            elif "webcam" in query:
                speak(responses.get("webcam_question", "Que souhaitez-vous faire avec l'image de la webcam ?"))
                llm_state = "taking_webcam"
                continue
            else:
                gemini_response = send_to_gemini(query)
                speak(gemini_response)
                
        elif llm_state == "taking_screenshot":
            image = take_screenshot()
            if image:
               handle_image_query(image)
            else:
               llm_state = "listening"
        elif llm_state == "taking_webcam":
            image = take_webcam_capture()
            if image:
                handle_image_query(image)
            else:
                llm_state = "listening"

def take_screenshot():
    try:
        with mss.mss() as sct:
             sct_img = sct.grab(sct.monitors[1])
             img_bytes = mss.tools.to_png(sct_img.rgb, sct_img.size)
        
        return img_bytes
    except Exception as e:
        speak(responses.get("screenshot_import_error", "Erreur: lors de la capture d'écran."))
        print(e)
        return None

def take_webcam_capture():
    global camera
    try:
        ret, frame = camera.read()
        if not ret:
            speak(responses.get("webcam_error","Impossible de lire la webcam"))
            return None
        
        _, encoded_image = cv2.imencode('.png', frame)
        image_bytes = encoded_image.tobytes()

        return image_bytes

    except Exception as e:
        speak(responses.get("webcam_capture_error", "Une erreur s'est produite lors de la capture de l'image avec la webcam."))
        print(e)
        return None

def handle_image_query(image):
    global llm_state
    while True:
        query = get_audio()
        if query == "":
            continue
        if "décris l'image" in query:
            response = send_image_to_gemini(image, query, "Décris cette image")
            speak(response)
            llm_state = "listening"
            return
        elif "sauvegarde l'image" in query:
            save_image(image)
            llm_state = "listening"
            return
        else:
            response = send_image_to_gemini(image, query, "Analyse cette image")
            speak(response)
            llm_state = "listening"
            return

def send_image_to_gemini(image, query, prompt_placeholder):
    try:
        print(f"Type de l'image envoyée à Gemini: {type(image)}")
        if not isinstance(image, bytes):
            return responses.get("image_process_error","Erreur: Le format de l'image n'est pas supporté, l'image doit etre un byte.")
            
        contents = [Blob(mime_type='image/png', data=image), f"{prompt_placeholder}. {query}"]
        
        response = model.generate_content(contents)
        return response.text
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'image à l'API Gemini: {e}")
        return responses.get("gemini_image_error", "Erreur lors du traitement de l'image avec Gemini")

def send_to_gemini(query):
    try:
        response = model.generate_content(query)
        return response.text
    except Exception as e:
        print(e)
        return responses.get("gemini_error", "Erreur lors de la communication avec Gemini.")
    
def save_image(image):
  try:
      timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
      filepath = f"image_{timestamp}.png"
      with open(filepath,"wb") as f:
         f.write(image)
      speak(responses.get("image_saved", f"Image sauvegardée en tant que {filepath}"))
  except Exception as e:
      print(e)
      speak(responses.get("image_save_error", "Erreur lors de la sauvegarde de l'image"))

# ----- Fonctions de l'Interface Graphique -----
def update_config(new_config):
    global config, engine, voices
    config.update(new_config)
    save_config(config)

    try:
        engine.setProperty('voice', voices[config.get("voice_index",0)].id)
    except Exception as e:
        print(f"Erreur lors de la mise à jour de la voix: {e}")
    try:
       genai.configure(api_key=config.get("gemini_api_key"))
       global model
       model = genai.GenerativeModel('gemini-2.0-flash-exp')
    except Exception as e:
        print(f"Erreur lors de la mise à jour de l'API Gemini: {e}")

def save_settings():
    new_gemini_key = gemini_key_entry.get()
    new_voice_index = voice_names.index(voice_combo.get())
    update_config({"gemini_api_key": new_gemini_key, "voice_index": new_voice_index})
    messagebox.showinfo("Configuration", "Configuration enregistrée.")

def add_command():
    new_command_window = tk.Toplevel(root)
    new_command_window.title("Ajouter une commande")

    tk.Label(new_command_window, text="Commande vocale:").grid(row=0, column=0, sticky=tk.W)
    command_entry = tk.Entry(new_command_window)
    command_entry.grid(row=0, column=1, sticky=tk.W)

    tk.Label(new_command_window, text="Type:").grid(row=1, column=0, sticky=tk.W)
    command_type_combo = ttk.Combobox(new_command_window, values=["open_file", "launch", "take_note","time", "date","ask_calculate","google","youtube","wikipedia","say"], state="readonly")
    command_type_combo.set("say")
    command_type_combo.grid(row=1, column=1, sticky=tk.W)
    
    tk.Label(new_command_window, text="Path (si applicable):").grid(row=2, column=0, sticky=tk.W)
    path_entry = tk.Entry(new_command_window)
    path_entry.grid(row=2, column=1, sticky=tk.W)

    tk.Label(new_command_window, text="Texte (si applicable):").grid(row=3, column=0, sticky=tk.W)
    text_entry = tk.Entry(new_command_window)
    text_entry.grid(row=3,column=1, sticky=tk.W)

    def save_new_command():
        new_command = command_entry.get()
        new_command_type = command_type_combo.get()
        new_path = path_entry.get()
        new_text = text_entry.get()
        
        if not new_command:
            messagebox.showerror("Erreur", "La commande vocale ne peut pas être vide.")
            return

        if new_command in commands:
            messagebox.showerror("Erreur", "Cette commande existe déjà, veuillez la modifier")
            return
        
        if new_command_type == "open_file" or new_command_type == "launch":
            if not new_path:
                messagebox.showerror("Erreur", "Le chemin du fichier ou de l'application est requis pour ce type de commande.")
                return
            commands[new_command] = {"type": new_command_type,"path": new_path}

        elif new_command_type == "say":
            if not new_text:
                messagebox.showerror("Erreur", "Le texte à prononcer est requis pour ce type de commande.")
                return
            commands[new_command] = {"type": new_command_type, "text": new_text}
        else:
            commands[new_command] = {"type": new_command_type}
                
        save_commands(commands)
        refresh_command_list()
        new_command_window.destroy()
        messagebox.showinfo("Succès","Commande ajoutée avec succès.")

    save_new_command_button = tk.Button(new_command_window, text="Enregistrer", command=save_new_command)
    save_new_command_button.grid(row=4, column=1, sticky=tk.E)

def edit_command():
    selected_item = command_list.focus()
    if not selected_item:
        messagebox.showerror("Erreur", "Veuillez sélectionner une commande à modifier.")
        return
    
    selected_command = command_list.item(selected_item)["text"]
    
    edit_command_window = tk.Toplevel(root)
    edit_command_window.title("Modifier la commande")
    
    tk.Label(edit_command_window, text="Commande vocale:").grid(row=0, column=0, sticky=tk.W)
    command_entry = tk.Entry(edit_command_window)
    command_entry.insert(0,selected_command)
    command_entry.grid(row=0, column=1, sticky=tk.W)
    
    tk.Label(edit_command_window, text="Type:").grid(row=1, column=0, sticky=tk.W)
    command_type_combo = ttk.Combobox(edit_command_window, values=["open_file", "launch", "take_note","time","date","ask_calculate","google","youtube","wikipedia","say"], state="readonly")
    command_type_combo.set(commands[selected_command].get("type","say"))
    command_type_combo.grid(row=1, column=1, sticky=tk.W)
    
    tk.Label(edit_command_window, text="Path (si applicable):").grid(row=2, column=0, sticky=tk.W)
    path_entry = tk.Entry(edit_command_window)
    path_entry.insert(0, commands[selected_command].get("path",""))
    path_entry.grid(row=2, column=1, sticky=tk.W)

    tk.Label(edit_command_window, text="Texte (si applicable):").grid(row=3, column=0, sticky=tk.W)
    text_entry = tk.Entry(edit_command_window)
    text_entry.insert(0, commands[selected_command].get("text",""))
    text_entry.grid(row=3,column=1, sticky=tk.W)

    def save_edited_command():
        new_command = command_entry.get()
        new_command_type = command_type_combo.get()
        new_path = path_entry.get()
        new_text = text_entry.get()
        if not new_command:
            messagebox.showerror("Erreur", "La commande vocale ne peut pas être vide.")
            return
        if new_command != selected_command and new_command in commands:
            messagebox.showerror("Erreur", "Cette commande existe déjà, veuillez la modifier")
            return
            
        del commands[selected_command]
        if new_command_type == "open_file" or new_command_type == "launch":
            if not new_path:
                messagebox.showerror("Erreur", "Le chemin du fichier ou de l'application est requis pour ce type de commande.")
                return
            commands[new_command] = {"type": new_command_type,"path": new_path}

        elif new_command_type == "say":
            if not new_text:
                messagebox.showerror("Erreur", "Le texte à prononcer est requis pour ce type de commande.")
                return
            commands[new_command] = {"type": new_command_type, "text": new_text}
        else:
            commands[new_command] = {"type": new_command_type}
                
        save_commands(commands)
        refresh_command_list()
        edit_command_window.destroy()
        messagebox.showinfo("Succès","Commande modifiée avec succès.")
            
    save_edited_command_button = tk.Button(edit_command_window, text="Enregistrer", command=save_edited_command)
    save_edited_command_button.grid(row=4, column=1, sticky=tk.E)

def delete_command():
    selected_item = command_list.focus()
    if not selected_item:
        messagebox.showerror("Erreur", "Veuillez sélectionner une commande à supprimer.")
        return
    
    selected_command = command_list.item(selected_item)["text"]
    if messagebox.askyesno("Supprimer la commande",f"Êtes vous sûr de vouloir supprimer la commande {selected_command} ?"):
        del commands[selected_command]
        save_commands(commands)
        refresh_command_list()

def refresh_command_list():
        command_list.delete(*command_list.get_children())
        for command in commands:
             command_list.insert("",tk.END,text=command)

def add_response():
    new_response_window = tk.Toplevel(root)
    new_response_window.title("Ajouter une phrase")

    tk.Label(new_response_window, text="Phrase clé:").grid(row=0, column=0, sticky=tk.W)
    key_entry = tk.Entry(new_response_window)
    key_entry.grid(row=0, column=1, sticky=tk.W)

    tk.Label(new_response_window, text="Réponse:").grid(row=1, column=0, sticky=tk.W)
    response_entry = tk.Entry(new_response_window)
    response_entry.grid(row=1, column=1, sticky=tk.W)

    def save_new_response():
        key = key_entry.get()
        response = response_entry.get()
        
        if not key or not response:
            messagebox.showerror("Erreur", "Veuillez remplir les deux champs.")
            return
        
        if key in responses:
            messagebox.showerror("Erreur", "Cette phrase existe déjà, veuillez la modifier.")
            return
        
        responses[key] = response
        save_responses(responses)
        refresh_responses_list()
        new_response_window.destroy()
        messagebox.showinfo("Succès", "Phrase ajoutée avec succès.")

    save_new_response_button = tk.Button(new_response_window, text="Enregistrer", command=save_new_response)
    save_new_response_button.grid(row=2, column=1, sticky=tk.E)

def edit_response():
    selected_item = responses_list.focus()
    if not selected_item:
        messagebox.showerror("Erreur", "Veuillez sélectionner une phrase à modifier.")
        return
    selected_key = responses_list.item(selected_item)["text"]

    edit_response_window = tk.Toplevel(root)
    edit_response_window.title("Modifier la phrase")

    tk.Label(edit_response_window, text="Phrase clé:").grid(row=0, column=0, sticky=tk.W)
    key_entry = tk.Entry(edit_response_window)
    key_entry.insert(0, selected_key)
    key_entry.grid(row=0, column=1, sticky=tk.W)

    tk.Label(edit_response_window, text="Réponse:").grid(row=1, column=0, sticky=tk.W)
    response_entry = tk.Entry(edit_response_window)
    response_entry.insert(0, responses[selected_key])
    response_entry.grid(row=1, column=1, sticky=tk.W)

    def save_edited_response():
        new_key = key_entry.get()
        new_response = response_entry.get()
        if not new_key or not new_response:
                messagebox.showerror("Erreur", "Veuillez remplir les deux champs.")
                return
        
        if new_key != selected_key and new_key in responses:
                messagebox.showerror("Erreur", "Cette phrase existe déjà, veuillez la modifier")
                return
        del responses[selected_key]
        responses[new_key] = new_response
        save_responses(responses)
        refresh_responses_list()
        edit_response_window.destroy()
        messagebox.showinfo("Succès", "Phrase modifiée avec succès")

    save_edited_response_button = tk.Button(edit_response_window, text="Enregistrer", command=save_edited_response)
    save_edited_response_button.grid(row=2, column=1, sticky=tk.E)

def delete_response():
    selected_item = responses_list.focus()
    if not selected_item:
        messagebox.showerror("Erreur", "Veuillez sélectionner une phrase à supprimer")
        return
    selected_key = responses_list.item(selected_item)["text"]
    if messagebox.askyesno("Supprimer la phrase", f"Êtes vous sûr de vouloir supprimer la phrase {selected_key} ?"):
        del responses[selected_key]
        save_responses(responses)
        refresh_responses_list()

def refresh_responses_list():
    responses_list.delete(*responses_list.get_children())
    for key,response in responses.items():
        responses_list.insert("",tk.END,text=key)

def main_loop():
    global mode
    global camera
    listening = False
    while True:
        if mode == "standard":
            if not listening:
                print("Écoute...")
                listening = True
            query = get_audio()
            if not query:
                continue
            
            command_recognized = False
            if "discuter" in query:
                mode = "gemini"
                speak(responses.get("gemini_mode", "Mode Gemini activé."))
                gemini_mode_interaction()
                mode = "standard"
                continue
            
            for command, action in commands.items():
                if command in query:
                    command_recognized = True
                    print(f"Vous avez dit : {query}")  # affichage uniquement si command reconnu
                    listening = False # On veut relancer l'écoute après avoir executé la commande.
                    command_type = commands.get(command,{}).get("type")
                    if isinstance(action,dict) and action.get("type") == "open_file":
                        open_file(action.get("path"))
                    elif isinstance(action,dict) and action.get("type") == "take_note":
                        take_note()
                    elif isinstance(action,dict) and action.get("type") == "launch":
                        launch_app(action.get("path"))
                    elif isinstance(action,dict) and action.get("type") == "time":
                        get_time()
                    elif isinstance(action,dict) and action.get("type") == "date":
                        get_date()
                    elif command_type == "ask_calculate":
                        ask_calculate()
                    elif isinstance(action,dict) and action.get("type") == "google":
                        search_web(query.replace("google","").strip(), "google")
                    elif isinstance(action,dict) and action.get("type") == "youtube":
                        search_web(query.replace("youtube","").strip(), "youtube")
                    elif isinstance(action,dict) and action.get("type") == "wikipedia":
                        search_web(query.replace("wikipedia","").strip(), "wikipedia")
                    elif isinstance(action,dict) and action.get("type") == "say":
                        speak(action.get("text"))
                    break
            if not command_recognized:
                continue

# ----- Initialisation de l'Interface Graphique -----
root = tk.Tk()
root.title("Assistant Vocal")
root.geometry("800x600")

# --- Configuration Frame ---
config_frame = ttk.LabelFrame(root, text="Configuration")
config_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

tk.Label(config_frame, text="Clé API Gemini:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
gemini_key_entry = tk.Entry(config_frame, width=40)
gemini_key_entry.insert(0, config.get("gemini_api_key", ""))
gemini_key_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

tk.Label(config_frame, text="Voix:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
voice_names = [voice.name for voice in voices]
voice_combo = ttk.Combobox(config_frame, values=voice_names, state="readonly")
voice_combo.set(voice_names[config.get("voice_index", 0)])
voice_combo.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

save_button = tk.Button(config_frame, text="Enregistrer", command=save_settings)
save_button.grid(row=2, column=1, sticky=tk.E, padx=5, pady=5)

# --- Command Frame ---
command_frame = ttk.LabelFrame(root, text="Gestion des Commandes")
command_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

command_list = ttk.Treeview(command_frame)
command_list["columns"] = ("Commandes")
command_list.column("#0", width=200)
command_list.heading("#0", text="Commandes Vocales")
command_list.grid(row=0,column=0, padx=5, pady=5, columnspan=3)
refresh_command_list()
    
add_command_button = tk.Button(command_frame, text="Ajouter", command=add_command)
add_command_button.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
    
edit_command_button = tk.Button(command_frame, text="Modifier", command=edit_command)
edit_command_button.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
    
delete_command_button = tk.Button(command_frame, text="Supprimer", command=delete_command)
delete_command_button.grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)

# --- Response Frame ---
response_frame = ttk.LabelFrame(root, text="Gestion des Phrases")
response_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

responses_list = ttk.Treeview(response_frame)
responses_list["columns"] = ("Phrases")
responses_list.column("#0", width=200)
responses_list.heading("#0", text="Phrases")
responses_list.grid(row=0,column=0, padx=5, pady=5, columnspan=3)
refresh_responses_list()
   
add_response_button = tk.Button(response_frame, text="Ajouter", command=add_response)
add_response_button.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
    
edit_response_button = tk.Button(response_frame, text="Modifier", command=edit_response)
edit_response_button.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
    
delete_response_button = tk.Button(response_frame, text="Supprimer", command=delete_response)
delete_response_button.grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)

# --- Démarrage de la boucle principale ---
speak(responses.get("startup_message", "Bonjour, je suis à votre écoute."))

# Démmarrer la boucle principale dans un thread séparé
threading.Thread(target=main_loop, daemon=True).start()

try:
    root.mainloop()
except KeyboardInterrupt:
    print("\nProgramme interrompu par l'utilisateur.")
finally:
    if camera.isOpened():
        camera.release()