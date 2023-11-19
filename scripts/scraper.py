import requests
from bs4 import BeautifulSoup
import sqlite3
import os
from dotenv import load_dotenv

class Scraper:
    load_dotenv()
    URL = os.getenv('URL')

    def __init__(self):
        self.response = requests.get(self.URL)
        self.soup = BeautifulSoup(self.response.text, 'html.parser')

    @staticmethod
    def convert_data_into_dict(cursor, results):
        columns = [column[0] for column in cursor.description]
        results = [dict(zip(columns, row)) for row in results]

        return results

    @staticmethod
    def connect_database():
        db = sqlite3.connect('database.db')
        cursor = db.cursor()
        cursor.execute('PRAGMA encoding="UTF-8";')
        cursor.execute('CREATE TABLE IF NOT EXISTS fixture  \
                       ( gameweek integer, game_date date, home_team text, \
                        score integer, away_team text, venue text)')
        cursor.close()
        return db

    def parse_scores(self):

        self.results = self.soup.select('tbody')

        for result in self.results:
            for row in result.select('tr'):
                gameweek = row.select('th', {'class': 'right', 'data-stat': 'gameweek'})[0].text
                game_date = row.find('td', {'data-stat': 'date'}).text
                home_team = row.find('td', {'data-stat': 'home_team'}).text
                away_team = row.find('td', {'data-stat': 'away_team'}).text
                score = row.find('td', {'data-stat': 'score'}).text
                venue = row.find('td', {'data-stat': 'venue'}).text

                if gameweek:
                    self.insert(gameweek, game_date, home_team,
                                score, away_team, venue)

    def insert(self, gameweek, game_date, home_team, score, away_team, venue):
        db = self.connect_database()
        cursor = db.cursor()
        cursor.execute('INSERT INTO fixture VALUES (?, ?, ?, ?, ?, ?)',
                       (gameweek, game_date, home_team, score, away_team, venue))

        db.commit()
        cursor.close()
        db.close()

    def update(self):
        pass

    @classmethod
    def retrieve(cls):
        db = cls.connect_database()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM fixture')
        results = cursor.fetchall()

        results = cls.convert_data_into_dict(cursor, results)

        cursor.close()
        db.close()

        if results:
            return results
        return 'Could not retrieve data from database.'

    @classmethod
    def filter_by_team(cls, team):
        db = cls.connect_database()
        cursor = db.cursor()
        cursor.execute(
            'SELECT * FROM fixture WHERE home_team = ? OR away_team = ?', (team, team))
        results = cursor.fetchall()

        results = cls.convert_data_into_dict(cursor, results)

        cursor.close()
        db.close()

        if results:
            return results
        return 'Could not retrieve data from database.'

    @classmethod
    def filter_by_date(cls, date):
        db = cls.connect_database()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM fixture WHERE game_date = ?', (date,))
        results = cursor.fetchall()

        results = cls.convert_data_into_dict(cursor, results)

        cursor.close()
        db.close()

        if results:
            return results
        return 'Could not retrieve data from database.'


if __name__ == "__main__":
    d = Scraper()
    print(d.parse_scores())
