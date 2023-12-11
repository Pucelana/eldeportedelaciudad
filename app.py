from flask import Flask
from flask import render_template, request, redirect,url_for, session
from flask_mysqldb import MySQL
from os import path
import uuid


app = Flask(__name__)

# Creado la conexión a la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'app_suculentas'
mysql = MySQL(app)

# Página Inicio
@app.route('/')
def sitio_home():
    return render_template('sitio/home.html')

# Creacción de noticias
@app.route('/mi_zona/nueva_noticia', methods=['GET','POST'])
def nueva_noticia():
    return redirect(url_for('public_noticia'))

# Publicar nuevas noticias
@app.route('/mi_zona/public_noticia', methods=['GET','POST'])
def public_noticia():
    return redirect(url_for('noticias'))

# Página de Noticias
@app.route('/noticias/', methods=['GET','POST'])
def noticias():
    noticias=[
        {
            
            'titulo': 'Asalto al Wicky Center',
            'contenido': 'El UEMC Valladolid lográ una victoria épica en casa del lider.Con un marcador final 91-92, y tras una prorroga, los jugadores pucelanos mostrarón un rendimiento excepcional, en una emocionante batalla en la cancha.La intensidad del juego mantuvo al público del Wicky Center al borde de sus asientos. Con esta victoria el UEMC Valladolid demuestra su determinación y habilidades excepcionales en esta Leb Oro.',
            'categoria': 'Baloncesto',
            'fecha': 'Publicado: 26-11-2023'
        },
        {
            'titulo': 'Victorias que valen ascensos',
            'contenido': 'El Real Valladolid ganó 0-1 en casa del Huesca donde no había ganado en liga, sin desplegar un buen juego pero haciendo un buen trabajo en lo defensivo. Gracias a un penalti de Monchu, que lo tansformó en el rechace que el portero tocá, mandandoló al palo y vuleve a Monchu que hay no falló. Con esta victoria el Pucela dormira como segundo hasta el partido del lunes del Sporting.',
            'categoria': 'Fútbol',
            'fecha': 'Publicado: 24-11-2023' 
        },
        {
            'titulo': 'La Copa Ibérica viaja a Valladolid',
            'contenido': 'El VRAC se proclamó campeón por primera vez, en la Copa Ibérica ante el equipo portugues, con un resultado ajustado 9-13. Un partido vibrante y emocionante hasta el final,que no se podía ni pestañear. Primera vez que es ganada tanto por el VRAC como por un equipo español.',
            'categoria': 'Rugby',
            'fecha': 'Publicado: 25-11-2023'   
        },
    ]
    return render_template('sitio/noticias.html', noticias=noticias_publicadas)

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
        return redirect('/crear_noticia')
    else:
        return render_template('admin/home.html')

# Sección de la creación de las noticias 
noticias = []
noticias_publicadas = []

@app.route('/admin/crear_noticia', methods=['GET','POST'])
def crear_noticia():
    if request.method == 'GET':
        return render_template('admin/crear_noticia.html')
    titulo = request.form.get('titulo')
    contenido = request.form.get('contenido')
    categoria = request.form.get('categoria')
    fecha_publi = request.form.get('fecha_publi')
    nueva_noticia = {'titulo': titulo, 'contenido': contenido, 'categoria': categoria, 'fecha_publi': fecha_publi}
    noticias.append(nueva_noticia)
    return render_template('admin/publi_noticia.html', noticias=noticias)

@app.route('/admin/publi_noticia')
def publi_noticia():
    for noticia in noticias:
        noticias_publicadas.append(noticia)
    noticias.clear()    
    return render_template('admin/publi_noticia.html', noticias_publicadas=noticias_publicadas)

# Creación de partidos y resultados
resultados = []
resultados_publicados = []

@app.route('/admin/pub_marcadores')
def pub_marcadores():
    for marcador in resultados:
<<<<<<< HEAD
        resultados.append(marcador)    
=======
        resultados.append(marcador)
    resultados.clear()    
>>>>>>> 69369505b0269027869fa8f080baddfc853ca928
    return render_template('admin/pub_marcadores.html', resultados=resultados)

@app.route('/crear_resultados/', methods=['GET','POST'])
def crear_resultado():
    if request.method == 'GET':
        return render_template('admin/.html')
    
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

"""@app.route('/admin/publi_resultados')
def publi_resultados():
    for marcador in resultados:
        resultados_publicados.append(marcador)
    resultados.clear()    
    return render_template('admin/publi_resultados.html', resultados_publicados=resultados_publicados)"""   

@app.route('/modificar_marcador/<int:id>', methods=['POST'])
def modificar_marcador(id):
    if request.method == 'POST':
        seccion = request.form.get('seccion')
        liga = request.form.get('liga')
        equipoA = request.form.get('equipoA')
        resultado1 = request.form.get('resultado1')
        equipoB = request.form.get('equipoB')
        resultado2 = request.form.get('resultado2')
        fecha_parti = request.form.get('fecha_parti')
        
        marcador_a_modificar = next((marcador for marcador in resultados_publicados if marcador['id'] == id), None)
          
        if marcador_a_modificar:
            marcador_a_modificar['seccion'] = seccion
            marcador_a_modificar['liga'] = liga
            marcador_a_modificar['equipoA'] = equipoA
            marcador_a_modificar['resultado1'] = resultado1
            marcador_a_modificar['equipoB'] = equipoB
            marcador_a_modificar['resultado2'] = resultado2
            marcador_a_modificar['fecha_parti'] = fecha_parti
    return redirect(url_for('pub_marcadores'))   


    
            

    


          

            






if __name__ == '__main__':
    app.secret_key = 'pinchellave'
    app.run(debug=True)
 
 