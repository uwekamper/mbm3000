#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import time
from flask import Flask, jsonify, redirect
from flask import render_template
import threading
import random
import json

#from OpenSSL import SSL
#context = SSL.Context(SSL.SSLv23_METHOD)
#context.use_privatekey_file('server.key')
        #context.use_certificate_file('server.crt')

people = [{'name': 'John', 'mustvote': False, 'voted': 0},
            {'name': 'Jane', 'mustvote': False, 'voted': 0,}]
wave_the_flag = {'flag': False}

app = Flask(__name__)

VOTING_PERIOD = 30.0

def getuser(name):
    for person in people:
        print person, name
        if name == person['name']:
            return person
    return None

def start_vote():
    print("starting vote")
    # select randomly
    if len(people) > 1:
        selected = random.sample(people, 1)[0]
        selected['mustvote'] = True
    
t = threading.Timer(VOTING_PERIOD, start_vote)

@app.route('/')
@app.route('/<name>')
def index(name=None):
    return render_template('index.html', name=name)

@app.route('/startmeeting')
def hello():
    wave_the_flag['flag'] = False
    for p in people:
        people.remove(p)
    return render_template('thanks.html')


@app.route('/addperson/<name>')
def addperson(name):
    people.append({'name': name, 'mustvote': False, 'voted': 0})
    return render_template('thanks.html')
    

@app.route('/listpeople')
def listpeople():
    data = json.dumps(people)
    return render_template('people.html', people=people, data=data)

@app.route('/flag')
def flag():
    return jsonify(wave_the_flag)
    
@app.route('/toggleflag')
def toggleflag():
    if wave_the_flag['flag'] == True:
        wave_the_flag['flag'] = False
    else:
        wave_the_flag['flag'] = True
        
    return jsonify(wave_the_flag)
    
@app.route('/status/<name>')
def status(name):
    mustvote = False
    person = getuser(name)
    
    votes = sum([x['voted'] for x in people])
    sthwrong = False
    if votes > 1:
        sthwrong = True
        
    if sthwrong:
        wave_the_flag['flag'] = True
    if person is not None:
        myname = person['name']
        mustvote = person['mustvote']
        return render_template('status.html', name=myname, mustvote=mustvote, sthwrong=sthwrong)
    
    return render_template('thanks.html')
    
@app.route('/vote/<name>/<button>')
def vote(name, button):
    person = getuser(name)
    if person is not None:
        if button == "yes":
            person['voted'] = 0
        elif button == "no":
            person['voted'] = 1
        return redirect('/status/%s' % name)
    
        
    
if __name__ == '__main__':
    app.debug = True
    t.start()
    app.run()
    # app.run(use_reloader=False, host='0.0.0.0') # ssl_context=context)
