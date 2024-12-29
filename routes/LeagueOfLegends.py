from flask import Blueprint, render_template, request, redirect, url_for, current_app, render_template_string
import os
import requests
from jinja2 import Template
import json

LeagueOfLegends = Blueprint( "LeagueOfLegends", __name__,)

class LoL_API():
    def __init__(self):
        self.key = os.getenv("RIOT_API_KEY")
        self.puuid = None
    
    def setPuuid(self, userId, tag): 
        response = requests.get(f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{userId}/{tag}?api_key={self.key}")
        if response.status_code != 200:
            return response.status_code 

        data = response.json()
        self.puuid = data["puuid"]
        return 200 

    def getChampionMastery(self):
        response = requests.get(f"https://na1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{self.puuid}?api_key={self.key}")
        data = response.json()
        return data

    def getAccountDetails(self):
        url = f"https://na1.api.riotgames.com/tft/summoner/v1/summoners/by-puuid/{self.puuid}?api_key={self.key}" 
        response = requests.get(url)
        data = response.json()
        level = data['summonerLevel']
        imageId = data['profileIconId']
        image = f"https://ddragon.leagueoflegends.com/cdn/14.24.1/img/profileicon/{imageId}.png"
        return (level, image)

@LeagueOfLegends.route("home")
def goToLeagueOfLegends():
    return render_template("LeagueOfLegends.html")

@LeagueOfLegends.route('LeagueOfLegendsID', methods=['POST'])
def getLeagueOfLegendsID():
    user_id = request.form.get('user-id')
    tag = request.form.get('tag')
    return redirect(url_for('LeagueOfLegends.getStats', user_id=user_id, tag=tag))

@LeagueOfLegends.route('getLoLStats', methods=['GET', 'POST'])
def getStats():
    user_id = request.args.get("user_id")    
    tag = request.args.get("tag")

    api_caller = LoL_API()

    response = api_caller.setPuuid(user_id, tag)  
    if response != 200:
        if response == 403:
           return render_template("error.html", errorMessage = f"Error: {response}, API key expired")  
        return render_template("error.html", errorMessage = f"Error: {response}, User not found") 
    
    profile = api_caller.getAccountDetails()
    print(profile)
    summonerLevel = profile[0]
    pfp = profile[1]

    champions = {}
    listOfChampionsData = requests.get(f"https://ddragon.leagueoflegends.com/cdn/14.24.1/data/en_US/champion.json")
    listOfChampions = listOfChampionsData.json() 

    for champion_data, champion in listOfChampions['data'].items():
        key = int(champion['key'])
        name = champion['name']
        image = f"https://ddragon.leagueoflegends.com/cdn/14.24.1/img/champion/{champion['image']['full']}"
        champions[key] = {'name': name, 'image': image}

    championsData = api_caller.getChampionMastery()
    for champion in championsData:
        id = int(champion['championId'])
        level = champion['championLevel']
        points = champion['championPoints']
        levelUp = champion['championPointsUntilNextLevel']
        stats = [id, level, points, levelUp]
        for stat in stats:
            champions[id][str(stat)] = stat

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
                                    div{
                                    margin: 10px; 
                                    }
                                    #container {
                                    display: flex;
                                    border-width: 10px;
                                    justify-content: center;
                                    flex-direction: row;
                                  align-content: center;
                                    }
                                </style>
                                <center>
                                    <h1>{{ heading }}</h1>
                                    <div id="container">
                                        <div>
                                            <img src="{{ pfp }}">
                                        </div>
                                        <div style="align-self: center" >
                                            <p>{{ name }}</p>
                                            <p>{{ level }}</p>
                                        </div>
                                    </div>
                                        <table>
                                            {% for key, value in games.items() %}
                                                <tr>
                                                    {% for key, value in value.items() %}
                                                        {% if value is string and value.endswith("png") %}
                                                            <td> <img src="{{ value }}"/> </td>
                                                        {% else %}
                                                            <td>{{ value }}</td>
                                                        {% endif %}
                                                    {% endfor %}
                                                </tr>
                                            {% endfor %}
                                        </table>
                                </center>
                            {% endblock %}
                    ''', heading = "Games", games = champions,  name = user_id , level = summonerLevel, pfp = pfp)