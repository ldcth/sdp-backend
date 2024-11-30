from flask import Blueprint
from .auth import bp as auth_bp
from .admin import bp as admin_bp
from .crawl import bp as crawl_bp
from .dashboard import bp as dashboard_bp
from .links import bp as links_bp
from .model import bp as model_bp
from .settings import bp as settings_bp
from .user import bp as user_bp
from .general import bp as general_bp
from .finetune import bp as finetune_bp


all_blueprints = [
    auth_bp,
    admin_bp,
    crawl_bp,
    dashboard_bp,
    links_bp,
    model_bp,
    settings_bp,
    user_bp,
    general_bp,
    finetune_bp
]

def init_app(app):
    """Register all blueprints with the app"""
    for bp in all_blueprints:
        app.register_blueprint(bp) 