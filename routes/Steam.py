from flask import ( Blueprint, flash, g, redirect, render_template, request, session, url_for, render_template_string)
import requests
from dotenv import load_dotenv
import os 
Steam = Blueprint( "Steam", __name__ )

class Steam_API:
    def __init__(self):
        load_dotenv()
        self.key = os.getenv('STEAM_API_KEY')

    def getGames(self, steamId):
        response = requests.get(f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={self.key}&steamid={steamId}&format=json&include_appinfo=true")
        data = response.json()
        return data
    
    def getAchievements(self, steamId, appId):
        response = requests.get(f'https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={appId}&key={self.key}&steamid={steamId}')
        data = response.json()
        return data

@Steam.route("Steam.html")
def goToSteam():
    return render_template("Steam.html")

@Steam.route('SteamID', methods=['POST'])
def getSteamID():
    user_id = request.form.get('user-id')
    return redirect(url_for('Steam.getSteamStats', user_id=user_id))

@Steam.route('SteamStats', methods=['GET', 'POST'])
def getSteamStats():
    if request.method == 'POST':
        return redirect(url_for('Steam.getSteamID'))
    
    steamId = request.args.get('user_id')

    api_caller = Steam_API()
    try:
        gamesData = api_caller.getGames(steamId)
    except:
        return 'User not found' 
    
    games = {}
    for game in gamesData['response']['games']:
        appId = game['appid'] 
        achievementsData = api_caller.getAchievements(steamId, appId) 
        #print(achievementsData)
        count = [0,0]
        if 'error' not in achievementsData['playerstats']:
            for achievement in achievementsData['playerstats']['achievements']:
                if achievement['achieved'] == 1:
                    count[0] += 1
                count[1] += 1 
        img = f' http://media.steampowered.com/steamcommunity/public/images/apps/{appId}/{game["img_icon_url"]}.jpg'
        percentage = f'{count[0]}/{count[1]} achievements'
        playtime = f'{game['playtime_forever']} minutes'
        games[appId] = [ img, game['name'], playtime, percentage]
    
    return render_template_string('''
                                    {% extends "layout.html" %}
                                        {% block body%}
                                            <style>
                                                table {
                                                    width: 50%;
                                                    tr:nth-of-type(odd) {
                                                        background-color:#ccc;
                                                    }
                                                    table tr:nth-child(even) td{
                                                        background:#fff;
                                                    }
                                                } 
                                                td {
                                                    padding: 10px;     
                                                    justify-content: center; 
                                                    text-align: center;
                                                }
                                            </style>
                                            <center>
                                                <h1>{{ heading }}</h1>
                                                    <table>
                                                        {% for key, value in games.items() %}
                                                            <tr>
                                                            {% for i in value %}
                                                                {% if i is string and i.endswith("jpg") %}
                                                                    <td> <img src="{{ i }}"/> </td>
                                                                {% else %}
                                                                    <td>{{ i }}</td>
                                                                {% endif %}
                                                            {% endfor %}
                                                            </tr>
                                                        {% endfor %}
                                                    </table>
                                            </center>
                                        {% endblock %}
                                  ''', heading = "Games", games = games)

