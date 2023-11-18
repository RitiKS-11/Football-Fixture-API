from flask import Blueprint, jsonify
import csv
from scripts.scraper import Scraper

api = Blueprint('api', __name__, url_prefix='/api')    

@api.route('/')
@api.route('/endpoints')
def index():
    return 'This will show the available endpoints'

@api.route('/fixtures')
def fixtures():
    receiver = Scraper()
    data = receiver.retrieve()

    return jsonify(data)

@api.route('/fixtures/<str:team>')
def get_team_fixtuer(team):
    pass

@api.route('/fixtures/<str:date>')
def get_fixture_date(date):
    pass