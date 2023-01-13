from app.db import db
from app.models import User


def create_user(
    gender: str, age: str, place_of_residence: str,
    marital_status: str, income: str
):
    user = User(
        gender=gender,
        age=age,
        zip_code=place_of_residence,
        marital_status=marital_status,
        income=income
    )
    db.session.add(user)
