# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw, ImageTk, ImageEnhance
import tkinter as Tk
import tkinter.ttk as ttk
import os

import time

from Entity import Player, Monster


__author__ = 'Yoann'

# *****************************************************************************
# ** Classe du context Graphique, cette classe assure la création de la      **
# ** fenêtre graphique, et la gestion de ces propriétés et dimension.        **
# *****************************************************************************

class CtxGfx():


    def __init__(self, title='Le labyrinthe oufff & Connceté! - V0.60'):


        # taille des cases du labyrinthe x/y en pixel
        self.rx = 32
        self.ry = 32
        # Nb case
        self.nx = 20
        self.ny = 20
        
        # Objets graphiques        
        self.can = None
        
        # Objets Widget
        self.playerLKP = None        # Liste Déroulante pour les joueurs
        self.selectedPlayer = None   # Variable contenant le joueur sélectioné        
        self.playerPV = None         # Zone text pour afficher les info d'un joueur


        # Message par défaut
        self._defaultMsg = title
        self._callbackID = None

        self.fenetre = Tk.Tk()
        self.fenetre.title(title)
        
        # Tableau des monstres
        self.tkMonsterBoard = None
        self.tkMonsterBoardId = None

    def construitInterface(self):
        """
        Cette fonction se charge de la construction de l'interface
        :return:
        """

        w = self.nx*self.rx
        h = self.ny*self.ry
        
        # Création de la barre des infos
        self.cInfo = Tk.Canvas(self.fenetre, width=w, height=80, bd=0, bg='black')        
        self.cInfo.pack()
        
        # Création du context graphique
        self.can = Tk.Canvas(self.fenetre, width=w, height=h, bd=0, bg='black')
        
        
        x = (w - 240) // 2
        # Création de la liste des monstres
        self.monster_cadre = self.cInfo.create_rectangle(w - 2*x, 0, w-240, 40, fill='#4F0000', width=1, outline='#FFFFFF')
        
        # Création de la boite de message
        self.msg_cadre = self.cInfo.create_rectangle(w - 2*x, 41, w-240, 80, fill='#00007F', width=1, outline='#FFFFFF')
        
        self.cInfoMsg = self.cInfo.create_text(w // 2, 60, width=w-240, fill='white', 
                             text=self._defaultMsg, justify=Tk.LEFT, font=('Courrier', 20,))
      

        # création du context graphique
        #self.can = Canvas(self.fenetre, width=600, height=600)
        self.can.pack()

    def addGUIPlayer(self, playerName):
        self.playerLKP['values'] = list(self.playerLKP['values']) + [playerName]


    # **************************************************************************
    # **  Fonctions de gestion de l'affichage des messages.                   **
    # **************************************************************************
        
    def setDefaultMsg(self, msg):
        
        self._defaultMsg = msg
        
        
    def showMessage(self, message, time=5):
        """
        Cette fonction assure l'affichage du message pendant time ms
        """                
        
        # Affiche le cadre des message        
        self.cInfo.itemconfig(self.cInfoMsg, text=message)     
        print("MSG: ",message)   
        self.msgTimeToLive = time
        

        
    def clearMessage(self):
        
        """
        Fonction appelée après n ms pour effacer le message
        """
        
        # Affiche le cadre des message        
        self.cInfo.itemconfig(self.cInfoMsg, text=self._defaultMsg)
        self.msgTimeToLive = -1
    
    def doUpdate(self,dt, LabyObj):
        """
        Fonction assurant la mise à jour de l'interface
        """        
        
        # Gestion des messages
        if self.msgTimeToLive > 0:
            self.msgTimeToLive -= dt
            if self.msgTimeToLive <= 0:
                if LabyObj.countMessage() == 0:
                    self.clearMessage()
            elif (self.msgTimeToLive > 2) and (LabyObj.countMessage() > 0):
                self.msgTimeToLive = 2
        else:
            (m,t) = LabyObj.popMessage()
            if m is not None:
                self.showMessage(m,t)
                
                
    # **************************************************************************
    # **  Fonctions de gestion de l'affichage des montres.                    **
    # **************************************************************************
    
    def doMonsterStatus(self, MonsterList):
        """
        Fonction assurant l'affichage de l'état des monstres
        """
        
        # Si pas de changement exit direct
        if not(MonsterList.hasUpdate): return None
        
        print("CtxGfx::doMonsterStatus >> Doing")
        MonsterList.hasUpdate = False
        
        w = self.nx*self.rx
        
        nb_total = len(MonsterList.ActiveMonsterList) + len(MonsterList.InActiveMonsterList)
        
        w_monster = nb_total * (self.rx + 2)
        
        x_offset = (self.nx*self.rx - w_monster) // 2
        
        # Création du tableau des monstres
        
        monsterBoard = Image.new('RGBA',(w_monster, 40), (0,0,255,0)) 
                
        k = 0
        for m in MonsterList.ActiveMonsterList:            
            monsterBoard.paste(m.Sprite,(k*(self.rx + 2), 4))
            k = k+1
    
        for m in MonsterList.InActiveMonsterList:
            tmpSprite = ImageEnhance.Color(m.Sprite)
            monsterBoard.paste(tmpSprite.enhance(0.0),(k*(self.rx + 2), 4))
            k = k+1
          
        self.cInfo.delete(self.tkMonsterBoard) 
        self.cInfo.delete(self.tkMonsterBoardId) 
        self.tkMonsterBoard = ImageTk.PhotoImage(image=monsterBoard,  master=self.cInfo)
        self.tkMonsterBoardId = self.cInfo.create_image(x_offset, 0, anchor=Tk.NW, image=self.tkMonsterBoard, state= Tk.NORMAL)
        
    
    
