from game_object import GameObject

class Bullet(GameObject):
    def __init__(self, x, y, vy, owner):
        super().__init__(x-3, y-10, 6, 15)
        self.vy = vy
        self.owner = owner

    def update(self):
        self.y += self.vy

class Laser(GameObject):
    def __init__(self, x, y):
        super().__init__(x-2, y-10, 4, 20)
        self.vy = -15

    def update(self):
        self.y += self.vy
