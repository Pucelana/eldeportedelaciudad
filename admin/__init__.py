from flask import Blueprint

admin_blueprint = Blueprint('admin',__name__,template_folder='templates')

from . import admin_routes

def init_app(app):
    app.register_blueprint(admin_blueprint, url_prefix='/admin')