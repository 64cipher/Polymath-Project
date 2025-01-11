import keyboard
import time

def envoyer_alt_f4():
  """Simule la pression de Alt+F4."""
  keyboard.press("alt")
  keyboard.press("f4")
  time.sleep(0.1)  # Petit délai pour s'assurer que les touches sont bien enfoncées
  keyboard.release("f4")
  keyboard.release("alt")

if __name__ == "__main__":
  print("Envoi de la combinaison Alt+F4 dans 3 secondes...")
  time.sleep(0)
  envoyer_alt_f4()
  print("Alt+F4 a été envoyé.")