from flask import Flask
from flask_redis import Redis
from flask_socketio import SocketIO
from flask_cors import CORS

socketio = SocketIO()
redis = Redis()
cors = CORS()


def create_app(debug=False):
    """Create an application."""
    app = Flask(__name__,
                instance_relative_config=True,
                template_folder="../dist",
                static_folder="../dist/static")
    app.config.from_object('config')
    app.config.from_pyfile('config.py', silent=True)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    cors.init_app(app)
    redis.init_app(app, 'REDIS_ROOMS')
    socketio.init_app(app, cors_allowed_origins="*")
    return app

