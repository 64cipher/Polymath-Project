import pyautogui
import time

def maintenir_clic_gauche():
    """Simule l'action de maintenir le clic gauche enfoncé à la position actuelle de la souris."""
    x, y = pyautogui.position()
    pyautogui.mouseDown(x, y, button='left')
    print(f"Clic gauche maintenu à la position ({x}, {y})")

if __name__ == "__main__":
    print("Maintien du clic gauche en cours...")
    maintenir_clic_gauche()
    print("Fin de l'action.")