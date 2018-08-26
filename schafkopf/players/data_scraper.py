from selenium import webdriver
from schafkopf.game_modes import NO_GAME, PARTNER_MODE, SOLO, WENZ
from schafkopf.suits import ACORNS, BELLS, LEAVES, HEARTS
from bs4 import BeautifulSoup


class DataScraper():
    def __init__(self):
        self.card_encodings = {'Schellen-Sieben': (0, 0), 'Schellen-Acht': (1, 0), 'Schellen-Neun': (2, 0),
                               'Schellen-Unter': (3, 0), 'Der Runde': (4, 0), 'Schellen-König': (5, 0),
                               'Schellen-Zehn':(6, 0), 'Die Hundsgfickte': (7, 0),
                               'Herz-Sieben': (0, 1), 'Herz-Acht': (1, 1), 'Herz-Neun': (2, 1), 'Herz-Unter': (3, 1),
                               'Der Rote': (4, 1), 'Herz-König': (5, 1),'Herz-Zehn':(6, 1), 'Herz-Sau': (7, 1),
                               'Gras-Sieben': (0, 2), 'Gras-Acht': (1, 2), 'Gras-Neun': (2, 2), 'Gras-Unter': (3, 2),
                               'Der Blaue': (4, 2), 'Gras-König': (5, 2), 'Gras-Zehn': (6, 2), 'Die Blaue': (7, 2),
                               'Eichel-Sieben': (0, 3), 'Eichel-Acht': (1, 3), 'Eichel-Neun': (2, 3),
                               'Eichel-Unter': (3, 3), 'Der Alte': (4, 3), 'Eichel-König': (5, 3),
                               'Eichel-Zehn': (6, 3), 'Die Alte': (7, 3)}

    def get_html(self, game_number):

        chromedriver = 'C:\\Users\\Taschee\\Downloads\\chromedriver_win32\\chromedriver.exe'
        driver = webdriver.Chrome(chromedriver)
        driver.get('http://www.sauspiel.de/spiele')

        username_box = driver.find_element_by_name('login')
        username_box.send_keys('taschee')
        password_box = driver.find_element_by_name('password')
        password_box.send_keys('WASwas')
        password_box.submit()

        game_search_box = driver.find_element_by_name('game_id')
        game_search_box.send_keys(str(game_number))
        game_search_box.submit()

        html = driver.page_source

        return html

    def get_soup(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    def scrape_game_mode(self, soup):
        title_tag = soup.find_all('meta', attrs={'name': 'twitter:title'})[0]
        title_str = title_tag['content']
        if title_str[:8] == 'Sauspiel':
            if title_str[17:21] == 'Alte':
                return (PARTNER_MODE, ACORNS)
            elif title_str[17:21] == 'Blau':
                return (PARTNER_MODE, LEAVES)
            elif title_str[17:21] == 'Hund':
                return (PARTNER_MODE, BELLS)
        elif title_str[:4] == 'Wenz':
            return (WENZ, None)
        elif title_str[:9] == 'Herz-Solo':
            return (SOLO, HEARTS)
        elif title_str[:9] == 'Gras-Solo':
            return (SOLO, LEAVES)
        elif title_str[:11] == 'Eichel-Solo':
            return (SOLO, ACORNS)
        elif title_str[:13] == 'Schellen-Solo':
            return (SOLO, BELLS)
        else:
            return

    def find_declaring_player_name(self, soup):
        title_tag = soup.find_all('meta', attrs={'name': 'twitter:title'})[0]
        title_str = title_tag['content']
        starting_index = None
        for i in range(len(title_str) - 1, -1, -1):
            if title_str[i] == ' ':
                starting_index = i + 1
                break
        return title_str[starting_index:]

    def find_dealing_tag(self, soup):
        card_soup = soup.find_all(class_='card')
        dealing_tag = None
        for tag in card_soup:
            s = tag.find('h4')
            if s.text == 'Karten werden ausgegeben':
                dealing_tag = tag
                break
        return dealing_tag


    # leading player ist immer im Index 0

    def scrape_declaring_player_index(self, soup):
        name = self.find_declaring_player_name(soup)
        dealing_tag = self.find_dealing_tag(soup)
        usernames = dealing_tag.find_all(class_='avatar-username')
        for n, index in zip(usernames, range(len(usernames))):
            if name in n.text:
                return index

    def scrape_player_hands(self, soup):
        dealing_tag = self.find_dealing_tag(soup)
        hand_tags = dealing_tag.find_all(class_='game-protocol-cards')
        playerhands = []
        for tag in hand_tags:
            card_tags = tag.find_all(class_='card-image')
            hand = []
            for card_tag in card_tags:
                card_encoded = card_tag.text
                hand.append(self.card_encodings[card_encoded])
            playerhands.append(hand)
        return playerhands

    def scrape_tricks(soup):
        pass

    def scrape_results(soup):
        pass

    def scrape_mode_proposals(soup):
        pass
