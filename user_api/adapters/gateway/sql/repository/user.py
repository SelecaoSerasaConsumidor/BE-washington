from datetime import datetime
from typing import Dict

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from user_api.entities.user import UserEntity
from user_api.adapters.gateway.sql.models import UserModel


class UserRepository:

    def __init__(self, bd_url):
        self.engine = create_engine(bd_url)

    def _get_session(self):
        session = Session(self.engine)
        return session

    def insert(self, entity) -> dict:
        session = self._get_session()
        user_model = UserModel()
        user_entity = UserEntity().dump(entity)
        user = self._set_model(user_model, user_entity)
        session.add(user)
        session.commit()
        return {"message": "Was saved successfully!"}

    def update(self, id, user) -> dict:
        session = self._get_session()
        user_entity = UserEntity().dump(user)
        result = session.query(UserModel).filter(UserModel.id == id).update(user_entity)
        if result > 0:
            session.commit()
            return {"message": "Has been updated successfully!"}
        return {"message": "User does not exist!"}

    def delete(self, user) -> dict:
        session = self._get_session()
        session.delete(user)
        session.commit()
        return {"message": "Has been successfully deleted!"}

    def get_by_id(self, _id) -> Dict[str, str]:
        session = self._get_session()
        user = session.query(UserModel).filter(UserModel.id == _id).first()
        if user:
            return UserEntity().dump(user)
        return {"message": "This user does not exist. contact the admin!"}

    def get_by_name(self, name) -> Dict[str, str]:
        session = self._get_session()
        user = session.query(UserModel).filter(UserModel.name == name).first()
        if user:
            return UserEntity().dump(user)
        return {"message": "This user does not exist. contact the admin!"}

    def get_all(self):
        session = self._get_session()
        users = session.query(UserModel).filter().all()
        if users:
            return [UserEntity().dumps(user) for user in users]
        return []

    @staticmethod
    def _set_model(user_model: UserModel, user_entity: UserEntity) -> UserModel:
        user_model.name = user_entity.get("name")
        user_model.cpf = user_entity.get("cpf")
        user_model.email = user_entity.get("email")
        user_model.phone_number = user_entity.get("phone_number")
        user_model.created_at = user_entity.get("created_at")
        return user_model
