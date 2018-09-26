from bs4 import BeautifulSoup
import pandas as pd
import requests


URL = "https://www.pro-football-reference.com"
PLAYER = "players"

def get_players_by_letter(letter: str):
    url = URL + '/' + PLAYER + '/' + letter
    print(url)
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "lxml")
    players = soup.find_all('div', {'id': 'div_players'})

    links = [link for link in players[0].find_all('a')]
    urls = [u.get('href') for u in links]
    return urls


if __name__ == '__main__':
    all = []
    for i in range(65, 91):
        all.extend(get_players_by_letter(chr(i)))

    print(len(all))
    with open('all_players_url.txt', 'w') as f:
        f.writelines(['%s\n' % url for url in all])

