import pygame
from network import Network


class Player():

    def __init__(self, startx, starty, color):
        self.x = startx
        self.y = starty
        self.width = self.height = 50
        self.velocity = 2
        self.current_x_velocity = 0
        self.current_y_velocity = 0
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def move(self):

        self.x += self.current_x_velocity
        self.y += self.current_y_velocity

        if self.x <= 0:
            self.x = 0
        elif self.x >= 1000 - self.width:
            self.x = 1000 - self.width

        if self.y <= 0:
            self.y = 0
        elif self.y >= 1000 - self.height:
            self.y = 1000 - self.height

    def detect_collision(self, walls):

        for wall in walls:
            if wall.x - self.width < self.x < wall.x + wall.width and \
                    wall.y - self.height < self.y < wall.y + wall.height:

                if self.current_x_velocity > 0:
                    self.x = wall.x - self.height
                elif self.current_x_velocity < 0:
                    self.x = wall.x + wall.width
                elif self.current_y_velocity > 0:
                    self.y = wall.y - self.height
                elif self.current_y_velocity < 0:
                    self.y = wall.y + wall.height


class Game:

    def __init__(self, w, h):
        self.net = Network()
        self.width = w
        self.height = h
        self.player = Player(50, 50, (0, 128, 0))
        self.player2 = Player(900, 900, (255, 0, 0))
        #self.walls = [Wall(25, 0, 8, 1000, (0, 0, 0)), Wall(37, 0, 8, 1000, (0, 0, 0)),
        #              Wall(955, 0, 8, 1000, (0, 0, 0)), Wall(967, 0, 8, 1000, (0, 0, 0)),
        #              Wall(0, 25, 1000, 8, (0, 0, 0)), Wall(0, 37, 1000, 8, (0, 0, 0)),
        #              Wall(0, 955, 1000, 8, (0, 0, 0)), Wall(0, 967, 1000, 8, (0, 0, 0)),
        #              Wall(105, 100, 10, 400, (0, 0, 0))
        #              ]
        self.canvas = Canvas(self.width, self.height, "NorseMan")

    def run(self):
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.K_ESCAPE:
                    run = False

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_w:
                        if self.player.y >= self.player.velocity:
                            self.player.current_x_velocity = 0
                            self.player.current_y_velocity = self.player.velocity * -1
                    if event.key == pygame.K_a:
                        if self.player.x >= self.player.velocity:
                            self.player.current_y_velocity = 0
                            self.player.current_x_velocity = self.player.velocity * -1

                    if event.key == pygame.K_s:
                        if self.player.y <= self.height - self.player.velocity:
                            self.player.current_x_velocity = 0
                            self.player.current_y_velocity = self.player.velocity

                    if event.key == pygame.K_d:
                        if self.player.x <= self.width - self.player.velocity:
                            self.player.current_y_velocity = 0
                            self.player.current_x_velocity = self.player.velocity

            self.player.move()
            self.player.detect_collision(self.walls)

            self.player2.x, self.player2.y = self.parse_data(self.send_data())

            self.canvas.draw_background()
            for i in range(0, len(self.walls)):
                self.walls[i].draw(self.canvas.get_canvas())
            self.player2.draw(self.canvas.get_canvas())
            self.player.draw(self.canvas.get_canvas())
            self.canvas.update()

        pygame.quit()

    def send_data(self):
        data = str(self.net.id) + ":" + str(self.player.x) + "," + str(self.player.y)
        reply = self.net.send(data)
        return reply

    @staticmethod
    def parse_data(data):
        try:
            d = data.split(":")[1].split(",")
            return int(d[0]), int(d[1])
        except:
            return 0, 0


class Canvas:

    def __init__(self, w, h, name="None"):
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((w, h))
        pygame.display.set_caption(name)

    @staticmethod
    def update():
        pygame.display.update()

    def draw_text(self, text, size, x, y):
        pygame.font.init()
        font = pygame.font.SysFont("calibri", size)
        render = font.render(text, 1, (0, 0, 0))

        self.screen.draw(render, (x, y))

    def get_canvas(self):
        return self.screen

    def draw_background(self):
        self.screen.fill((255, 255, 255))


class Wall:

    def __init__(self, x, y, width, height, colour=(0, 0, 0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height), 0)
