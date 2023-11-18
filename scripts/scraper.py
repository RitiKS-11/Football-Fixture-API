import requests
from bs4 import BeautifulSoup
import sqlite3

class Scraper:
    URL = "https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures"

    def __init__(self):
        self.response = requests.get(self.URL)
        self.soup = BeautifulSoup(self.response.text, 'html.parser')

    def connect_database(self):
        db = sqlite3.connect('database.db')
        cursor = db.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS fixture  \
                       ( gameweek integer, game_date date, home_team varchar(30), \
                        score integer, away_team varchar(30), venue varchar(25))')
        cursor.close()
        return db
    
    def parse_scores(self):

        self.results = self.soup.select('tbody')

        for result in self.results:
            for row in result.select('tr'):
                gameweek = row.select('th', {'class':'right', 'data-stat':'gameweek'})[0].text
                game_date = row.find('td', {'data-stat':'date'}).text
                home_team = row.find('td', {'data-stat':'home_team'}).text
                away_team = row.find('td', {'data-stat':'away_team'}).text
                score = row.find('td', {'data-stat':'score'}).text
                venue = row.find('td', {'data-stat':'venue'}).text

                if gameweek:
                    self.insert(gameweek, game_date, home_team, score, away_team, venue)

    def insert(self, gameweek, game_date, home_team, score, away_team, venue):
        db = self.connect_database()
        cursor = db.cursor()
        cursor.execute('INSERT INTO fixture VALUES (?, ?, ?, ?, ?, ?)',(gameweek, game_date, home_team, score, away_team, venue))
        cursor.commit()
        cursor.close()

    def update(self):
        pass

    def retrieve(self):
        db = self.connect_database()
        cursor = db.cursor()

        cursor.execute('SELECT * FROM fixture')
        data = cursor.fetchall()

        columns = [column[0] for column in cursor.description]
        results = [dict(zip(columns, row)) for row in data]

        cursor.close()
        db.close()

        if results:
            return results
        return 'Could not retrieve data from database'



if __name__ == "__main__":
    run = Scraper()
    run.parse_scores()