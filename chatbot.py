import json

import random
import string
import unicodedata
import os
import re
from datetime import datetime
from nltk.tokenize import word_tokenize
from fuzzywuzzy import process
import speech_recognition as sr
import pyttsx3
# === Fonctions Utilitaires ===

def normalize_text(text):
    """
    Normalise le texte en supprimant les accents, les ponctuations et en le mettant en minuscule.
    """
    text = ''.join(c for c in unicodedata.normalize('NFKD', text)
                   if not unicodedata.combining(c)).lower()
    text = re.sub(r'\s+', ' ', text)  # Remplacer les espaces multiples par un seul
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text.strip()

def load_histo():
    """Charge l'historique des entrées utilisateur depuis un fichier JSON."""
    if os.path.exists("history.json"):
        with open("history.json", "r") as file:
            return json.load(file)
    return []

def save_to_histo(user_input, history):
    """Sauvegarde une nouvelle entrée utilisateur dans l'historique."""
    history.append(user_input)
    with open("history.json", "w") as file:
        json.dump(history, file)

def call_counter(func):
    """
    Décorateur pour compter les appels à une fonction donnée.
    """
    func._call_count = 0

    def wrapper(*args, **kwargs):
        func._call_count += 1
        return func(*args, **kwargs)

    wrapper.get_count = lambda: func._call_count
    return wrapper

# === Gestion des Données ===

def clean_rep():
    """Nettoie et charge les réponses depuis le fichier JSON."""
    with open("rep_fr.json", "r") as file:
        data = json.load(file)
    return {
        normalize_text(key.translate(str.maketrans('', '', string.punctuation.replace("'", "")))): {
            "response": value["response"],
            "transitions": value.get("transitions", {})
        }
        for key, value in data.items()
    }

def clean_text(user_input):
    """Nettoie et tokenize l'entrée utilisateur."""
    user_input = user_input.lower().translate(str.maketrans("", "", string.punctuation.replace("'", "")))
    tokens = word_tokenize(user_input, language='french')
    return [normalize_text(token) for token in tokens]

# === Fonctionnalités ===

def detect_time_request(user_phrase):
    """Détecte si l'utilisateur demande l'heure."""
    time_keywords = ["heure", "quelle heure", "quelle heure est", "c'est quelle heure", "heures"]
    user_phrase = normalize_text(user_phrase)
    return any(keyword in user_phrase for keyword in time_keywords)

def find_best_match(user_input, rep):
    """Trouve la meilleure correspondance pour une entrée utilisateur."""
    best_match, score = process.extractOne(user_input, rep.keys())
    return best_match if score > 75 else None

def display_response_and_return_node(rep, node):
    """Affiche une réponse pour un nœud donné et retourne ce nœud."""
    if node in rep:
        print(random.choice(rep[node]["response"]))
    else:
        print(f"Erreur : le nœud '{node}' est introuvable.")
    return node

def process_input(cleaned_tokens, current_node):
    """
    Gère l'entrée utilisateur et les transitions des nœuds.
    """
    rep = clean_rep()
    user_phrase = " ".join(cleaned_tokens)

    if detect_time_request(user_phrase):
        response = f"[DEBUG] Il est {datetime.now().strftime('%H:%M')}."
        speak_live(response)  # Parle de l'heure en temps réel
        return current_node

    if current_node not in rep:
        print(f"Erreur : le nœud '{current_node}' n'existe pas. Redirection vers 'hall'.")
        return "hall"

    current_data = rep[current_node]
    transitions = {
        normalize_text(key): value
        for key, value in current_data.get("transitions", {}).items()
    }

    for token in cleaned_tokens:
        token = normalize_text(token)
        if token in transitions:
            next_node = transitions[token]
            if next_node in rep:
                response = random.choice(rep[next_node]["response"])
                speak_live(response)  # Lire la réponse en temps réel
                return next_node

    best_match = find_best_match(user_phrase, rep)
    if best_match:
        response = random.choice(rep[best_match]["response"])
        speak_live(response)  # Lire la réponse en temps réel
        return best_match

    response = random.choice(rep["hall"]["response"])  # Réponse par défaut
    speak_live(response)  # Lire la réponse par défaut en temps réel
    return "hall"



def save_voice_preference(voice_id):
    with open("voice_preference.json", "w") as file:
        json.dump({"voice_id": voice_id}, file)

def load_voice_preference():
    if os.path.exists("voice_preference.json"):
        with open("voice_preference.json", "r") as file:
            data = json.load(file)
            return data.get("voice_id")
    return None

engine = pyttsx3.init()

def set_voice(engine):
    voice_id = load_voice_preference()
    if voice_id:
        engine.setProperty('voice', voice_id)
        print(f"Voix définie sur : {voice_id}")
    else:
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)  # Choisir la première voix par défaut
        save_voice_preference(voices[0].id)  # Sauvegarder la voix par défaut
        print(f"Aucune préférence de voix trouvée. La voix par défaut ({voices[0].id}) a été choisie.")


def speak_live(text):
    """Fonction de synthèse vocale en temps réel (live)."""
    set_voice(engine)  # Utilise la fonction pour charger et définir la voix
    print(f"[DEBUG] Lecture du texte : {text}")
    engine.say(text)
    engine.runAndWait()  # Cette ligne est nécessaire pour lancer la lecture immédiatement


def speak(text):
    """Cette fonction est maintenant un alias de speak_live pour lire immédiatement."""
    speak_live(text)



# === Interaction Utilisateur ===

# Variable globale pour conserver le mode de reconnaissance vocale
use_speech_recognition = None

def set_speech_recognition_preference():
    global use_speech_recognition
    # Si la préférence n'a pas encore été définie, demande à l'utilisateur
    if use_speech_recognition is None:
        mode = input("Souhaitez-vous utiliser la reconnaissance vocale ? (O/N) > ").lower()
        use_speech_recognition = (mode == 'o')
@call_counter
def get_user_input():
    global use_speech_recognition
    if use_speech_recognition:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Veuillez parler...")
            recognizer.adjust_for_ambient_noise(source)  # Ajuste le bruit ambiant
            audio = recognizer.listen(source)  # Écoute la parole de l'utilisateur
            try:
                user_input = recognizer.recognize_google(audio, language="fr-FR")  # Utilise Google Speech Recognition
                print(f"Vous avez dit : {user_input}")
                return user_input
            except sr.UnknownValueError:
                print("Je n'ai pas compris ce que vous avez dit.")
                return ""
            except sr.RequestError:
                print("Le service de reconnaissance vocale est inaccessible.")
                return ""
    else:
        return input("> ")


def welcome():
    """Affiche un message de bienvenue."""
    history = load_histo()
    call_count = get_user_input.get_count()

    if len(history) == 0:
        print("Bonjour, comment puis-je t'aider ?")
    elif len(history) <= 3:
        print("Oh, tu es revenu.")
    else:
        print("Pas besoin d'un guide, tu connais la maison.")
    print("-------------------------------------------")

def main_loop():
    set_speech_recognition_preference()  # Demande la préférence au début
    history = load_histo()
    welcome()
    current_node = "hall"  # Point d'entrée de l'arbre
    while True:
        user_input = get_user_input()  # Utilise la reconnaissance vocale ou le texte
        if user_input.lower() == "quitter":
            print("Au revoir !")
            break
        save_to_histo(user_input, history)
        cleaned_tokens = clean_text(user_input)
        current_node = process_input(cleaned_tokens, current_node)


# === Démarrage ===
if __name__ == "__main__":
    main_loop()
