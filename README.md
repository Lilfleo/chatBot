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


# Roadmap

## 🚀 Phase 1: Initialisation et Fonctionnalités de Base
- **Création du chatbot** : Mise en place d'une interface simple et de la logique de base pour gérer les interactions avec l'utilisateur.
- **Réponses dynamiques** : Le bot répond aux questions simples avec des règles de correspondance exactes ou floues.
- **Enregistrement des entrées** : Suivi des conversations pour un historique utilisateur.

## 🔄 Phase 2: Amélioration de l'Interaction
- **Reconnaissance d'intentions** : Introduction d'un moteur basique pour comprendre les requêtes comme demander l'heure.
- **Gestion des erreurs et aide contextuelle** : Le bot propose des réponses par défaut et aide l'utilisateur en cas de non-compréhension.

## 🧠 Phase 3: Évolution de la Logique du Bot
- **Tokenisation et NLP (Natural Language Processing)** : Intégration d'un système pour analyser les entrées utilisateur de manière plus complexe. **(En cours de développement, certaines fonctionnalités sont encore incomplètes !)**
- **Amélioration des règles de correspondance floue** : Affinement des algorithmes pour rendre le bot plus réactif et précis dans la gestion des requêtes floues.

## 🔊 Phase 4: Enrichissement de l'Expérience Utilisateur
- **Synthèse vocale** : Ajout de la fonctionnalité de réponse auditive pour rendre les interactions plus naturelles. **(Partiellement fonctionnelle, des améliorations sont à prévoir pour une meilleure fluidité)**
- **Amélioration de l'interface graphique** : Mise à jour de l'interface utilisateur pour rendre l'expérience plus agréable et intuitive.

## 🚧 Phase 5: Optimisation et Fonctionnalités Avancées
- **Gestion des contextes de conversation** : Ajout de la possibilité pour le bot de maintenir un état de conversation à travers plusieurs échanges.
- **Support multilingue** : Ajout de la gestion de plusieurs langues pour toucher un public plus large.

## 📅 Phase 6: Déploiement et Feedback
- **Tests avec utilisateurs réels** : Recueillir des retours pour améliorer la précision des réponses et l'ergonomie de l'application.
- **Optimisation finale** : Correction des bugs et amélioration des performances avant le déploiement en production.

---

> **Note importante** : Certaines fonctionnalités sont encore en développement, comme la tokenisation et les capacités avancées de traitement du langage naturel. 

### Installation :

1. Clonez le repository :
   ```bash
   git clone https://github.com/ton-utilisateur/chatbot.git

2.Installez les dépendances nécessaires : 
```bash
   pip install pyqt5 pyttsx3 fuzzywuzzy
  
