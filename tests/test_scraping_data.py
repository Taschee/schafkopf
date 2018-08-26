import pytest
from schafkopf.players.scrape_data import get_html, get_soup, scrape_game_mode, find_declaring_player_name, \
     scrape_declaring_player_index
from schafkopf.game_modes import PARTNER_MODE, SOLO, WENZ, NO_GAME
from schafkopf.suits import ACORNS, LEAVES, HEARTS, BELLS


def test_scraping():
    html = get_html(game_number=846389616)
    soup_partnermode = get_soup(html)
    assert scrape_game_mode(soup_partnermode) == (PARTNER_MODE, LEAVES)
    assert find_declaring_player_name(soup_partnermode) == 'taschee'
    assert scrape_declaring_player_index(soup_partnermode) == 2