import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from order_api import create_app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
