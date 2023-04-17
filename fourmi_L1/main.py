import tkinter as tk
import json
from tkinter import filedialog

# Taille de la grille (100x100)
grid_size = 100

# Couleur de chaque état
color_white = "#FFFFFF"  # blanc
color_black = "#000000"  # noir

# Créer la fenêtre principale
root = tk.Tk()
root.title("Langton's ant")

# Créer un canvas pour dessiner la grille
canvas = tk.Canvas(root, width=grid_size*5, height=grid_size*5)
canvas.grid(column = 1, rowspan = 10)

# Créer la grille (une liste de listes)
states = [[color_white for col in range(grid_size)] for row in range(grid_size)]

speed_scale = tk.Scale(root, from_=1, to=100, orient=tk.HORIZONTAL)
speed_scale.grid(column = 2, row = 8)

# Créer la fourmi
ant_row = grid_size // 2
ant_col = grid_size // 2
ant_direction = "up"
running = False
step = True
back = False
speed = int(speed_scale.get())

# Définir les règles de Langton's ant
def langtons_ant():
    global ant_row, ant_col, ant_direction
    global running, step , speed , back
    if running:
        if back :
            # Déplacer la fourmi
            if ant_direction == "up":
                ant_row += 1
            elif ant_direction == "right":
                ant_col -= 1
            elif ant_direction == "down":
                ant_row -= 1
            else:
                ant_col += 1
            # Vérifier que la fourmi ne sort pas de la grille
            if ant_row < 0:
                ant_row = grid_size - 1
            elif ant_row >= grid_size:
                ant_row = 0
            if ant_col < 0:
                ant_col = grid_size - 1
            elif ant_col >= grid_size:
                ant_col = 0
        # Si la case sur laquelle se trouve la fourmi est blanche
        if states[ant_row][ant_col] == color_white:
            # Tourner à droite
            if ant_direction == "up":
                ant_direction = "right"
            elif ant_direction == "right":
                ant_direction = "down"
            elif ant_direction == "down":
                ant_direction = "left"
            else:
                ant_direction = "up"
            # Changer la couleur de la case en noir
            states[ant_row][ant_col] = color_black
        # Si la case sur laquelle se trouve la fourmi est noire
        else:
            # Tourner à gauche
            if ant_direction == "up":
                ant_direction = "left"
            elif ant_direction == "right":
                ant_direction = "up"
            elif ant_direction == "down":
                ant_direction = "right"
            else:
                ant_direction = "down"
            # Changer la couleur de la case en blanc
            states[ant_row][ant_col] = color_white
        # Mettre à jour la couleur de la case dans l'interface graphique
        canvas.itemconfig(cells[ant_row][ant_col], fill=states[ant_row][ant_col])
        if not back:
            # Déplacer la fourmi
            if ant_direction == "up":
                ant_row -= 1
            elif ant_direction == "right":
                ant_col += 1
            elif ant_direction == "down":
                ant_row += 1
            else:
                ant_col -= 1
            # Vérifier que la fourmi ne sorte pas de la grille
            if ant_row < 0:
                ant_row = grid_size - 1
            elif ant_row >= grid_size:
                ant_row = 0
            if ant_col < 0:
                ant_col = grid_size - 1
            elif ant_col >= grid_size:
                ant_col = 0
            # Appeler cette fonction à nouveau après un court délai
            if step:
                canvas.after(speed, langtons_ant)      


            """Le code ci-dessus implémente les règles du Langton's ant, un automate cellulaire dont le comportement est très complexe et imprévisible malgré des règles très simples.

La fonction langtons_ant est appelée répétitivement et met à jour l'état de chaque case de la grille selon les règles suivantes :

Si la case sur laquelle se trouve la fourmi est blanche :
La fourmi tourne à droite.
La case devient noire.
Si la case sur laquelle se trouve la fourmi est noire :
La fourmi tourne à gauche.
La case devient blanche.
La position et la direction de la fourmi sont également mises à jour après chaque mouvement, en prenant en compte les limites de la grille.

Le code utilise également une interface graphique pour afficher la grille et les cases, ainsi que pour animer la fourmi.

Enfin, il y a plusieurs variables globales qui contrôlent le fonctionnement de la simulation, notamment running pour indiquer si la simulation est en cours, step pour indiquer si la simulation doit avancer d'un pas à la fois, et speed pour contrôler la vitesse de la simulation.""" 

