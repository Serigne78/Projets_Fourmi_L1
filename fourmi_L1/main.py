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
        