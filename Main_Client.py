import pygame
from Stub import StubClient
from Client_UI import GameUI


def main():
    pygame.init()
    stub = StubClient()
    ui = GameUI(stub)
    ui.run(stub)


main()
