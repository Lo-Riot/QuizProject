from flask import Blueprint, request, jsonify, session
from datetime import datetime
from app.db import db
from app.services import (
    get_user_by_uuid, create_user, update_user, create_order
)


users_bp = Blueprint('users', __name__, url_prefix='/api')


@users_bp.route('/users', methods=["POST"])
def quiz():
    data = request.get_json()
    print(data)
    print(session)
    if data == {'test': 'test'}:
        return jsonify({'success': True})

    quiz_answers = (
        data['Gender'],
        data['Age'],
        data['Zip-code'],
        data['Marital status'],
        data['Income'],
    )

    user = get_user_by_uuid(session.get('user_id'))

    if user is not None:
        update_user(user, *quiz_answers)
        db.session.commit()
    else:
        user = create_user(*quiz_answers)
        db.session.commit()

        session.clear()
        session['user_id'] = user.uuid
        session.permanent = True

    return jsonify({'success': True})


@users_bp.route('/orders', methods=["POST"])
def order():
    data = request.get_json()
    if data == {'test': 'test'}:
        return jsonify({'success': True})
    print(data)

    order_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    user = get_user_by_uuid(session.get('user_id'))
    create_order(
        user,
        data['email'],
        data['variant'],
        order_date,
        data['Page']
    )
    db.session.commit()

    return jsonify({'success': True})
