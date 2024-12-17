import os
from flask import Flask, render_template
from views import views
from routes.roblox import roblox
from routes.Mojang import Mojang
from routes.Steam import Steam
from routes.LeagueOfLegends import LeagueOfLegends
from routes.Valorant import Valorant
from routes.Apex import Apex
from routes.Overwatch import Overwatch
from routes.Account import account
import db
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'TrackIt.sqlite'),
    )
app.config['VALORANT_API_KEY'] = os.getenv('VALORANT_API_KEY')

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

@app.route("/test")
def test():
    return render_template("layout.html")

if __name__=='__main__':
    app.run(debug=True)
