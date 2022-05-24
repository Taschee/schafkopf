import pygame

from schafkopf.pygame_gui.NextGameButton import NextGameButton
from schafkopf.pygame_gui.PlayerCard import PlayerCard
from schafkopf.pygame_gui.SchafkopfGame import SchafkopfGame
from schafkopf.pygame_gui.colors import BLACK
from schafkopf.ranks import OBER
from schafkopf.suits import ACORNS

pygame.init()
FONT = pygame.font.Font(None, 30)

clock = pygame.time.Clock()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_size = screen_width, screen_height = screen.get_size()
background = pygame.transform.scale(pygame.image.load("../images/wood.jpg").convert(), screen_size)


class Game:
    def __init__(self):
        self.leading_player_index = 0
        self.schafkopf_game = SchafkopfGame(leading_player_index=self.leading_player_index)
        self.buttons = self.get_buttons()
        self.done = False

    def next_game(self):
        self.leading_player_index += 1
        self.schafkopf_game = SchafkopfGame(self.leading_player_index)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.done = True

            for button in self.buttons:
                button.handle_event(event)

    def draw(self):
        screen.blit(background, (0, 0))
        for b in self.buttons:
            b.draw(screen)

        txt = FONT.render(str(self.schafkopf_game.game_state), True, BLACK)
        screen.blit(txt, (0, 206))

        pygame.display.flip()

    def get_buttons(self):
        return [
            NextGameButton((0, 0), self.next_game),
            PlayerCard((100, 100), (OBER, ACORNS), self.foo((OBER, ACORNS)))
        ]

    def foo(self, b):
        return lambda: print(b)

    def run(self):
        while not self.done:
            self.handle_events()
            self.draw()
            clock.tick(30)



if __name__ == "__main__":
    Game().run()
    pygame.quit()
