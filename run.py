#https://scotch.io/tutorials/getting-started-with-flask-a-python-microframework

import os
from app import create_app

# set env variable FLASK_CONFIG to 'development' while in development
# >export FLASK_CONFIG='development'
config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
