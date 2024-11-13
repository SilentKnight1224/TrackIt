from flask import Blueprint, render_template, request, redirect, url_for
import requests
from jinja2 import Template
import json

views = Blueprint(__name__, "views")

#Index
@views.route("index.html")
def goToIndex():
    return render_template("index.html")

#About
@views.route("About.html")
def goToAbout():
    return render_template("About.html")

@views.route("UserGuide.html")
def goToUserGuide():
    return render_template("UserGuide.html")
