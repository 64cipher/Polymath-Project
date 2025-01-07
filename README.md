# Polymath-Project
JARVIS-like avec Gemini

Assistant virtuel personnalisable pour Windows 

![image](https://github.com/user-attachments/assets/a8cffdf6-2e77-47d9-9a7b-baa0ee554535)

# Installation et Usage

Placez votre clé API Gemini dans ```config.json```

```pip install -r requirements.py```

```python jargui.py ```
ou
Lancez ```start.bat```

# Exemples de commandes vocales

    "ouvre firefox"
    "ouvre discord"
    "quelle heure est-il"
    "google"
    "youtube"
    "dis bonjour"
    "test"
    "prends note"
    "ouvre chrome"
    "ouvre le terminal"
    "ouvre notepad"
    "calculer"
    "ouvre vscode"
    "Saisie vocale" (STT On)
    "Arrêt de la saisie" (STT Off)
    "on est quel jour"
    "Planifier tâche"
    "discuter" (chat avec Gemini)
    "screenshot" (En mode Gemini)
    "webcam" (En mode Gemini)
    "standard" (retour en mode assistant)

Pour ouvrir une console, configurer "ouvrir le terminal" et créer un fichier ```cmd.bat``` et mettre le chemin de ce fichier dans nouvelle commande sur le type ```Launch```.

    "@echo on"
    "start powershell"

Ouvrir un site web spécifique depuis un fichier bat qui contient

    "powershell start "https://google.com""

D'autres fonctionnalités sont à venir en fonction de mon inspiration.

# Note

le programme a quelques défauts comme le calcul.

Dites 2 astérisque 3, et non 2 fois 3 car le "fois" est le symbole x et c'est compris comme étant la lettre x et non le symbole multiplier
