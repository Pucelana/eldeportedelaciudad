from flask import Blueprint

my_admin = Blueprint('my_admin',__name__,template_folder='templates')

from . import admin_routes    