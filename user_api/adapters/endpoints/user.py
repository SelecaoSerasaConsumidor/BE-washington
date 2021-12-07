import json

from flask import make_response, jsonify, request
from flask_cors import cross_origin
from flask_restplus import Resource, Namespace, fields
from user_api.business_rules.use_cases.user import UserUseCase
from user_api.entities.user import UserEntity

api = Namespace('user', description='Users API')

user = api.model('user', {
    'name': fields.String(required=True),
    'cpf': fields.String(required=True),
    'email': fields.String(required=True),
    'phone_number': fields.String(required=True)
    }
)


@api.route("/")
class UserAPI(Resource):

    @cross_origin()
    def get(self):
        user_use_case = UserUseCase()
        users = user_use_case.get_all()
        return make_response(jsonify({"users": users}), 200)

    @cross_origin()
    @api.expect(user)
    def post(self):
        user_use_case = UserUseCase()
        user = request.get_json()
        user_entity = UserEntity().dump(user)
        result = user_use_case.insert(user_entity)
        return make_response(jsonify(result), 200)


@api.route("/<int:id>")
class UserDetail(Resource):

    @cross_origin()
    def get(self, id):
        user_use_case = UserUseCase()
        user = user_use_case.get_by_id(id)
        return make_response(jsonify(user), 200)

    @cross_origin()
    def delete(self, id):
        user_use_case = UserUseCase()
        result = user_use_case.delete(id)
        return make_response(jsonify(result), 200)

    @cross_origin()
    @api.expect(user)
    def put(self, id):
        user_use_case = UserUseCase()
        user = request.get_json()
        user_entity = UserEntity().dump(user)
        result = user_use_case.update(id, user_entity)
        return make_response(jsonify(result), 200)


@api.route("/<string:name>")
class UserIntegration(Resource):

    @cross_origin()
    def get(self, name):
        user_use_case = UserUseCase()
        user = user_use_case.get_by_name(name)
        return make_response(jsonify(user), 200)
