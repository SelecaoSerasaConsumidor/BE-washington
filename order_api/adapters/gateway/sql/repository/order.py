import logging
from typing import Dict

from flask import jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from order_api.entities import OrderEntity
from order_api.adapters.gateway.sql.models import OrderModel

LOGGER = logging.getLogger(__name__)


class OrderRepository:

    def __init__(self, bd_url):
        self.engine = create_engine(bd_url)

    def _get_session(self):
        LOGGER.info(f"[User Repository] Creating session...")
        session = Session(self.engine)
        return session

    def insert(self, entity) -> dict:
        """Insert a new order."""
        LOGGER.info(f"[Order Repository] Inserting a new order...")
        session = self._get_session()
        order_model = OrderModel()
        order_entity = OrderEntity().dump(entity)
        order = self._set_model(order_model, order_entity)
        session.add(order)
        session.commit()
        LOGGER.info(f"[Order Repository] The new order inserted.")
        return {"message": "Was saved successfully!"}

    def update(self, id, order) -> dict:
        """Update order."""
        LOGGER.info(f"[Order Repository] Updating a new order {id}...")
        session = self._get_session()
        order_entity = OrderEntity().dump(order)
        result = session.query(OrderModel).filter(OrderModel.id == id).update(order_entity)
        if result > 0:
            session.commit()
            LOGGER.info(f"[Order Repository] The order was updated {id}.")
            return {"message": "Has been updated successfully!"}
        LOGGER.warning(f"[Order Repository] The order wasn't updated {id}.")
        return {"message": "Order does not exist!"}

    def delete(self, order) -> dict:
        """Delete order."""
        LOGGER.info(f"[Order Repository] Deleting order {order}...")
        session = self._get_session()
        session.delete(order)
        session.commit()
        LOGGER.info(f"[Order Repository] User {order} deleted.")
        return {"message": "Has been successfully deleted!"}

    def get_by_id(self, _id) -> Dict[str, str]:
        """Get order by ID."""
        LOGGER.info(f"[Order Repository] Getting order by id {_id}...")
        session = self._get_session()
        order = session.query(OrderModel).filter(OrderModel.id == _id).first()
        if order:
            LOGGER.info(f"[Order Repository] Got order by id {_id}.")
            return OrderEntity().dump(order)
        return {"message": "This order does not exist. contact the admin!"}

    def get_by_name(self, name) -> Dict[str, str]:
        """Get order by name."""
        LOGGER.info(f"[Order Repository] Getting order by name {name}...")
        session = self._get_session()
        order = session.query(OrderModel).filter(OrderModel.name == name).first()
        if order:
            LOGGER.info(f"[Order Repository] Got order by name {name}.")
            return OrderEntity().dump(order)
        return {"message": "This order does not exist. contact the admin!"}

    def get_by_user_id(self, user_id) -> list:
        """Get order by user ID."""
        LOGGER.info(f"[Order Repository] Getting orders by user_id {user_id}...")
        session = self._get_session()
        orders = session.query(OrderModel).filter(OrderModel.user_id == user_id).all()
        if orders:
            LOGGER.info(f"[Order Repository] Got orders by user_id {user_id}...")
            return [OrderEntity().dumps(order) for order in orders]
        return []

    def get_all(self):
        """Get all users."""
        LOGGER.info(f"[Order Repository] Getting all orders...")
        session = self._get_session()
        orders = session.query(OrderModel).filter().all()
        if orders:
            LOGGER.info(f"[Order Repository] Got all orders.")
            return [OrderEntity().dumps(order) for order in orders]
        return []

    @staticmethod
    def _set_model(order_model: OrderModel, order_entity: OrderEntity) -> OrderModel:
        order_model.user_id = order_entity.get("user_id")
        order_model.item_description = order_entity.get("item_description")
        order_model.item_quantity = order_entity.get("item_quantity")
        order_model.item_price = order_entity.get("item_price")
        order_model.total_value = order_entity.get("total_value")
        order_model.created_at = order_entity.get("created_at")
        return order_model
