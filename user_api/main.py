import logging
from user_api import create_app


LOGGER = logging.getLogger(__name__)


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