# *****************************************************************************
# ** Classe dérivant du Player pour introduire les spécificité de l'affichage**
# ** en mode graphique.                                                      **
# *****************************************************************************

class GfxPlayer(Player):

    """
       Cette classe dérive de la classe Player afin de définir
       les methode et propriété pour l'affichage d'un joueur
       en mode graphique
    """

    def __init__(self, ctxGfx, initPv=100, spriteFile='sprite/Hero/hero.png'):
        """
        Fonction d'initialisation du Player mode Graphique
        :param gfxCtx: Context TK
        :param initPv: Point de vie Initial
        :param spriteFile: Fichier image représantant le joueur
        :return: NA
        """

        # Référence sur context graphique
        self._ctxGfx = ctxGfx

        Player.__init__(self,initPv)

        # Contient le sprite du joueur
        # self.Sprite = Tk.PhotoImage(file=spriteFile, master=self._ctxGfx.fenetre)
        self.Sprite = Image.open(spriteFile)
        self._img = None

        # Déclanche l'affichage
        self._hasChanged = True

    def __str__(self):
        """ Methode appelée lorsque que l'on utilise la fonction print() """
        return "P[{0} PV:{1}]".format(self.Name, self.PV)

    def bindKey(self, listKey):
        """
        :param listKey: Liste nommé des touche : { "N":"<Up>", "S":"<Down>", "O":"<Left>", "E":"<Right>" }
        :return: True/False
        """

        if self._ctxGfx is None:
            print("GfxPlayer:bindKey : Erreur pas de context graphique")
            return False

        # Ici, nous parcourrons le dictionaire pour associer les touches de dépalcement
        for k, i in listKey.items():
            self._ctxGfx.fenetre.bind(i, lambda event, o=self, ky=k: o.move(ky))

        return True

    def render(self, t):
        """
        Fonction assurant l'affichage du player
        :param t:
        :return:
        """

        if not self._hasChanged:
            return None

        if self._img is None:            
            self.tkSprite = ImageTk.PhotoImage(image=self.Sprite, master=self._ctxGfx.can)
            self._img = self._ctxGfx.can.create_image(self.x*self._ctxGfx.ry, self.y*self._ctxGfx.ry, anchor=Tk.NW,
                                                      image=self.tkSprite, tag='sprite')
        else:
            self._ctxGfx.can.coords(self._img, self.x*self._ctxGfx.ry, self.y*self._ctxGfx.ry)
            self._ctxGfx.can.tag_raise(self._img) 

        self._hasChanged = False

        return None

# *****************************************************************************
# ** Classe dérivant du Monster pour introduire les spécificités de          **
# ** l'affichage en mode graphique.                                          **
# *****************************************************************************

