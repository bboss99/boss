import blf

class HudText():
    def __init__(
            self,
            texts,
            pos = (0,0),
            space = 30,
            direction = 'up',
            color = (1, 1, 1, 1),
            font_size = 15,
            font_id = 0
    ):
        self.texts = texts
        self.pos = pos
        self.space = space
        self.direction = direction
        self.color = color
        self.font_size = font_size
        self.font_id = font_id

    def draw(self):
        blf.size(self.font_id,self.font_size,72) 
        blf.color(self.font_id,*self.color)
        if self.direction == 'down':
            self.space = -self.space
        for i, text in enumerate(self.texts):
            blf.position(self.font_id, self.pos[0], self.pos[1] + self.space * i, 0)
            blf.draw(self.font_id, text)

msgType = {
    0: {'INFO'},
    1: {'WARNING'},
    2: {'ERROR'}
}

