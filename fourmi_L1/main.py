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