class GfxMonster(Monster):

    """
       Cette classe dérive de la classe Player afin de définir
       les methode et propriété pour l'affichage d'un joueur
       en mode graphique
    """

    def __init__(self, ctxGfx, speed=1000, initPv=100, spriteFile='sprite/Hero/monster.png'):
        """
        Fonction d'initialisation du Player mode Graphique
        :param gfxCtx: Context TK
        :param initPv: Point de vie Initial
        :param spriteFile: Fichier image représantant le joueur
        :return: NA
        """

        # Référence sur context graphique
        self._ctxGfx = ctxGfx

        Monster.__init__(self,speed,initPv)

        # Contient le sprite du joueur
        self.Sprite = Image.open(spriteFile)
        self._img = None

        # Déclanche l'affichage
        self._hasChanged = True
        

    def __str__(self):
        """ Methode appelée lorsque que l'on utilise la fonction print() """
        return "M[{0} PV:{1}]".format(self.Name, self.PV)


    def render(self, t):
        """
        Fonction assurant l'affichage du player
        :param t:
        :return:
        """

        if not self._hasChanged:
            return None

        if self._img is None:
            self.tkSprite = ImageTk.PhotoImage(image=self.Sprite, master=self._ctxGfx.can)
            if self.isVisible:               
                self._img = self._ctxGfx.can.create_image(self.x*self._ctxGfx.ry, self.y*self._ctxGfx.ry, anchor=Tk.NW,
                                                      image=self.tkSprite, tag='sprite')
            else:
                self._img = self._ctxGfx.can.create_image(self.x*self._ctxGfx.ry, self.y*self._ctxGfx.ry, anchor=Tk.NW,
                                                      image=self.tkSprite, tag='sprite', state=Tk.HIDDEN)
                            
        else:
            if self.isVisible:
                self._ctxGfx.can.itemconfig(self._img, state=Tk.NORMAL) 
            else:
                self._ctxGfx.can.itemconfig(self._img, state=Tk.HIDDEN) 
            
            self._ctxGfx.can.coords(self._img, self.x*self._ctxGfx.ry, self.y*self._ctxGfx.ry)
            self._ctxGfx.can.tag_raise(self._img) 
            

        self._hasChanged = False

        return None
        
    def kill(self):
        
        #print("GfxMonster::kill:tagList:",self._ctxGfx.can.find_all())
        if self._img is not None:
            self._ctxGfx.can.delete(self._img)
            self._img = None
        
        #self._ctxGfx.can.delete(self.Sprite)
        #self.Sprite = None
        
        # Appel de la fonction héritée
        Monster.kill(self)
        
        #print("GfxMonster::kill:tagList AFTER:",self._ctxGfx.can.find_all())

