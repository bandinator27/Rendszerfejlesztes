from flask import Flask
from config import Config
from flask_migrate import Migrate
from app.database import db
from app.main.blueprint import main_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate = Migrate(app, db, render_as_batch=True)

    app.register_blueprint(main_bp)

    import init_db

    return app