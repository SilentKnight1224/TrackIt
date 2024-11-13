import os
from flask import Flask, render_template
from views import views
from roblox import roblox
from Mojang import Mojang
from Steam import Steam
from LeagueOfLegends import LeagueOfLegends
from Valorant import Valorant
from Apex import Apex
from Overwatch import Overwatch
from Account import account
import db

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'TrackIt.sqlite'),
    )
db.init_app(app)
app.register_blueprint(account, url_prefix='/Account')
app.register_blueprint(views, url_prefix="/")
app.register_blueprint(roblox, url_prefix="/")
app.register_blueprint(Mojang, url_prefix="/")
app.register_blueprint(Steam, url_prefix="/")
app.register_blueprint(LeagueOfLegends, url_prefix="/")
app.register_blueprint(Valorant, url_prefix="/")
app.register_blueprint(Apex, url_prefix="/")
app.register_blueprint(Overwatch, url_prefix="/")
db.init_app(app)
@app.route("/")
def index():
    return render_template("index.html")

if __name__=='__main__':
    app.run(debug=True)
