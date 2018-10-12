from bs4 import BeautifulSoup
import requests

URL = "https://www.pro-football-reference.com/years/{}/probowl.htm"
FIRST_YEAR = 1950
LAST_YEAR = 2017


class PlayerStats(object):
    DELIMITER = '|'

    def __init__(self, year: str, pos: str = '', team: str = ''):
        self.__year = year.strip()
        self.__pos = pos.strip()
        self.__team = team.strip()
        self.__total_appearance = 1

    def __str__(self):
        return '{},{},{}'.format(
            self.__year,
            self.__pos,
            self.__team)

    def add_parameters(self, year: str, pos: str = None, team: str = None):
        self.__year = self.add_delimited_param(year, self.__year)

        if pos:
            self.__pos = self.add_delimited_param(pos, self.__pos)
        if team:
            self.__team = self.add_delimited_param(team, self.__team)

    @staticmethod
    def add_delimited_param(val: str, current: str):
        val = val.strip()

        if current == '':
            return val

        vals = current.split('|')
        for v in vals:
            if v == val:
                return current

        return current + PlayerStats.DELIMITER + val


class ProBowlRoster(object):
    def __init__(self):
        self.__roster = dict()

    def get_roster_copy(self):
        return self.__roster.copy()

    def add_player(self, name: str, year: str, pos: str = None, team: str = None):
        name = name.replace('+', '').replace('%', '').replace('*', '')
        player = self.__roster.get(name)

        if player:
            player.add_parameters(year, pos, team)
        else:
            self.__roster[name] = PlayerStats(year=year, pos=pos, team=team)

    def get_comma_delimited_sting(self):
        return ['{},{}{}'.format(k, v, '\n') for k, v in self.__roster.items()]

def get_years_roster(yr, roster: ProBowlRoster):
    req = requests.get(URL.format(yr))
    soup = BeautifulSoup(req.text, "lxml")
    table = soup.find('table', {'class': 'sortable stats_table',
                                     'id': 'pro_bowl'})
    if table:
        body = table.find('tbody')
        for row in body.find_all('tr'):
            name, pos, team = process_row(row)
            roster.add_player(name=name, year=str(yr), pos=pos, team=team)


def process_row(row):
    pos_element = row.find('th', {'data-stat': 'pos'})
    pos = pos_element.text if pos_element is not None else ''
    name, team = '', ''
    found_play, found_team = False, False

    for cell in row.find_all('td'):
        if cell.get("data-stat") == "player":
            name = cell.get('csk', '')
            found_play = True
        if cell.get("data-stat") == "team":
            team_tag = cell.find('a')
            team = team_tag.text if team_tag is not None else ''
            found_team = True
        if found_play and found_team:
            break


    return name, pos, team


if __name__ == '__main__':
    print('ProwBowl Scrapper')
    play_roster = ProBowlRoster()

    for yr in range(FIRST_YEAR, LAST_YEAR+1):
        print('Year = {}'.format(yr))
        get_years_roster(yr, play_roster)

    print(*play_roster.get_comma_delimited_sting())

