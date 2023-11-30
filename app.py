from flask import Flask
from flask import render_template, request, redirect,url_for, session
from flask_mysqldb import MySQL
from os import path

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
    return render_template('sitio/noticias.html', noticias=noticias)

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
@app.route('/admin/home')
def creadores_home():
    return render_template('admin/home.html')

@app.route('/usuarios/home')
def usuarios_home():
    return render_template('usuarios/home.html')        
            






if __name__ == '__main__':
    app.secret_key = 'pinchellave'
    app.run(debug=True)
 
 