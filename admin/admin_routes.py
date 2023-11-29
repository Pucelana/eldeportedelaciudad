from flask import Blueprint, render_template, request

from . import admin_blueprint

@admin.blueprint.router('/create-new', methods=['GET','POST'])
def create_new():
    if request.method == 'POST':
        return render_template('new_created.html')
    return render_template('create_new_admin.html')