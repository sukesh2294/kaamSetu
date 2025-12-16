from flask import Flask
from flask_session import Session
from .extensions import db,jwt,mail
from .config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    Session(app) 
   

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    from .routes import auth, users, booking, workers

    # Register blueprints
    app.register_blueprint(auth.bp, url_prefix="/auth")
    app.register_blueprint(workers.bp, url_prefix="/workers")
    app.register_blueprint(booking.bp, url_prefix="/bookings")
    app.register_blueprint(users.bp, url_prefix="/users")

    return app


