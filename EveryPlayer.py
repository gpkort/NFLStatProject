from bs4 import BeautifulSoup
import pandas as pd
import requests
import numpy as np


URL = "https://www.pro-football-reference.com"
PLAYER = "players"

def get_players_by_letter(letter: str):
    url = URL + '/' + PLAYER + '/' + letter
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "lxml")
    players = soup.find_all('div', {'id': 'div_players'})

    links = [link for link in players[0].find_all('a')]
    urls = [u.get('href') for u in links]
    return urls


def get_player_summary(url: str):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "lxml")
    body = soup.find_all('table', {'class': 'row_summable sortable stats_table'})[0].find('tbody')
    rows = body.find_all('tr', {'class': 'full_table'})

    totalgames, gamestart = 0, 0

    for row in rows:
        for g in row.find_all('td', {'data-stat': 'g'}):
            if len(g.text) > 0:
                totalgames = totalgames + int(g.text)
        for gs in row.find_all('td', {'data-stat': 'gs'}):
            if len(gs.text) > 0:
                gamestart = gamestart + int(gs.text)

    print(totalgames)
    print(gamestart)



if __name__ == '__main__':
    get_player_summary(URL + '/players/A/AaitIs00.htm')
    # all = []
    # for i in range(65, 91):
    #     all.extend(get_players_by_letter(chr(i)))

    # print(len(all))
    # with open('all_players_url.txt', 'w') as f:
    #     f.writelines(['%s\n' % url for url in all])

