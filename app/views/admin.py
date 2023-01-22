from flask import (
    current_app, Blueprint, request, session,
    redirect, render_template, send_from_directory, jsonify
)
from werkzeug.security import check_password_hash
from app.db import db
from app.services import (
    get_admin_by_username, get_admin_by_id, export_statistics, delete_tables
)


admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/panel', methods=["GET"])
def panel():
    admin_id = session.get('admin_id')
    admin = get_admin_by_id(admin_id)

    if admin is not None:
        return render_template("admin_panel.html")
    else:
        return redirect('/admin/login')


@admin_bp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        admin = get_admin_by_username(username)
        if admin is not None and check_password_hash(admin.password, password):
            session['admin_id'] = admin.id
            return redirect('/admin/panel')

    admin_id = session.get('admin_id')
    admin = get_admin_by_id(admin_id)

    if admin is not None:
        return redirect('/admin/panel')

    return render_template("admin_login.html")


@admin_bp.route('/statistics', methods=["GET"])
def statistics():
    admin_id = session.get('admin_id')
    admin = get_admin_by_id(admin_id)

    if admin is not None:
        statistics_filename = "statistics.xlsx"
        export_statistics(statistics_filename)
        return send_from_directory(
            current_app.config['UPLOAD_FOLDER'], statistics_filename
        )


@admin_bp.route('/reset', methods=["GET"])
def reset_db():
    admin_id = session.get('admin_id')
    admin = get_admin_by_id(admin_id)

    if admin is not None:
        delete_tables()
        db.session.commit()
        return jsonify({'success': True, 'msg': "Данные из всех таблиц удалены."})
