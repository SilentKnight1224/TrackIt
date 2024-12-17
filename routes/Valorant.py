from flask import ( Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app)
import requests
from jinja2 import Template
import json
from db import get_db
from dotenv import load_dotenv
import os

load_dotenv()

Valorant = Blueprint( "Valorant", __name__,)

key = os.getenv("VALORANT_API_KEY")

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
    #try:
    name = request.args.get('user_id')
    tag = request.args.get('tag')
    profile = requests.get(f'https://api.henrikdev.xyz/valorant/v1/account/{name}/{tag}?api_key={key}')
    profile = json.loads(profile.content)
    puuid = profile['data']['puuid']
    accountLevel = (profile['data']['account_level'])
    widePic = profile['data']['card']['wide']
    matches = requests.get(f'https://api.henrikdev.xyz/valorant/v1/by-puuid/lifetime/matches/na/{puuid}?=api_key={key}')
    matches = json.loads(matches.content)
    icons = []
    numberOfmatches = matches['results']['total']
    kills = 0
    deaths = 0
    i = 0
    for j in range(0,len(matches['data'])):
        kills += matches['data'][i]['stats']['kills']
        deaths += matches['data'][i]['stats']['deaths']
        i+=1
    estimate = (f'Your estimated kill to death ratio over the past {numberOfmatches} matches is {kills/deaths:.2f}')

    return render_template("myValorantPage.html", title = "my Valorant Stats", accountLevel = accountLevel, estimate = estimate, heading = "My Valorant Stats",img = widePic )
    #except:
        #return render_template("Valorant.html")
 
