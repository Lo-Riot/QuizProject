from flask import Blueprint, request, jsonify, session
from datetime import datetime
from app.db import db
from app.services import create_user, create_order


users_bp = Blueprint('users', __name__, url_prefix='/api')


@users_bp.route('/users', methods=["POST"])
def quiz():
    data = request.get_json()
    print(data)
    print(session)
    if data == {'test': 'test'}:
        return jsonify({'success': True})

    user = create_user(
        data['Gender'],
        data['Age'],
        data['Zip-code'],
        data['Marital status'],
        data['Income'],
    )
    db.session.commit()

    session.clear()
    session['user_id'] = user.id
    session.permanent = True

    return jsonify({'success': True})


@users_bp.route('/orders', methods=["POST"])
def order():
    data = request.get_json()
    if data == {'test': 'test'}:
        return jsonify({'success': True})
    print(data)

    order_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    create_order(
        session.get('user_id'),
        data['email'],
        data['variant'],
        order_date
    )
    db.session.commit()

    return jsonify({'success': True})
