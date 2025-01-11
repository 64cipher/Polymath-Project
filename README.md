# Polymath-Project

Assistant virtuel personnalisable pour Windows 

![image](https://github.com/user-attachments/assets/a8cffdf6-2e77-47d9-9a7b-baa0ee554535)


https://github.com/user-attachments/assets/82dba3f6-cfe6-45c8-a6ed-3e9eaa29f992


# Installation et Usage

Placez votre clé API Gemini dans ```config.json```

```pip install -r requirements.py```

```python main.py ```
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
    "ouvre code"
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

# Commande du mode "Saisie Vocale"

```
"retour à la ligne"
"effacer le mot"
"effacer le texte"
"tout sélectionner"
"copier le texte"
"coller le texte"
"menu" (touche windows)
"switch" (changer de fenêtre)
"annuler l'action"
"rétablir l'action"
```

# Note

Vous pouvez personnaliser la table des caractères dans ```main.py``` Ligne 166

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
        text = re.sub(r'\s*(?:point final)\s*$', '.', text)
```
Vous pouvez modifier les mots pour déclancher copier-coller, séléctionner, etc... à partir de la ligne 761, ultisez elif ```query == "votre phrase de commande":``` pour les phrases et ```elif word == "mot":``` pour les mots seuls. 
```keyboard.press('TOUCHE')``` pour maintenir une touche, ```keyboard.press_and_release('TOUCHE')``` et ```keyboard.press_and_release('TOUCHE')``` pour un appui simple

```
                    for word in query.split():
                        if query == "retour à la ligne":  # On simule le "Entrer" pour le retour à la ligne
                            keyboard.press_and_release('enter')
                        elif query == "effacer le mot": # On simule un "ctrl + backspace" pour effacer le mot précédent
                            keyboard.press('ctrl')
                            keyboard.press_and_release('backspace')
                            keyboard.release('ctrl')
                        elif query == "effacer le texte": # On simule un "ctrl + backspace" pour effacer le mot précédent                            
                            keyboard.press_and_release('backspace')
                        elif query == "tout sélectionner": # On simule un "ctrl + A" pour selectionner le texte
                            keyboard.press('ctrl')
                            keyboard.press_and_release('a')
                            keyboard.release('ctrl')                        
                        elif query == "copier le texte": # On simule un "ctrl + C" pour copier
                            keyboard.press('ctrl')
                            keyboard.press_and_release('c')
                            keyboard.release('ctrl') 
                        elif query == "coller le texte": # On simule un "ctrl + V" pour coller
                            keyboard.press('ctrl')
                            keyboard.press_and_release('v')
                            keyboard.release('ctrl') 
                        elif word == "menu": # On simule un "Touche Windows" pour ouvrir le menu démarrer
                            keyboard.press_and_release('cmd')
                        elif word == "switch": # On simule un "ctrl + V" pour coller
                            keyboard.press('alt')
                            keyboard.press_and_release('tab')
                            keyboard.release('alt') 
```
