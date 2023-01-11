from flask import Flask
from app.db import db
from app.views import users_bp


app = Flask(__name__)
app.config.from_pyfile("application.cfg")
db.init_app(app)

app.register_blueprint(users_bp)
