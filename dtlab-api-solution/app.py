import os
from flask import Flask

from routers import router_blueprint
from switches import switches_blueprint

from dotenv import load_dotenv


# load environment variables from '.env' file
load_dotenv()

# create flask instance
app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URI")
db_uri = os.getenv("DB_URI")

with open("/run/secrets/postgres_password", "r") as f:
    password = f.readline().strip()
    db_uri = db_uri.replace("__pass__", password)
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri

# db connection ana start application
from models import db

db.init_app(app)

# create all models
with app.app_context():
    db.create_all()


# mount endpoint defined in other files
app.register_blueprint(router_blueprint, url_prefix="/routers")
app.register_blueprint(switches_blueprint, url_prefix="/switches")


@app.route("/", methods=["GET"])
def test() -> str:
    return "Test succeded!"
