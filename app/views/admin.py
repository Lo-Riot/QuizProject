from flask import (
    current_app, Blueprint, request, session,
    redirect, render_template, send_from_directory
)
from werkzeug.security import check_password_hash
from app.services import (
    get_admin_by_username, get_admin_by_id, export_statistics
)


admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        admin = get_admin_by_username(username)
        if admin is not None and check_password_hash(admin.password, password):
            session['admin_id'] = admin.id
            return redirect('/statistics')
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
