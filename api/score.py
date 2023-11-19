from flask import Blueprint, jsonify, render_template
import csv
from scripts.scraper import Scraper

api = Blueprint('api', __name__, url_prefix='/api')    

@api.route('/')
@api.route('/endpoints')
def index():
    endpoints = {
        'Get API Endpoints': 'http://127.0.0.1:5000/api',
        'All Fixtures': 'http://127.0.0.1:5000/api/fixtures',
        'Fixture of Manchester United': 'http://127.0.0.1:5000/api/fixtures/manchester-united',
        'Fixture of 2023-08-11': 'http://127.0.0.1:5000/api/fixtures/2023-08-11'
    }
    return jsonify(endpoints)

@api.route('/fixtures')
def fixtures():
    receiver = Scraper()
    data = receiver.retrieve()

    return jsonify(data)

@api.route('/fixtures/<string:team>')
def get_team_fixtuer(team):
    receiver = Scraper()
    data = receiver.filter_by_team(team)

    return jsonify(data)

@api.route('/fixtures/date=<string:date>')
def get_fixture_date(date):
    receiver = Scraper()
    data = receiver.filter_by_date(date)

    return jsonify(data)