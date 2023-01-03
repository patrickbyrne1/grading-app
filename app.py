# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
import datetime, random, json

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
        "Joe Biden"
]

studId = {"Cameron A":"a8ae97", "Devin G":"128224", "CameronT":"d17857", "Jaxson":"ff044b", "jc":"069da2", 
        "Jeremiah Hawthorne":"be3a3c", "Joshua Mason":"fd7dc6", "kadden":"d9be24", "Katie":"7c78b1", 
        "Nathan McMaster":"16842d", "Parker V":"fb9484", "Tyler Vargas":"6e99ed", "VasillyK":"4248f2",
        "Zachary_Terry":"fa1307", "Heeya Paul":"ea6925"}





"""
# using ID I gave them
studId = {"Cameron A":"a8ae97", "Devin G":"128224", "CameronT":"d17857", "Jaxson":"ff044b", "jc":"069da2", 
        "Jeremiah Hawthorne":"be3a3c", "Joshua Mason":"fd7dc6", "kadden":"d9be24", "Katie":"7c78b1", 
        "Nathan McMaster":"16842d", "Parker V":"fb9484", "Tyler Vargas":"6e99ed", "VasillyK":"4248f2",
        "Zachary_Terry":"fa1307", "Heeya Paul":"ea6925"}


# using student ID from skyward
studId = {"Cameron A":"76171", "Devin G":"07091", "CameronT":"66060", "Jaxson":"01925", "jc":"69385", 
        "Jeremiah Hawthorne":"49562", "Joshua Mason":"96231", "kadden":"49117", "Katie":"43175", 
        "Nathan McMaster":"92121", "Parker V":"83431", "Tyler Vargas":"22066", "VasillyK":"20451", 
        "Heeya Paul": "76262", "Zachary_Terry":"85191"}
"""

print(studId.keys())
# citation: https://www.geeksforgeeks.org/python-get-key-from-value-in-dictionary/
val_list = list(studId.values())
#stud_name=""

with open('./data/students.json', 'r') as studFile:
    data = studFile.read()

# convert file string to json
data = json.loads(data)

with open('./data/studentspt1.json', 'r') as studFile1:
    data1 = studFile1.read()

# convert file string to json
data1 = json.loads(data1)

with open('./data/studentspt2.json', 'r') as studFile2:
    data2 = studFile2.read()

# convert file string to json
data2 = json.loads(data2)
#print(data)

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
@app.route('/changeMe')
def changeMe():
    email = 'Cameron A'
    password = 'poop'
    if email in studId:
        flash('Found you!')
        studId[email] = password
        print(studId)
    else:
        flash('Email not recognized!')
    return render_template('home.html')


@app.route('/tests/<name>')
def tests(name):
    #global stud_name
    correct = 0
    total = 0
    if len(name) < 7:
        error = 'Invalid credentials.  Please try again.'
        return render_template("login.html", error=error)
    stud_name = list(studId.keys())[list(studId.values()).index(name[-6:len(name)])]
    for x in data[stud_name]:
        for y in x:
            if y[3] == "C" or y[4] == "C":
                correct +=1
    total = str(round(correct/20*100, 2)) + "%"
    return render_template('home.html', studId=studId, stud_name=stud_name, data=data, total=total)

@app.route('/testpt1/<name>')
def testpt1(name):
    #global stud_name
    correct = 0
    total = 0
    if len(name) < 7:
        error = 'Invalid credentials.  Please try again.'
        return render_template("login.html", error=error)
    stud_name = list(studId.keys())[list(studId.values()).index(name[-6:len(name)])]
    for x in data1[stud_name]:
        for y in x:
            if y[3] == "C" or y[4] == "C":
                correct +=1
    total = str(round(correct/20*100, 2)) + "%"
    return render_template('home.html', studId=studId, stud_name=stud_name, data=data1, total=total)


@app.route('/testpt2/<name>')
def testpt2(name):
    #global stud_name
   
    correct = 0
    total = 0
    if len(name) < 7:
        error = 'Invalid credentials.  Please try again.'
        return render_template("login.html", error=error)
    stud_name = list(studId.keys())[list(studId.values()).index(name[-6:len(name)])]
    print(stud_name)
    for x in data2[stud_name]:
        for y in x:
            if y[3] == "C" or y[4] == "C":
                correct +=1
    total = str(round(correct/20*100, 2)) + "%"
    return render_template('home.html', studId=studId, stud_name=stud_name, data=data2, total=total)

"""
@app.route('/tests')
def tests():
    return render_template('home.html', studId=studId, stud_name=stud_name, data=data)
"""

@app.route('/choice/<name>')
def choice(name):
    
    stud_name = list(studId.keys())[list(studId.values()).index(name[-6:len(name)])]
    return render_template("test.html", stud_name=stud_name, name=name)

@app.route('/testit/<arg1>/<arg2>')
def testit(arg1=None, arg2=None):
    #arg1 = request.args.get()
    #arg2 = request.args.get()
    return "" + arg1 + " " + arg2



# Joke of the day endpoint
@app.route('/joke_of_the_day')
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
    return jokes[index]   #today.strftime("%m/%d/%Y, %H:%M:%S")
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
            print(name)
            return redirect(url_for('choice', name=name))
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

@app.route('/all_scores')
def all_scores():
    return data
    #return render_template('scores.html', title="scores", jsonfile=json.dumps(data))
    
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")