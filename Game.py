# -*- coding: utf-8 -*-

import GfxRender as Gfx
#import LabyText as Laby
import CustomLaby as Laby

__author__ = 'Yoann'

"""
    Programme principal
"""


# Vérification que nous sommes dans le programme principal
if __name__ == "__main__":

    print("Lancement du jeu de labyrinthe V1.04")

    # Création du Labyrinthe
    print("1/ Création du Labyrinthe ....")
    #MonLaby = Laby.LabyText()
    MonLaby = Laby.LabyCustom()
    
    # Création du context Graphique
    print("2/ Création de l'environnement Graphique")
    LabyGfx = Gfx.GfxRender(MonLaby)

    # Ajout du premier joueur
    J1 = LabyGfx.AddUser('Yoann')
    # Affectation des touches
    J1.bindKey({"N": "<Up>", "S": "<Down>", "O": "<Left>", "E": "<Right>"})
    # Positionnement du joueur
    #   Plus tard il sera nécessaire de faire une fonction pour générer une position
    #   aléatoire possible dans le labyrinthe
    J1.x = 1
    J1.y = 1

    # Ajout du second joueur
    J2 = LabyGfx.AddUser('Inconnu', spriteFile='sprite/Hero/hero2.png')
    # Affectation des touches
    J2.bindKey({"N": "z", "S": "s", "O": "q", "E": "d"})
    J2.x = 1
    J2.y = 18

    # Première génération de l'affichage du Labyrinthe
    LabyGfx.render(0)

    # Lancement de la boucle principal (boucle graphique)
    LabyGfx.mainLoop()

