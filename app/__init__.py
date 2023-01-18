import logging
import click

from flask import Flask
from flask_cors import CORS
from werkzeug.security import generate_password_hash

from app.db import db
from app.views.user import users_bp
from app.views.admin import admin_bp

from app.services import create_admin


app = Flask(__name__)
app.config.from_pyfile("application.cfg")

CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}})
logging.getLogger('flask_cors').level = logging.DEBUG
db.init_app(app)

app.register_blueprint(users_bp)
app.register_blueprint(admin_bp)


@app.cli.command("create-admin")
@click.argument('username', nargs=1)
@click.argument('password', nargs=1)
def create_admin_command(username, password):
    create_admin(username, generate_password_hash(password))
    db.session.commit()
