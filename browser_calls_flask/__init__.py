from browser_calls_flask.config import config_classes
from flask import Flask

from flask_bootstrap import Bootstrap


# create and configure the app
app = Flask(__name__, instance_relative_config=True)

Bootstrap(app)

# load the instance config, if it exists, when not testing
env = app.config.get('ENV', 'production')
app.config.from_object(config_classes[env])

from . import views  # noqa E402
