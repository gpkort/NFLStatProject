from bs4 import BeautifulSoup
import requests

URL = "https://www.pro-football-reference.com/years/{}/probowl.htm"
FIRST_YEAR = 1950
LAST_YEAR = 2017


class ProwBowlPlayer(object):
    DELIMITER = '|'

    def __init__(self, name: str, year: str, pos: str = '', team: str = ''):
        self.__name = name.replace('+', '').replace('%', '').replace('*', '')
        self.__year = year.strip()
        self.__pos = pos.strip()
        self.__team = team.strip()
        self.__total_appearance = 1

    def __str__(self):
        return '{},{},{},{}'.format(
            self.__name,
            self.__year,
            self.__pos,
            self.__team)
    @property
    def Name(self):
        return self.__name

    def add_parameters(self, year: str, pos: str = '', team: str = ''):
        self.__year = self.add_delimited_param(year)

        if pos != '':
            self.__pos = self.add_delimited_param(pos, self.__pos)
        if team != '':
            self.__team = self.add_delimited_param(team, self.__team)

    def add_delimited_param(self, val: str, current: str):
        val = val.strip()

        if current == '':
            return val

        vals = current.split('|')
        for v in vals:
            if v == val:
                return current

        return current + ProwBowlPlayer.DELIMITER + val


class ProBowlRoster(object):
    def __init__(self):
        self.__roster = []

    def get_roster_copy(self):
        return self.__roster.copy()

    def add_player(self, player: ProwBowlPlayer):
        pass


if __name__ == '__main__':
    print('ProwBowl Scrapper')
