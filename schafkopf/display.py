import os
import pygame


pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont(None, 50)

SUITS = {"0": "Schellen", "1": "Herz", "2": "Gras", "3": "Eichel"}
SYMBOLS = {"0": "7", "1": "8", "2": "9", "3": "U", "4": "O", "5": "K", "6": "10", "7": "A"}


class Card(pygame.sprite.Sprite):
    def __init__(self, card, face_down=False, angle=0, size=None):
        pygame.sprite.Sprite.__init__(self)
        self.card = card
        self.angle = angle
        self.size = size
        self.face_down = face_down
        file = SYMBOLS[str(card[0])] + SUITS[str(card[1])] + ".jpg"
        self.frontside = self.transform(pygame.image.load(os.path.join("images", file)).convert())
        self.backside = self.transform(pygame.image.load(os.path.join("images", "Rueckseite.jpg")).convert())
        if face_down:
            self.image = self.backside
        else:
            self.image = self.frontside
        self.rect = self.image.get_rect()
        self.in_current_trick = False

    def transform(self, image):
        if self.size is not None:
            image = pygame.transform.scale(image, self.size)
        return pygame.transform.rotate(image, self.angle)

    def turn_over(self):
        if self.face_down:
            self.image = self.frontside
            self.face_down = False
        else:
            self.image = self.backside
            self.face_down = True

class TableViewer:
    def __init__(self, screensize, game):
        self.screensize = screensize
        self.current_game = game
        self.cardsize = screensize[0] * 7 // 100, screensize[1] * 14 // 100
        self.playerlist = game.playerlist

    def prepare_hand(self, player, angle):
        hand = [Card(card, angle=angle, size=self.cardsize) for card in player.get_hand()]
        if self.playerlist.index(player) == 0:
            for card, i in zip(hand, range(8)):
                card.rect.topleft = (self.screensize[0] / 5 + i * self.screensize[0] * 75 / 1000,
                                     self.screensize[1] * (83 / 100))
        elif self.playerlist.index(player) == 1:
            for card, i in zip(hand, range(8)):
                card.rect.topleft = (self.screensize[0] * 83 / 100,
                                     self.screensize[0] / 5 + i * self.screensize[1] * 75 / 1000)
        elif self.playerlist.index(player) == 2:
            for card, i in zip(hand, range(8)):
                card.rect.topleft = (self.screensize[0] / 5 + i * self.screensize[0] * 75 / 1000,
                                     self.screensize[1] * 3 / 100)
        elif self.playerlist.index(player) == 3:
            for card, i in zip(hand, range(8)):
                card.rect.topleft = (self.screensize[0] * 3 / 100,
                                     self.screensize[0] / 5 + i * self.screensize[1] * 75 / 1000)
        return hand

    def prepare_current_trick(self):
        pos_curr_trick = [(self.screensize[0] * 465 // 1000, self.screensize[1] * 55 // 100),
                          (self.screensize[0] * 55 // 100, self.screensize[1] * 465 // 1000),
                          (self.screensize[0] * 465 // 1000, self.screensize[1] * 31 // 100),
                          (self.screensize[0] * 31 // 100, self.screensize[1] * 465 // 1000)]
        curr_trick = self.current_game.trick_game.current_trick
        curr_trick_sprites = []
        for card, i in zip(curr_trick.cards, range(4)):
            if card is not None:
                sprite = Card(card, angle=90*i, size=self.cardsize)
                sprite.rect.topleft = pos_curr_trick[i]
                curr_trick_sprites.append(sprite)
        return curr_trick_sprites

    def view_table(self):
        screensize = (700, 700)
        screen = pygame.display.set_mode(screensize)
        pygame.display.set_caption(str(self.current_game.trick_game.game_mode))
        brown = [139, 69, 19]
        screen.fill(brown)
        pygame.display.flip()

        all_cards = self.prepare_current_trick()
        for player, i in zip(self.playerlist, range(len(self.playerlist))):
            hand = self.prepare_hand(player=player, angle=i * 90)
            all_cards.append(hand)

        all_sprites = pygame.sprite.RenderPlain(all_cards)

        all_sprites.draw(screen)
        pygame.display.flip()

        running = True
        while running:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                if ev.type == pygame.MOUSEBUTTONUP:

                    self.current_game.next_action()

                    screen.fill(brown)
                    pygame.display.flip()

                    all_cards = self.prepare_current_trick()
                    for player, i in zip(self.playerlist, range(len(self.playerlist))):
                        hand = self.prepare_hand(player=player, angle=i * 90)
                        all_cards.append(hand)

                    pygame.display.set_caption("Player " + str(self.current_game.trick_game.offensive_players[0])
                                               + str(self.current_game.bidding_game.game_mode))

                    all_sprites = pygame.sprite.RenderPlain(all_cards)

                    all_sprites.draw(screen)
                    pygame.display.flip()



