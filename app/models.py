from app.db import db

user_order_table = db.Table(
    "user_order",
    db.metadata,
    db.Column("user_id", db.ForeignKey("users.id", ondelete="CASCADE")),
    db.Column("order_id", db.ForeignKey("orders.id", ondelete="CASCADE")),
)


class Admin(db.Model):
    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String, unique=True)
    gender = db.Column(db.Enum("Female", "Male", name="gender_type"))
    age = db.Column(db.Enum(
        "20-24", "25-29", "30-34", "35-39", "40-44",
        "45-49", "50-54", "55-59", "60-64", "65-69", "> 70",
        name="age_type"
    ))
    zip_code = db.Column(db.Integer)
    marital_status = db.Column(db.Enum(
        "No married without children",
        "No married with children",
        "Married without children",
        "Married with children",
        name="martial_status_type"
    ))
    income = db.Column(db.Enum(
        "Above average", "Average", "Below average",
        name="income_type"
    ))

    orders = db.relationship(
        "Order",
        secondary=user_order_table,
        back_populates="users",
        cascade="all, delete",
        lazy="selectin",
    )


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    price = db.Column(db.String)
    date = db.Column(db.String)
    page = db.Column(db.String)

    users = db.relationship(
        "User",
        secondary=user_order_table,
        back_populates="orders",
    )
