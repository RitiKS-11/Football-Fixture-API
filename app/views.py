from flask import render_template
from app import app

@app.route('/')
def home():
    base_url = 'http://127.0.0.1:5000'
    api_endpoints = [
        {
        'url' : base_url + '/api',
        'description': 'This is the api to get all the endpoints of the football api'
    },
    {
        'url' : base_url + '/api/endpoints',
        'description': 'test new api'
    }
    ]
    return render_template('app/index.html', endpoints=api_endpoints)