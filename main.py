
"""
from toolbox.Debug import Debug, Style
from toolbox.Speeker import Speaker, GttsEngine, Pyttsx3Engine
import time

from objects.button.Button import Button
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

import random



Debug.prefixActive = False


# toolbox.ImageDisplayer.display_image("./Images/Questions/question.png", 0, 0)

# Speaker.say("Bonjour à tous, je suis enchanté !", GttsEngine())


questions = [
    "Pourquoi les nuages sont blancs ?",
    "Combien de grains de sable y a-t-il dans le désert ?",
    "Est-ce que les poissons rouges peuvent nager à l'envers ?",
    "Pourquoi le ciel est bleu ?",
    "Est-ce que les chats peuvent voir dans le noir ?",
    "Combien de temps faut-il pour cuire un œuf sur le trottoir en plein soleil ?",
    "Est-ce que les pingouins ont des genoux ?",
    "Pourquoi les arbres sont verts ?",
    "Est-ce que les chiens peuvent regarder la télévision ?",
    "Combien de temps faut-il pour que la lumière du soleil atteigne la Terre ?",
    "Est-ce que les éléphants ont peur des souris ?",
    "Pourquoi les girafes ont un long cou ?",
    "Est-ce que les canards peuvent voler à reculons ?",
    "Combien de grains de riz peut-on mettre dans un verre ?",
    "Est-ce que les escargots laissent des traces de bave sur les vitres ?",
    "Pourquoi les abeilles font-elles du miel ?",
    "Est-ce que les papillons peuvent compter jusqu'à dix ?",
    "Combien de temps faut-il pour qu'un arbre pousse d'un mètre ?",
    "Est-ce que les grenouilles peuvent respirer sous l'eau ?",
    "Pourquoi les bananes sont-elles courbées ?"
]

result = [
    "C'est faux !",
    "Mauvaise réponse !",
    "C'est une mauvaise réponse pour vous !",
    "C'est encore une mauvaise réponse...",
    "Décidément, vous n'êtes vraiment pas doués",
    "C'est toujours faux. Vous le faites exprès ? C'est pourtant facile."
]


# Exemple d'utilisation
button = Button(16)  # Crée un objet Button pour la broche GPIO 18
MIFAREReader = SimpleMFRC522()

try:
    while True:
        Debug.LogWhisper("Passez le badge devant le capteur RFID...")
        id, text = MIFAREReader.read()
        
        # Poser une question aléatoire
        question = random.choice(questions)
        Debug.LogColor(f"Question : {question}", [Style.OK_CYAN, Style.UNDERLINE])
        Speaker.say(question, GttsEngine())
        
        Debug.LogWhisper("Appuyez sur le bouton svp...")
        # Attendre que le bouton soit pressé
        button_pressed = False
        while not button_pressed:
            button_pressed = button.process()
            time.sleep(0.1)

        # Donner une réponse aléatoire
        reponse = random.choice(result)
        Debug.LogColor(f"Réponse : {reponse}", [Style.PURPLE, Style.ITALIC])
        Speaker.say(reponse, GttsEngine())
        
        # Pause avant la prochaine question
        time.sleep(2)

except KeyboardInterrupt:
    Debug.LogSuccess("Programme interrompu par l'utilisateur")
finally:
    GPIO.cleanup()  # Nettoyer les configurations GPIO
    



"""

from toolbox.Debug import Debug, Style
from toolbox.Speeker import Speaker, GttsEngine, Pyttsx3Engine
import time

from objects.button.Button import Button
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

import random

from objects.Displayer.WebDisplayer import *

import threading


Debug.prefixActive = False


questions = [
    "Pourquoi les nuages sont blancs ?",
    "Combien de grains de sable y a-t-il dans le désert ?",
    "Est-ce que les poissons rouges peuvent nager à l'envers ?",
    "Pourquoi le ciel est bleu ?",
    "Est-ce que les chats peuvent voir dans le noir ?",
    "Combien de temps faut-il pour cuire un œuf sur le trottoir en plein soleil ?",
    "Est-ce que les pingouins ont des genoux ?",
    "Pourquoi les arbres sont verts ?",
    "Est-ce que les chiens peuvent regarder la télévision ?",
    "Combien de temps faut-il pour que la lumière du soleil atteigne la Terre ?",
    "Est-ce que les éléphants ont peur des souris ?",
    "Pourquoi les girafes ont un long cou ?",
    "Est-ce que les canards peuvent voler à reculons ?",
    "Combien de grains de riz peut-on mettre dans un verre ?",
    "Est-ce que les escargots laissent des traces de bave sur les vitres ?",
    "Pourquoi les abeilles font-elles du miel ?",
    "Est-ce que les papillons peuvent compter jusqu'à dix ?",
    "Combien de temps faut-il pour qu'un arbre pousse d'un mètre ?",
    "Est-ce que les grenouilles peuvent respirer sous l'eau ?",
    "Pourquoi les bananes sont-elles courbées ?"
]

result = [
    "C'est faux !",
    "Mauvaise réponse !",
    "C'est une mauvaise réponse pour vous !",
    "C'est encore une mauvaise réponse...",
    "Décidément, vous n'êtes vraiment pas doués",
    "C'est toujours faux. Vous le faites exprès ? C'est pourtant facile."
]


rfid_lock = threading.Lock()

# Thread 2
# ---------------------------------------------------------------------------- #
def thread_rfid_reader(string_updater):
    button = Button(16)  # Crée un objet Button pour la broche GPIO 18
    MIFAREReader = SimpleMFRC522()

    try:
        while True:
            with rfid_lock:  # Acquérir le verrou avant d'accéder au capteur RFID
                Debug.LogWhisper("Passez le badge devant le capteur RFID...")
                id, text = MIFAREReader.read()

                # Poser une question aléatoire
                question = random.choice(questions)
                Debug.LogColor(f"Question : {question}", [Style.OK_CYAN, Style.UNDERLINE])

                string_updater.write(question=question, answer="")

                # Speaker.say(question, GttsEngine())

                Debug.LogWhisper("Appuyez sur le bouton svp...")
                # Attendre que le bouton soit pressé
                button_pressed = False
                while not button_pressed:
                    button_pressed = button.process()
                    time.sleep(0.1)

                # Donner une réponse aléatoire
                reponse = random.choice(result)
                Debug.LogColor(f"Réponse : {reponse}", [Style.PURPLE, Style.ITALIC])
                
                string_updater.write(question=question, answer=reponse)
                
                # Speaker.say(reponse, GttsEngine())

                # Pause avant la prochaine question
                time.sleep(2)

    except KeyboardInterrupt:
        Debug.LogSuccess("Programme interrompu par l'utilisateur")

    finally:
        GPIO.cleanup() # Nettoyer les configurations GPIO




# Thread principal
# ---------------------------------------------------------------------------- #
string_updater = StringUpdater(update_interval=1)
web_app = WebApp(string_updater)

# Créer et démarrer le thread secondaire
thread_rfid = threading.Thread(target=thread_rfid_reader, args=(string_updater,))
thread_rfid.start()

# Exécuter l'application web Flask dans le thread principal
web_app.run()

# Attendre que le thread secondaire se termine
thread_rfid.join()

