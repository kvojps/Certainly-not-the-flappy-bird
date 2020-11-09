import pyxel
from random import random,randint,randrange

SCENE_TITLE = 0
SCENE_PLAY = 1
SCENE_GAMEOVER = 2


STAR_COUNT = 100
STAR_COLOR_HIGH = 12
STAR_COLOR_LOW = 5

largura_tela = 160
distancia_canos = 70
cano1 = largura_tela + distancia_canos * 0, -10 * randint(1, 10)
cano2 = largura_tela + distancia_canos * 1, -10 * randint(1, 10)
cano3 = largura_tela + distancia_canos * 2, -10 * randint(1, 10)
cano4 = largura_tela + distancia_canos * 3, -10 * randint(1, 10)

#Tela inicial
class Background:
    def __init__(self):
        self.star_list = []
        for i in range(STAR_COUNT):
            self.star_list.append(
                (random() * pyxel.width, random() * pyxel.height, random() * 1.5 + 1)
            )

    def update(self):
        for i, (x, y, speed) in enumerate(self.star_list):
            y += speed
            if y >= pyxel.height:
                y -= pyxel.height
            self.star_list[i] = (x, y, speed)

    def draw(self):
        for (x, y, speed) in self.star_list:
            pyxel.pset(x, y, STAR_COLOR_HIGH if speed > 1.8 else STAR_COLOR_LOW)


class Game:
    def __init__(self):
        pyxel.init(160, 120, caption="Deep web bird")
        pyxel.load("assets/game.pyxres")

        self.player_x = 8
        self.player_y = 30
        self.player_vy = 0

        self.scene = SCENE_TITLE
        self.background = Background()

        self.far_cloud = [(-10, 75), (40, 65), (90, 60)]
        self.near_cloud = [(10, 25), (70, 35), (120, 15)]

        self.canos = [cano1, cano2, cano3, cano4]
        
        self.score = 0

        pyxel.run(self.update, self.draw)

#MECANICA DO JOGO

    def processar_entrada(self):
        if pyxel.btn(pyxel.KEY_UP):
            self.player_y -= 6
        self.player_y += self.player_vy
        self.player_vy = min(self.player_vy + 1, 2)

    def atualizar_canos(self):
        i = 0
        for x, y in self.canos:
            if x < -30:
                x = x + 1 * distancia_canos * 4
                y = -10 * randint(1, 10)
            self.canos[i] = x - 1, y
            i = i + 1
    
    def atualizar_colisoes(self):
        abertura_cano = 125
        if self.player_y > 95:
            self.scene = SCENE_GAMEOVER
        for x, y in self.canos:
            colide_x = self.player_x + 20  > x and  self.player_x  <  x + 20
            colide_y = self.player_y < y + 85  or self.player_y + 15 > y + abertura_cano
            
            if colide_x and colide_y:
                self.scene = SCENE_GAMEOVER
    
    def atualizar_score(self):
        for x,y in self.canos:
            if self.player_x == x :
                self.score += 1


#ATUALIZANDO JOGO

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        self.background.update()
        if self.scene == SCENE_TITLE:
            self.update_title_scene()
        elif self.scene == SCENE_PLAY:
            self.update_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.update_gameover_scene()

    def update_title_scene(self):
        if pyxel.btnp(pyxel.KEY_ENTER):
            self.scene = SCENE_PLAY

    def update_play_scene(self):
        self.atualizar_colisoes()
        self.player_y = max(self.player_y, 2)
        self.player_y = min(self.player_y, 95)
        self.processar_entrada()
        self.atualizar_canos()
        self.atualizar_score()

    def update_gameover_scene(self):
        if pyxel.btnp(pyxel.KEY_ENTER):
            self.scene = SCENE_PLAY
            self.player_x = 8
            self.player_y = 30
            self.canos = [cano1,cano2,cano3,cano4]
            self.score = 0
            

#DESENHANDO JOGO
        
    def desenhar_canos(self):
        cor = 11
        largura = 15
        altura = 85
        abertura_cano = 125
        for x, y in self.canos:
            pyxel.rect(x, y, largura, altura, cor)
            pyxel.rect(x, y + abertura_cano, largura, altura, cor)

    def draw(self):
        pyxel.cls(0)
        self.background.draw()

        if self.scene == SCENE_TITLE:
            self.draw_title_scene()
        elif self.scene == SCENE_PLAY:
            self.draw_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.draw_gameover_scene()

    def draw_title_scene(self):
        pyxel.text(55, 50, "Deep web bird \n \n PRESS ENTER", pyxel.frame_count % 16)

    def draw_play_scene(self):
        pyxel.cls(1)
        pyxel.blt(self.player_x, self.player_y,0,0,0,21,15,12)
        self.desenhar_canos()

        #Chao
        pyxel.blt(0, 113, 0, 0, 113, 160, 32)

        # nuvens
        offset = (pyxel.frame_count // 16) % 160
        for i in range(2):
            for x, y in self.far_cloud:
                pyxel.blt(x + i * 160 - offset, y, 0, 64, 32, 32, 8, 12)

        offset = (pyxel.frame_count // 8) % 160
        for i in range(2):
            for x, y in self.near_cloud:
                pyxel.blt(x + i * 160 - offset, y, 0, 0, 32, 56, 8, 12)

    def draw_gameover_scene(self):
        pyxel.cls(0)
        pyxel.text(50, 30, f"  SCORE =  {self.score}", 7)
        pyxel.text(52, 50, "  GAME OVER \n \n PRESS ENTER", pyxel.frame_count % 16)
        



Game()
