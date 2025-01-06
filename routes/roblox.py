from flask import ( Blueprint, flash, g, redirect, render_template, request, session, url_for)
import requests
from db import get_db
roblox = Blueprint( "roblox", __name__ )

@roblox.route("Roblox.html")
def goToRoblox():
    try:
        if g.user:
            db = get_db()
            row = db.execute(
            'SELECT * FROM user WHERE id = ?', (session.get('user_id'),)
            ).fetchone()
            roblox_id = row[3]
            if roblox_id == None:
                return render_template("Roblox.html")
            else:
                return redirect(url_for('roblox.getRobloxStats', user_id=roblox_id))
        else:
            return render_template("Roblox.html")
    except:
        return render_template("Roblox.html")

@roblox.route('RobloxID', methods=['POST'])
def getRobloxID():
    user_id = request.form.get('user-id')
    return redirect(url_for('roblox.getRobloxStats', user_id=user_id))

@roblox.route('RobloxStats', methods=['GET', 'POST'])
def getRobloxStats():
    if request.method == 'POST':
        return redirect(url_for('roblox.getRobloxID'))
    try:
        user_id = request.args.get('user_id', '56592984')
        
        response = requests.get(f'https://thumbnails.roblox.com/v1/users/avatar?userIds={user_id}&size=250x250&format=Png&isCircular=false')
        data = response.json()
        img_data = data["data"][0]["imageUrl"]
        
        response = requests.get(f"https://games.roblox.com/v2/users/{user_id}/favorite/games?accessFilter=2&limit=10&sortOrder=Asc")
        data = response.json()
        game_list = {}
        for game in data["data"]:
            game_list[game['name']] = game['name']
        
        response = requests.get(f"https://badges.roblox.com/v1/users/{user_id}/badges?limit=10&sortOrder=Asc")
        data = response.json()
        badges = {}
        for badge in data['data']:
            badges[badge['name']] = badge['name']
        
        if g.user != None:
            db = get_db()
            db.execute(
                "UPDATE user SET roblox = ? WHERE id = ?",
                (user_id, session.get('user_id'))
            )
            db.commit()


        return render_template("myRobloxPage.html", title="My Roblox Page", heading="My Game List", heading2 = "My Achivements", game_list=game_list,badges=badges,img_data=img_data)
    except:
        return render_template("Roblox.html")
