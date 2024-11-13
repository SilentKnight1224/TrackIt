from flask import ( Blueprint, flash, g, redirect, render_template, request, session, url_for)
import requests
from db import get_db
import requests
from datetime import datetime
from mojang import Client

Mojang = Blueprint(__name__, "Mojang")

@Mojang.route("Mojang.html")
def goToMojang():
    try:
        if g.user:
            db = get_db()
            row = db.execute(
            'SELECT * FROM user WHERE id = ?', (session.get('user_id'),)
            ).fetchone()
            mojang_name = row[7]
            if mojang_name == None:
                return render_template("Mojang.html")
            else:
                return redirect(url_for('Mojang.getMojangStats', user_name=mojang_name))
        else:
            return render_template("Mojang.html")
    except:
        return render_template("Mojang.html")

@Mojang.route('MojangID', methods=['POST'])
def getMojangID():
    user_id = request.form.get('user-id')
    password = request.form.get('password')
    user_name = request.form.get('user-name')
    return redirect(url_for('Mojang.getMojangStats', user_name=user_name))

@Mojang.route('MojangStats', methods=['GET', 'POST'])
def getMojangStats():
    if request.method == 'POST':
        return redirect(url_for('Mojang.getMojangID'))
    try:
    #Placeholder, it is my minecraft account, user input will be needed.
        #user_id = request.args.get('user_id')
        #password = request.args.get('password')
        user_name= request.args.get('user_name')

        uuid_response = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{user_name}')
        uuid = uuid_response.json()['id']
        skin = (f'https://crafatar.com/skins/{uuid}')
        cape =(f'https://crafatar.com/capes/{uuid}')
        body = (f'https://crafatar.com/renders/body/{uuid}')
        avatar = (f'https://crafatar.com/avatars/{uuid}')

        try:
            if g.user != None:
                db = get_db()
                db.execute(
                    'UPDATE user SET mojangname = ? WHERE id = ?',
                    (user_name, session.get('user_id'))
                )
                db.commit()
        except:
            return render_template("index.html")
        return render_template("myMojangPage.html", skin=skin, cape=cape, body=body, avatar=avatar,
                                skin_heading="Skin",cape_heading="Cape", body_heading="Body", avatar_heading="Avatar")
    except:
        return render_template("Mojang.html")
