# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
import datetime, random, json
from bs4 import BeautifulSoup, NavigableString, Tag
import requests
import re
import unicodedata

# create the application object
app = Flask(__name__)

"""
@app.route("/<country>")
def countryInfo(country):
    countStuff = {}
    site = requests.get('https://wiki-text-scraper.herokuapp.com/wiki/' + country + '/infobox')
    for x in range(len(site)):
        if site[x] == "Population":
             countStuff.update({"Population":site[x+1]})

    return countStuff

"""



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=4000)
    

