# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
import datetime, random, json
import requests
from bs4 import BeautifulSoup

# create the application object
app = Flask(__name__)

#req = requests.get("https://coinmarketcap.com", timeout=1)
req = requests.get("https://api.cryptonator.com/api/ticker/btc-usd/")

soup = BeautifulSoup(req.text, 'lxml')

@app.route("/")
def prices():
    return soup.text



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=4000)