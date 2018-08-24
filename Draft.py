from string import ascii_lowercase
from typing import Dict, Any

from bs4 import BeautifulSoup
import pandas as pd
import requests
import numpy as np
import matplotlib.pyplot as plt

TRACKED_STATS = ['draft_pick', 'team', 'player', 'pos', 'year_max',
                 'all_pros_first_team', 'pro_bowls', 'years_as_primary_starter', 'g']

URL = "https://www.pro-football-reference.com/years/{}/draft.htm"

CSV_FILE = 'AllDraftPicks.csv'


def get_parse_row(row, year) -> dict:
    stat_dict = dict()  # type: Dict[str, str]

    if row.has_attr('class') and row['class'][0] == 'thead':
        return stat_dict

    draft_round = row.find_all('th', {'data-stat': 'draft_round'})
    draft_round = int(draft_round[0].string)

    stats = row.find_all('td')

    stat_dict['round'] = draft_round
    stat_dict['year'] = year

    for stat in stats:
        stat_name = stat.get('data-stat')

        if stat_name in TRACKED_STATS:
            stat_dict[stat_name] = stat.string

    return stat_dict


def get_draftpicks(tables, year: int) -> list:
    picks = list()

    for table in tables:
        rows = table.find_all('tr')

        for row in rows:
            picks.append(get_parse_row(row, year))

    return picks


def get_all_draft(years):
    all_rounds = list()

    for year in years:
        draft_url = URL.format(year)
        print(draft_url)

        req = requests.get(draft_url)
        soup = BeautifulSoup(req.text, 'html.parser')
        players = soup.find_all('tbody')
        draft_picks = get_draftpicks(players, year)
        all_rounds = all_rounds + draft_picks

    return pd.DataFrame(all_rounds)


def save_to_csv():
    df = get_all_draft(range(1950, 2018))
    df.to_csv(CSV_FILE)


def get_dataframe():
    df = pd.read_csv('AllDraftPicks.csv')
    df.drop('Unnamed: 0', inplace=True, axis=1)
    df = df[['year', 'round', 'draft_pick', 'player', 'pos', 'g',
             'year_max', 'years_as_primary_starter', 'all_pros_first_team']]
    df['round'].fillna(value=30, inplace=True)
    df['round'] = df['round'].apply(lambda x: int(x))

    return df


def add_general_position(df: pd.DataFrame) -> pd.Series:
    df['general_pos'] = df['pos'].copy()
    df['general_pos'] = np.where(df['general_pos'] == 'HB', 'RB', df['general_pos'])
    df['general_pos'] = np.where(df['general_pos'] == 'WB', 'RB', df['general_pos'])
    df['general_pos'] = np.where(df['general_pos'] == 'B', 'RB', df['general_pos'])
    df['general_pos'] = np.where(df['general_pos'] == 'FB', 'RB', df['general_pos'])
    df['general_pos'] = np.where(df['general_pos'] == 'BB', 'RB', df['general_pos'])

    df['general_pos'] = np.where(df['general_pos'] == 'OLB', 'LB', df['general_pos'])
    df['general_pos'] = np.where(df['general_pos'] == 'ILB', 'LB', df['general_pos'])

    df['general_pos'] = np.where(df['general_pos'] == 'T', 'OL', df['general_pos'])
    df['general_pos'] = np.where(df['general_pos'] == 'G', 'OL', df['general_pos'])
    df['general_pos'] = np.where(df['general_pos'] == 'C', 'OL', df['general_pos'])

    df['general_pos'] = np.where(df['general_pos'] == 'SS', 'S', df['general_pos'])
    df['general_pos'] = np.where(df['general_pos'] == 'FS', 'S', df['general_pos'])
    df['general_pos'] = np.where(df['general_pos'] == 'S', 'DB', df['general_pos'])

    df['general_pos'] = np.where(df['general_pos'] == 'DE', 'DL', df['general_pos'])
    df['general_pos'] = np.where(df['general_pos'] == 'DG', 'DL', df['general_pos'])
    df['general_pos'] = np.where(df['general_pos'] == 'DT', 'DL', df['general_pos'])

    df['general_pos'] = np.where(df['general_pos'] == 'E', 'TE', df['general_pos'])
    df['general_pos'] = np.where(df['general_pos'] == 'SE', 'WR', df['general_pos'])
    df['general_pos'] = np.where(df['general_pos'] == 'FL', 'WR', df['general_pos'])

    df['general_pos'] = np.where(df['general_pos'] == 'KR', 'ST', df['general_pos'])
    df['general_pos'] = np.where(df['general_pos'] == 'LS', 'ST', df['general_pos'])

    df['general_pos'] = np.where(df['general_pos'] == 'CB', 'DB', df['general_pos'])

    df['general_pos'] = np.where(df['general_pos'] == 'NT', 'DL', df['general_pos'])
    df['general_pos'] = np.where(df['general_pos'] == 'MG', 'DL', df['general_pos'])


def show_frequency_by_position(df: pd.DataFrame, graph_title: str, fig_num: int):
    plt.figure(fig_num)
    df['general_pos'].value_counts(normalize=True).plot(kind='pie', title=graph_title)


def show_frequency_by_decade(df: pd.DataFrame):
    df1950 = df[(df['year'] >= 1950) & (df['year'] < 1960)]
    df1960 = df[(df['year'] >= 1960) & (df['year'] < 1970)]
    df1970 = df[(df['year'] >= 1970) & (df['year'] < 1980)]
    df1980 = df[(df['year'] >= 1980) & (df['year'] < 1990)]
    df1990 = df[(df['year'] >= 1990) & (df['year'] < 2000)]
    df2000 = df[(df['year'] >= 2000) & (df['year'] < 2010)]
    df2010 = df[(df['year'] >= 2010)]

    show_frequency_by_position(df1950, '1950s', 1)
    show_frequency_by_position(df1960, '1960s', 2)
    show_frequency_by_position(df1970, '1970s', 3)
    show_frequency_by_position(df1980, '1980s', 4)
    show_frequency_by_position(df1990, '1990s', 5)
    show_frequency_by_position(df2000, '2000s', 6)
    show_frequency_by_position(df2010, '2010s', 7)
    plt.show()


def show_frequency_round(df: pd.DataFrame):
    for i in range(1, 11):
        show_frequency_by_position(df[(df['round'] == i)],
                                   'Round {}'.format(i),
                                   i)
    plt.show()


def get_draft_data_file():
    df = get_dataframe()
    return add_general_position(df)

def get_num_name(name: str):
    return len(name.split(' '))

if __name__ == '__main__':
    df = get_dataframe()
    add_general_position(df)
    print(df.columns)
    df['player'] = df['player'].apply(lambda x: str(x))
    df['names'] = 0
    df.assign(names=lambda row: len(row['player'].split(' ')))
    # df['names'] = df.apply(lambda row: len(row.player.split(' ')))
    print(df['player'].head())
    print(df['names'].head())
    #
    # df_recent = df[df['year'] > 2010]
    # for i in range(1, 7):
    #     show_frequency_by_position(df[(df['round'] == i)],
    #                                'Round {}'.format(i),
    #                                i)
    # plt.show()
