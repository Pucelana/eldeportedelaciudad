from flask import Flask
from flask import render_template, request, redirect,url_for, session
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
from flask_caching import Cache
import os
import uuid

UPLOAD_FOLDER = 'static/imagenes/'
ALLOWED_EXTENSIONS = {'txt','pdf','png','jpg','jpeg','gif'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower()in ALLOWED_EXTENSIONS

# Creado la conexión a la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'app_suculentas'
mysql = MySQL(app)

# Creando el registro del usuario
@app.route('/registro/', methods=['GET', 'POST'])
def sitio_registro():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM tipo_acceso")
    tipo = cursor.fetchall()
    cursor.close()
    notificacion = Notify()
    if request.method == "GET":
        return render_template('sitio/registro.html', tipo = tipo)
    else:
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        tip = request.form['tipo']
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO usuarios(nombre,email,password,id_acceso) VALUES(%s,%s,%s,%s)",(nombre,email,password,tip))
        mysql.connection.commit()
        notificacion.title = "Registro exitoso"
        notificacion.message = "Ya te encuentras registrado en Cactus & Suculentas, ya puedes Iniciar sesión"
        notificacion.send()
        return render_template('sitio/login.html')
    
# Creando el login del usuario        
@app.route('/login/', methods=['GET','POST'])
def sitio_login():
    notificacion = Notify()
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email=%s",(email,))
        user = cursor.fetchone()
        cursor.close()
        if len(user)>0:
            if password == user["password"]:
                session['nombre'] = user['nombre']
                session['email'] = user['email']
                session['tipo'] = user['id_acceso']
                if session['tipo'] == 1:
                    return redirect(url_for('/usuarios/home'))
                elif session['tipo'] == 2:
                    return redirect(url_for('/creadores/home'))
            else:
                notificacion.title = "Error de acceso"
                notificacion.message = "Correo o contraseña no valida"
                notificacion.send()
                return render_template('sitio/login.html')
        else:
            notificacion.title = "Error de acceso"
            notificacion.message = "Este usuario no existe"
            notificacion.send()
            return render_template('sitio/registro.html')
    else:
        return render_template('sitio/login.html')
    
usuarios = {
    'acebesvanesa@gmail.com': 'Pucela83@'
}   
    
# Página del admin    
@app.route('/news', methods=['GET','POST'])
def admin_home():
    usuario = request.form.get('usuario')
    password = request.form.get('password')
    if usuario in usuarios and usuarios[usuario] == password:
        return redirect(url_for('crear_noticia'))
    else:
        return render_template('admin/home.html')

# Página de Noticias
@app.route('/noticias/', methods=['GET','POST'])
def noticias():
    nuevas_noticias = [noticia for noticia in noticias if noticia['publicacion']]
    return render_template('sitio/noticias.html', nuevas_noticias=nuevas_noticias)

# Sección de la creación de las noticias 
noticias = []

# Ruta donde ver las noticias creadas
@app.route('/admin/publi_noticia')
def publi_noticia():
    noticias_publicadas = noticias[:]  
    return render_template('admin/publi_noticia.html', noticias_publicadas=noticias_publicadas)

# Ruta para crear la noticia
@app.route('/admin/crear_noticia', methods=['GET','POST'])
def crear_noticia():
    if request.method == 'GET':
        return render_template('admin/crear_noticia.html')
    
    id_noticia = str(uuid.uuid4())
    
    titulo = request.form.get('titulo')
    contenido = request.form.get('contenido')
    categoria = request.form.get('categoria')
    fecha_publi = request.form.get('fecha_publi')
    if 'imagen' in request.files:
        imagen = request.files['imagen']
        if imagen and allowed_file(imagen.filename):
            filename = secure_filename(imagen.filename)
            imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = None
    else:
        filename = None        
    nueva_noticia = {'id': id_noticia,'titulo': titulo, 'contenido': contenido, 'categoria': categoria, 'fecha_publi': fecha_publi, 'imagen': filename, 'publicacion': False}
    noticias.append(nueva_noticia)
    return redirect(url_for('publi_noticia'))

# Ruta para la publicación de la noticia
@app.route('/publicar_noticia/<string:id>', methods=['POST'])
def publicar_noticia(id):
        texto = next((item for item in noticias if item['id'] == id), None)
        if texto:
           texto['publicacion'] =True
        return redirect(url_for('noticias'))

#Ruta para mostrar las imagenes
@app.route('/imagenes/<imagen>')
def imagenes(imagen):
    print(imagen)
    return send_from_directory(UPLOAD_FOLDER, imagen)       

# Ruta para modificar las noticias
@app.route('/modificar_noticia/<string:id>', methods=['POST'])
def modificar_noticia(id):
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        contenido = request.form.get('contenido')
        categoria = request.form.get('categoria')
        fecha_publi = request.form.get('fecha_publi')
        
        noticia_a_modificar = next((texto for texto in noticias if texto['id'] == id), None)
          
        if noticia_a_modificar:
            noticia_a_modificar['titulo'] = titulo
            noticia_a_modificar['contenido'] = contenido
            noticia_a_modificar['categoria'] = categoria
            noticia_a_modificar['fecha_publi'] = fecha_publi
    return redirect(url_for('publi_noticia')) 

# Página inicio y resultados
@app.route('/')
def sitio_home():
    nuevos_resultados = [dato for dato in resultados if dato['enfrentamiento']]
    return render_template('sitio/home.html', nuevos_resultados=nuevos_resultados)

# Creación de partidos y resultados
resultados = []

# Ruta de los resultados creados
@app.route('/admin/pub_marcadores')
def pub_marcadores():
    resultados_publicados = resultados[:]       
    return render_template('admin/pub_marcadores.html', resultados_publicados=resultados_publicados)

# Ruta de la creación de los resultados
@app.route('/admin/crear_resultados', methods=['GET','POST'])
def crear_resultado():
    if request.method == 'GET':
        return render_template('admin/crear_resultados.html')
    
    id_nuevo = str(uuid.uuid4()) 
     
    seccion = request.form.get('seccion')
    liga = request.form.get('liga')
    equipoA = request.form.get('equipoA')
    resultado1 = request.form.get('resultado1')
    equipoB = request.form.get('equipoB')
    resultado2 = request.form.get('resultado2')
    fecha_parti = request.form.get('fecha_parti')
    nuevo_resultado = {'id': id_nuevo, 'seccion': seccion, 'liga': liga, 'equipoA': equipoA, 'resultado1': resultado1, 'equipoB': equipoB, 'resultado2': resultado2, 'fecha_parti':fecha_parti}
    resultados.append(nuevo_resultado)
    return redirect(url_for('pub_marcadores'))

# Ruta para la publicación de los resultados
@app.route('/publicar_resultados/<string:id>', methods=['POST'])
def publicar_resultados(id):
        marcadores = next((item for item in resultados if item['id'] == id), None)
        if marcadores:
           marcadores['enfrentamiento'] =True
        return redirect(url_for('sitio_home'))  

# Ruta para modificar los resultados
@app.route('/modificar_marcador/<string:id>', methods=['POST'])
def modificar_marcador(id):
    if request.method == 'POST':
        seccion = request.form.get('seccion')
        liga = request.form.get('liga')
        equipoA = request.form.get('equipoA')
        resultado1 = request.form.get('resultado1')
        equipoB = request.form.get('equipoB')
        resultado2 = request.form.get('resultado2')
        fecha_parti = request.form.get('fecha_parti')
        
        marcador_a_modificar = next((marcador for marcador in resultados if marcador['id'] == id), None)
          
        if marcador_a_modificar:
            marcador_a_modificar['seccion'] = seccion
            marcador_a_modificar['liga'] = liga
            marcador_a_modificar['equipoA'] = equipoA
            marcador_a_modificar['resultado1'] = resultado1
            marcador_a_modificar['equipoB'] = equipoB
            marcador_a_modificar['resultado2'] = resultado2
            marcador_a_modificar['fecha_parti'] = fecha_parti
    return redirect(url_for('pub_marcadores'))

# Ruta sección de baloncesto
@app.route('/seccion/baloncesto')
def seccion_baloncesto():
    return render_template('secciones/baloncesto.html')

# Ruta sección de balonmano
@app.route('/seccion/balonmano')
def seccion_balonmano():
    return render_template('secciones/balonmano.html')

# Ruta sección de fútbol
@app.route('/seccion/futbol')
def seccion_futbol():
    return render_template('secciones/futbol.html')

# Ruta sección de hockey línea
@app.route('/seccion/hockey')
def seccion_hockey():
    return render_template('secciones/hockey.html')

# Ruta sección de rugby
@app.route('/seccion/rugby')
def seccion_rugby():
    return render_template('secciones/rugby.html')

# Ruta sección de clasificación y áanalisis del UEMC Valladolid 
@app.route('/equipos_basket/clasif_analisis_uemc')
def clasif_analisis_uemc():
    return render_template('equipos_basket/clasif_analisis_uemc.html')

# Ruta sección de clasificación y áanalisis del Ponce Valladolid 
@app.route('/equipos_basket/clasif_analisis_ponce')
def clasif_analisis_ponce():
    return render_template('equipos_basket/clasif_analisis_ponce.html')

# Ruta sección de clasificación y ánalisis del Fundaión Aliados 
@app.route('/equipos_basket/clasif_analisis_aliados')
def clasif_analisis_aliados():
    return render_template('equipos_basket/clasif_analisis_aliados.html')

# Ruta calendario UEMC
@app.route('/equipos_basket/calendario_uemc')
def calendario_uemc():
    return render_template('equipos_basket/calendario_uemc.html')

# Ruta calendario Ponce Valladolid
@app.route('/equipos_basket/calendario_ponce')
def calendario_ponce():
    return render_template('equipos_basket/calendario_ponce.html')

# Ruta calendario Fundación Aliados
@app.route('/equipos_basket/calendario_aliados')
def calendario_aliados():
    return render_template('equipos_basket/calendario_aliados.html')  


    
            

    


          

            






if __name__ == '__main__':
    app.secret_key = 'pinchellave'
    app.run(debug=True)
 
 