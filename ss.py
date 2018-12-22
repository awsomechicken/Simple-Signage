from flask import *
#from flask import render_template, request
import os, time

class SimpleSignage(object):
    app = None

    def __init__(self, name):
    #app = SimpleSignage(__name__)
        self.app = Flask(__name__)

    def run(self):
        self.app.run()

app = Flask(__name__)
app.run();

@app.route("/", methods=['GET','POST'])
def hello(name=None, video=None):
    #return 'Hello WOrld! you assah <br> <a href="/display">display</a>'
    return render_template('t-index.html', name="Rowdy")#, video=video())

@app.route("/display")
def display():
    print("SOMEONE IS TOUCHING ME!")
    return 'this will do something too..'

@app.route('/deck', methods=['GET', 'POST'])
def deck(title=None):
    # title: deck title
    return "WIP"

@app.route("/tl")
def video():
    z = url_for('/display')
    print(z)
    return z
