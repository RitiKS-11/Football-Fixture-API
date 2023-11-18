from flask import Flask

from api.score import api

app = Flask(__name__)
app.register_blueprint(api)

from app import views