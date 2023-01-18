from app.db import db

user_order_table = db.Table(
    "user_order",
    db.metadata,
    db.Column("user_id", db.ForeignKey("users.id")),
    db.Column("order_id", db.ForeignKey("orders.id")),
)


class Admin(db.Model):
    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.Enum("Female", "Male", name="gender_type"))
    age = db.Column(db.Enum(
        "20-24", "25-29", "30-34", "35-39", "40-44",
        "45-49", "50-54", "55-59", "60-64", "65-69", "> 70",
        name="age_type"
    ))
    zip_code = db.Column(db.Integer)
    marital_status = db.Column(db.Enum(
        "Single without children",
        "Single with children",
        "Married without children",
        "Married with children",
        name="martial_status_type"
    ))
    income = db.Column(db.Enum(
        "Above average", "Average", "Below average",
        name="income_type"
    ))

    orders = db.relationship(
        "Order", secondary=user_order_table, lazy="selectin"
    )


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    price = db.Column(db.String)
    date = db.Column(db.String)
