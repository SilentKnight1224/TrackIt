from flask import Blueprint, render_template, request, redirect, url_for

from jinja2 import Template
import json
import requests
from datetime import datetime

import requests
import json


Apex = Blueprint("Apex", __name__)

@Apex.route("Apex.html")
def goToApex():
    return render_template("Apex.html")

@Apex.route("ApexLegends.html")
def goToApexLegends():
    return render_template("myApexPage.html")

@Apex.route("Username", methods=["POST"])
def getUsernameAndPlatform():
    username = request.form.get("Username")
    platform = request.form.get("Platform")
    return redirect(url_for("Apex.getApexStats", username=username, platform=platform))


def timeConvertor(time): # Takes time in minutes as a parameter and returns a string that is formatted in terms of days, hours and minutes. Example return value: 8.0 days 6.0 hours and 15.0 minutes
    days = time // 1440
    if days >= 1:
        time -= (days * 1440)
    
    hours = time // 60
    if hours >= 1:
        time -= (hours * 60)
        
    minutes = time
    
    result = ""
    if days > 0:
        result += str(days) + " day"
        if days > 1:
            result += "s"
    if hours > 0:
        if result:
            result += ", "
        result += str(hours) + " hour"
        if hours > 1:
            result += "s"
    if minutes > 0:
        if result:
            result += " and "
        result += str(minutes) + " minute"
        if minutes > 1:
            result += "s"
    if not result:
        result = "0 minutes"
    
    return result


@Apex.route("ApexStats", methods=["GET", "POST"])
def getApexStats():
    if request.method == "POST":
        return redirect(url_for("Apex.getUsernameAndPlatform"))
    try:
        platform = request.args.get("platform")
        username = request.args.get("username")

        url = f"https://public-api.tracker.gg/v2/apex/standard/profile/{platform}/{username}"

        headers = {
            "TRN-Api-Key": "8f143659-336b-474c-9798-6d8564d2a316",
            "Cookie": "__cf_bm=_uDyLoMlBdCMRiTvOqtpR6zKyv0cLLNko_OT0wYnW.I-1677382263-0-AZ67sX8zljR/XyqtXKsnyi2L+NC5P8BGKjy6V4r0fNTZvMzS493SL+oMpWCaGAhvQ9+iggxcgqzZ1Ze9Ecohj0hhzrKXvlVIM99xlwGkZoFo; X-Mapping-Server=s13",
        }

        response = requests.get(url, headers=headers)

        data = json.loads(response.text)

        counter = 0
        legend_stats = {}

        for segment in data["data"]["segments"]:
            if segment["type"] == "legend":
                counter += 1
                legend_name = segment["metadata"]["name"]
                kills = segment["stats"].get("kills", {}).get("value", 0)
                winning_kills = segment["stats"].get("winningKills", {}).get("value", 0)
                matches_played = segment["stats"].get("matchesPlayed", {}).get("value", 0)

                # Add a new entry to the legend_stats dictionary for this legend
                legend_stats[legend_name] = {
                    "kills": kills,
                    "winning_kills": winning_kills,
                    "matches_played": matches_played,
                }



        overall_stats = {}
        total_kills = data['data']['segments'][0]['stats']['kills']['value']
        total_matches_played = data['data']['segments'][0]['stats']['matchesPlayed']['value']
        approximate_playtime_minutes = total_matches_played * 15
        overall_stats = {
            "total_kills": total_kills,
            "total_matches_played": total_matches_played,
            "approximate_playtime": timeConvertor(approximate_playtime_minutes)
}


        return render_template("myApexPage.html", title="My Apex Page", heading="My Legend List", legend_stats=legend_stats, overall_stats=overall_stats)

    except:
        return render_template("Apex.html")
