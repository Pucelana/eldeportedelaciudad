from flask import render_template, request
from . import admin_blueprint

@admin_blueprint.route('/create-new', methods=['GET','POST'])
def create_new():
    if request.method == 'POST':
        return render_template('new_created.html')
    return render_template('create_new_admin.html')