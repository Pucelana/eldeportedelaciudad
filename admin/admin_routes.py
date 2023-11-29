from flask import render_template, request, redirect, url_for
from . import admin_blueprint

noticias = []

@admin_blueprint.route('/create_new', methods=['GET','POST'])
def create_new():
    if request.method == 'POST':
        titulo = request.form['titulo']
        contenido = request.form['contenido']
        categoria = request.form['categoria']
        fecha_publi = request.form['fecha_publi']
        
        nueva_noticia = {'titulo': titulo, 'contenido': contenido, 'categoria': categoria, 'fecha_publi':fecha_publi}
        
        noticias.append(nueva_noticia)
         
        return render_template('new_news.html')
    return render_template('create_new.html')