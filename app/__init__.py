from flask import Flask
from flask_cors import CORS
from app.db import db
from app.views import users_bp


app = Flask(__name__)
app.config.from_pyfile("application.cfg")
CORS(app)
db.init_app(app)

app.register_blueprint(users_bp)
