from flask import Flask
from apiflask import APIFlask
from config import Config
from flask_migrate import Migrate
from app.database import db
from app.blueprints import main_bp
from app.blueprints.user import user_bp
from app.blueprints.cars import car_bp
from app.blueprints.rentals import rental_bp

def create_app(config_class=Config):
    app = APIFlask(__name__, json_errors= True,
                   title="Berauto API",
                   docs_path="/swagger")
    app.config.from_object(config_class)

    db.init_app(app)
    migrate = Migrate(app, db, render_as_batch=True)

    app.register_blueprint(main_bp, url_prefix='/api')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(car_bp, url_prefix='/car')
    app.register_blueprint(rental_bp, url_prefix='/rental')

    import init_db

    return app