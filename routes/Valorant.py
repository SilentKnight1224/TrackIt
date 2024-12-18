from flask import ( Blueprint, flash, g, redirect, render_template, render_template_string, request, session, url_for, current_app)
import requests
from jinja2 import Template
import json
from db import get_db
from dotenv import load_dotenv
import os

Valorant = Blueprint( "Valorant", __name__,)

class Valorant_API:
    def __init__(self):
        load_dotenv()
        self.key = os.getenv("VALORANT_API_KEY")

    def getAccountDetails(self, name, tag):
        response = requests.get(f'https://api.henrikdev.xyz/valorant/v1/account/{name}/{tag}?api_key={self.key}')
        data = response.json() 
        return data

    def getMatchHistory(self, name, tag):
        region = self.getAccountDetails(name, tag)['data']['region']
        response = requests.get(f'https://api.henrikdev.xyz/valorant/v1/stored-matches/{region}/{name}/{tag}?api_key={self.key}')
        data = response.json()
        return data
 
@Valorant.route("Valorant.html")
def goToValorant():
    return render_template("Valorant.html")

@Valorant.route("ValorantID", methods= ['POST'])
def getValorantID():
    user_id = request.form.get('user-id')
    tag = request.form.get('tag')
    return redirect(url_for('Valorant.getValorantStats', user_id=user_id, tag = tag))

@Valorant.route("ValorantID", methods= ['GET', 'POST'])
def getValorantStats():
    if request.method == 'POST':
        return redirect(url_for('Valorant.getValorantID'))

    name = request.args.get('user_id')
    tag = request.args.get('tag')

    if (name and tag) == False:
        return "Bad request", 400

    api_caller = Valorant_API()  
    accountData = api_caller.getAccountDetails(name, tag)

    if accountData['status']:
        if accountData['status'] != 200:
            return accountData, 404

    accountLevel = (accountData['data']['account_level'])
    banner = accountData['data']['card']['wide']
    pfp = accountData['data']['card']['small']
    card = accountData['data']['card']['large']

    matchData = api_caller.getMatchHistory(name, tag) 
    if matchData['status']:
        if matchData['status'] !=200:
            return matchData, 404

    count = 0
    kills = 0
    deaths = 0
    for match in matchData['data']:
        kills += match['stats']['kills']
        deaths += match['stats']['deaths']
        count += 1

    estimate = (f'Your estimated kill to death ratio over the past {count} matches is {kills/deaths:.2f}')
    
    return render_template_string('''
        {% extends "layout.html" %} 
        {% block body%}
        <style>
           .container {
        width: 600px;
        height: 190px;
        padding: 35px 15px 5px;
        margin-bottom: 20px;
      }
      .container:before,
      .container:after {
        content: "";
        display: table;
        clear: both;
      }
      .container div {
        float: left;
        width: 180px;
        height: 160px;
      }
      #box2 {
        margin-left: 30px;
        margin-right: 30px;
      }
      p {
        padding: 5px 10px;
        text-align: center;
      } 
        </style>
        <center>    
            <h2> <img src="{{ banner }}"> </h2> 
            <div class='container'>
                <div id='box1'>
                   <img src="{{ pfp }}">  
                </div>
                <div id='box2'>
                    <p>{{ name }}</p>
                    <p>{{accountLevel}}</p>
                </div>
            </div>
            <img src = {{ card }}>
            <p>{{estimate}}</p>
        </center>
        {% endblock %}
        ''', accountLevel = accountLevel, estimate = estimate, name = name, banner = banner, pfp = pfp, card=card )
