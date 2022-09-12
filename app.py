from flask import Flask

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import config
from application.pybo.filter import format_datetime
import os

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)

    # Blue Print
    from application.demo.entrypoint import demo_entrypoint
    from application.pybo.pybo_views import bp as pybe_bp
    from application.pybo.answer_view import bp as answer_bp

    app.register_blueprint(demo_entrypoint)
    app.register_blueprint(pybe_bp)
    app.register_blueprint(answer_bp)

    app.jinja_env.filters['datetime'] = format_datetime

    return app
