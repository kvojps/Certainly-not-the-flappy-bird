import pyxel
from random import random,randint,randrange

SCENE_TITLE = 0
SCENE_PLAY = 1


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

        self.x = 8
        self.y = 80
        self.vy = 0

        self.scene = SCENE_TITLE
        self.background = Background()

        self.far_cloud = [(-10, 75), (40, 65), (90, 60)]
        self.near_cloud = [(10, 25), (70, 35), (120, 15)]

        self.canos = [cano1, cano2, cano3, cano4]

        pyxel.run(self.update, self.draw)

#MECANICA DO JOGO

    def processar_entrada(self):
        if pyxel.btn(pyxel.KEY_UP):
            self.y -= 6
        self.y += self.vy
        self.vy = min(self.vy + 1, 2)

    def atualizar_canos(self):
        i = 0
        for x, y in self.canos:
            if x < -30:
                x = x + 4 * distancia_canos * 4
                y = -10 * randint(1, 10)
            self.canos[i] = x - 1, y
            i = i + 1

#ATUALIZANDO JOGO

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        self.background.update()

        if self.scene == SCENE_TITLE:
            self.update_title_scene()
        elif self.scene == SCENE_PLAY:
            self.update_play_scene()

    def update_title_scene(self):
        if pyxel.btnp(pyxel.KEY_ENTER):
            self.scene = SCENE_PLAY

    def update_play_scene(self):
        self.y = max(self.y, 2)
        self.y = min(self.y, 95)
        self.processar_entrada()
        self.atualizar_canos()

#DESENHANDO JOGO
        
    def desenhar_canos(self):
        cor = 11
        largura = 20
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

    def draw_title_scene(self):
        pyxel.text(55, 50, "Deep web bird \n \n PRESS ENTER", pyxel.frame_count % 16)

    def draw_play_scene(self):
        pyxel.cls(1)
        pyxel.blt(self.x, self.y,0,0,0,21,15,12)
        self.desenhar_canos()

        #Chao
        pyxel.blt(0, 112, 0, 0, 112, 160, 32)

        # nuvens
        offset = (pyxel.frame_count // 16) % 160
        for i in range(2):
            for x, y in self.far_cloud:
                pyxel.blt(x + i * 160 - offset, y, 0, 64, 32, 32, 8, 12)

        offset = (pyxel.frame_count // 8) % 160
        for i in range(2):
            for x, y in self.near_cloud:
                pyxel.blt(x + i * 160 - offset, y, 0, 0, 32, 56, 8, 12)



Game()