# **************************************************************************
# ** Classe qui s'occupe de la génération graphique du Labyrinthe         **
# **************************************************************************
class GfxRender():

    def __init__(self, laby, monsterList):
        
         
        # Initialisation du callback de mise à jour des IA
        self._OnUpdateCbk = None
        
        # Initialisation des variables locales
        self.photo_wall_list = []   # Liste des images de mur
        self.photo_asset_list= []   # Liste des images d'objet
        self.photo_shadow_list=[]   # Liste des ombres
        self.photo_error = None     # Image Erreur

        self.plateau     = None     # Pillow image pour traitement rapide
        self.mapFx       = None
        self.tkPlateau   = None     # Objet Image tk
        self.tkPlateauId = None     # Id de l'objet tk        

        # Mémorisation de la référence sur l'objet de type Laby
        self._Map = laby
        self._MonsterList = monsterList

        # Création du context Graphique
        self._ctxGfx = CtxGfx()
        self._ctxGfx.nx = self._Map.LX
        self._ctxGfx.ny = self._Map.LY
        self._ctxGfx.construitInterface()


        # Initialisation des ressources grafiques
        self._initGfx()
        

        # point référence temps
        self._lastTime  = time.time()
        

    def _initGfx(self):
        
        self.photo_error = Image.open("sprite/Std/ErrorTile.png")
        self.photo_back  = Image.open("sprite/"+self._Map.Theme +"/background.png")
        
        # Extraction des images mur
        photo_set = Image.open("sprite/"+self._Map.Theme +"/walls.png")
        for i in range(0,16) :
            img = photo_set.crop((i*self._ctxGfx.rx, 0, (i+1)*self._ctxGfx.rx, self._ctxGfx.ry))
            img.load()
            self.photo_wall_list.append(img)
            
            
        # Extraction des objets
        photo_set = Image.open("sprite/"+self._Map.Theme +"/assets.png")
        (w,h) = photo_set.size
        for i in range(0,w // self._ctxGfx.rx) :
            img = photo_set.crop((i*self._ctxGfx.rx, 0, (i+1)*self._ctxGfx.rx, self._ctxGfx.ry))
            img.load()
            self.photo_asset_list.append(img)     
            
        # Extraction des ombres        
        photo_set = Image.open("sprite/"+self._Map.Theme +"/shadows.png")
        (w,h) = photo_set.size
        for i in range(0,w // self._ctxGfx.rx) :
            img = photo_set.crop((i*self._ctxGfx.rx, 0, (i+1)*self._ctxGfx.rx, self._ctxGfx.ry))
            img.load()
            self.photo_shadow_list.append(img)    
           

    def mainLoop(self):
        
        # Association de la call back Graphique
        self._ctxGfx.fenetre.after(1000, self.onUpdate)
        
        self._ctxGfx.fenetre.mainloop()


    def AddUser(self, playerName, pv=100, spriteFile='sprite/Hero/hero.png'):
        """
            Créer et Ajoute un joueur dans le labyrinthe
        :param player: GfxPlayer
        :return: None
        """

        if self._ctxGfx is None:
            print("GfxRender:AddUser : Pas de context graphique initialisé !")
            return None

        #try:
        # Création du nouveau joueur (et de son contexte graphique)
        p = GfxPlayer(self._ctxGfx, initPv=pv, spriteFile=spriteFile)
        p.Name = playerName
        
        # Ajout dans la liste des joueurs
        self._Map.addPlayer(p)            

        return p
        #except e:
        #    return None
            
            
    def AddMonster(self, monsterName, speed=2, pv=5000, spriteFile='sprite/Hero/monster.png'):
        """
            Créer et Ajoute un monstre dans le labyrinthe
        :param 
        :return: None
        """

        if self._ctxGfx is None:
            print("GfxRender::AddMonster : Pas de context graphique initialisé !")
            return None

        try:
            # Création du nouveau joueur (et de son contexte graphique)
            p = GfxMonster(self._ctxGfx, speed, initPv=pv, spriteFile=spriteFile)
            p.Name = monsterName
            
            # Ajout dans la liste des joueurs
            self._MonsterList.addMonster(p)
            
            return p
        except e:
            return None




    def renderMap(self):
        """
            Cette fonction s'occupe de la génération de l'image graphique
            Pour le moment elle intègre que la mise à jour du Laby et des Perso
        :return: None
        """
                
         
        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        # %% Génération deu Labyrinthe %%
        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        # Dessine le fond
        
        self._ctxGfx.setDefaultMsg(self._Map.NomLaby)
        self._ctxGfx.showMessage('Bienvenu dans')
        

        self.plateau = Image.new('RGBA',(self._ctxGfx.nx * self._ctxGfx.rx, self._ctxGfx.ny * self._ctxGfx.ry), (255,255,255,255))
        
        (bw,bh) = self.photo_back.size

        (nbx, r) = divmod(self._ctxGfx.nx * self._ctxGfx.rx, bw)
        if r > 0: nbx += 1
        
        (nby, r) = divmod(self._ctxGfx.ny * self._ctxGfx.ry,bh)
        if r > 0: nby += 1
        
        for y in range(0,nby):
            for x in range(0,nbx):
                self.plateau.paste(self.photo_back,(x*bw, y*bh))                


        # Génération des murs

        # Pour chaque ligne du Labyrinthe
        for ly in range(0,self._ctxGfx.ny):

            # Pour chaque colonne du Labyrinthe
            for lx in range(0,self._ctxGfx.nx):

                # Est ce un Mur ?
                code = self._Map.Carte[ly * self._Map.LX + lx] & 0x0F
                
                #print("render::code (lx,ly) = (",lx, ",", ly, ")", code)
                if code != 0:
                    self.plateau.paste(self.photo_wall_list[code],(lx*self._ctxGfx.ry, ly*self._ctxGfx.ry))                
                            

    def renderFx(self, dt):
        """
        Fonction qui générent les modifications graphiques au dessus de la map  
        pour l'affichage des effets (porte, trésor, etc...)
        """
        
        if self.mapFx is None:
            self.mapFx = Image.new('RGBA',(self._ctxGfx.nx * self._ctxGfx.rx, self._ctxGfx.ny * self._ctxGfx.ry), (0,0,255,0))
        
        for k in self._Map.FXList:
            self._Map.FXList[k].renderFx(self, dt)
            
    def addFxTile(self,x,y,tileId):
        """
        Cette fonction est appelée par la classe LabyTextFx lors de la mise
        à jour graphique.
        """
        
        if tileId > len(self.photo_asset_list)-1:
            self.mapFx.paste(self.photo_error,(x*self._ctxGfx.ry, y*self._ctxGfx.ry))   
        else:
            self.mapFx.paste(self.photo_asset_list[tileId],(x*self._ctxGfx.ry, y*self._ctxGfx.ry))   
                
        return None

    def renderShadow(self):
        
        self.mapShadow = Image.new('RGBA',(self._ctxGfx.nx * self._ctxGfx.rx, self._ctxGfx.ny * self._ctxGfx.ry), (255,255,255,0))
        
        for x in range(0,self._ctxGfx.nx):
            for y in range(0,self._ctxGfx.ny):
                code = (self._Map.Carte[y * self._Map.LX + x] & 0xF0) >> 4
                code = code & 0x0F
                if code != 0x0F:
                    self.mapShadow.paste(self.photo_shadow_list[code],(x*self._ctxGfx.ry, y*self._ctxGfx.ry))
                
                
        
    def render(self, dt):
        """
        Fonction qui assure le mix des map pour générer l'image final
        """
        
        #self.mapFinal = Image.new('RGBA',(self._ctxGfx.nx * self._ctxGfx.rx, self._ctxGfx.ny * self._ctxGfx.ry), (0,0,0,255))
        
        # Vérifie si le plateau de base a été généré
        if self.plateau is None : self.renderMap()
        
        # calcule la couche dynamique (basé sur l'état des effets)
        self.renderFx(dt)
        
        self.mapFinal = Image.alpha_composite(self.plateau,self.mapFx)
        
        # Calcul l'éclairage
        if self._Map.IsShadowEnabled == True:            
            self.renderShadow()
            self.mapFinal = Image.alpha_composite(self.mapFinal,self.mapShadow)
                      
        
        # dump vers Tk
        #OldTkId = self.tkPlateauId
        
        
        self._ctxGfx.can.delete(self.tkPlateau) 
        self._ctxGfx.can.delete(self.tkPlateauId) 
        self.tkPlateau = ImageTk.PhotoImage(image=self.mapFinal,  master=self._ctxGfx.fenetre)
        self.tkPlateauId = self._ctxGfx.can.create_image(0, 0, anchor=Tk.NW, image=self.tkPlateau, state= Tk.NORMAL)
        self._ctxGfx.can.tag_lower(self.tkPlateauId) 
        
        
        
        
        
        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        # %% Affichage des Persos      %%
        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        # Pour chaque perso
        for p in self._Map.PlayerList:
            p.render(dt)
            
        # Pour chaque monstre
        for p in self._MonsterList.ActiveMonsterList:
            p.render(dt)
        

    def onUpdate(self):
        """
            Fonction appeler régulièrement pour mettre à jour la position des joueurs
        :return:
        """

        # Récupère le point temps
        cur = time.time()
        # Calcule la différence
        dt = cur - self._lastTime


        # Mise à jour de l'interface
        self._ctxGfx.doUpdate(dt, self._Map)

        # Mise à jour des positions des monstres
        self._MonsterList.updateMonster(dt)
        
        self._ctxGfx.doMonsterStatus(self._MonsterList)
        
        # Appel du callback pour MAj de l'IA...
        try:
            self._OnUpdateCbk(dt)
        except:
            pass
        
        self.render(dt)


        # Mise à jour de la référence temporelle
        self._lastTime  = cur

        # Association de la call back Graphique
        self._ctxGfx.fenetre.after(50, self.onUpdate)
