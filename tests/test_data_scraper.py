from schafkopf.game_modes import PARTNER_MODE, SOLO, WENZ
from schafkopf.players.data.data_scraper import DataScraper
from schafkopf.ranks import SEVEN, EIGHT, NINE, TEN, KING, UNTER, OBER, ACE
from schafkopf.suits import ACORNS, LEAVES, HEARTS, BELLS
import pytest


with open('login_data.txt') as f:
    username = f.readline().translate({ord(char): None for char in ' \n'})
    password = f.readline().translate({ord(char): None for char in ' \n'})

s = DataScraper()
driver = s.login_to_sauspiel(username, password)


def test_scraping_partnermode():
    html = s.get_html(game_number=846389616, driver=driver)
    soup_partnermode = s.get_soup(html)
    assert s.game_with_eight_cards(html)
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


def test_scraping_solo():
    html = s.get_html(game_number=846389389, driver=driver)
    soup_solo = s.get_soup(html)
    assert s.game_with_eight_cards(html)
    assert s.scrape_game_mode(soup_solo) == (SOLO, LEAVES)
    assert s.find_declaring_player_name(soup_solo) == 'taschee'
    assert s.scrape_declaring_player_index(soup_solo) == 3
    assert s.scrape_player_hands(soup_solo) == [[(OBER, BELLS), (UNTER, BELLS), (TEN, LEAVES), (TEN, ACORNS),
                                                 (TEN, HEARTS), (KING, HEARTS), (EIGHT, BELLS), (SEVEN, BELLS)],
                                                [(OBER, HEARTS), (UNTER, ACORNS), (NINE, LEAVES), (EIGHT, LEAVES),
                                                 (ACE, ACORNS), (SEVEN, ACORNS), (NINE, HEARTS), (SEVEN, HEARTS)],
                                                [(KING, ACORNS), (NINE, ACORNS), (EIGHT, ACORNS), (ACE, HEARTS),
                                                 (EIGHT, HEARTS), (ACE, BELLS), (TEN, BELLS), (NINE, BELLS)],
                                                [(OBER, ACORNS), (OBER, LEAVES), (UNTER, LEAVES), (UNTER, HEARTS),
                                                 (ACE, LEAVES), (KING, LEAVES), (SEVEN, LEAVES), (KING, BELLS)]]
    assert s.get_player_names(soup_solo) == ['lutz_the_machine', 'yyxcx', 'dichtls', 'taschee']
    assert s.scrape_played_cards(soup_solo) == [((SEVEN, BELLS), 0), ((SEVEN, HEARTS), 1),
                                                ((TEN, BELLS), 2), ((KING, BELLS), 3),
                                                ((ACE, BELLS), 2), ((UNTER, LEAVES), 3),
                                                ((EIGHT, BELLS), 0), ((UNTER, ACORNS), 1),
                                                ((ACE, ACORNS), 1), ((EIGHT, ACORNS), 2),
                                                ((ACE, LEAVES), 3), ((TEN, ACORNS), 0),
                                                ((OBER, LEAVES), 3), ((TEN, LEAVES), 0),
                                                ((EIGHT, LEAVES), 1), ((NINE, ACORNS), 2),
                                                ((SEVEN, LEAVES), 3), ((UNTER, BELLS), 0),
                                                ((NINE, LEAVES), 1), ((ACE, HEARTS), 2),
                                                ((TEN, HEARTS), 0), ((NINE, HEARTS), 1),
                                                ((EIGHT, HEARTS), 2), ((KING, LEAVES), 3),
                                                ((OBER, ACORNS), 3), ((OBER, BELLS), 0),
                                                ((OBER, HEARTS), 1), ((NINE, BELLS), 2),
                                                ((UNTER, HEARTS), 3), ((KING, HEARTS), 0),
                                                ((SEVEN, ACORNS), 1), ((KING, ACORNS), 2)]


def test_scraping_wenz():
    html = s.get_html(game_number=786157276, driver=driver)
    soup_wenz = s.get_soup(html)
    assert s.game_with_eight_cards(html)
    assert s.scrape_game_mode(soup_wenz) == (WENZ, None)
    assert s.find_declaring_player_name(soup_wenz) == 'taschee'
    assert s.scrape_declaring_player_index(soup_wenz) == 3
    assert s.scrape_player_hands(soup_wenz) == [[(TEN, ACORNS), (OBER, ACORNS), (EIGHT, ACORNS), (SEVEN, ACORNS),
                                                 (KING, LEAVES), (EIGHT, LEAVES), (TEN, HEARTS), (TEN, BELLS)],
                                                [(UNTER, HEARTS), (ACE, ACORNS), (OBER, LEAVES), (NINE, LEAVES),
                                                 (ACE, HEARTS), (NINE, HEARTS), (ACE, BELLS), (KING, BELLS)],
                                                [(KING, ACORNS), (NINE, ACORNS), (SEVEN, LEAVES), (EIGHT, HEARTS),
                                                 (OBER, BELLS), (NINE, BELLS), (EIGHT, BELLS), (SEVEN, BELLS)],
                                                [(UNTER, ACORNS), (UNTER, LEAVES), (UNTER, BELLS), (ACE, LEAVES),
                                                 (TEN, LEAVES), (KING, HEARTS), (OBER, HEARTS), (SEVEN, HEARTS)]]
    assert s.get_player_names(soup_wenz) == ['Monty12', 'Blauweiss63', 'niemand123', 'taschee']
    assert s.scrape_played_cards(soup_wenz) == [((TEN, ACORNS), 0), ((ACE, ACORNS), 1),
                                                ((KING, ACORNS), 2), ((UNTER, BELLS), 3),
                                                ((UNTER, LEAVES), 3), ((SEVEN, ACORNS), 0),
                                                ((UNTER, HEARTS), 1), ((NINE, ACORNS), 2),
                                                ((KING, HEARTS), 3), ((TEN, HEARTS), 0),
                                                ((ACE, HEARTS), 1), ((EIGHT, HEARTS), 2),
                                                ((ACE, BELLS), 1), ((OBER, BELLS), 2),
                                                ((UNTER, ACORNS), 3), ((TEN, BELLS), 0),
                                                ((ACE, LEAVES), 3), ((EIGHT, LEAVES), 0),
                                                ((NINE, LEAVES), 1), ((SEVEN, LEAVES), 2),
                                                ((TEN, LEAVES), 3), ((KING, LEAVES), 0),
                                                ((OBER, LEAVES), 1), ((SEVEN, BELLS), 2),
                                                ((OBER, HEARTS), 3), ((EIGHT, ACORNS), 0),
                                                ((NINE, HEARTS), 1), ((EIGHT, BELLS), 2),
                                                ((SEVEN, HEARTS), 3), ((OBER, ACORNS), 0),
                                                ((KING, BELLS), 1), ((NINE, BELLS), 2)]


def test_game_with_six_cards():
    html = s.get_html(game_number=846388807, driver=driver)
    assert not s.game_with_eight_cards(html)


def test_closing():
    driver.close()
