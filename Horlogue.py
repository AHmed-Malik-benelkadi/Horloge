from time import *
from tkinter import *
from tkinter import messagebox

''''''


Windows = Tk()  # creation de la fenetre principale (la fenetre de l'horloge)

Windows.geometry("400x200") # taille de la fenetre
Windows.title("Horloge")

# Variables utilisées pour l'affichage de l'heure
timeClock = [15, 59, 55] # Heure, minute, seconde
hourMinSec = {"heure": 23, "MinSec": 59} # Heure et minute maximum
clock = f"{timeClock[0]}:{timeClock[1]}:{timeClock[2]}" # Heure affichée

# Variables pour la fonction SetTime et SetAlarm (les entrées de texte)
timeSet = [] # Les entrées de texte pour régler l'heure
alarmEntry = [] # Les entrées de texte pour régler l'alarme
alarmSet = [0, 0, 0] # Heure, minute, seconde de l'alarme (par défaut, l'alarme est réglée à 00:00:00)
alarmEnabled = False # Variable qui permet d'activer/désactiver l'alarme

# Variables pour le mode AM/PM (si on est en mode AM/PM, on affiche le mode en plus de l'heure)
paused = False
AmPmMode = False
mode = "H"

# Creation des frames  pour l'horloge et les boutons (les frames permettent de mieux organiser les widgets)
clockFrame = Frame(Windows, height=200)
clockFrame.pack(expand=True, fill="both") # on affiche la frame de l'horloge
buttonsFrame = Frame(Windows)   # on crée la frame des boutons sans l'afficher
buttonsFrame.pack(expand=True, fill="both")
for i in range(2): # on affiche la frame des boutons
    buttonsFrame.rowconfigure(i, weight=1)
    buttonsFrame.columnconfigure(i, weight=1)

# Creation des boutons
clockLabel = Label(clockFrame, text=clock, font=("Arial", 30, "bold"), anchor=CENTER)
clockLabel.pack(expand=True, fill="both")



def HoursMinSec(alarmMode):
    # Fonction qui ajuste les heures, minutes et secondes en fonction de la limite définie dans "hourMinSec"
    global timeClock, alarmSet, hourMinSec  # permet d'accéder aux variables globales

    # On initialise la variable "time" à l'heure actuelle ou à l'heure de l'alarme en fonction de "alarmMode"
    time = alarmSet if alarmMode else timeClock

    # On ajuste les secondes si elles dépassent la limite définie dans "hourMinSec"
    if time[2] > hourMinSec["MinSec"]:
        time[2] -= 60
        if not alarmMode:  # Si on n'est pas en train de régler l'alarme
            time[1] += 1  # On ajoute une minute

    # On ajuste les minutes si elles dépassent la limite définie dans "hourMinSec"
    if time[1] > hourMinSec["MinSec"]:
        time[1] -= 60
        if not alarmMode:  # Si on n'est pas en train de régler l'alarme
            time[0] += 1  # On ajoute une heure

    # On ajuste les heures si elles dépassent la limite définie dans "hourMinSec"
    if time[0] > hourMinSec["heure"]:
        time[0] -= 24

    # On met à jour la variable "alarmSet" ou "timeClock" en fonction de "alarmMode"
    if alarmMode:
        alarmSet = time
    else:
        timeClock = time



def Clock():
    # Fonction qui affiche l'heure actuelle
    global mode, timeClock, clock # permet d'accéder aux variables globales
    clock = f"{timeClock[0]}{mode}:{timeClock[1]}m:{timeClock[2]}s" # si on est en mode AM/PM, on affiche le mode en plus de l'heure
    timeClock[2] += 1 # on ajoute une seconde à l'heure actuelle

    HoursMinSec(False)  # On ajuste les heures, minutes et secondes en fonction de la limite définie dans "hourMinSec"
    Alarm() # On vérifie si l'alarme doit sonner
    if AmPmMode and timeClock[0] > 12:  # Si on est en mode AM/PM et que l'heure dépasse 12
        timeClock[0] = 1
        if mode == "AM":
            mode = "PM"
        else:
            mode = "AM"

    clockLabel.config(text=clock)
    Windows.update()
    sleep(1)
    Windows.after(1000, Clock())


def SetTime():
    # Fonction qui permet de régler l'heure
    global timeSet, timeClock, mode, AmPmMode # permet d'accéder aux variables globales
    for i in range(3): # on crée 3 entrées de texte
        try: # on vérifie que les entrées sont des nombres
            if timeSet[i].get().isalnum(): # on vérifie que les entrées sont des nombres
                timeClock[i] = int(timeSet[i].get())
                if AmPmMode == True: # si on est en mode AM/PM
                    AmPmMode = False
                    mode = "H"
        except:  # si les entrées ne sont pas des nombres
            messagebox.showerror("Erreur ", "saisie invalide")
            break


