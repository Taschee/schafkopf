from schafkopf.suits import BELLS, ACORNS, HEARTS, LEAVES

# Game modes are given by a tuple (game_type, suit). NO_GAME and WENZ don't require a suit.
# Examples: (0, None) for no game, (3, 1) for (SOLO, HEARTS), (1, 2) for partner mode with the (ACE, LEAVES)

NO_GAME = 0
PARTNER_MODE = 1
WENZ = 2
SOLO = 3
GAME_MODES = [(NO_GAME, None), (PARTNER_MODE, BELLS), (PARTNER_MODE, LEAVES), (PARTNER_MODE, ACORNS),
              (WENZ, None), (SOLO, BELLS), (SOLO, HEARTS), (SOLO, LEAVES), (SOLO, ACORNS)]
