import pygame
from Stub import StubClient


class GameUI(object):

    def __init__(self, stub: StubClient, grid_size: int = 40):
        # receber dimensão da grid
        dim = stub.grid_size()
        self.x_max = dim[0]
        self.y_max = dim[1]
        self.stub = stub
        # criar o ecrã
        self.width, self.height = self.x_max * grid_size, self.y_max * grid_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        # definir cores
        self.grass_color = (167, 209, 61)
        self.grid_color = (213, 255, 107)
        # definir o background
        self.grid_size = grid_size
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill(self.grass_color)
        self.screen.blit(self.background, (0, 0))
        # desenhar a grid
        self.draw_grid(self.grid_color)
        pygame.display.update()

    def draw_grid(self, color):
        for x in range(0, self.x_max):
            pygame.draw.line(self.screen, color, (x * self.grid_size, 0), (x * self.grid_size, self.height))
        for y in range(0, self.y_max):
            pygame.draw.line(self.screen, color, (0, y * self.grid_size), (self.width, y * self.grid_size))

    def run(self, stub: StubClient):
        end = False
        while end == False:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stub.end_connection()
                    end = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    stub.end_connection()
                    end = True

        return
