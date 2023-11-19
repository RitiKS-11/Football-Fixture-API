from flask import render_template
from app import app

@app.route('/')
def home():
    base_url = 'http://127.0.0.1:5000'
    api_endpoints = [
        {
        'url' : base_url + '/api',
        'description': 'Get API Endpoints'
    },
    {
        'url' : base_url + '/api/fixtures',
        'description': 'All Fixtures'
    },
    {
        'url' : base_url + '/api/fixtures/Manchester Utd',
        'description': 'Fixture of Manchester United'
    },
    {
        'url' : base_url + '/api/fixtures/date=2023-08-11',
        'description': 'Fixture of 2023-08-11'
    }
    ]
    return render_template('app/index.html', endpoints=api_endpoints)