from pathlib import Path
from flask import Flask
from config import Config
from .extensions import db, login_manager, migrate, csrf

def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    # Import models so SQLAlchemy metadata is registered before create_all/migrations.
    from . import models  # noqa: F401

    from .auth import auth_bp
    from .main import main_bp

    @login_manager.user_loader
    def load_user(user_id):
        from .models import User
        return db.session.get(User, int(user_id))

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")

    from .cli import register_commands
    register_commands(app)

    @app.get("/api/health")
    def health():
        return {"status": "ok", "service": "Aroma Cafe API"}

    return app
