from game_object import GameObject

class Enemy(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 36, 24)

    def update(self, vx):
        self.x += vx
