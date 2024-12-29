from flask import ( Blueprint, redirect, render_template, render_template_string, request, url_for)
import requests
from dotenv import load_dotenv
import os

Valorant = Blueprint( "Valorant", __name__,)

class Valorant_API:
    def __init__(self):
        self.key = os.getenv("VALORANT_API_KEY")

        if not self.key:
            print("Error: API key not found!")
        else:
            print(f"API Key loaded: ${self.key}")

        self.name = None
        self.tag = None
        self.region = None
        self.puuid = None 

    def errorHandler(self, data):
        if 'status' in data.keys():
            if data['status'] == 200:
                return True
            else:
                return False 
        else:
            print(data)
            return False

    # Use this method to set parameters for all other API calls
    def getAccountDetails(self, name, tag):
        response = requests.get(f'https://api.henrikdev.xyz/valorant/v1/account/{name}/{tag}?api_key={self.key}')
        data = response.json() 

        status = self.errorHandler(data)
        if not status:
            return status

        self.name = name
        self.tag = tag
        self.region = data['data']['region']
        self.puuid = data['data']['puuid']
        return data

    def getMatchHistory(self):
        response = requests.get(f'https://api.henrikdev.xyz/valorant/v1/stored-matches/{self.region}/{self.name}/{self.tag}?api_key={self.key}')
        data = response.json()
        return data
 
    def getRankData(self):
        response = requests.get(f'https://api.henrikdev.xyz/valorant/v2/by-puuid/mmr/{self.region}/{self.puuid}?api_key={self.key}')
        data = response.json()
        return data

@Valorant.route("home")
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

    if name == "" or tag == "":
        return "Bad request", 400

    api_caller = Valorant_API()  
    accountData = api_caller.getAccountDetails(name, tag)
    if not accountData:
        return f'User not found' 

    accountLevel = (accountData['data']['account_level'])
    banner = accountData['data']['card']['wide']
    pfp = accountData['data']['card']['small']
    card = accountData['data']['card']['large']

    matchData = api_caller.getMatchHistory()
    kd = []
    if not api_caller.errorHandler(matchData):
        kd = [matchData['errors'][0]['message']]
    else:
        stats = {}
        for match in matchData['data']:
            mode = match['meta']['mode'] 
            sumKills = match['stats']['kills'] 
            sumDeaths = match['stats']['deaths']
            sumAssists = match['stats']['assists'] 
            if mode in stats: 
                sumKills += stats[mode]['kills'] 
                sumDeaths += stats[mode]['deaths']
                sumDeaths += stats[mode]['assists'] 
                stats[mode]['kills'] = sumKills
                stats[mode]['deaths'] = sumDeaths
                stats[mode]['assists'] = sumAssists
                stats[mode]['count'] += 1
            else:
                stats[mode] = { 'kills': sumKills, 'deaths': sumDeaths, 'assists': sumAssists, 'count': 1}
        for i in stats.keys():
            kd.append( f"{i}:\t {stats[i]['kills']}/{stats[i]['deaths']}/{stats[i]['assists']} over {stats[i]['count']} game(s) played ")

    rankData = api_caller.getRankData() 
    if not api_caller.errorHandler(rankData):
        ranks = [rankData['errors'][0]['message']]
    else:
        ranks = [rankData['data']['current_data']['images']['small'], rankData['data']['current_data']['currenttierpatched'], 
                f"Elo: {rankData['data']['current_data']['elo']}", rankData['data']['highest_rank']['patched_tier']] 

    return render_template_string('''
        {% extends "layout.html" %} 
        {% block body%}
            <style>
                .container {
                    background-color: #0059b3;
                    width: 400px;
                    height: 350px;
                    margin: 20px;
                    border: 2px solid black;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }
                .container div {
                    background-color: lightblue;
                    width: 150px;
                    height: 260px;
                    border: 2px solid black;
                    padding: 5px;
                    margin: 10px;
                }
                #box1 {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    flex-direction: column;
                }
                #box2 {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    flex-direction: column;
                }
                p {
                    text-align: center ;
                } 

                .container2 {
                    background-color: #0059b3;
                    width: 800px;
                    height: 700px;
                    margin: 20px;
                    border: 2px solid black; 
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }
                
                .container2 div {
                    background-color: lightblue;
                    float: left;
                    width: 300px;
                    height: 400px;
                    border: 2px solid black;
                    margin: 10px;
                }
                #box3 {
                    width: 400px;
                    height: 650px;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    flex-direction: column;
                }
                #box4 {
                    width: 400px;
                    display: flex;
                    justify-content: center;
                    align-items: left;
                    flex-direction: column;
                }
            </style>
            <center>    
                <h2> <img src="{{ banner }}"> </h2> 
                <div class='container'>
                    <div id='box1'>
                    <img src="{{ pfp }}">  
                    <p> Lv. {{accountLevel}}</p>
                    </div>
                    <div id='box2'>
                        {% for i in rankData %}
                            {% if i.endswith('.png') %}
                                <img src="{{ i }}" alt="Image">
                            {% else %}
                                <p>{{ i }}</p>
                            {% endif %}
                        {% endfor %} 
                    </div>
                </div> 
                <div class='container2'>
                    <div id='box3'>
                        <img src = {{ card }}>
                    </div>
                    <div id='box4'>
                        {% for i in estimate %}
                            <p>{{ i }}</p>
                        {% endfor %}                        
                    </div>
                </div>
            </center>
        {% endblock %}
        ''', accountLevel = accountLevel, estimate = kd, name = name, banner = banner, pfp = pfp, card=card, rankData=ranks)
