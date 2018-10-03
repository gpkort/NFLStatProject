from bs4 import BeautifulSoup
import pandas as pd
import requests
import numpy as np
import collections

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
    playername = soup.find('h1', {'itemprop': 'name'}).text
    tables = soup.find_all('table', {'class': 'row_summable sortable stats_table'})

    if len(tables) == 0:
        tables = soup.find_all('table', {'class': 'sortable stats_table'})

    if len(tables) == 0:
        raise Exception("Cannot find Table")

    body = tables[0].find('tbody')
    rows = body.find_all('tr', {'class': 'full_table'})

    if len(rows) == 0 and len(tables) > 1:
        body = tables[1].find('tbody')
        rows = body.find_all('tr', {'class': 'full_table'})

    if len(rows) == 0:
        raise Exception('Could not find rows in table')

    totalgames, gamestart = 0, 0
    teams, pos = str(), str()

    for row in rows:
        for g in row.find_all('td', {'data-stat': 'g'}):
            if len(g.text) > 0:
                totalgames = totalgames + int(g.text)
        for gs in row.find_all('td', {'data-stat': 'gs'}):
            if len(gs.text) > 0:
                gamestart = gamestart + int(gs.text)
        for team in row.find_all('td', {'data-stat': 'team'}):
            if len(team.text) > 0 and team.text not in teams:
                teams = teams + team.text + ','
        for p in row.find_all('td', {'data-stat': 'pos'}):
            if len(p.text) > 0 and p.text not in pos:
                pos = p.text + ','

    yr = rows[0].find_all('th', {'data-stat': 'year_id'})
    startyear = int(yr[0].text.replace('*', '').replace('+', '')) if len(yr[0].text) > 0 else None

    if len(rows) > 1:
        yr = rows[-1].find_all('th', {'data-stat': 'year_id'})
        stopyear = int(yr[0].text.replace('*', '').replace('+', '')) if len(yr[0].text) > 0 else None
    else:
        stopyear = startyear

    return {
        'name': playername,
        'position': (pos[:-1] if len(pos) > 0 else ''),
        'teams': teams[:-1] if len(teams) > 0 else '',
        'start_year': startyear,
        'stop_year': stopyear,
        'total_game': totalgames,
        'games_started': gamestart
    }


def make_every_player_file(player_url: str, out_file: str):
    # player_url = 'all_players_url.txt'
    roster, errors = [], []

    with open(player_url) as f:
        players = f.readlines()

    players_url = [l.strip() for l in players]

    for i, p in enumerate(players_url):
        player_url = p

        if i % 10 == 0:
            print('{}: {}'.format(i, player_url))

        try:
            roster.append(get_player_summary(URL + player_url))
        except Exception as e:
            print('****{}'.format(player_url))
            errors.append('{} - {}\n'.format(player_url, e))

    with open(out_file, 'w') as pf:
        pf.write('name,teams,position,start_year,stop_year,total_game,games_started\n')

        for p in roster:
            pf.write('{},{},{},{},{},{},{}\n'.format(
                p['name'],
                p['teams'],
                p['position'],
                p['start_year'],
                p['stop_year'],
                p['total_game'],
                p['games_started']
            ))

    with open('Error.log', 'w') as err:
        for e in errors:
            err.write(e)


if __name__ == '__main__':
    # print(get_player_summary('https://www.pro-football-reference.com/players/A/AdamDa01.htm'))
    make_every_player_file('wrongtable.txt', 'ErrTable.log')
    # print('1975*+'.replace('*', '').replace('+', ''))