def reset_langtons_ant():
    global ant_row, ant_col, ant_direction, running, step, back
    # Remet les cases de la grille en blanc 
    for row in range(grid_size):
        for col in range(grid_size):
            states[row][col] = color_white
            canvas.itemconfig(cells[row][col], fill=states[row][col])
    # Reinitialise la position et la direction de la fourmi
    ant_row = grid_size // 2
    ant_col = grid_size // 2
    ant_direction = "up"
    # Arrete le jeu et reinitialise la variable "step"
    running = False
    step = True
    back = False

    """Cette fonction reset_langtons_ant() remet la grille du jeu de la fourmi de Langton à son état initial. Elle remet toutes les cases de la grille en blanc et replace la fourmi au centre de la grille, orientée vers le haut. Elle arrête également le jeu et réinitialise la variable "step" à True."""

def start_langtons_ant():
    global running , step, back
    running = True
    step = True
    back= False
    langtons_ant()

    """La fonction start_langtons_ant() initialise les variables running, step et back pour démarrer le jeu de la fourmi de Langton en continu. Elle appelle ensuite la fonction langtons_ant() pour faire avancer la fourmi. """
    """La variable step est initialisée à False car le jeu doit fonctionner en continu sans interruption. La variable back est également initialisée à False car la fourmi doit avancer dans la direction actuelle."""

def stop_langtons_ant():
    global running
    running = False
    """La fonction "stop_langtons_ant" arrête le jeu en mettant la variable "running" à False .Cette fonction permettra d'arrêter la fourmi de Langton en cours d'exécution."""

def step_langtons_ant():
    global step , running, back
    step = False
    running = True
    back = False
    langtons_ant()
    """Cette fonction permet d'exécuter une étape du jeu de la fourmi de Langton. Elle modifie les variables globales "step", "running" et "back" pour démarrer le jeu et s'assurer qu'il avance d'une seule étape.

La variable "step" est définie à True pour permettre l'exécution de l'étape, puis à False pour indiquer que l'étape a été exécutée. La variable "running" est définie à True pour lancer le jeu, et la variable "back" est définie à False pour que la fourmi avance normalement.

Enfin, la fonction appelle la fonction "langtons_ant()" pour exécuter une étape du jeu."""

   
def back_step_langtons_ant():
    global running , step, back
    running = True
    back = True
    langtons_ant()

    """Cette fonction permet d'exécuter une étape en arrière dans le jeu de la fourmi de Langton. Elle initialise la variable "running" à True pour lancer l'exécution de la fonction "langtons_ant()", qui va faire avancer la fourmi d'une case dans la direction opposée à sa direction actuelle et changer la couleur de la case sur laquelle elle se trouve en fonction de l'état précédent de cette case.

La variable "back" est initialisée à True pour indiquer que l'on souhaite effectuer une étape en arrière, et non pas avancer la fourmi comme dans la fonction "step_langtons_ant()". Enfin, la variable "step" n'est pas modifiée pour permettre de continuer à faire avancer la fourmi case par case en appuyant sur le bouton "Step" après avoir effectué une étape en arrière."""


def update_speed(*args):
    global speed
    speed = int(speed_scale.get())
speed_scale.config(command=update_speed)

"""Ce code permet de lier une fonction à une commande d'un widget Scale dans Tkinter. Plus précisément, lorsque la valeur de la Scale est modifiée, la fonction update_speed est appelée avec les arguments *args.

La fonction update_speed met à jour la variable globale speed en convertissant la valeur actuelle de la Scale (qui est une chaîne de caractères) en entier avec la fonction int(). Ainsi, la variable speed contiendra la valeur numérique correspondante à la position de la Scale.

Ensuite, la commande speed_scale.config(command=update_speed) lie la fonction update_speed à la Scale speed_scale en tant que commande. Cela signifie que chaque fois que la position de la Scale est modifiée, la fonction update_speed sera appelée automatiquement pour mettre à jour la variable speed."""

def save_state():
    # Créer un dictionnaire qui répertorie les différents états du jeu pour pouvoir sauvegarder une instance
    state_dict = {
        "grid_size": grid_size,
        "states": states,
        "ant_row": ant_row,
        "ant_col": ant_col,
        "ant_direction": ant_direction
    }

    
    # Converti le dictionnaire en  JSON
    state_json = json.dumps(state_dict)
    # Ouvre l'explorateur de fichier pour enregistrer une partie
    file_path = tk.filedialog.asksaveasfilename(defaultextension=".json")
    # Ecrit la chaine de caractère JSON dansd le fichier 
    with open(file_path, "w") as f:
        f.write(state_json)

    """La fonction save_state permet de sauvegarder l'état actuel du jeu Langton's Ant en créant un dictionnaire qui répertorie les différents états du jeu. Le dictionnaire contient les clés grid_size, states, ant_row, ant_col, et ant_direction qui correspondent respectivement à la taille de la grille, les états des cases, la ligne et la colonne actuelles de la fourmi, et sa direction actuelle.
        Ensuite, la fonction convertit le dictionnaire en JSON à l'aide de la fonction json.dumps(). Elle ouvre ensuite une boîte de dialogue de l'explorateur de fichiers pour permettre à l'utilisateur de choisir le chemin et le nom du fichier à enregistrer. Puis elle écrit la chaîne de caractères JSON dans le fichier choisi à l'aide de la fonction open et write. De cette façon, l'état actuel du jeu peut être sauvegardé dans un fichier JSON."""
