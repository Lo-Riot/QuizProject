from typing import Optional
from openpyxl import Workbook
from openpyxl.utils import get_column_letter

from app.db import db
from app.models import Admin, User, Order


def create_admin(username: str, password: str) -> None:
    admin = Admin(username=username, password=password)
    db.session.add(admin)


def get_admin_by_username(username: str) -> Optional[Admin]:
    stmt = db.select(Admin).where(Admin.username == username)
    result = db.session.execute(stmt)
    admin = result.scalar()
    return admin


def get_admin_by_id(admin_id: int) -> Optional[Admin]:
    admin = db.session.get(Admin, admin_id)
    return admin


def create_user(
    gender: str, age: str, place_of_residence: str,
    marital_status: str, income: str
) -> User:
    user = User(
        gender=gender,
        age=age,
        zip_code=place_of_residence,
        marital_status=marital_status,
        income=income
    )
    db.session.add(user)
    return user


def get_users() -> list[User]:
    stmt = db.select(User).options(db.selectinload(User.orders))
    result = db.session.execute(stmt)
    users = result.scalars().all()
    return users


def create_order(
    user_id: str, email: str, price: str, date: str, page: str
) -> None:
    order = Order(
        email=email,
        price=price,
        date=date,
        page=page
    )
    db.session.add(order)

    user = db.session.get(User, user_id)
    user.orders.append(order)


def export_to_excel() -> Workbook:
    wb = Workbook()
    ws = wb.active
    ws.title = "Статистика"
    users = get_users()

    row = 1
    for user in users:
        for col, user_column in enumerate(user.__table__.columns.keys()):
            ws.cell(column=col+1, row=row, value=getattr(user, user_column))
        row += 1

        for order in user.orders:
            for col, order_column in enumerate(order.__table__.columns.keys()):
                if order_column != 'id':
                    ws.cell(column=col+1, row=row, value=getattr(order, order_column))
            row += 1
        row += 1

    for idx, col in enumerate(ws.columns, 1):
        ws.column_dimensions[get_column_letter(idx)].auto_size = True
    return wb


def export_statistics(filename: str) -> None:
    wb = export_to_excel()
    wb.save(f"uploads/{filename}")
