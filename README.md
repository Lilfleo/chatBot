# ChatBot

## Chatbot Simple avec Réponses Dynamiques

Ce projet implémente un chatbot interactif avec une interface graphique et un moteur de réponses basé sur un ensemble de règles définies par l'utilisateur. Le bot peut répondre à des questions, donner l'heure actuelle, et gérer des transitions de conversation simples.

### Fonctionnalités principales :

- **Réponses dynamiques** : Le bot répond à des entrées textuelles en se basant sur des règles de correspondance exactes ou floues.
- **Enregistrement des entrées** : Les messages de l'utilisateur sont enregistrés pour l'historique de la conversation.
- **Reconnaissance d'intentions** : Le bot peut détecter des requêtes spécifiques, telles que demander l'heure.
- **Gestion des erreurs** : Si l'utilisateur pose une question incomprise, le bot fournit une réponse par défaut et propose une aide.
- **Synthèse vocale** : Le bot utilise la synthèse vocale pour répondre de manière auditive.

### Technologies utilisées :

- **Python 3**
- **PyQt5** pour l'interface graphique
- **pyttsx3** pour la synthèse vocale
- **FuzzyWuzzy** pour la correspondance floue des entrées utilisateur
- **datetime** pour gérer les demandes d'heure

### Installation :

1. Clonez le repository :
   ```bash
   git clone https://github.com/ton-utilisateur/chatbot.git

2.Installez les dépendances nécessaires : 
```bash
   pip install pyqt5 pyttsx3 fuzzywuzzy
  
