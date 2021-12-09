import json

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


@api.route("/")
class OrderAPI(Resource):

    @cross_origin()
    def get(self):
        order_use_case = OrderUseCase()
        orders = order_use_case.get_all()
        return make_response({"orders": orders}, 200)

    @cross_origin()
    @api.expect(order)
    def post(self):
        order_use_case = OrderUseCase()
        order = request.get_json()
        order_entity = OrderEntity().dump(order)
        result = order_use_case.insert(order_entity)
        return make_response(result, 200)


@api.route("/<int:id>")
class OrderDetail(Resource):

    @cross_origin()
    def get(self, id):
        order_use_case = OrderUseCase()
        order = order_use_case.get_by_id(id)
        return make_response(order, 200)

    @cross_origin()
    def delete(self, id):
        order_use_case = OrderUseCase()
        result = order_use_case.delete(id)
        return make_response(result, 200)

    @cross_origin()
    @api.expect(order)
    def put(self, id):
        order_use_case = OrderUseCase()
        order = request.get_json()
        order_entity = OrderEntity().dump(order)
        result = order_use_case.update(id, order_entity)
        return make_response(result, 200)


@api.route("/user/<int:user_id>")
class OrderIntegration(Resource):

    @cross_origin()
    def get(self, user_id):
        order_use_case = OrderUseCase()
        orders = order_use_case.get_by_user_id(user_id)
        return make_response({"orders": orders}, 200)
