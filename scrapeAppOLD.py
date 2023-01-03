# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
import datetime, random, json
from bs4 import BeautifulSoup
import requests
import re

# create the application object
app = Flask(__name__)

#app.config['SERVER_NAME'] = 'http://dogwater.org:5000'

# very insecure way of doing things b/c key is not random 
# and is not in separate configuration file added to imports
app.secret_key = "my precious"

today = datetime.datetime.now()
jokes=[
        "Who's yo daddy",
        "Your mommy",
        "Joe Biden",
        "Paulage",
        "YOUR DADDY!!!",
        "Slow Biden",
        "Ronald Rump"
]


index = 0

# use decorators to link the function to a url
"""
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')
"""


@app.route('/wiki/<title>/<section>')
def wiki(title, section):
    text = "" + section
    site = requests.get('https://en.wikipedia.org/wiki/' + title)
    soup = BeautifulSoup(site.content, 'lxml')
    for para in soup.find_all('p'):
        text += para.text
    #global stud_name
    return text

@app.route('/wiki/<title>/infobox')
def wikibox(title):
    site = requests.get('https://en.wikipedia.org/wiki/' + title)
    soup = BeautifulSoup(site.content, 'lxml')
    text = ''
    #items = []
    regex = re.compile('infobox.*')
    for info in soup.find('table', {"class":regex}):
        for data in info.find_all('tr'):
            #text += info.text
            #text += "\n"
            dataStr = data.text.replace('\xa0', ' ')
            dataStr = dataStr.replace('\n',' ')
            dataStr = dataStr.replace('\ufeff',' ')
            #items.append(dataStr)
            text += dataStr
        #text += "\n"
    return text
    #return json.dumps(items)

@app.route('/wiki/<title>/table/<identifier>')
def wikitable(title, identifier):
    tableStuff = ""
    site = requests.get('https://en.wikipedia.org/wiki/' + title)
    soup = BeautifulSoup(site.content, 'lxml')
    
    for stuff in soup.find_all('table', {"class":identifier}):
        tableStuff += stuff.get_text()
    

    return tableStuff

@app.route('/wiki/<title>/table')
def wikitable2(title):
    tableStuff = ""
    site = requests.get('https://en.wikipedia.org/wiki/' + title)
    soup = BeautifulSoup(site.content, 'lxml')
    tableList = []
 
    for stuff in soup.find_all('table'):
        #tableStuff += stuff.get_text()
        tableList.append(stuff.get_text())
    return json.dumps(tableList)

# Joke of the day endpoint
@app.route('/joke')
def joke():
    global today
    global index
    print(today)
    if today != datetime.datetime.now():
        temp = index
        index = random.randrange(0, len(jokes)) 
        if index == temp:
            index += 1
        if index == len(jokes):
            index = 0
    return render_template("jokes.html", joke = random.choice(jokes))   #today.strftime("%m/%d/%Y, %H:%M:%S")
    #else:
    #    return "Poop"

# this decorator needs HTTP methods as an argument
# by default, flask assumes that the method is a GET request
# login needs a POST request as well so users can send login
# information to this login endpoint
@app.route('/', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] not in studId.values(): #or request.form['passwd'] != 'admin':
            error = 'Invalid credentials.  Please try again.'
        else:
            session['logged_in'] = True
            #flash(stud_name)
            #return stud_name
            hash = random.getrandbits(20)
            name = str(hash) + request.form['username'] 
            return redirect(url_for('testpt2', name=name))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    # pop the value of True out of session object and replace it with None
    # maybe use session.clear() instead
    #session.pop('logged_in', None)
    session['logged_in'] = False
    session.clear()
    flash('You were just logged out!')
    return redirect(url_for('login'))



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3600)


