from flask import Flask
from flask_restplus import Api, reqparse

from flask_migrate import Migrate
from order_api.adapters.gateway.sql.models import OrderModel, db
from order_api.entities.order import ma
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.utils import cached_property

from order_api.adapters.endpoints.order import api as order

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

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5442/order_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    api = Api(
        app,
        title='Order API',
        version='1.0',
        description='API',
        # authorizations=authorizations,
        security='apikey',
        doc='/swagger'
    )

    api.add_namespace(order)

    parser = reqparse.RequestParser()
    parser.add_argument('rate', type=int, help='Rate cannot be converted')

    db.init_app(app)
    ma.init_app(app)

    migrate.init_app(app, db)

    return app