#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time
import threading
import random
import json
import atexit
from flask import Flask, jsonify, redirect, request, render_template, g
from models import Meeting, Person
from redisco.containers import Hash

#from OpenSSL import SSL
#context = SSL.Context(SSL.SSLv23_METHOD)
#context.use_privatekey_file('server.key')
        #context.use_certificate_file('server.crt')


app = Flask(__name__)

# time between votings.
VOTING_TIME = 5.0
VOTE_THRESHOLD = 2
MODEL = 'MODEL'
timer_thread = threading.Thread()

def get_meeting():
    """
    Retrieve a meeting from the database or create one if there isn't one.
    """
    meetings = Meeting.objects.all()
    if len(meetings) < 1:
        meeting = Meeting(name='Meeting without a name')
    else:
        meeting = meetings[0]
    return meeting

@app.route('/')
def index():
    meeting = get_meeting()
    people = meeting.people
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
        'flag': meeting.wave_the_flag
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
    try:
        meeting = get_meeting()
        people = meeting.people
        person = Person.objects.filter(name=name)[0]
    except IndexError:
        return redirect('/')

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
        return render_template('status.html', meeting=meeting, people=meeting.people,
            name=person.name, mustvote=person.mustvote, sthwrong=sthwrong)

    return render_template('thanks.html')

@app.route('/vote/<name>/<button>')
def vote(name, button):
    meeting = get_meeting()
    person = Person.objects.filter(name=name)[0]
    if person is not None:
        person.mustvote = False
        if button == "yes":
            person.voted = 0
        elif button == "no":
            person.voted = 1
        person.save()
        return redirect('/status/%s' % name)

def run_vote():
    """
    This function is called every x seconds by the background thread.
    """
    meeting = get_meeting()
    people = meeting.people
    print("run vote")
    # If the meeting is already gone bad, we don't do anything.
    if meeting.every_one_must_vote:
        print("every one must vote")
        return
    if not meeting.started:
        print("meeting not started")
        return

    total_votes = sum([x.voted for x in people])
    if total_votes > VOTE_THRESHOLD:
        meeting.every_one_must_vote = True
        meeting.save()

    # select randomly
    selected = None
    if len(meeting.people) > 1:
        selected = random.sample(people, 1)[0]

    # People that have voted need not vote again.
    if selected.voted != 1:
        selected.mustvote = True
        selected.save()
        print('selected {} for voting'.format(selected.name))

def setup_app(debug):
    """
    Configure a periodic timer thread.
    """
    def interrupt():
        global timer_thread
        timer_thread.cancel()

    def run_periodically():
        global timer_thread
        run_vote()
        timer_thread = threading.Timer(VOTING_TIME, run_periodically, ())
        timer_thread.start()


    def start_timer_thread():
        global timer_thread
        timer_thread = threading.Timer(VOTING_TIME, run_periodically, ())
        timer_thread.start()

    start_timer_thread()
    atexit.register(interrupt)
    app.config.update(DEBUG=debug)


if __name__ == '__main__':
    setup_app(debug=True)
    app.run(use_reloader=False, host='0.0.0.0') # ssl_context=context)
