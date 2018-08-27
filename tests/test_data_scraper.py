import pytest
from schafkopf.players.data_scraper import DataScraper
from schafkopf.game_modes import PARTNER_MODE, SOLO, WENZ, NO_GAME
from schafkopf.suits import ACORNS, LEAVES, HEARTS, BELLS
from schafkopf.ranks import SEVEN, EIGHT, NINE, TEN, KING, UNTER, OBER, ACE


def test_scraping():
    s = DataScraper()
    html = s.get_html(game_number=846389616)
    soup_partnermode = s.get_soup(html)
    assert s.scrape_game_mode(soup_partnermode) == (PARTNER_MODE, LEAVES)
    assert s.find_declaring_player_name(soup_partnermode) == 'taschee'
    assert s.scrape_declaring_player_index(soup_partnermode) == 2
    assert s.scrape_player_hands(soup_partnermode) == [[(3, 2), (7, 1), (5, 1), (1, 3), (7, 2), (0, 2), (7, 0), (0, 0)],
                                                       [(4, 2), (4, 0), (1, 1), (0, 1), (6, 3), (2, 3), (6, 2), (5, 0)],
                                                       [(4, 3), (4, 1), (3, 0), (2, 1), (7, 3), (5, 2), (6, 0), (2, 0)],
                                                       [(3, 3), (3, 1), (6, 1), (5, 3), (0, 3), (2, 2), (1, 2), (1, 0)]]
    assert s.get_player_names(soup_partnermode) == ['yyxcx', 'Vollpfo5ten', 'taschee', 'lutz_the_machine']
    assert s.scrape_played_cards(soup_partnermode) == [((UNTER, LEAVES), 0), ((OBER, BELLS), 1),
                                                       ((OBER, HEARTS), 2), ((UNTER, HEARTS), 3),
                                                       ((OBER, ACORNS), 2), ((TEN, HEARTS), 3),
                                                       ((ACE, HEARTS), 0), ((SEVEN, HEARTS), 1),
                                                       ((NINE, HEARTS), 2), ((UNTER, ACORNS), 3),
                                                       ((KING, HEARTS), 0), ((EIGHT, HEARTS), 1),
                                                       ((NINE, LEAVES), 3), ((ACE, LEAVES), 0),
                                                       ((TEN, LEAVES), 1), ((KING, LEAVES), 2),
                                                       ((ACE, BELLS), 0), ((KING, BELLS), 1),
                                                       ((TEN, BELLS), 2), ((EIGHT, BELLS), 3),
                                                       ((SEVEN, LEAVES), 0), ((NINE, ACORNS), 1),
                                                       ((NINE, BELLS), 2), ((EIGHT, LEAVES), 3),
                                                       ((SEVEN, ACORNS), 3), ((EIGHT, ACORNS), 0),
                                                       ((TEN, ACORNS), 1), ((ACE, ACORNS), 2),
                                                       ((UNTER, BELLS), 2), ((KING, ACORNS), 3),
                                                       ((SEVEN, BELLS), 0), ((OBER, LEAVES), 1)]


