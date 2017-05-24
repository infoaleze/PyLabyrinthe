# -*- coding: utf-8 -*-

import GfxRender as Gfx
import CustomLaby as Laby
import MonsterEngine

__author__ = 'Yoann'

"""
    Programme principal
"""


# Vérification que nous sommes dans le programme principal
if __name__ == "__main__":

    print("Lancement du jeu de labyrinthe V0.60")

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
    J1.setInitialPos(1,1)
    J1.moveToInitialPos()

    # Ajout du second joueur
    J2 = LabyGfx.AddUser('Inconnu', spriteFile='sprite/Hero/hero2.png')
    # Affectation des touches
    J2.bindKey({"N": "z", "S": "s", "O": "q", "E": "d"})
    J2.setInitialPos(1,18)
    J2.moveToInitialPos()
    
    # Ajout d'un monstre
    M1 = LabyGfx.AddMonster('AHRRR', speed=0.5)
    M1.engine = MonsterEngine.MME_Basic
    M1.setInitialPos(38,1)
    M1.moveToInitialPos()
    
    # Ajout d'un monstre
    M2 = LabyGfx.AddMonster('AHRRR2', speed=0.5, spriteFile="sprite/Hero/monster02.png")
    M2.engine = MonsterEngine.MME_Standard
    M2.setInitialPos(15,17)
    M2.moveToInitialPos()
    
    # Ajout d'un monstre
    M3 = LabyGfx.AddMonster('AHRRR3', speed=0.2, spriteFile="sprite/Hero/monster03.png")
    M3.engine = MonsterEngine.MME_Foward
    M3.setInitialPos(15,15)
    M3.moveToInitialPos()
    


    # Première génération de l'affichage du Labyrinthe
    LabyGfx.render(0)

    # Lancement de la boucle principal (boucle graphique)
    LabyGfx.mainLoop()
    
    # Nettoyage
    #LabyGfx = None
    #MonLaby = None
    

