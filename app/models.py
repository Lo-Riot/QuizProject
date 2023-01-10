from enum import Enum
from app import db


class Gender(Enum):
    female = 1
    male = 2


class MaritalStatus(Enum):
    status_1 = "Single without children"
    status_2 = "Single with children"
    status_3 = "Married without children"
    status_4 = "Married with children"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.Enum(Gender))
    age = db.Column(db.Integer)
    place_of_residence = db.Column(db.String)
    martial_status = db.Column()
