from enum import Enum
from app.db import db


class Gender(Enum):
    female = "female"
    male = "male"


class MaritalStatus(Enum):
    status_1 = "Single without children"
    status_2 = "Single with children"
    status_3 = "Married without children"
    status_4 = "Married with children"


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.Enum("female", "male", name="gender_type"))
    age = db.Column(db.Enum(
        "20-24", "25-29", "30-34", "35-39", "40-44",
        "45-49", "50-54", "55-59", "60-64", "65-69", "> 70",
        name="age_type"
    ))
    place_of_residence = db.Column(db.String)
    marital_status = db.Column(db.Enum(
        "Single without children",
        "Single with children",
        "Married without children",
        "Married with children",
        name="martial_status_type"
    ))
    income = db.Column(db.Enum(
        "above average", "average", "below average",
        name="income_type"
    ))
