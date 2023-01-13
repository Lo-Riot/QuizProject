from flask import Blueprint, request, jsonify, make_response, redirect
from app.db import db
from app.services import create_user


users_bp = Blueprint('users', __name__, url_prefix='/api')


@users_bp.route('/users', methods=["POST"])
def quiz():
    data = request.get_json()
    if data == {'test': 'test'}:
        return jsonify({'success': True})

    create_user(
        data['Gender'],
        data['Age'],
        data['Zip-code'],
        data['Marital status'],
        data['Income']
    )

    db.session.commit()
    return jsonify({'success': True})
