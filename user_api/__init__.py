from flask import Flask
from flask_restplus import Api, reqparse

from flask_migrate import Migrate
from user_api.adapters.gateway.sql.models.user import UserModel, db
from user_api.entities.user import ma
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.utils import cached_property

from user_api.adapters.endpoints.user import api as user

migrate = Migrate()

# authorizations = {
#     'apikey': {
#         'type': 'apiKey',
#         'in': 'header',
#         'name': 'Authorization',
#         'description': "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'**, where JWT is the token"
#     }
# }


def create_app():
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/user_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    api = Api(
        app,
        title='Users API',
        version='1.0',
        description='API',
        # authorizations=authorizations,
        security='apikey',
        doc='/swagger'
    )

    api.add_namespace(user)

    parser = reqparse.RequestParser()
    parser.add_argument('rate', type=int, help='Rate cannot be converted')

    db.init_app(app)
    ma.init_app(app)

    migrate.init_app(app, db)

    return app
