# Polymath-Project

Assistant virtuel personnalisable pour Windows 

![image](https://github.com/user-attachments/assets/a8cffdf6-2e77-47d9-9a7b-baa0ee554535)


https://github.com/user-attachments/assets/0e8568c2-79c1-418c-b1fc-d23b3f2d134d


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
    "ouvre google"
    "ouvre youtube"
    "dis bonjour"
    "test"
    "prends note"
    "ouvre chrome"
    "ouvre le terminal"
    "ouvre notepad"
    "calculer"
    "ouvre vscode"
    "Saisie vocale" (STT On)
    "Fin de la saisie" (STT Off)
    "on est quel jour"
    "Planifier tâche"
    "discuter" (chat avec Gemini)
    "screenshot" (En mode Gemini)
    "webcam" (En mode Gemini)
    "standard" (retour en mode assistant)

Vous pouvez ouvrir une console ou autre, configurer "ouvrir le terminal" ou autre application et créer un fichier ```cmd.bat``` et mettre le chemin de ce fichier (```Path```) en cliquant sur Ajouter, à la section ```Gestion de Commandes``` commande sur le type ```launch```.

    "@echo on"
    "start powershell"

Ouvrir un site web spécifique depuis un fichier bat qui contient

    "powershell start "https://google.com""

D'autres fonctionnalités sont à venir en fonction de mon inspiration.

# Note

Vous pouvez personnaliser la table des caractères dans ```jargui.py``` Ligne 166

```        # On remplace les mots clés par de la ponctuation.
        text = re.sub(r'\b(?:signe dièse)\b', '#', text)
        text = re.sub(r'\b(?:signe plus)\b', '+', text)
        text = re.sub(r'\b(?:astérisque)\b', '*', text)
        text = re.sub(r'\b(?:signe fois)\b', '*', text)
        text = re.sub(r'\b(?:pourcent)\b', '%', text)
        text = re.sub(r'\b(?:signe moins)\b', '-', text)
        text = re.sub(r'\b(?:guillemet)\b', '"', text)
        text = re.sub(r'\b(?:slash)\b', '/', text)
        text = re.sub(r'\b(?:signe euro)\b', '€', text)
        text = re.sub(r'\b(?:point d\'interrogation)\b', '?', text)
        text = re.sub(r'\b(?:point d\'exclamation|exclamation)\b', '!', text)
        text = re.sub(r'\b(?:virgule)\b', ',', text)
        text = re.sub(r'\b(?:deux points)\b', ':', text)
        text = re.sub(r'\b(?:point virgule)\b', ';', text)
        text = re.sub(r'\b(?:retour à la ligne)\b', '\n', text)
        text = re.sub(r'\b(?:arobase)\b', '@', text)
        text = re.sub(r'\s*(?:point final)\s*$', '.', text)```
