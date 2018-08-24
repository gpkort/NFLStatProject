from string import ascii_lowercase
from bs4 import BeautifulSoup
import pandas as pd
import requests
import Draft



URL = "https://www.pro-football-reference.com/years/{}/probowl.htm"
PLAYERS_URL = "https://www.pro-football-reference.com/players/{}/"


def get_probowl_players():
    with open("players.csv", "w") as f:
        f.write("Last,First\n")

        for i in range(1950, 2018):
            print(URL.format(i))
            req = requests.get(URL.format(i))
            soup = BeautifulSoup(req.text, 'html.parser')
            players = soup.find_all('td', {'data-stat': 'player'})

            for player in players:
                f.write(player['csk'] + '\n')


def get_frequency(df: pd.DataFrame):
    df['combined'] = df['Last'] + ',' + df['First']
    appear_dict = proplays['combined'].value_counts().to_dict()
    freq_df = pd.DataFrame(columns=['last_name', 'first_name', 'no_of_appearance'])

    for key, value in appear_dict.items():
        names = key.split(',')
        freq_df = freq_df.append({'last_name': names[0], 'first_name': names[1],
                                  'no_of_appearance': value}, ignore_index=True)

    return freq_df


ALL_PLAYERS_URL = "https://www.pro-football-reference.com/players/{}/"


def scrap_all_players():
    with open("all_players.text", "w") as file:
        for char in range(65, 91):
            print(URL.format(chr(char)))
            req = requests.get(ALL_PLAYERS_URL.format(chr(char)))

            if req.status_code == 200:
                soup = BeautifulSoup(req.text, 'html.parser')
                players = soup.find_all('div', {'id': 'div_players'})

                for name in players[0].strings:
                    file.write(name.string.strip() + '\n')


def massage_data():
    print('Massage Data')
    with open("all_players.text", 'r') as read_file:
        with open('all_players.csv', 'w') as file:
            empty = ['', '', '', '']
            file.write('first_name,last_name,position\n')
            first, second = empty[0:2]
            for line in read_file:
                if len(line) > 0:
                    if '(' in line:
                        second = line.replace('\n', '').replace(',', '-')
                    else:
                        first = line.replace('\n', '')

                if len(first) > 0 and len(second) > 0:
                    names = first.split(' ')
                    firstname, secondname = empty[0:2]
                    length = len(names)

                    if length == 1:
                        secondname = names[0]
                    elif length == 2:
                        firstname, secondname = names[0:2]
                    else:
                        firstname = names[0]
                        secondname = names[length - 1]

                    file.write(firstname + "," + secondname + "," + second + '\n')
                    first, second, secondname, firstname = empty[0:5]


if __name__ == "__main__":
    proplays = pd.read_csv("players.csv")
    massage_data()
