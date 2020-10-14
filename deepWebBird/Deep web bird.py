import pyxel

#direcoes da cobra
CIMA = 0
DIREITA = 1
BAIXO = 2

class Game:
  def __init__(self):
      pyxel.init(160, 120, caption="Flappy bird")
      pyxel.load("assets/jump_game.pyxres")

      self.x = pyxel.width / 4
      self.y = pyxel.height / 2

      self.direcao = DIREITA
      self.tamanho_sprite = 8
      self.far_cloud = [(-10, 75), (40, 65), (90, 60)]
      self.near_cloud = [(10, 25), (70, 35), (120, 15)]
      pyxel.run(self.update, self.draw)


  def processar_entrada(self):
      if pyxel.btn(pyxel.KEY_UP):
        self.direcao = CIMA
      elif pyxel.btn(pyxel.KEY_DOWN):
        self.direcao = BAIXO

      if pyxel.frame_count % 15 == 0:
        if self.direcao == CIMA:
            if self.y - self.tamanho_sprite < 0:
                self.y =  pyxel.height - self.tamanho_sprite
            else:
                self.y -= 8
        elif self.direcao == BAIXO:
            if self.y + self.tamanho_sprite > pyxel.height - self.tamanho_sprite:
                self.y = 0
            else:
                self.y += 8

  def update(self):
    self.processar_entrada()



  def draw(self):
      pyxel.cls(12)
      pyxel.rect(self.x, self.y, 8, 8, 10)

      # draw sky
      pyxel.blt(0, 88, 0, 0, 88, 160, 32)

      # draw mountain
      pyxel.blt(0, 88, 0, 0, 64, 160, 24, 12)

      # draw clouds
      offset = (pyxel.frame_count // 16) % 160
      for i in range(2):
          for x, y in self.far_cloud:
              pyxel.blt(x + i * 160 - offset, y, 0, 64, 32, 32, 8, 12)

      offset = (pyxel.frame_count // 8) % 160
      for i in range(2):
          for x, y in self.near_cloud:
              pyxel.blt(x + i * 160 - offset, y, 0, 0, 32, 56, 8, 12)


Game()
