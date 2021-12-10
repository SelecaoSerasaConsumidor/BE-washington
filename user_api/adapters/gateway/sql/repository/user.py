import logging
from typing import Dict

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from user_api.entities.user import UserEntity
from user_api.adapters.gateway.sql.models import UserModel

LOGGER = logging.getLogger(__name__)


class UserRepository:

    def __init__(self, bd_url):
        self.engine = create_engine(bd_url)

    def _get_session(self):
        """Get Session."""
        LOGGER.info(f"[User Repository] Creating session...")
        session = Session(self.engine)
        return session

    def insert(self, entity) -> dict:
        """Insert a new user."""
        LOGGER.info(f"[User Repository] Inserting a new user...")
        session = self._get_session()
        user_model = UserModel()
        user_entity = UserEntity().dump(entity)
        user = self._set_model(user_model, user_entity)
        session.add(user)
        session.commit()
        LOGGER.info(f"[User Repository] The new user inserted.")
        return {"message": "Saved successfully!"}

    def update(self, id, user) -> dict:
        """Update user."""
        LOGGER.info(f"[User Repository] Updating a new user {id}...")
        session = self._get_session()
        user_entity = UserEntity().dump(user)
        result = session.query(UserModel).filter(UserModel.id == id).update(user_entity)
        if result > 0:
            session.commit()
            LOGGER.info(f"[User Repository] The user was updated {id}.")
            return {"message": "Has been updated successfully!"}
        LOGGER.warning(f"[User Repository] The user wasn't updated {id}.")
        return {"message": "User does not exist!"}

    def delete(self, user) -> dict:
        """Delete user."""
        LOGGER.info(f"[User Repository] Deleting user {user}...")
        session = self._get_session()
        session.delete(user)
        session.commit()
        LOGGER.info(f"[User Repository] User {user} deleted.")
        return {"message": "Has been successfully deleted!"}

    def get_by_id(self, _id) -> Dict[str, str]:
        """Get user by ID."""
        LOGGER.info(f"[User Repository] Getting user by id {_id}...")
        session = self._get_session()
        user = session.query(UserModel).filter(UserModel.id == _id).first()
        if user:
            LOGGER.info(f"[User Repository] Got user by id {_id}.")
            return UserEntity().dump(user)
        return {"message": "This user does not exist. contact the admin!"}

    def get_by_name(self, name) -> Dict[str, str]:
        """Get user by name."""
        LOGGER.info(f"[User Repository] Getting user by name {name}...")
        session = self._get_session()
        user = session.query(UserModel).filter(UserModel.name == name).first()
        if user:
            LOGGER.info(f"[User Repository] Got user by name {name}.")
            return UserEntity().dump(user)
        return {"message": "This user does not exist. contact the admin!"}

    def get_all(self):
        """Get all users."""
        LOGGER.info(f"[User Repository] Getting all users...")
        session = self._get_session()
        users = session.query(UserModel).filter().all()
        if users:
            LOGGER.info(f"[User Repository] Got all users.")
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
