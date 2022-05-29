from pygame import *
import pygame
from game import Game


# Main
if __name__ == '__main__':
    pygame.init()
    game = Game()
    game.run()