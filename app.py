from flask import Flask, Blueprint, flash, request, redirect, url_for, render_template, send_from_directory, jsonify, Response
from flask_cors import CORS
import yfinance as yf
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
import json, secrets


with open('config.json') as config_file:
    config = json.load(config_file)


db = (MongoClient()).freetradingsim
cors = CORS()
bcrypt = Bcrypt()

app = Flask(__name__)
api = Blueprint('api', __name__)
app.config['SECRET_KEY'] = config.get('SECRET_KEY')

cors.init_app(app)

@app.route('/')
def index():
    return("<h1>FreeTradingSim</h1><p>Check out the api</p>")

#limit requests to 10 per minute or something, don't want people abusing sign up
@api.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json(silent=True)
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = {"email": email,
            "username": username,
            "password": hashed_password}
    user_id = db.users.insert_one(user).inserted_id
    return("User inserted with id: " + str(user_id))

#Should I make this available via api or should I require you to go through the website to generate a token?
@api.route('/create_api_token', methods=['GET'])
def create_api_token():
    token = secrets.token_urlsafe(30)
    hashed_token = bcrypt.generate_password_hash(token).decode('utf-8')
    db.users.update_one({"email": "lukew25073@gmail.com"}, {'$push': {'apiTokens': hashed_token}})
    return token

@api.route('/check_token', methods=['POST', 'GET'])
def check_token():
    data = request.get_json(silent=True)
    username = data.get('username')
    token = data.get('token')
    return str(check_api_token(username, token))

def check_api_token(username, token):
    #should I just check every user for the token hash or prompt for username?
    user = db.users.find_one({"username": username})
    if user:
        for validHash in user['apiTokens']:
            if bcrypt.check_password_hash(validHash, token):
                return True
    return False


def update_price(symbol):
    pair = f"USD/{symbol}"
    tick = yf.Ticker(symbol)
    hist = tick.history(period='1d', interval='1m')
    print(hist)


app.register_blueprint(api, url_prefix='/api')


if __name__ == "__main__":
    app.run(port=5000, debug=True)
