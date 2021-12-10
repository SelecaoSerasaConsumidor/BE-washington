from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class OrderModel(db.Model):

    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    item_description = db.Column(db.String, nullable=False)
    item_quantity = db.Column(db.Integer, nullable=True)
    item_price = db.Column(db.Float, nullable=True)
    total_value = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=True)
