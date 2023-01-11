from flask import Blueprint, request, jsonify, redirect
from app.db import db
from app.services import create_user


users_bp = Blueprint('users', __name__, url_prefix='/api')


@users_bp.route('/users', methods=["POST"])
def quiz():
    data = request.get_json()
    create_user(
        data['gender'],
        data['age'],
        data['place_of_residence'],
        data['marital_status'],
        data['income']
    )

    db.session.commit()
    return jsonify({'status': "ok"})
