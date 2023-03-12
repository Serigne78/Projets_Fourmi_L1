from tkinter import *
import math

# colors
WHITE = "white"
BLACK = "black"
YELLOW = "yellow"
GRAY = "gray"
# Cette fonction permet de changer la couleur en noir ou en blanc en fonction du positionnemnt de la fourmi 
def get_flipped_color(color):
    if color == BLACK:
        return WHITE
    if color == WHITE or color == GRAY:
        return BLACK


# directions
devant= 0
droit = 1
bas = 2
gauche = 3

def right_dir(direction):
    # Calcule la direction à droite de la direction donnée.
    # La direction est un entier compris entre 0 et 3.
    # La fonction renvoie un entier compris entre 0 et 3.
    return (direction + 1) % 4


def left_dir(direction):
    # Calcule la direction à gauche de la direction donnée.
    # La direction est un entier compris entre 0 et 3.
    # La fonction renvoie un entier compris entre 0 et 3.
    # Le résultat est calculé en soustrayant 1 de la direction
    # donnée, en prenant le modulo 4 pour s'assurer que le
    # résultat reste compris entre 0 et 3.
    return (direction - 1) % 4

# Configuration de TK
X_CELLS = 71          # Nombre de cellules en largeur
Y_CELLS = 53       # Nombre de cellules en hauteur
CELL_SIZE = 14    # Taille d'une cellule en pixels
SLEEP_TIME = 1        # Temps en ms entre deux déplacements
DEFAULT_SPEED = 1     # Nombre de déplacements avant un temps de pause



class Cell:
    def __init__(self, widget, x, y, color=WHITE):
        # Initialise une nouvelle instance de la classe Cell avec les
        # propriétés suivantes :
        # - widget : le widget TK qui représente la cellule sur l'écran
        # - x : la coordonnée en abscisse de la cellule dans la grille
        # - y : la coordonnée en ordonnée de la cellule dans la grille
        # - color : la couleur de la cellule, par défaut "BLANCHE"
        self.widget = widget
        self.x = x
        self.y = y
        self.color = color

class Ant:
    def __init__(self, widget, x, y, direction=devant):
        # Initialise une nouvelle instance de la classe Ant avec les
        # propriétés suivantes :
        # - widget : le widget TK qui représente la fourmi sur l'écran
        # - x : la coordonnée en abscisse de la fourmi dans la grille
        # - y : la coordonnée en ordonnée de la fourmi dans la grille
        # - direction : la direction de la fourmi (devant, derrière, gauche ou droite)
        self.widget = widget
        self.x = x
        self.y = y
        self.dir = direction    
        

class App(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.cells = {}
        self.finished = False   # impossible d'aller plus loin en raison de la taille de la grille
        self.stopped = False    # l'utilisateur a interrompu l'exécution
        self.running = False    # actuellement en cours d'exécution (évite les rappels multiples)
        self.steps = 0
        self.speed = DEFAULT_SPEED
        if X_CELLS % 2 == 0 or Y_CELLS % 2 == 0:
            raise Exception("Impossible")
            
#titre
self.title_label = Label(self, text="Fourmi de Langton", justify=CENTER)
self.title_label.pack()

#frame
self.frame = Frame(self, padx=1, pady=1, borderwidth=2, relief=GROOVE)
self.frame.pack()



# Créer une instance de la classe App
app = App()

# Lancer la boucle principale d'affichage pour l'interface utilisateur
app.mainloop()




