from flask import ( Blueprint, flash, g, redirect, render_template, request, session, url_for)
import requests
from db import get_db

Steam = Blueprint( "Steam", __name__ )

@Steam.route("Steam.html")
def goToSteam():
    try:
        if g.user:
            db = get_db()
            row = db.execute(
            'SELECT * FROM user WHERE id = ?', (session.get('user_id'),)
            ).fetchone()
            steam_id = row[6]
            if steam_id == None:
                return render_template("Steam.html")
            else:
                return redirect(url_for('Steam.getSteamStats', user_id=steam_id))
        else:
            return render_template("Steam.html")
    except:
        return render_template("Steam.html")

@Steam.route('SteamID', methods=['POST'])
def getSteamID():
    user_id = request.form.get('user-id')
    return redirect(url_for('Steam.getSteamStats', user_id=user_id))

@Steam.route('SteamStats', methods=['GET', 'POST'])
def getSteamStats():
    if request.method == 'POST':
            return redirect(url_for('Steam.getSteamID'))
    try:
        game_playtime = {}
        user_id = request.args.get('user_id', '76561197960434622')
        steam_id = int(user_id)
        api_key = '5D5EC3147B58B6B3BBB3F23BC5A64E6F'
        url1 = f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={api_key}&steamid={steam_id}&format=json'
        url2 = f'https://api.steampowered.com/ISteamApps/GetAppList/v2/'
        response1 = requests.get(url1)
        response2 = requests.get(url2)
        data1 = response1.json()
        games1 = data1['response']['games']
        data2 = response2.json()['applist']['apps']
        numberOfGames = (f'Number of games: {len(games1)}')
        for game1 in games1:
            for app2 in data2:
                if game1["appid"] == app2['appid']:
                    game_name = app2['name']
                    playtime = game1['playtime_forever']
                    game_playtime[game_name] = playtime
                    break
        try:
            if g.user != None:
                db = get_db()
                db.execute(
                    "UPDATE user SET steamid = ? WHERE id = ?",
                    (user_id, session.get('user_id')) 
                )
                db.commit()
        except:
            return render_template("index.html")
        return render_template("mySteamPage.html", title="My Steam Page", heading="My Game List", game_playtime=game_playtime)
    except:
        return render_template("Steam.html")

