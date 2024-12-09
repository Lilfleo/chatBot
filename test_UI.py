import sys
import json
import string
import unicodedata
import pyttsx3
import os
import re
import random
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QTextBrowser, QMessageBox
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import speech_recognition as sr
from fuzzywuzzy import process
from nltk import word_tokenize

engine = pyttsx3.init()
def normalize_text(text):
    """
    Normalise le texte en supprimant les accents, les ponctuations et en le mettant en minuscule.
    """
    text = ''.join(c for c in unicodedata.normalize('NFKD', text)
                   if not unicodedata.combining(c)).lower()
    text = re.sub(r'\s+', ' ', text)  # Remplacer les espaces multiples par un seul
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text.strip()

def find_best_match(user_input, rep):
    """Trouve la meilleure correspondance pour une entrée utilisateur."""
    best_match, score = process.extractOne(user_input, rep.keys())
    return best_match if score > 75 else None

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

def speak_live(text):

    engine.say(text)
    engine.runAndWait()

# === Thread de reconnaissance vocale ===
class SpeechRecognitionThread(QThread):
    recognized_text = pyqtSignal(str)  # Signal pour envoyer le texte reconnu à l'interface

    def run(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Veuillez parler...")
            recognizer.adjust_for_ambient_noise(source)  # Ajuste le bruit ambiant
            audio = recognizer.listen(source)  # Écoute la parole de l'utilisateur
            try:
                user_input = recognizer.recognize_google(audio, language="fr-FR")
                print(f"Vous avez dit : {user_input}")
                self.recognized_text.emit(user_input)  # Émet le texte reconnu
            except sr.UnknownValueError:
                print("Je n'ai pas compris ce que vous avez dit.")
                self.recognized_text.emit("")  # Si rien n'est compris
            except sr.RequestError:
                print("Le service de reconnaissance vocale est inaccessible.")
                self.recognized_text.emit("")  # Si le service est inaccessible

# === Classe pour l'interface graphique ===
class ChatbotApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chatbot")
        self.setGeometry(100, 100, 600, 400)

        # Historique et état
        self.history = load_histo()
        self.rep = clean_rep()
        self.current_node = "hall"

        # Création des widgets
        self.chat_display = QTextBrowser(self)
        self.chat_display.setReadOnly(True)

        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Tapez votre message ici...")
        self.input_field.returnPressed.connect(self.process_input)

        self.send_button = QPushButton("Envoyer", self)
        self.send_button.clicked.connect(self.process_input)

        self.speech_button = QPushButton("Utiliser Reconnaissance Vocale", self)
        self.speech_button.clicked.connect(self.start_speech_recognition)

        # Mise en page
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel("Chatbot", self, alignment=Qt.AlignCenter))
        main_layout.addWidget(self.chat_display)
        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.speech_button)

        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Message de bienvenue
        self.welcome_message()

        # Initialisation du thread de reconnaissance vocale
        self.speech_recognition_thread = SpeechRecognitionThread()
        self.speech_recognition_thread.recognized_text.connect(self.process_voice_input)

    def welcome_message(self):
        if len(self.history) == 0:
            self.chat_display.append("Bot: Bonjour, comment puis-je t'aider ?")
        elif len(self.history) <= 3:
            self.chat_display.append("Bot: Oh, tu es revenu.")
        else:
            self.chat_display.append("Bot: Pas besoin d'un guide, tu connais la maison.")

    def process_input(self):
        user_input = self.input_field.text().strip()
        if not user_input:
            return

        # Affichage de l'entrée utilisateur
        self.chat_display.append(f"Vous: {user_input}")
        self.input_field.clear()

        # Sauvegarde de l'entrée dans l'historique
        save_to_histo(user_input, self.history)

        # Nettoyage de l'entrée utilisateur
        cleaned_input = normalize_text(user_input)

        # Détection de la demande d'heure
        if detect_time_request(cleaned_input):
            response = f"Il est {datetime.now().strftime('%H:%M')}."
            self.chat_display.append(f"Bot: {response}")
            speak_live(response)
            return

        # Recherche de la réponse correspondante
        response = self.rep.get(cleaned_input, {}).get("response", ["Je ne comprends pas."])[0]
        self.chat_display.append(f"Bot: {response}")
        speak_live(response)

    def process_voice_input(self, user_input):
        if not user_input:
            return
        # Affichage de l'entrée vocale
        self.chat_display.append(f"Vous (voix): {user_input}")
        # Traitement de l'entrée vocale
        self.process_input_from_text(user_input)

    def process_input_from_text(self, user_input):
        # Cette méthode est utilisée pour traiter le texte entrant
        save_to_histo(user_input, self.history)
        if detect_time_request(user_input):
            response = f"Il est {datetime.now().strftime('%H:%M')}."
            self.chat_display.append(f"Bot: {response}")
            speak_live(response)
        else:
            response = self.rep.get(normalize_text(user_input), {}).get("response", ["Je ne comprends pas."])[0]
            self.chat_display.append(f"Bot: {response}")
            speak_live(response)

    def start_speech_recognition(self):
        """Démarre la reconnaissance vocale dans un thread séparé."""
        self.speech_recognition_thread.start()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Quitter', "Voulez-vous vraiment quitter ?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


# === Point d'entrée ===
if __name__ == "__main__":
    app = QApplication(sys.argv)
    chatbot = ChatbotApp()
    chatbot.show()
    sys.exit(app.exec_())




