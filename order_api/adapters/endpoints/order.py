import json
import logging

from flask import make_response, jsonify, request
from flask_cors import cross_origin
from flask_restplus import Resource, Namespace, fields
from order_api.business_rules.use_cases import OrderUseCase
from order_api.entities import OrderEntity

api = Namespace('order', description='Orders API')

order = api.model('order', {
    'user_id': fields.Integer(required=True),
    'item_description': fields.String(required=True),
    'item_quantity': fields.Integer(required=True),
    'item_price': fields.Float(required=True),
    'total_value': fields.Float(required=True)
    }
)

LOGGER = logging.getLogger(__name__)


@api.route("/")
class OrderAPI(Resource):

    @cross_origin()
    def get(self):
        LOGGER.info(f"[Order API] Method GET started...")
        order_use_case = OrderUseCase()
        orders = order_use_case.get_all()
        LOGGER.info(f"[Order API] Method GET finished {orders}.")
        return make_response({"orders": orders}, 200)

    @cross_origin()
    @api.expect(order)
    def post(self):
        LOGGER.info(f"[Order API] Method POST started...")
        order_use_case = OrderUseCase()
        order = request.get_json()
        order_entity = OrderEntity().dump(order)
        result = order_use_case.insert(order_entity)
        LOGGER.info(f"[Order API] Method POST finished.")
        return make_response(result, 200)


@api.route("/<int:id>")
class OrderDetail(Resource):

    @cross_origin()
    def get(self, id):
        LOGGER.info(f"[Order API] Method GET by ID started...")
        order_use_case = OrderUseCase()
        order = order_use_case.get_by_id(id)
        LOGGER.info(f"[Order API] Method GET by ID finished.")
        return make_response(order, 200)

    @cross_origin()
    def delete(self, id):
        LOGGER.info(f"[Order API] Method DELETE by ID started...")
        order_use_case = OrderUseCase()
        result = order_use_case.delete(id)
        LOGGER.info(f"[Order API] Method DELETE by ID finished.")
        return make_response(result, 200)

    @cross_origin()
    @api.expect(order)
    def put(self, id):
        LOGGER.info(f"[Order API] Method PUT by ID started...")
        order_use_case = OrderUseCase()
        order = request.get_json()
        order_entity = OrderEntity().dump(order)
        result = order_use_case.update(id, order_entity)
        LOGGER.info(f"[Order API] Method PUT by ID finished.")
        return make_response(result, 200)


@api.route("/user/<int:user_id>")
class OrderIntegration(Resource):

    @cross_origin()
    def get(self, user_id):
        LOGGER.info(f"[Order API] Method GET by USER_ID started...")
        order_use_case = OrderUseCase()
        orders = order_use_case.get_by_user_id(user_id)
        LOGGER.info(f"[Order API] Method GET by USER_ID finished.")
        return make_response({"orders": orders}, 200)
