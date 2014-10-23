#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import time
from flask import Flask
from flask import render_template
import threading
#from OpenSSL import SSL
#context = SSL.Context(SSL.SSLv23_METHOD)
#context.use_privatekey_file('server.key')
#context.use_certificate_file('server.crt')


app = Flask(__name__)

@app.route('/')
@app.route('/<name>')
def index(name=None):
    return render_template('index.html', name=name)

# @app.route('/hello')
# @app.route('/hello/<name>')
#def hello(name=None):
#    return render_template('hello.html', name=name)

if __name__ == '__main__':
    app.debug = True
    app.run(use_reloader=False, host='0.0.0.0') # ssl_context=context)
