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

        self.saved_button= Button(self, text="Saved")
        self.saved_button.pack(side="right")


        #Création d'une variable pour la vitesse de l'exécution du programme
        var = IntVar()
        var.set(DEFAULT_SPEED)


         # Fonction appelée lorsqu'un nouvel état est sélectionné pour la vitesse
        def update_speed():
            self.speed = var.get() #Definition de la vitesse par défaut 


        Label(self, text=' ', padx=20).pack(side='left')  # Espaceur 
        Label(self, text="Speed : ").pack(side="left") #indiquer l'option de vitesse 
        Radiobutton(self, text="x1", variable=var, value=1, command=update_speed).pack(side="left") #Bouton radio pour vitesse x1
        Radiobutton(self, text="x5", variable=var, value=5, command=update_speed).pack(side="left") #Bouton radio pour vitesse x5
        Radiobutton(self, text="x10", variable=var, value=10, command=update_speed).pack(side="left") #Bouton radio pour vitesse x10
        
        # Création des labels pour l'affichage du nombre d'étapes
        self.steps_label1 = Label(self, text="Step : ")
        self.steps_label2 = Label(self, text="0")

        # Placement du label "0" à droite du label "Step :"
        self.steps_label2.pack(side="right")
        self.steps_label1.pack(side="right")

       
    def get_next_cell(self, direction):
        # Récupérer les coordonnées actuelles de la fourmi
        x = self.ant.x
        y = self.ant.y
        
        # Vérifier quelle direction a été donnée
        if direction == devant:
            # Si la direction est "devant", calculer les coordonnées de la cellule suivante en soustrayant 1 de la coordonnée "y"
            return x, y - 1
        if direction == droit:
            # Si la direction est "droit", calculer les coordonnées de la cellule suivante en ajoutant 1 à la coordonnée "x"
            return x + 1, y
        if direction == bas:
            # Si la direction est "bas", calculer les coordonnées de la cellule suivante en ajoutant 1 à la coordonnée "y"
            return x, y + 1
        if direction == gauche:
            # Si la direction est "gauche", calculer les coordonnées de la cellule suivante en soustrayant 1 de la coordonnée "x"
            return x - 1, y
    
    
    def get_back_cell(self, direction):
        # Récupérer les coordonnées actuelles de la fourmi
        x = self.ant.x
        y = self.ant.y
        
        # Vérifier quelle direction a été donnée
        if direction == devant:
            # Si la direction est "devant", calculer les coordonnées de la cellule suivante en soustrayant 1 de la coordonnée "y"
            return x, y + 1
        if direction == droit:
            # Si la direction est "droit", calculer les coordonnées de la cellule suivante en ajoutant 1 à la coordonnée "x"
            return x - 1, y
        if direction == bas:
            # Si la direction est "bas", calculer les coordonnées de la cellule suivante en ajoutant 1 à la coordonnée "y"
            return x, y - 1
        if direction == gauche:
            # Si la direction est "gauche", calculer les coordonnées de la cellule suivante en soustrayant 1 de la coordonnée "x"
            return x + 1, y

    def ant_cell_color(self):
        # Renvoie la couleur de la cellule sur laquelle se trouve la fourmi
        return self.cells[(self.ant.x, self.ant.y)].color

    def get_next_dir(self):
        # Récupère la couleur de la cellule sur laquelle se trouve la fourmi
        curr_color = self.ant_cell_color()
        # Si la cellule est noire, tourne à gauche
        if curr_color == BLACK:
            return left_dir(self.ant.dir)
            # Si la cellule est blanche ou grise, tourne à droite
        elif curr_color == WHITE or curr_color == GRAY:
             return right_dir(self.ant.dir)
    
    def get_back_dir(self):
        # Récupère la couleur de la cellule sur laquelle se trouve la fourmi
        curr_color = self.ant_cell_color()
        # Si la cellule est noire, tourne à gauche
        if curr_color == BLACK:
            return right_dir(self.ant.dir)
            # Si la cellule est blanche ou grise, tourne à droite
        elif curr_color == WHITE or curr_color == GRAY:
             return left_dir(self.ant.dir)
    
    
    def move_ant_back(self):
        # Obtenir la prochaine direction
        direction = self.get_back_dir()

        # Obtenir les coordonnées de la prochaine cellule
        (back_x, back_y) = self.get_back_cell(direction)

        # Vérifier si la fourmi est hors de la grille
        if not 0 >= back_x < X_CELLS or not 0 >= back_y < Y_CELLS:
            return False  # Sortir de la grille
        else:
             # Calculer le déplacement de la fourmi
            dx = (back_x - self.ant.x) * CELL_SIZE
            dy = (back_y - self.ant.y) * CELL_SIZE

            # Déplacer la fourmi sur la nouvelle cellule
            self.canvas.move(self.ant.widget, dx, dy)

            # Mettre à jour le nombre d'étapes
            self.steps += 1
            self.steps_label2.config(text=str(self.steps))

            # Mettre à jour la position et la direction de la fourmi
            self.ant.x = back_x
            self.ant.y = back_y
            self.ant.dir = direction

    


    def move_ant(self):
        # Obtenir la prochaine direction
        direction = self.get_next_dir()
    
        # Obtenir les coordonnées de la prochaine cellule
        (next_x, next_y) = self.get_next_cell(direction)
    
        # Vérifier si la fourmi est hors de la grille
        if not 0 <= next_x < X_CELLS or not 0 <= next_y < Y_CELLS:
            return False  # Sortir de la grille
        else:
             # Calculer le déplacement de la fourmi
            dx = (next_x - self.ant.x) * CELL_SIZE
            dy = (next_y - self.ant.y) * CELL_SIZE
        
            # Déplacer la fourmi sur la nouvelle cellule
            self.canvas.move(self.ant.widget, dx, dy)
        
            # Mettre à jour le nombre d'étapes
            self.steps += 1
            self.steps_label2.config(text=str(self.steps))
        
            # Mettre à jour la position et la direction de la fourmi
            self.ant.x = next_x
            self.ant.y = next_y
            self.ant.dir = direction
        
            return True


    def set_cell_color(self, x, y, color):
        # Récupère la cellule correspondante aux coordonnées x et y
        cell = self.cells[(x, y)]
        
        # Modifie la couleur de la cellule en lui assignant la couleur fournie en argument (modification logique)
        cell.color = color  
        
        # Met à jour la couleur visuelle de la cellule sur le canvas en utilisant la méthode "itemconfigure" de l'objet canvas (modification visuelle)
        self.canvas.itemconfigure(cell.widget, fill=color)


    def flip_cell_color(self, x, y):
        # Récupère la cellule correspondante aux coordonnées x et y
        cell = self.cells[(x, y)]
        
        # Détermine la couleur inverse de la couleur actuelle de la cellule en appelant la fonction "get_flipped_color"
        next_color = get_flipped_color(cell.color)
        
        # Met à jour la couleur de la cellule avec la nouvelle couleur calculée précédemment en appelant la méthode "set_cell_color"
        self.set_cell_color(x, y, next_color)
            

    def next_turn(self):
        # Récupère la cellule sur laquelle se trouve la fourmi avant qu'elle ne se déplace
        cell_before_move = self.cells[(self.ant.x, self.ant.y)]
        
        # Déplace la fourmi en appelant la méthode "move_ant"
        moved = self.move_ant()
        
        # Si la fourmi a bougé, inverse la couleur de la cellule précédente en appelant la méthode "flip_cell_color"
        if moved:
            self.flip_cell_color(cell_before_move.x, cell_before_move.y)
        
        # Renvoie un booléen qui indique si la fourmi a bougé ou non
        return moved
    
    def back_turn(self):
        # Récupère la cellule sur laquelle se trouve la fourmi avant qu'elle ne se déplace
        cell_before_move = self.cells[(self.ant.x, self.ant.y)]
        
        # Déplace la fourmi en appelant la méthode "move_ant"
        moved = self.move_ant_back()
        
        # Si la fourmi a bougé, inverse la couleur de la cellule précédente en appelant la méthode "flip_cell_color"
        if moved:
            self.flip_cell_color(cell_before_move.x, cell_before_move.y)
        
        # Renvoie un booléen qui indique si la fourmi a bougé ou non
        return moved

   


    def start_play_loop(self):
        # Vérifie si le jeu est terminé ou arrêté
        if self.finished or self.stopped:
            return
        
        # Initialise la variable "moved" à False
        moved = False
        
        # Appelle la méthode "next_turn" un certain nombre de fois (déterminé par "self.speed")
        for _ in range(self.speed):
            moved = self.next_turn()
        
        # Si la fourmi a bougé, attend un certain temps (déterminé par "SLEEP_TIME") avant de rappeler la méthode "start_play_loop"
        if moved:
            self.after(SLEEP_TIME, self.start_play_loop)
        
        # Si la fourmi n'a pas bougé, met à jour la variable "finished" pour indiquer que le jeu est terminé
        else:
            self.finished = True


    def next_button_click(self):
        # Vérifie si le jeu est terminé ou s'il est déjà en train d'être exécuté
        if self.finished or self.running:
            return
        
        # Exécute la méthode "next_turn" une seule fois
        moved = self.next_turn()
        
        # Si la fourmi n'a pas bougé pendant l'appel, met à jour la variable "finished" pour indiquer que le jeu est terminé
        if not moved:
            self.finished = True
    
    def back_button_click(self):
        # permet de revenir a l'etape d'avant "yassine"
        moved = self.back_turn()
        if moved:
            self.stopped = False


    def run_button_click(self):
        # Vérifie si le jeu est terminé ou s'il est déjà en train d'être exécuté
        if self.finished or self.running:
            return
        
        # Met à jour les variables "stopped" et "running"
        self.stopped = False
        self.running = True
        
        # Démarrer la boucle de jeu
        self.start_play_loop()
        
        # Met à jour la variable "running" pour indiquer que le jeu a été exécuté
        self.running = False


    def stop_button_click(self):
        # Met à jour la variable "stopped" à True pour arrêter le jeu
        self.stopped = True


    def reset_button_click(self):
        # Réinitialiser la grille
        for i in range(0, X_CELLS):
            for j in range(0, Y_CELLS):
                self.set_cell_color(i, j, GRAY)
        
        # Réinitialiser la position de la fourmi
        dx = (self.x0 - self.ant.x) * CELL_SIZE
        dy = (self.y0 - self.ant.y) * CELL_SIZE
        self.canvas.move(self.ant.widget, dx, dy)
        self.steps = 0
        self.ant.x = self.x0
        self.ant.y = self.y0
        self.ant.dir = devant
        
        
        # Réinitialiser les indicateurs de statut
        self.stopped = False
        self.finished = False
        self.running = False
    
    #Bouton de sauvegarde




    
  








   
        


# Créer une instance de la classe App
app = App()

# Lancer la boucle principale d'affichage pour l'interface utilisateur
app.mainloop()






# Créer une instance de la classe App
app = App()

# Lancer la boucle principale d'affichage pour l'interface utilisateur
app.mainloop()






