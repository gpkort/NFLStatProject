import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re


df = pd.read_csv('data/players_2013-12-12.csv')
players2 = pd.read_csv('data/all_players.csv')

def remove_death_columns(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop(columns=['death_date', 'death_city', 'death_state', 'death_country'])

def add_yrs_played(df: pd.DataFrame) -> pd.DataFrame:
    yrsadded = df.copy()
    yrsadded['years_played'] = yrsadded['year_end'] - yrsadded['year_start']

    return yrsadded


def filldraft_pick(df: pd.DataFrame):
    # df['draft_pick'] = df['draft_pick'].str.replace(r'[0-9]+th|[0-9]+st|[0-9]+rd|[0-9]+nd'
    #                          , '', flags=re.IGNORECASE)
    df['draft_pick'] = df['draft_pick'].str.replace('th', '', case=False)
    df['draft_pick'] = df['draft_pick'].str.replace('st', '', case=False)
    df['draft_pick'] = df['draft_pick'].str.replace('rd', '', case=False)
    df['draft_pick'] = df['draft_pick'].str.replace('nd', '', case=False)
    df['draft_pick'] = pd.to_numeric(df['draft_pick'], errors='coerce')
    max = df['draft_pick'].max(skipna=True)
    df['draft_pick'].fillna(max+1, inplace=True)


def clean_position(pos: pd.Series):
    pos = pos.apply(lambda x: str(x))
    pos = pos.apply(lambda x: x.split('-')[0])
    pos = pos.apply(lambda x: x.split('/')[0])

    return pos.copy()


if __name__ == "__main__":
    df['position'] = clean_position(df['position'])
    print(df.columns)
    # df['position'].plot.hist()
    # players = remove_death_columns(df)
    # players = add_yrs_played(players)
    # filldraft_pick(players)
    #
    # df3 = players.merge(players2, on=['first_name', 'last_name'], how='outer')
    # print('First Count {}'.format(players['name'].count()))
    # print('Other Count {}'.format(players['first_name'].count()))
    # print('Combined Count {}'.format(df3['first_name'].count()))
    # print(df3['name'].isnull().sum())

    # print(df.describe())





'''
'name', 'first_name', 'last_name', 'birth_city', 'birth_state',
       'birth_country', 'birth_date', 'college', 'draft_team', 'draft_round',
       'draft_pick', 'draft_year', 'position', 'height', 'weight',
       'year_start', 'year_end', years_played
       
'all_pros_first_team', 'draft_pick', 'g', 'player', 'pos',
       'pro_bowls', 'round', 'team', 'year', 'year_max',
       'years_as_primary_starter'
'''



