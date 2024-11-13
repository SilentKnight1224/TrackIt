from flask import Blueprint, render_template, request, redirect, url_for
import requests
from jinja2 import Template
import json

Overwatch = Blueprint(__name__, 'Overwatch')

@Overwatch.route("Overwatch.html")
def goToOverwatch():
    return render_template("Overwatch.html")

@Overwatch.route("OverwatchID", methods= ['POST'])
def getOverwatchID():
    user_id = request.form.get('user-id')
    tag = request.form.get('tag')
    platform = request.form.get('platform')
    region = request.form.get('region')
    return redirect(url_for('Overwatch.getOverwatchStats', user_id=user_id, tag = tag, platform = platform, region = region))

@Overwatch.route("OverwatchID", methods= ['GET', 'POST'])
def getOverwatchStats():
    if request.method == 'POST':
        return redirect(url_for('Overwatch.getOverwatchID'))
    try:
        name = request.args.get('user_id')
        tag = request.args.get('tag')
        platform = request.args.get('platform')
        region = request.args.get('region')
        profile = requests.get(f'http://owapi.io/profile/{platform}/{region}/{name}-{tag}')
        profile = profile.json()
        portrait = profile['portrait']
        stats = []
        for key, value in (profile['games'].items()):
            stats.append(key)
            for a, b in value.items():
                stats.append(f'{a} : {b}')
        stats.append("Playtime")
        for key, value in (profile['playtime'].items()):
            stats.append(f'{key} : {value}')
        #stats +=(profile['competitive'])

        return render_template("myOverwatchPage.html", title = "my OverWatch Stats", stats = stats, img = portrait)
    except:
        return render_template("Overwatch.html")