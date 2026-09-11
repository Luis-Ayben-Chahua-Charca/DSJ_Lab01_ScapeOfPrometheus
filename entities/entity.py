class Entity:
    def __init__(self, screen, image, x, y):
        self.screen = screen
        self.image = image
        self.x = x
        self.y = y

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))