def open_instance():
    # Ouvre l'explorateur de fichier pour ouvrir une partie sauvegardée 
    filename = filedialog.askopenfilename(title="Open a saved instance", filetypes=[("JSON files", "*.json")])

    # Charge les données d'une partie depuis un fichier enregistré
    with open(filename, "r") as f:
        instance_data = json.load(f)

    # Met à jour les variables principales 
    global states, ant_row, ant_col, ant_direction
    states, ant_row, ant_col, ant_direction = instance_data["states"], instance_data["ant_row"], instance_data["ant_col"], instance_data["ant_direction"]

    # met à jour le canevas pour qu'il corresponde aux nouvelles variables
    for row in range(grid_size):
        for col in range(grid_size):
            canvas.itemconfig(cells[row][col], fill=states[row][col])

    """La fonction open_instance() permet d'ouvrir une partie sauvegardée en format JSON. Elle utilise le module tk.filedialog pour ouvrir une fenêtre de sélection de fichier et l'utilisateur doit choisir un fichier avec l'extension .json. Ensuite, elle lit les données du fichier sélectionné en utilisant la fonction json.load() et stocke les données dans la variable instance_data. Les données de la partie sont ensuite assignées aux variables principales states, ant_row, ant_col et ant_direction.

Enfin, la fonction met à jour le canevas pour refléter les nouvelles données de la partie en utilisant une boucle for pour parcourir toutes les cases du canevas et en utilisant la fonction itemconfig() de tkinter pour modifier la couleur de chaque case en fonction des données de la partie chargée."""



# Créer les cases dans le canvas
cells = []
for row in range(grid_size):
    row_cells = []
    for col in range(grid_size):
        x1 = col * 5
        y1 = row * 5
        x2 = x1 + 5
        y2 = y1 + 5
        cell = canvas.create_rectangle(x1, y1, x2, y2, fill=states[row][col], outline="")
        row_cells.append(cell)
    cells.append(row_cells)


    """Ce code est utilisé pour créer une grille de cellules sur le canevas en utilisant la bibliothèque Tkinter.

La variable cells est une liste de listes qui stocke les identifiants des rectangles (cellules) créés pour chaque case de la grille.

La boucle externe parcourt les rangées de la grille, tandis que la boucle interne parcourt les colonnes de la grille.

Pour chaque case de la grille, les coordonnées x1, y1, x2 et y2 sont calculées pour dessiner un rectangle de 5 pixels de large et de 5 pixels de hauteur. La couleur de remplissage de chaque rectangle est déterminée par la valeur de l'état de la case dans la liste states.

Ensuite, chaque rectangle est créé en utilisant la méthode create_rectangle de la classe Canvas de Tkinter, avec les coordonnées calculées précédemment et la couleur de remplissage correspondante. L'ID de chaque rectangle est stocké dans la liste row_cells.

Enfin, la liste row_cells est ajoutée à la liste principale cells, créant ainsi une grille de rectangles pour toutes les cases de la grille."""

# Création et ajout des boutons dans le canevas    
start_button = tk.Button(root, text="start", command=start_langtons_ant)
start_button.grid(column = 2, row = 1)

stop_button = tk.Button(root, text="stop", command=stop_langtons_ant)
stop_button.grid(column = 2, row = 2)

step_button = tk.Button(root, text="step", command=step_langtons_ant)
step_button.grid(column = 2, row = 3)

reset_button = tk.Button(root, text="reset", command=reset_langtons_ant)
reset_button.grid(column = 2, row = 4)

back_button = tk.Button(root, text="back", command=back_step_langtons_ant)
back_button.grid(column = 2, row = 5)

save_button = tk.Button(root, text="Save", command=save_state)
save_button.grid(column = 2, row = 6)

open_button = tk.Button(root, text="Open instance", command=open_instance)
open_button.grid(column = 2, row = 7)


# Fonction permettant de maintenir la fenêtre Tkinter ouverte
root.mainloop()

