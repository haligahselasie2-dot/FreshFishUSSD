from flask import Flask
from config import Config
from models import db
from ussd.router import ussd_bp
from admin.routes import admin_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    # register blueprints
    app.register_blueprint(ussd_bp, url_prefix="/ussd_api")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    # ensure DB created
    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