def SetAlarm():
    # Fonction qui permet de régler l'alarme et de l'activer/désactiver en fonction de son état
    global alarmEntry, alarmSet, alarmEnabled, AmPmMode, mode
    if alarmEnabled == False: # si l'alarme est désactivée
        for i in range(3): # on crée 3 entrées de texte
            try: # on vérifie que les entrées sont des nombres
                if alarmEntry[i].get().isalnum():
                    alarmSet[i] = int(alarmEntry[i].get())
                    HoursMinSec(True)
            except:
                messagebox.showerror("Erreur", "saisie invalide")
                return None
        if AmPmMode == True: # si on est en mode AM/PM
            AmPmMode = False
            mode = "H" # on désactive le mode AM/PM
        alarmEnabled = True
        messagebox.showinfo("Alarm", f"L'alarme a été réglée sur {alarmSet[0]}H:{alarmSet[1]}m:{alarmSet[2]}s") # on affiche l'heure de l'alarme
    else:
        alarmEnabled = False
        messagebox.showinfo("Alarm", "L'alarme a été désactivée")


def Alarm():
    # Fonction qui vérifie si l'alarme doit sonner
    global timeClock, alarmSet, alarmEnabled
    if timeClock == alarmSet and alarmEnabled: # si l'heure actuelle est égale à l'heure de l'alarme et que l'alarme est activée
        messagebox.showinfo("Alarm", "L'alarme a sonné ! ! ! ")
        alarmEnabled = False # on désactive l'alarme


def AmPmSet():
    # Fonction qui permet de passer du mode 24h au mode AM/PM et inversement
    global AmPmMode, mode, timeClock
    if AmPmMode == False: # si on est en mode 24h
        AmPmMode = True # on passe en mode AM/PM
        mode = "AM" # on initialise le mode à AM
        if timeClock[0] > 12:
            timeClock[0] -= 12
            mode = "PM"
        elif timeClock[0] == 0:
            timeClock[0] = 12
    else:
        AmPmMode = False
        if mode == "PM":
            timeClock[0] += 12
        elif mode == "AM" and timeClock[0] == 12:
            timeClock[0] = 0
        mode = "H"


# Fonction qui permet de mettre en pause l'horloge
def Pause():
    global paused, timeClock
    if paused == False:
        paused = True
    else:
        paused = False

    pausedAt = timeClock
    clock = f"{pausedAt[0]}{mode}:{pausedAt[1]}m:{pausedAt[2]}s"

    while paused:
        clockLabel.config(text=clock)
        Windows.update()


# Fonction qui permet de quitter l'application en fermant la fenêtre principale et en arrêtant le programme en cours d'exécution
def TimeEntryFrame():
    global timeSet, alarmSet
    setFrame = Frame(buttonsFrame)
    setFrame.grid(row=0, column=0, sticky=NSEW)
    alarmFrame = Frame(buttonsFrame)
    alarmFrame.grid(row=0, column=1, sticky=NSEW)

    setDict = {setFrame: "Définir l'heure", alarmFrame: "Définir l'alarme"}

    for frame, label in setDict.items(): # on crée les frames et les entrées de texte
        for i in range(3): # on crée 3 entrées de texte
            setEntry = Entry(frame, width=5)
            setEntry.pack(side=LEFT, padx=4)
            if frame is setFrame: # on ajoute les entrées de texte dans les listes correspondantes
                timeSet.append(setEntry)
            elif frame is alarmFrame:  # on ajoute les entrées de texte dans les listes correspondantes
                alarmEntry.append(setEntry)
        if frame is setFrame: # on crée les boutons de définition de l'heure et de l'alarme
            setButton = Button(frame, text=label, font=("Arial", 10), command=SetTime)
        elif frame is alarmFrame:
            setButton = Button(frame, text=label, font=("Arial", 10), command=SetAlarm)
        setButton.pack(expand=True)


def Features():
    # Fonction qui crée les boutons et les frames de l'interface graphique
    TimeEntryFrame() # on crée les frames et les entrées de texte
    modeButton = Button(buttonsFrame, text="AM/PM", font=("Arial", 10), command=AmPmSet).grid(row=1, column=0,
                                                                                              sticky=NSEW)
    pauseButton = Button(buttonsFrame, text="Pause", font=("Arial", 10), command=Pause).grid(row=1, column=1,
                                                                                             sticky=NSEW)


def main(): # Fonction principale
    try: # on vérifie que le programme ne plante pas
        Features() # on crée les boutons
        Clock() # on lance l'horloge
        Windows.mainloop()  # on lance la fenêtre
    except: # si le programme plante
        print("programme terminé ! ")


if __name__ == "__main__": # on lance le programme
    main()  # on lance la fonction principale
