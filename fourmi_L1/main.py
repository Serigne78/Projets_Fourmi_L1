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

        
        # Titre
        self.title_label = Label(self, text="Fourmi de Langton", justify=CENTER)
        self.title_label.pack()

        # Frame
        self.frame = Frame(self, padx=1, pady=1, borderwidth=2, relief=GROOVE)
        self.frame.pack()

       #Définir la taille du canvas
        self.canvas = Canvas(self.frame,
                             width=10 + X_CELLS * CELL_SIZE,
                             height=10 + Y_CELLS * CELL_SIZE,
                             bd=0, background=WHITE)

        for i in range(0, 1 + X_CELLS):
            self.canvas.create_line(5 + CELL_SIZE * i, 5,
                                    5 + CELL_SIZE * i, 5 + Y_CELLS * CELL_SIZE,
                                    fill=BLACK)
        for j in range(0, 1 + Y_CELLS):
            self.canvas.create_line(5, 5 + CELL_SIZE * j,
                                    5 + X_CELLS * CELL_SIZE, 5 + CELL_SIZE * j,
                                    fill=BLACK)
        self.canvas.pack()


        for i in range(0, X_CELLS):
            for j in range(0, Y_CELLS):
                cell = self.canvas.create_rectangle(
                    5 + i * CELL_SIZE + 1, 5 + j * CELL_SIZE + 1,
                    (i + 1) * CELL_SIZE + 5, 5 + (j + 1) * CELL_SIZE,
                    fill=GRAY, outline="")
                self.cells[(i, j)] = Cell(cell, i, j)

        # Déterminer les coordonnées de départ pour la fourmi
        self.x0= math.trunc(X_CELLS / 2)
        self.y0= math.trunc(Y_CELLS / 2)

        # Créer un widget pour la fourmi
        ant_widget = self.canvas.create_oval(
            5 + self.x0 * CELL_SIZE + 1 + 1, 5 + self.y0 * CELL_SIZE + 1 + 1,
            5 + (self.x0 + 1) * CELL_SIZE - 1, 5 + (self.y0 + 1) * CELL_SIZE - 1,
            fill=YELLOW, outline="")
        

        # Créer une instance de la fourmi et la stocker dans l'attribut de la classe correspondant
        self.ant = Ant(ant_widget, self.x0, self.y0)

       # Création des boutons pour contrôler l'exécution du programme
        self.bottom_frame = Frame(self)
        self.bottom_frame.pack()

        # Bouton "Next" pour exécuter une seule étape à la fois
        self.next_button = Button(self, text="Next", command=self.next_button_click)
        self.next_button.pack(side="right")

        # Bouton "Play" pour exécuter le programme en continu
        self.run_button = Button(self, text="Play", command=self.run_button_click)
        self.run_button.pack(side="right")
        # Bouton revenir en arriere
        self.back_button = Button(self,text="Back", command=self.back_button_click)
        self.back_button.pack(side="right")

        # Bouton "Pause" pour arrêter l'exécution du programme
        self.stop_button = Button(self, text="Pause", command=self.stop_button_click)
        self.stop_button.pack(side="right")


        # Bouton "Reset" pour réinitialiser le programme à son état initial
        self.reset_button = Button(self, text="Reset", command=self.reset_button_click)
        self.reset_button.pack(side="right")


        #Création d'une variable pour la vitesse de l'exécution du programme
        var = IntVar()
        var.set(DEFAULT_SPEED)



# Créer une instance de la classe App
app = App()

# Lancer la boucle principale d'affichage pour l'interface utilisateur
app.mainloop()






