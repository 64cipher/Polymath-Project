import pyautogui
import time

def clic_droit():
    """Simule un clic droit simple à la position actuelle de la souris."""
    x, y = pyautogui.position()
    pyautogui.click(x, y, button='right')
    print(f"Clic droit effectué à la position ({x}, {y})")

if __name__ == "__main__":
    print("Clic droit en cours...")
    clic_droit()
    print("Fin de l'action.")