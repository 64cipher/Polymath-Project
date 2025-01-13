import keyboard
import time

def envoyer_cmd():
  keyboard.press("cmd")
  time.sleep(0.1)  # Petit délai pour s'assurer que les touches sont bien enfoncées
  keyboard.release("cmd")

if __name__ == "__main__":
  time.sleep(0)
  envoyer_cmd()
  print("WIN a été envoyé.")