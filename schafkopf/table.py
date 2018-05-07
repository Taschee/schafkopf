#!/usr/bin/env python3

import pygame
from schafkopf.players import RandomPlayer
from schafkopf.game import Game
pygame.init()

SCREENSIZE = (800, 800)
locs_player1 = [(200 + i*50, 600) for i in range(8)]
locs_player2 = [(600, 200 + i*50) for i in range(8)]
locs_player3 = [(200 + i*50, 0) for i in range(8)]
locs_player4 = [(0, 200 + i*50) for i in range(8)]


Alfons = RandomPlayer(name="Alfons")
Bertl = RandomPlayer(name="Bertha")
Chrissie = RandomPlayer(name="Chris")
Dora = RandomPlayer(name="Dora")
playerlist = [Alfons, Bertl, Chrissie, Dora]

suit_dict = {"0": "Schellen", "1":"Herz", "2": "Gras", "3":"Eichel"}
symbol_dict = {"0": "7", "1": "8", "2": "9", "3": "U", "4": "O", "5": "K", "6": "10", "7": "A"}

game = Game(players=playerlist, leading_player_index=0)

game.decide_game_mode()


def main():

    screen = pygame.display.set_mode(SCREENSIZE)
    pygame.display.set_caption('Schafkopf!')

    brown = [139, 69, 19]
    screen.fill(brown)
    pygame.display.flip()

    running = True
    while running:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                running = False
                pygame.quit()

if __name__=="__main__":
    main()
