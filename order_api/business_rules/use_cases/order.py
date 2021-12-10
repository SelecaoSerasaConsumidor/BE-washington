import logging
from datetime import datetime
from ast import literal_eval
from flask import jsonify

from order_api.adapters.gateway.sql.repository import OrderRepository
from order_api.adapters.gateway.services import UserIntegration
from order_api.entities import OrderEntity

LOGGER = logging.getLogger(__name__)


class OrderUseCase:

    def __init__(self):
        self.order_repository = OrderRepository("postgresql://postgres:postgres@localhost:5442/order_db")

    def get_by_id(self, _id):
        """Get order by id."""
        LOGGER.info(f"[Order UseCase] Get order by id {_id}")
        return self.order_repository.get_by_id(_id)

    def get_by_name(self, name):
        """Get order by name."""
        LOGGER.info(f"[Order UseCase] Get order by name {name}")
        return self.order_repository.get_by_name(name)

    def get_by_user_id(self, user_id):
        """Get orders by user ID."""
        LOGGER.info(f"[Order UseCase] Get orders by user_id {user_id}.")
        return self.order_repository.get_by_user_id(user_id)

    def get_all(self):
        """Get all orders."""
        LOGGER.info(f"[Order UseCase] Get all orders.")
        return self.order_repository.get_all()

    def insert(self, entity: OrderEntity):
        """Insert a new order."""
        LOGGER.info(f"[Order UseCase] Insert a new order. {entity}")
        user_integration = UserIntegration()
        if user_integration.validate_user_by_user_id(entity["user_id"]):
            entity["created_at"] = datetime.now()
            order = OrderEntity().dump(entity)
            return self.order_repository.insert(order)
        return {"message": "This user does not exist. contact the admin!"}

    def delete(self, _id):
        """Delete order."""
        LOGGER.info(f"[Order UseCase] Delete a order. {_id}")
        order = self.order_repository.get_by_id(_id)
        if order:
            return self.order_repository.delete(order)
        return {"message": "This order does not exist. contact the admin!"}

    def update(self, id, entity: OrderEntity):
        """Update order."""
        LOGGER.info(f"[Order UseCase] Update a order. {id}")
        entity["updated_at"] = datetime.now()
        order = OrderEntity().dump(entity)
        return self.order_repository.update(id, order)
