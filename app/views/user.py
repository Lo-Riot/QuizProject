from flask import Blueprint, request, jsonify, session
from datetime import datetime
from app.db import db
from app.services import create_user, update_user, create_order


users_bp = Blueprint('users', __name__, url_prefix='/api')


@users_bp.route('/users', methods=["POST"])
def quiz():
    data = request.get_json()
    print(data)
    print(session)
    if data == {'test': 'test'}:
        return jsonify({'success': True})

    user_id = session.get('user_id')
    quiz_answers = (
        data['Gender'],
        data['Age'],
        data['Zip-code'],
        data['Marital status'],
        data['Income'],
    )

    if user_id is not None:
        update_user(user_id, *quiz_answers)
    else:
        user = create_user(*quiz_answers)
        session.clear()
        session['user_id'] = user.id
        session.permanent = True

    db.session.commit()
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
        order_date,
        data['Page']
    )
    db.session.commit()

    return jsonify({'success': True})
