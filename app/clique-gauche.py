import pyautogui
import time

def clic_gauche():
    """Simule un clic gauche simple à la position actuelle de la souris."""
    x, y = pyautogui.position()
    pyautogui.click(x, y, button='left')
    print(f"Clic gauche effectué à la position ({x}, {y})")

if __name__ == "__main__":
    print("Clic gauche en cours...")
    clic_gauche()
    print("Fin de l'action.")