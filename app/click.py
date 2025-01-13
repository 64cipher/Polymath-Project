import pyautogui
import time

def double_clic_gauche():
    """Simule un double-clic gauche à la position actuelle de la souris."""
    x, y = pyautogui.position()
    pyautogui.doubleClick(x, y, button='left') # force le button gauche
    print(f"Double-clic gauche effectué à la position ({x}, {y})")

if __name__ == "__main__":
    print("Double-clic gauche en cours...")
    double_clic_gauche()
    print("Fin de l'action.")