#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import time
import threading
import random
import json
from flask import Flask, jsonify, redirect, request, render_template, g
from models import Meeting, Person
from redisco.containers import Hash

app = Flask(__name__)

#from OpenSSL import SSL
#context = SSL.Context(SSL.SSLv23_METHOD)
#context.use_privatekey_file('server.key')
        #context.use_certificate_file('server.crt')

VOTING_PERIOD = 30.0

MODEL = 'MODEL'

def get_meeting():
    meetings = Meeting.objects.all()
    if len(meetings) < 1:
        meeting = Meeting(name='Meeting without a name')
    else:
        meeting = meetings[0]
    return meeting

def start_vote():
    print "started voting thread"
    while True:
        meeting = get_meeting()
        time.sleep(VOTING_PERIOD)
        print("starting vote")
        # select randomly
        if len(meeting.people) > 1:
            selected = random.sample(people, 1)[0]
            selected['mustvote'] = True

@app.route('/')
def index():
    meeting = get_meeting()
    people = meeting.people
    print people
    return render_template('index.html', people=people)

@app.route('/clear')
def clear():
    for person in Person.objects.all():
        person.delete()
    for meeting in Meeting.objects.all():
        meeting.delete()
    return redirect('/')

@app.route('/startmeeting')
def startmeeting():
    meeting = get_meeting()
    meeting.started = True
    meeting.save()
    return render_template('thanks.html', msg='Meeting started. Go back in your browser to continue.')

@app.route('/addperson', methods=['POST'])
def addperson():
    meeting = get_meeting()
    names = [x.name for x in meeting.people]
    if request.method == 'POST':
        name = request.form['username']
        if name not in names:
            person = Person(name=name)
            person.save()
            meeting.people.append(person)
            meeting.save()
        return redirect('/status/%s' % name)

@app.route('/listpeople')
def listpeople():
    meeting = get_meeting()
    return render_template('people.html', people=meeting.people, data=meeting.attributes_dict)

@app.route('/flag')
def flag():
    meeting = get_meeting()
    data = {
        'flag': meeting.wave_the_flag == True
    }
    return jsonify(data)

@app.route('/toggleflag')
def toggleflag():
    meeting = get_meeting()
    if meeting.wave_the_flag == True:
        meeting.wave_the_flag = False
    else:
        meeting.wave_the_flag = True
    meeting.save()
    return jsonify({'flag': meeting.wave_the_flag})

@app.route('/status/<name>')
def status(name):
    meeting = get_meeting()
    people = meeting.people
    person = Person.objects.filter(name=name)[0]

    names = [x.name for x in meeting.people]
    if name not in names:
        return redirect('/')

    votes = sum([x.voted for x in meeting.people])
    sthwrong = False
    if votes > 1:
        sthwrong = True

    if sthwrong:
        meeting.wave_the_flag = True
        meeting.save()
    if person is not None:
        return render_template('status.html', meeting=meeting, people=meeting.people, name=person.name, mustvote=person.mustvote, sthwrong=sthwrong)

    return render_template('thanks.html')

@app.route('/vote/<name>/<button>')
def vote(name, button):
    meeting = get_meeting()
    person = Person.objects.filter(name=name)[0]
    if person is not None:
        if button == "yes":
            person.voted = 0
        elif button == "no":
            perso.voted = 1
        person.save()
        return redirect('/status/%s' % name)


if __name__ == '__main__':
    app.config.update(DEBUG=True)
    threading.
    app.run()
    # app.run(use_reloader=False, host='0.0.0.0') # ssl_context=context)
