# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 16:57:08 2019

@author: THINK
"""

from flask import Flask
from xundaili import Redis


app = Flask(__name__)

@app.route('/')
def index():
    return "<h2>Welcom to Proxy Pool System</h2>"

@app.route('/random')
def get_proxy():
    db = Redis()
    return db.random().decode('utf-8')

app.run()