from datetime import datetime

from user_api.adapters.gateway.sql.repository.user import UserRepository
from user_api.entities.user import UserEntity


class UserUseCase:

    def __init__(self):
        self.user_repository = UserRepository("postgresql://postgres:postgres@localhost:5432/user_db")

    def get_by_id(self, _id):
        return self.user_repository.get_by_id(_id)

    def get_by_name(self, name):
        return self.user_repository.get_by_name(name)

    def get_all(self):
        return self.user_repository.get_all()

    def insert(self, entity: UserEntity):
        entity["created_at"] = datetime.now()
        user = UserEntity().dump(entity)
        return self.user_repository.insert(user)

    def delete(self, _id):
        user = self.user_repository.get_by_id(_id)
        if user:
            return self.user_repository.delete(user)
        return {"message": "This user does not exist. contact the admin!"}

    def update(self, id, entity: UserEntity):
        entity["updated_at"] = datetime.now()
        user = UserEntity().dump(entity)
        return self.user_repository.update(id, user)

