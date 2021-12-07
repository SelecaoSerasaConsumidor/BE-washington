from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class UserModel(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    cpf = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=True)
    phone_number = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=True)



