import logging
from datetime import datetime

from user_api.adapters.gateway.sql.repository.user import UserRepository
from user_api.entities.user import UserEntity


LOGGER = logging.getLogger(__name__)


class UserUseCase:

    def __init__(self):
        self.user_repository = UserRepository("postgresql://postgres:postgres@localhost:5432/user_db")

    def get_by_id(self, _id):
        """Get user by id."""
        LOGGER.info(f"[User UseCase] Get user by id {_id}")
        return self.user_repository.get_by_id(_id)

    def get_by_name(self, name):
        """Get user by name."""
        LOGGER.info(f"[User UseCase] Get user by name {name}")
        return self.user_repository.get_by_name(name)

    def get_all(self):
        """Get all users."""
        LOGGER.info(f"[User UseCase] Get all users.")
        return self.user_repository.get_all()

    def insert(self, entity: UserEntity):
        """Insert a new user."""
        LOGGER.info(f"[User UseCase] Insert a new user. {entity}")
        entity["created_at"] = datetime.now()
        user = UserEntity().dump(entity)
        return self.user_repository.insert(user)

    def delete(self, _id):
        """Delete user."""
        LOGGER.info(f"[User UseCase] Delete a user. {_id}")
        user = self.user_repository.get_by_id(_id)
        if user:
            return self.user_repository.delete(user)
        return {"message": "This user does not exist. contact the admin!"}

    def update(self, id, entity: UserEntity):
        """Update user."""
        LOGGER.info(f"[User UseCase] Update a user. {id}")
        entity["updated_at"] = datetime.now()
        user = UserEntity().dump(entity)
        return self.user_repository.update(id, user)

