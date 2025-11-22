from flask import Flask
from config import Config
from models import db
from ussd.router import ussd_bp
from admin.routes import admin_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = "supersecretkey"
    app.config.from_object(Config)
    db.init_app(app)

    # register blueprints
    app.register_blueprint(ussd_bp, url_prefix="/ussd_api")
    app.register_blueprint(admin_bp, url_prefix="/admin")

   # root route
    @app.route("/")
    def index():
        return "TechHarvest system is live!"

    # ensure DB created
    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    import os

    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

