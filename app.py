from flask import Flask
from flask import render_template, request, redirect,url_for, session, render_template_string, jsonify, flash
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
from flask_caching import Cache
from collections import defaultdict
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mysqldb import MySQL
from collections import defaultdict
import os
import uuid
import re
import random
#import mysql.connector

UPLOAD_FOLDER = 'static/imagenes/'
ALLOWED_EXTENSIONS = {'txt','pdf','png','jpg','jpeg','gif'}
app = Flask(__name__)

# Definir la función de reemplazo de regex
def regex_replace(s, find, replace):
    import re
    return re.sub(find, replace, s)
# Registrar la función como filtro personalizado en Flask
app.jinja_env.filters['regex_replace'] = regex_replace
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower()in ALLOWED_EXTENSIONS
# Creado la conexión a la base de datos
# Configura tu conexión MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'eldeportedb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

# Admin
@app.route('/news/admin/acceso')
def news():
    return render_template('admin/pub_marcadores.html')
# Cerrar Sesión
@app.route('/cerrar_sesion')
def cerrar_sesion():
    return render_template('sitio/home.html')
# Página de Noticias
"""@app.route('/noticias/', methods=['GET','POST'])
def noticias():
    nuevas_noticias = [noticia for noticia in noticias if noticia['publicacion']]
    return render_template('sitio/noticias.html', nuevas_noticias=nuevas_noticias)
# Sección de la creación de las noticias 
noticias = []
# Ruta donde ver las noticias creadas
@app.route('/admin/publi_noticia')
def publi_noticia():
    noticias_publicadas = noticias[:]  
    return render_template('admin/publi_noticia.html', noticias_publicadas=noticias_publicadas)"""
"""# Ruta para crear la noticia
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
    return redirect(url_for('publi_noticia'))"""
"""# Ruta para la publicación de la noticia
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
    return redirect(url_for('publi_noticia')) """

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
# Ruta sección de fútbol sala
@app.route('/seccion/futbol_sala')
def seccion_futbol_sala():
    return render_template('secciones/futbol_sala.html')
# Ruta sección de hockey línea
@app.route('/seccion/hockey')
def seccion_hockey():
    return render_template('secciones/hockey.html')
# Ruta sección de rugby
@app.route('/seccion/rugby')
def seccion_rugby():
    return render_template('secciones/rugby.html')
# Ruta sección de voleibol
@app.route('/seccion/voleibol')
def seccion_voleibol():
    return render_template('secciones/voleibol.html')
# Ruta sistema ligas futbol
@app.route('/sistema_ligas/futbol')
def sistema_ligas_futbol():
    return render_template('sistema_ligas/sistema_futbol.html')
# Ruta sistema ligas baloncesto
@app.route('/sistema_ligas/baloncesto')
def sistema_ligas_baloncesto():
    return render_template('sistema_ligas/sistema_baloncesto.html')
# Ruta sistema ligas balonmano
@app.route('/sistema_ligas/balonmano')
def sistema_ligas_balonmano():
    return render_template('sistema_ligas/sistema_balonmano.html')
# Ruta sistema ligas rugby
@app.route('/sistema_ligas/rugby')
def sistema_ligas_rugby():
    return render_template('sistema_ligas/sistema_rugby.html')
# Ruta sistema ligas hockey
@app.route('/sistema_ligas/hockey')
def sistema_ligas_hockey():
    return render_template('sistema_ligas/sistema_hockey.html')
# Ruta sistema ligas futbol_sala
@app.route('/sistema_ligas/futbol_sala')
def sistema_ligas_futbol_sala():
    return render_template('sistema_ligas/sistema_futbol_sala.html')
# Ruta sistema ligas voleibol
@app.route('/sistema_ligas/voleibol')
def sistema_ligas_voleibol():
    return render_template('sistema_ligas/sistema_voleibol.html')
# CREACIÓN DE LOS HORARIOS DE LOS DIFERENTES EQUIPOS
# Ruta principal para mostrar los resultados creados
@app.route('/')
def sitio_home():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM horarios')  # Reemplaza 'resultados' por el nombre de tu tabla
    resultados = cur.fetchall()
    cur.close()
    return render_template('index.html', resultados=resultados)
# Ruta de los resultados creados
@app.route('/admin/pub_marcadores')
def pub_marcadores():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM horarios')
    resultados_publicados = cur.fetchall()
    cur.close()
    return render_template('admin/pub_marcadores.html', resultados_publicados=resultados_publicados)
# Ruta de la creación de los resultados
@app.route('/admin/crear_resultados', methods=['GET','POST'])
def crear_resultado():
    if request.method == 'POST':
        id_nuevo = str(uuid.uuid4())
        seccion = request.form.get('seccion')
        liga = request.form.get('liga')
        equipoA = request.form.get('equipoA')
        resultado1 = request.form.get('resultado1')
        equipoB = request.form.get('equipoB')
        resultado2 = request.form.get('resultado2')
        fecha_parti = request.form.get('fecha_parti')
        # Verificar si algún campo es None y asignar valores por defecto
        if seccion is None:
            seccion = ''
        if liga is None:
            liga = ''
        if equipoA is None:
            equipoA = ''    
        if resultado1 is None:
            resultado1 = ''
        if equipoB is None:
            equipoB = ''    
        if resultado2 is None:
            resultado2 = ''
        if fecha_parti is None:
            fecha_parti = ''
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO horarios (id, seccion, liga, equipoA, resultado1, equipoB, resultado2, fecha_partido) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                    (id_nuevo, seccion, liga, equipoA, resultado1, equipoB, resultado2, fecha_parti))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('pub_marcadores'))
    else:
        return render_template('admin/crear_resultados.html')        
# Ruta para modificar los resultados
@app.route('/modificar_marcador/<string:id>', methods=['POST'])
def modificar_marcador(id):
    if request.method == 'POST':
        # Obtener datos del formulario
        seccion = request.form.get('seccion')
        liga = request.form.get('liga')
        equipoA = request.form.get('equipoA')
        resultado1 = request.form.get('resultado1')
        equipoB = request.form.get('equipoB')
        resultado2 = request.form.get('resultado2')
        fecha_parti = request.form.get('fecha_parti')
        # Ejecutar la actualización en la base de datos
        cur = mysql.connection.cursor()
        cur.execute('UPDATE horarios SET seccion=%s, liga=%s, equipoA=%s, resultado1=%s, equipoB=%s, resultado2=%s, fecha_partido=%s WHERE id=%s',
        (seccion, liga, equipoA, resultado1, equipoB, resultado2, fecha_parti, id))
        mysql.connection.commit()
    return redirect(url_for('pub_marcadores'))
# Ruta para eliminar los resultados
@app.route('/eliminar_resultado/<string:id>', methods=['POST'])
def eliminar_resultado(id):
    try:
        print(f"Intentando eliminar resultado con ID: {id}")
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM horarios WHERE id = %s', [id])
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        print(f"Error al eliminar el resultado: {str(e)}")
    return redirect(url_for('pub_marcadores'))

# EQUIPOS BALONCESTO
#Todo el proceso de calendario y clasificación del UEMC
# Ingresar los resultados de los partidos UEMC
@app.route('/admin/crear_calendario_uemc', methods=['POST'])
def ingresar_resultado_uemc():
    if request.method == 'POST':
        nombre_jornada = request.form['nombre']
        num_partidos = int(request.form['num_partidos'])       
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO jornadas_uemc (nombre) VALUES (%s)', (nombre_jornada,))
        jornada_id = cur.lastrowid        
        for i in range(num_partidos):
            fecha = request.form[f'fecha{i}']
            hora = request.form[f'hora{i}']
            local = request.form[f'local{i}']
            resultadoA = request.form[f'resultadoA{i}']
            resultadoB = request.form[f'resultadoB{i}']
            visitante = request.form[f'visitante{i}']          
            cur.execute('INSERT INTO uemc_partidos (jornada_id, fecha, hora, local, resultadoA, resultadoB, visitante) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                        (jornada_id, fecha, hora, local, resultadoA, resultadoB, visitante))       
        mysql.connection.commit()
        cur.close()        
        return redirect(url_for('calendarios_uemc'))   
    return render_template('admin/calend_uemc.html')
# Partidos UEMC
@app.route('/admin/calendario_uemc')
def calendarios_uemc():
    cur = mysql.connection.cursor()
    cur.execute('SELECT id, nombre FROM jornadas_uemc')
    jornadas = cur.fetchall()
    for jornada in jornadas:
        cur.execute('SELECT id, fecha, hora, local, resultadoA, resultadoB, visitante FROM uemc_partidos WHERE jornada_id = %s', (jornada['id'],))
        partidos = cur.fetchall()
        jornada['partidos'] = partidos
    cur.close()
    return render_template('admin/calend_uemc.html', jornadas=jornadas)
# Modificar los partidos de cada jornada
@app.route('/modificar_jornada_uemc/<string:id>', methods=['POST'])
def modificar_jornada_uemc(id):
    nombre_jornada = request.form['nombre']
    num_partidos = int(request.form['num_partidos'])
    cur = mysql.connection.cursor()
    # Actualizar la jornada
    cur.execute('UPDATE jornadas_uemc SET nombre = %s WHERE id = %s', (nombre_jornada, id))
    # Actualizar los partidos de la jornada
    for i in range(num_partidos):
        partido_id = request.form[f'partido_id{i}']
        fecha = request.form[f'fecha{i}']
        hora = request.form[f'hora{i}']
        local = request.form[f'local{i}']
        resultadoA = request.form[f'resultadoA{i}']
        resultadoB = request.form[f'resultadoB{i}']
        visitante = request.form[f'visitante{i}']   
        cur.execute('UPDATE uemc_partidos SET fecha = %s, hora = %s, local = %s, resultadoA = %s, resultadoB = %s, visitante = %s WHERE id = %s',
                    (fecha, hora, local, resultadoA, resultadoB, visitante, partido_id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('calendarios_uemc'))
# Ruta para borrar jornadas
@app.route('/eliminar_jornada_uemc/<string:id>', methods=['POST'])
def eliminar_jornada_uemc(id):
    cur = mysql.connection.cursor()
    # Eliminar los partidos asociados a la jornada
    cur.execute('DELETE FROM uemc_partidos WHERE jornada_id = %s', (id,))
    # Eliminar la jornada
    cur.execute('DELETE FROM jornadas_uemc WHERE id = %s', (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('calendarios_uemc'))
# Obtener datos par UEMC 
def obtener_datos_uemc():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM jornadas_uemc")
    jornadas = cur.fetchall()
    jornadas_con_partidos = []
    for jornada in jornadas:
        cur.execute("SELECT * FROM uemc_partidos WHERE jornada_id = %s", (jornada['id'],))
        partidos = cur.fetchall()
        jornada_con_partidos = {
            'nombre': jornada['nombre'],
            'partidos': partidos
        }       
        jornadas_con_partidos.append(jornada_con_partidos)
    cur.close()
    return jornadas_con_partidos
# Ruta y creación del calendario individual del UEMC
@app.route('/equipos_basket/calendario_uemc')
def calendario_uemc():
    datos = obtener_datos_uemc()
    nuevos_datos_uemc = [dato for dato in datos if dato]
    equipo_uemc = 'UEMC Valladolid'
    tabla_partidos_uemc = {}
    # Iteramos sobre cada jornada y partido
    for jornada in datos:
        for partido in jornada['partidos']:
            equipo_local = partido['local']
            equipo_visitante = partido['visitante']
            resultado_local = partido['resultadoA']
            resultado_visitante = partido['resultadoB']           
            # Verificamos si el UEMC está jugando
            if equipo_local == equipo_uemc or equipo_visitante == equipo_uemc:
                # Determinamos el equipo contrario y los resultados
                if equipo_local == equipo_uemc:
                    equipo_contrario = equipo_visitante
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_uemc = 'C'
                else:
                    equipo_contrario = equipo_local
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_uemc = 'F'
                # Verificamos si el equipo contrario no está en la tabla
                if equipo_contrario not in tabla_partidos_uemc:
                    tabla_partidos_uemc[equipo_contrario] = {'jornadas': {}}                       
                # Verificamos si es el primer o segundo enfrentamiento
                if 'primer_enfrentamiento' not in tabla_partidos_uemc[equipo_contrario]:
                    tabla_partidos_uemc[equipo_contrario]['primer_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_uemc[equipo_contrario]['resultadoA'] = resultado_a
                    tabla_partidos_uemc[equipo_contrario]['resultadoB'] = resultado_b
                elif 'segundo_enfrentamiento' not in tabla_partidos_uemc[equipo_contrario]:
                    tabla_partidos_uemc[equipo_contrario]['segundo_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_uemc[equipo_contrario]['resultadoAA'] = resultado_a
                    tabla_partidos_uemc[equipo_contrario]['resultadoBB'] = resultado_b  
                # Agregamos la jornada y resultados
                if jornada['nombre'] not in tabla_partidos_uemc[equipo_contrario]['jornadas']:
                    tabla_partidos_uemc[equipo_contrario]['jornadas'][jornada['nombre']] = {
                        'resultadoA': resultado_a,
                        'resultadoB': resultado_b,
                        'rol_uemc': rol_uemc
                    }
                # Asignamos los resultados según el rol del UEMC
                if equipo_local == equipo_contrario or equipo_visitante == equipo_contrario:
                  if not tabla_partidos_uemc[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA']:
                    tabla_partidos_uemc[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA'] = resultado_a
                    tabla_partidos_uemc[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoB'] = resultado_b
                    tabla_partidos_uemc[equipo_contrario]['jornadas'][jornada['nombre']]['rol_uemc'] = rol_uemc
                  else:
                    tabla_partidos_uemc[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_uemc[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_uemc[equipo_contrario]['jornadas'][jornada['nombre']]['rol_uemc'] = rol_uemc
                else:
                  if not tabla_partidos_uemc[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA']:
                    tabla_partidos_uemc[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_uemc[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_uemc[equipo_contrario]['jornadas'][jornada['nombre']]['rol_uemc'] = rol_uemc
                  else:
                    tabla_partidos_uemc[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_uemc[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_uemc[equipo_contrario]['jornadas'][jornada['nombre']]['rol_uemc'] = rol_uemc
    return render_template('equipos_basket/calendario_uemc.html', tabla_partidos_uemc=tabla_partidos_uemc, nuevos_datos_uemc=nuevos_datos_uemc)
# Crear la clasificación UEMC
def generar_clasificacion_analisis_baloncesto_uemc(data):
    clasificacion = defaultdict(lambda: {'jugados': 0, 'ganados': 0, 'perdidos': 0, 'favor': 0, 'contra': 0, 'diferencia_canastas': 0, 'puntos': 0})
    for jornada in data:
        for partido in jornada['partidos']:
            equipo_local = partido['local']
            equipo_visitante = partido['visitante']
            resultado_local = partido.get('resultadoA')
            resultado_visitante = partido.get('resultadoB')           
            if resultado_local is None or resultado_visitante is None:
                print(f"Partido sin resultados válidos: {partido}")
                continue            
            try:
                resultado_local = int(resultado_local)
                resultado_visitante = int(resultado_visitante)
            except ValueError:
                print(f"Error al convertir resultados a enteros en el partido {partido}")
                continue
            if resultado_local > resultado_visitante:
                clasificacion[equipo_local]['puntos'] += 2
                clasificacion[equipo_local]['ganados'] += 1
                clasificacion[equipo_visitante]['puntos'] += 1
                clasificacion[equipo_visitante]['perdidos'] += 1
            else:
                clasificacion[equipo_local]['puntos'] += 1
                clasificacion[equipo_local]['perdidos'] += 1
                clasificacion[equipo_visitante]['puntos'] += 2
                clasificacion[equipo_visitante]['ganados'] += 1           
            clasificacion[equipo_local]['jugados'] += 1
            clasificacion[equipo_visitante]['jugados'] += 1
            clasificacion[equipo_local]['favor'] += resultado_local
            clasificacion[equipo_local]['contra'] += resultado_visitante
            clasificacion[equipo_visitante]['favor'] += resultado_visitante
            clasificacion[equipo_visitante]['contra'] += resultado_local
            clasificacion[equipo_local]['diferencia_canastas'] += resultado_local - resultado_visitante
            clasificacion[equipo_visitante]['diferencia_canastas'] += resultado_visitante - resultado_local  
    clasificacion_ordenada = sorted(clasificacion.items(), key=lambda x: (x[1]['puntos'], x[1]['diferencia_canastas']), reverse=True)
    return [{'equipo': equipo, 'datos': datos} for equipo, datos in clasificacion_ordenada]
# Ruta para mostrar la clasificación y análisis del UEMC
@app.route('/equipos_basket/clasif_analisis_uemc/')
def clasif_analisis_uemc():
    data = obtener_datos_uemc()
    # Genera la clasificación y análisis actual
    clasificacion_analisis_uemc = generar_clasificacion_analisis_baloncesto_uemc(data)    
    # Obtén los equipos de la jornada 0
    clubs_uemc = obtener_clubs_uemc()
    # Inicializa las estadísticas de los equipos de la jornada 0 si no están ya en la clasificación
    for club in clubs_uemc:
        if not any(equipo['equipo'] == club['nombre'] for equipo in clasificacion_analisis_uemc):
            equipo = {
                'equipo': club['nombre'],
                'datos': {
                    'puntos': 0,
                    'jugados': 0,
                    'ganados': 0,
                    'empatados': 0,
                    'perdidos': 0,
                    'favor': 0,
                    'contra': 0,
                    'diferencia_goles': 0
                }
            }
            clasificacion_analisis_uemc.append(equipo)
    return render_template('equipos_futbol/clasi_analis_uemc.html', clasificacion_analisis_uemc=clasificacion_analisis_uemc)
# Función para obtener todos los clubes de la jornada 0 desde MySQL
def obtener_clubs_uemc():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM uemc_clubs")
    clubs = cur.fetchall()
    cur.close()
    return [{'id': club['id'], 'nombre': club['nombre']} for club in clubs]
@app.route('/admin/jornada0_uemc', methods=['GET', 'POST'])
def jornada0_uemc():
    if request.method == 'POST':
        if 'equipo' in request.form:
            club = request.form['equipo']
            if club:
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO uemc_clubs (nombre) VALUES (%s)", (club,))
                mysql.connection.commit()
                cur.close()
            return redirect(url_for('jornada0_uemc'))
        elif 'index' in request.form:
            index = int(request.form['index'])
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM uemc_clubs WHERE id = %s", (index + 1,))  # Suponiendo que el ID en MySQL comienza desde 1
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('jornada0_uemc'))
    clubs = obtener_clubs_uemc()
    return render_template('admin/clubs_uemc.html', clubs=clubs, indices=range(len(clubs)))
@app.route('/admin/eliminar_club_uemc/<string:club_id>', methods=['POST'])
def eliminar_club_uemc(club_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM uemc_clubs WHERE id = %s", (club_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('jornada0_uemc'))
# Fin proceso del UEMC

#Todo el proceso de calendario y clasificación del Ponce
# Ingresar los resultados de los partidos Ponce
@app.route('/admin/crear_calendario_ponce', methods=['POST'])
def ingresar_resul_ponce():
    if request.method == 'POST':
        nombre_jornada = request.form['nombre']
        num_partidos = int(request.form['num_partidos'])       
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO jornadas_ponce (nombre) VALUES (%s)', (nombre_jornada,))
        jornada_id = cur.lastrowid        
        for i in range(num_partidos):
            fecha = request.form[f'fecha{i}']
            hora = request.form[f'hora{i}']
            local = request.form[f'local{i}']
            resultadoA = request.form[f'resultadoA{i}']
            resultadoB = request.form[f'resultadoB{i}']
            visitante = request.form[f'visitante{i}']          
            cur.execute('INSERT INTO ponce_partidos (jornada_id, fecha, hora, local, resultadoA, resultadoB, visitante) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                        (jornada_id, fecha, hora, local, resultadoA, resultadoB, visitante))       
        mysql.connection.commit()
        cur.close()
    return redirect(url_for('calend_ponce'))
@app.route('/admin/calendario_ponce')
def calend_ponce():
    cur = mysql.connection.cursor()
    cur.execute('SELECT id, nombre FROM jornadas_ponce')
    jornadas = cur.fetchall()
    for jornada in jornadas:
        cur.execute('SELECT id, fecha, hora, local, resultadoA, resultadoB, visitante FROM ponce_partidos WHERE jornada_id = %s', (jornada['id'],))
        partidos = cur.fetchall()
        jornada['partidos'] = partidos
    cur.close()
    return render_template('admin/calend_ponce.html', jornadas=jornadas)
# Modificar los partidos de cada jornada
@app.route('/modificar_jornada_ponce/<string:id>', methods=['POST'])
def modificar_jorn_ponce(id):
    nombre_jornada = request.form['nombre']
    num_partidos = int(request.form['num_partidos'])
    cur = mysql.connection.cursor()
    # Actualizar la jornada
    cur.execute('UPDATE jornadas_ponce SET nombre = %s WHERE id = %s', (nombre_jornada, id))
    # Actualizar los partidos de la jornada
    for i in range(num_partidos):
        partido_id = request.form[f'partido_id{i}']
        fecha = request.form[f'fecha{i}']
        hora = request.form[f'hora{i}']
        local = request.form[f'local{i}']
        resultadoA = request.form[f'resultadoA{i}']
        resultadoB = request.form[f'resultadoB{i}']
        visitante = request.form[f'visitante{i}']   
        cur.execute('UPDATE ponce_partidos SET fecha = %s, hora = %s, local = %s, resultadoA = %s, resultadoB = %s, visitante = %s WHERE id = %s',
                    (fecha, hora, local, resultadoA, resultadoB, visitante, partido_id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('calend_ponce'))
# Ruta para borrar jornadas
@app.route('/eliminar_jorn_ponce/<string:id>', methods=['POST'])
def eliminar_jorn_ponce(id):
    cur = mysql.connection.cursor()
    # Eliminar los partidos asociados a la jornada
    cur.execute('DELETE FROM ponce_partidos WHERE jornada_id = %s', (id,))
    # Eliminar la jornada
    cur.execute('DELETE FROM jornadas_ponce WHERE id = %s', (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('calend_ponce'))
# Obtener datos par UEMC 
def obtener_datos_ponce():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM jornadas_ponce")
    jornadas = cur.fetchall()
    jornadas_con_partidos = []
    for jornada in jornadas:
        cur.execute("SELECT * FROM ponce_partidos WHERE jornada_id = %s", (jornada['id'],))
        partidos = cur.fetchall()
        jornada_con_partidos = {
            'nombre': jornada['nombre'],
            'partidos': partidos
        }       
        jornadas_con_partidos.append(jornada_con_partidos)
    cur.close()
    return jornadas_con_partidos
# Ruta y creación del calendario individual del Ponce
@app.route('/equipos_basket/calendario_ponce')
def calendarios_ponce():
    datos1 = obtener_datos_ponce()
    nuevos_datos_ponce = [dato for dato in datos1 if dato]
    equipo_ponce = 'Ponce Valladolid'
    tabla_partidos_ponce = {}
    # Iteramos sobre cada jornada y partido
    for jornada in datos1:
        for partido in jornada['partidos']:
            equipo_local = partido['local']
            equipo_visitante = partido['visitante']
            resultado_local = partido['resultadoA']
            resultado_visitante = partido['resultadoB']           
            # Verificamos si el UEMC está jugando
            if equipo_local == equipo_ponce or equipo_visitante == equipo_ponce:
                # Determinamos el equipo contrario y los resultados
                if equipo_local == equipo_ponce:
                    equipo_contrario = equipo_visitante
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_ponce = 'C'
                else:
                    equipo_contrario = equipo_local
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_ponce = 'F'
                # Verificamos si el equipo contrario no está en la tabla
                if equipo_contrario not in tabla_partidos_ponce:
                    tabla_partidos_ponce[equipo_contrario] = {'jornadas': {}}                       
                # Verificamos si es el primer o segundo enfrentamiento
                if 'primer_enfrentamiento' not in tabla_partidos_ponce[equipo_contrario]:
                    tabla_partidos_ponce[equipo_contrario]['primer_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_ponce[equipo_contrario]['resultadoA'] = resultado_a
                    tabla_partidos_ponce[equipo_contrario]['resultadoB'] = resultado_b
                elif 'segundo_enfrentamiento' not in tabla_partidos_ponce[equipo_contrario]:
                    tabla_partidos_ponce[equipo_contrario]['segundo_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_ponce[equipo_contrario]['resultadoAA'] = resultado_a
                    tabla_partidos_ponce[equipo_contrario]['resultadoBB'] = resultado_b  
                # Agregamos la jornada y resultados
                if jornada['nombre'] not in tabla_partidos_ponce[equipo_contrario]['jornadas']:
                    tabla_partidos_ponce[equipo_contrario]['jornadas'][jornada['nombre']] = {
                        'resultadoA': resultado_a,
                        'resultadoB': resultado_b,
                        'rol_ponce': rol_ponce
                    }
                # Asignamos los resultados según el rol del UEMC
                if equipo_local == equipo_contrario or equipo_visitante == equipo_contrario:
                  if not tabla_partidos_ponce[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA']:
                    tabla_partidos_ponce[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA'] = resultado_a
                    tabla_partidos_ponce[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoB'] = resultado_b
                    tabla_partidos_ponce[equipo_contrario]['jornadas'][jornada['nombre']]['rol_ponce'] = rol_ponce
                  else:
                    tabla_partidos_ponce[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_ponce[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_ponce[equipo_contrario]['jornadas'][jornada['nombre']]['rol_ponce'] = rol_ponce
                else:
                  if not tabla_partidos_ponce[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA']:
                    tabla_partidos_ponce[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_ponce[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_ponce[equipo_contrario]['jornadas'][jornada['nombre']]['rol_ponce'] = rol_ponce
                  else:
                    tabla_partidos_ponce[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_ponce[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_ponce[equipo_contrario]['jornadas'][jornada['nombre']]['rol_ponce'] = rol_ponce
    return render_template('equipos_basket/calendario_ponce.html', tabla_partidos_ponce=tabla_partidos_ponce, nuevos_datos_ponce=nuevos_datos_ponce)
# Crear la clasificación Ponce
def generar_clasificacion_analisis_baloncesto_ponce(data):
    clasificacion = defaultdict(lambda: {'jugados': 0, 'ganados': 0, 'perdidos': 0, 'favor': 0, 'contra': 0, 'diferencia_canastas': 0, 'puntos': 0})
    for jornada in data:
        for partido in jornada['partidos']:
            equipo_local = partido['local']
            equipo_visitante = partido['visitante']
            resultado_local = partido.get('resultadoA')
            resultado_visitante = partido.get('resultadoB')           
            if resultado_local is None or resultado_visitante is None:
                print(f"Partido sin resultados válidos: {partido}")
                continue            
            try:
                resultado_local = int(resultado_local)
                resultado_visitante = int(resultado_visitante)
            except ValueError:
                print(f"Error al convertir resultados a enteros en el partido {partido}")
                continue
            if resultado_local > resultado_visitante:
                clasificacion[equipo_local]['puntos'] += 2
                clasificacion[equipo_local]['ganados'] += 1
                clasificacion[equipo_visitante]['puntos'] += 1
                clasificacion[equipo_visitante]['perdidos'] += 1
            else:
                clasificacion[equipo_local]['puntos'] += 1
                clasificacion[equipo_local]['perdidos'] += 1
                clasificacion[equipo_visitante]['puntos'] += 2
                clasificacion[equipo_visitante]['ganados'] += 1           
            clasificacion[equipo_local]['jugados'] += 1
            clasificacion[equipo_visitante]['jugados'] += 1
            clasificacion[equipo_local]['favor'] += resultado_local
            clasificacion[equipo_local]['contra'] += resultado_visitante
            clasificacion[equipo_visitante]['favor'] += resultado_visitante
            clasificacion[equipo_visitante]['contra'] += resultado_local
            clasificacion[equipo_local]['diferencia_canastas'] += resultado_local - resultado_visitante
            clasificacion[equipo_visitante]['diferencia_canastas'] += resultado_visitante - resultado_local  
    clasificacion_ordenada = sorted(clasificacion.items(), key=lambda x: (x[1]['puntos'], x[1]['diferencia_canastas']), reverse=True)
    return [{'equipo': equipo, 'datos': datos} for equipo, datos in clasificacion_ordenada]
# Ruta para mostrar la clasificación y análisis del Ponce
@app.route('/equipos_basket/clasif_analisis_ponce/')
def clasif_analisis_ponce():
    data1 = obtener_datos_ponce()
    # Genera la clasificación y análisis actual
    clasificacion_analisis_ponce = generar_clasificacion_analisis_baloncesto_ponce(data1)    
    # Obtén los equipos de la jornada 0
    clubs_ponce = obtener_clubs_ponce()
    # Inicializa las estadísticas de los equipos de la jornada 0 si no están ya en la clasificación
    for club in clubs_ponce:
        if not any(equipo['equipo'] == club['nombre'] for equipo in clasificacion_analisis_ponce):
            equipo = {
                'equipo': club['nombre'],
                'datos': {
                    'puntos': 0,
                    'jugados': 0,
                    'ganados': 0,
                    'empatados': 0,
                    'perdidos': 0,
                    'favor': 0,
                    'contra': 0,
                    'diferencia_goles': 0
                }
            }
            clasificacion_analisis_ponce.append(equipo)
    return render_template('equipos_futbol/clasi_analis_ponce.html', clasificacion_analisis_ponce=clasificacion_analisis_ponce)
# Crear la Jornada 0, inscribir a los club participantes
def obtener_clubs_ponce():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM ponce_clubs")
    clubs = cur.fetchall()
    cur.close()
    return [{'id': club['id'], 'nombre': club['nombre']} for club in clubs]
@app.route('/admin/jornada0_ponce', methods=['GET', 'POST'])
def jornada0_ponce():
    if request.method == 'POST':
        if 'equipo' in request.form:
            club = request.form['equipo']
            if club:
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO ponce_clubs (nombre) VALUES (%s)", (club,))
                mysql.connection.commit()
                cur.close()
            return redirect(url_for('jornada0_ponce'))
        elif 'index' in request.form:
            index = int(request.form['index'])
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM ponce_clubs WHERE id = %s", (index + 1,))  # Asegúrate que el ID en MySQL comienza desde 1
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('jornada0_ponce'))
    clubs = obtener_clubs_ponce()
    return render_template('admin/clubs_ponce.html', clubs=clubs, indices=range(len(clubs)))
@app.route('/admin/eliminar_club_ponce/<string:club_id>', methods=['POST'])
def eliminar_club_ponce(club_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM ponce_clubs WHERE id = %s", (club_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('jornada0_ponce'))
# Fin proceso Ponce Valladolid

#Todo el proceso de calendario y clasificación de Fundación Aliados
# Ingresar los resultados de los partidos Fundación Aliados
@app.route('/admin/crear_calendario_aliados', methods=['POST'])
def ingresar_resul_aliados():
    if request.method == 'POST':
        nombre_jornada = request.form['nombre']
        num_partidos = int(request.form['num_partidos'])       
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO jornadas_aliados (nombre) VALUES (%s)', (nombre_jornada,))
        jornada_id = cur.lastrowid        
        for i in range(num_partidos):
            fecha = request.form[f'fecha{i}']
            hora = request.form[f'hora{i}']
            local = request.form[f'local{i}']
            resultadoA = request.form[f'resultadoA{i}']
            resultadoB = request.form[f'resultadoB{i}']
            visitante = request.form[f'visitante{i}']          
            cur.execute('INSERT INTO aliados_partidos (jornada_id, fecha, hora, local, resultadoA, resultadoB, visitante) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                        (jornada_id, fecha, hora, local, resultadoA, resultadoB, visitante))       
        mysql.connection.commit()
        cur.close()
    return redirect(url_for('calend_aliados'))
@app.route('/admin/calendario_aliados')
def calend_aliados():
    cur = mysql.connection.cursor()
    cur.execute('SELECT id, nombre FROM jornadas_aliados')
    jornadas = cur.fetchall()
    for jornada in jornadas:
        cur.execute('SELECT id, fecha, hora, local, resultadoA, resultadoB, visitante FROM aliados_partidos WHERE jornada_id = %s', (jornada['id'],))
        partidos = cur.fetchall()
        jornada['partidos'] = partidos
    cur.close()
    return render_template('admin/calend_aliados.html', jornadas=jornadas)
# Modificar los partidos de cada jornada
@app.route('/modificar_jornada_aliados/<string:id>', methods=['POST'])
def modificar_jorn_aliados(id):
    nombre_jornada = request.form['nombre']
    num_partidos = int(request.form['num_partidos'])
    cur = mysql.connection.cursor()
    # Actualizar la jornada
    cur.execute('UPDATE jornadas_aliados SET nombre = %s WHERE id = %s', (nombre_jornada, id))
    # Actualizar los partidos de la jornada
    for i in range(num_partidos):
        partido_id = request.form[f'partido_id{i}']
        fecha = request.form[f'fecha{i}']
        hora = request.form[f'hora{i}']
        local = request.form[f'local{i}']
        resultadoA = request.form[f'resultadoA{i}']
        resultadoB = request.form[f'resultadoB{i}']
        visitante = request.form[f'visitante{i}']   
        cur.execute('UPDATE aliados_partidos SET fecha = %s, hora = %s, local = %s, resultadoA = %s, resultadoB = %s, visitante = %s WHERE id = %s',
                    (fecha, hora, local, resultadoA, resultadoB, visitante, partido_id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('calend_aliados'))
# Ruta para borrar jornadas
@app.route('/eliminar_jorn_aliados/<string:id>', methods=['POST'])
def eliminar_jorn_aliados(id):
    cur = mysql.connection.cursor()
    # Eliminar los partidos asociados a la jornada
    cur.execute('DELETE FROM aliados_partidos WHERE jornada_id = %s', (id,))
    # Eliminar la jornada
    cur.execute('DELETE FROM jornadas_aliados WHERE id = %s', (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('calend_aliados'))
# Obtener datos para Aliados
def obtener_datos_aliados():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM jornadas_aliados")
    jornadas = cur.fetchall()
    jornadas_con_partidos = []
    for jornada in jornadas:
        cur.execute("SELECT * FROM aliados_partidos WHERE jornada_id = %s", (jornada['id'],))
        partidos = cur.fetchall()
        jornada_con_partidos = {
            'nombre': jornada['nombre'],
            'partidos': partidos
        }       
        jornadas_con_partidos.append(jornada_con_partidos)
    cur.close()
    return jornadas_con_partidos
# Ruta y creación del calendario individual del Ponce
@app.route('/equipos_basket/calendario_aliados')
def calendarios_aliados():
    datos2 = obtener_datos_aliados()
    nuevos_datos_aliados = [dato for dato in datos2 if dato]
    equipo_aliados = 'Fundación Aliados'
    tabla_partidos_aliados = {}
    # Iteramos sobre cada jornada y partido
    for jornada in datos2:
        for partido in jornada['partidos']:
            equipo_local = partido['local']
            equipo_visitante = partido['visitante']
            resultado_local = partido['resultadoA']
            resultado_visitante = partido['resultadoB']           
            # Verificamos si el UEMC está jugando
            if equipo_local == equipo_aliados or equipo_visitante == equipo_aliados:
                # Determinamos el equipo contrario y los resultados
                if equipo_local == equipo_aliados:
                    equipo_contrario = equipo_visitante
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_aliados = 'C'
                else:
                    equipo_contrario = equipo_local
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_aliados = 'F'
                # Verificamos si el equipo contrario no está en la tabla
                if equipo_contrario not in tabla_partidos_aliados:
                    tabla_partidos_aliados[equipo_contrario] = {'jornadas': {}}                       
                # Verificamos si es el primer o segundo enfrentamiento
                if 'primer_enfrentamiento' not in tabla_partidos_aliados[equipo_contrario]:
                    tabla_partidos_aliados[equipo_contrario]['primer_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_aliados[equipo_contrario]['resultadoA'] = resultado_a
                    tabla_partidos_aliados[equipo_contrario]['resultadoB'] = resultado_b
                elif 'segundo_enfrentamiento' not in tabla_partidos_aliados[equipo_contrario]:
                    tabla_partidos_aliados[equipo_contrario]['segundo_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_aliados[equipo_contrario]['resultadoAA'] = resultado_a
                    tabla_partidos_aliados[equipo_contrario]['resultadoBB'] = resultado_b  
                # Agregamos la jornada y resultados
                if jornada['nombre'] not in tabla_partidos_aliados[equipo_contrario]['jornadas']:
                    tabla_partidos_aliados[equipo_contrario]['jornadas'][jornada['nombre']] = {
                        'resultadoA': resultado_a,
                        'resultadoB': resultado_b,
                        'rol_aliados': rol_aliados
                    }
                # Asignamos los resultados según el rol del UEMC
                if equipo_local == equipo_contrario or equipo_visitante == equipo_contrario:
                  if not tabla_partidos_aliados[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA']:
                    tabla_partidos_aliados[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA'] = resultado_a
                    tabla_partidos_aliados[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoB'] = resultado_b
                    tabla_partidos_aliados[equipo_contrario]['jornadas'][jornada['nombre']]['rol_aliados'] = rol_aliados
                  else:
                    tabla_partidos_aliados[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_aliados[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_aliados[equipo_contrario]['jornadas'][jornada['nombre']]['rol_aliados'] = rol_aliados
                else:
                  if not tabla_partidos_aliados[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA']:
                    tabla_partidos_aliados[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_aliados[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_aliados[equipo_contrario]['jornadas'][jornada['nombre']]['rol_aliados'] = rol_aliados
                  else:
                    tabla_partidos_aliados[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_aliados[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_aliados[equipo_contrario]['jornadas'][jornada['nombre']]['rol_aliados'] = rol_aliados
    return render_template('equipos_basket/calendario_aliados.html', tabla_partidos_aliados=tabla_partidos_aliados, nuevos_datos_aliados=nuevos_datos_aliados)
# Crear la clasificación Fundación Aliados
def generar_clasificacion_analisis_baloncesto_aliados(data):
    default_dict = defaultdict(lambda: {})
    clasificacion = defaultdict(lambda: {'jugados': 0, 'ganados': 0, 'perdidos': 0, 'favor': 0, 'contra': 0, 'diferencia_canastas': 0, 'puntos': 0})
    print(clasificacion)
    for jornada in data:
        for partido in jornada['partidos']:
            equipo_local = partido['local']
            equipo_visitante = partido['visitante']
            try:
                result_local = int(partido['resultadoA'])
                result_visitante = int(partido['resultadoB'])
            except ValueError:
                print(f"Error al convertir resultados a enteros en el partido {partido}")
                continue
            if clasificacion[equipo_local]['jugados'] > 0:
                promedio_favor_local = clasificacion[equipo_local]['favor'] / clasificacion[equipo_local]['jugados']
            else:
                promedio_favor_local = 0
            # Ajusta la lógica según tus reglas para asignar puntos y calcular estadísticas en baloncesto
            if result_local > result_visitante:
                clasificacion[equipo_local]['puntos'] += 2
                clasificacion[equipo_local]['ganados'] += 1
                clasificacion[equipo_visitante]['puntos'] += 1
                clasificacion[equipo_visitante]['perdidos'] += 1
            else:
                clasificacion[equipo_local]['puntos'] += 1
                clasificacion[equipo_local]['perdidos'] += 1
                clasificacion[equipo_visitante]['puntos'] += 2
                clasificacion[equipo_visitante]['ganados'] += 1
            clasificacion[equipo_local]['jugados'] += 1
            clasificacion[equipo_visitante]['jugados'] += 1
            clasificacion[equipo_local]['favor'] += result_local
            clasificacion[equipo_local]['contra'] += result_visitante
            clasificacion[equipo_visitante]['favor'] += result_visitante
            clasificacion[equipo_visitante]['contra'] += result_local
            clasificacion[equipo_local]['diferencia_canastas'] += result_local - result_visitante
            clasificacion[equipo_visitante]['diferencia_canastas'] += result_visitante - result_local
    # Ordena la clasificación por puntos y diferencia de canastas
    clasificacion_ordenada = [{'equipo': equipo, 'datos': datos} for equipo, datos in sorted(clasificacion.items(), key=lambda x: (x[1]['puntos'], x[1]['diferencia_canastas']), reverse=True)]
    print(generar_clasificacion_analisis_baloncesto_aliados)
    return clasificacion_ordenada
# Ruta para mostrar la clasificación y análisis del Ponce
@app.route('/equipos_basket/clasif_analisis_aliados/')
def clasif_analisis_aliados():
    data2 = obtener_datos_aliados()
    # Genera la clasificación y análisis actual
    clasificacion_analisis_aliados = generar_clasificacion_analisis_baloncesto_aliados(data2)    
    # Obtén los equipos de la jornada 0
    clubs_aliados = obtener_clubs_aliados()
    # Inicializa las estadísticas de los equipos de la jornada 0 si no están ya en la clasificación
    for club in clubs_aliados:
        if not any(equipo['equipo'] == club['nombre'] for equipo in clasificacion_analisis_aliados):
            equipo = {
                'equipo': club['nombre'],
                'datos': {
                    'puntos': 0,
                    'jugados': 0,
                    'ganados': 0,
                    'empatados': 0,
                    'perdidos': 0,
                    'favor': 0,
                    'contra': 0,
                    'diferencia_goles': 0
                }
            }
            clasificacion_analisis_aliados.append(equipo)
    return render_template('equipos_futbol/clasi_analis_aliados.html', clasificacion_analisis_aliados=clasificacion_analisis_aliados)
# Crear la Jornada 0, inscribir a los club participantes
def obtener_clubs_aliados():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM aliados_clubs")
    clubs = cur.fetchall()
    cur.close()
    return [{'id': club['id'], 'nombre': club['nombre']} for club in clubs]
@app.route('/admin/jornada0_aliados', methods=['GET', 'POST'])
def jornada0_aliados():
    if request.method == 'POST':
        if 'equipo' in request.form:
            club = request.form['equipo']
            if club:
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO aliados_clubs (nombre) VALUES (%s)", (club,))
                mysql.connection.commit()
                cur.close()
            return redirect(url_for('jornada0_aliados'))
        elif 'index' in request.form:
            index = int(request.form['index'])
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM aliados_clubs WHERE id = %s", (index + 1,))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('jornada0_aliados'))
    clubs = obtener_clubs_aliados()
    return render_template('admin/clubs_aliados.html', clubs=clubs, indices=range(len(clubs)))
@app.route('/admin/eliminar_club_aliados/<string:club_id>', methods=['POST'])
def eliminar_club_aliados(club_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM aliados_clubs WHERE id = %s", (club_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('jornada0_aliados'))
# Fin proceso Fundación Aliados

# EQUIPOS FÚTBOL
#Todo el proceso de calendario y clasificación del Real Valladolid
# Ingresar los resultados de los partidos del Real Valladolid
@app.route('/admin/crear_calendario_valladolid', methods=['POST'])
def ingresar_resul_valladolid():
    if request.method == 'POST':
        nombre_jornada = request.form['nombre']
        num_partidos = int(request.form['num_partidos'])       
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO jornadas_valladolid (nombre) VALUES (%s)', (nombre_jornada,))
        jornada_id = cur.lastrowid        
        for i in range(num_partidos):
            fecha = request.form[f'fecha{i}']
            hora = request.form[f'hora{i}']
            local = request.form[f'local{i}']
            resultadoA = request.form[f'resultadoA{i}']
            resultadoB = request.form[f'resultadoB{i}']
            visitante = request.form[f'visitante{i}']          
            cur.execute('INSERT INTO valladolid_partidos (jornada_id, fecha, hora, local, resultadoA, resultadoB, visitante) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                        (jornada_id, fecha, hora, local, resultadoA, resultadoB, visitante))       
        mysql.connection.commit()
        cur.close()
    return redirect(url_for('calend_valladolid'))
# Partidos Real Valladolid
@app.route('/admin/calend_valladolid')
def calend_valladolid():
    cur = mysql.connection.cursor()
    cur.execute('SELECT id, nombre FROM jornadas_valladolid')
    jornadas = cur.fetchall()
    for jornada in jornadas:
        cur.execute('SELECT id, fecha, hora, local, resultadoA, resultadoB, visitante FROM valladolid_partidos WHERE jornada_id = %s', (jornada['id'],))
        partidos = cur.fetchall()
        jornada['partidos'] = partidos
    cur.close()
    return render_template('admin/calend_valladolid.html', jornadas=jornadas)
# Modificar los partidos de cada jornada
@app.route('/modificar_jornada_valladolid/<string:id>', methods=['POST'])
def modificar_jorn_valladolid(id):
    nombre_jornada = request.form['nombre']
    num_partidos = int(request.form['num_partidos'])
    cur = mysql.connection.cursor()
    # Actualizar la jornada
    cur.execute('UPDATE jornadas_valladolid SET nombre = %s WHERE id = %s', (nombre_jornada, id))
    # Actualizar los partidos de la jornada
    for i in range(num_partidos):
        partido_id = request.form[f'partido_id{i}']
        fecha = request.form[f'fecha{i}']
        hora = request.form[f'hora{i}']
        local = request.form[f'local{i}']
        resultadoA = request.form[f'resultadoA{i}']
        resultadoB = request.form[f'resultadoB{i}']
        visitante = request.form[f'visitante{i}']   
        cur.execute('UPDATE valladolid_partidos SET fecha = %s, hora = %s, local = %s, resultadoA = %s, resultadoB = %s, visitante = %s WHERE id = %s',
                    (fecha, hora, local, resultadoA, resultadoB, visitante, partido_id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('calend_valladolid'))
# Ruta para borrar jornadas
@app.route('/eliminar_jorn_valladolid/<string:id>', methods=['POST'])
def eliminar_jorn_valladolid(id):
    cur = mysql.connection.cursor()
    # Eliminar los partidos asociados a la jornada
    cur.execute('DELETE FROM valladolid_partidos WHERE jornada_id = %s', (id,))
    # Eliminar la jornada
    cur.execute('DELETE FROM jornadas_valladolid WHERE id = %s', (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('calend_valladolid'))
# Obtener datos para Real Valladolid
def obtener_datos_valladolid():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM jornadas_valladolid")
    jornadas = cur.fetchall()
    jornadas_con_partidos = []
    for jornada in jornadas:
        cur.execute("SELECT * FROM valladolid_partidos WHERE jornada_id = %s", (jornada['id'],))
        partidos = cur.fetchall()
        jornada_con_partidos = {
            'nombre': jornada['nombre'],
            'partidos': partidos
        }       
        jornadas_con_partidos.append(jornada_con_partidos)
    cur.close()
    return jornadas_con_partidos
# Ruta y creación del calendario individual del Real Valladolid
@app.route('/equipos_futbol/calendario_vallad')
def calendarios_valladolid():
    datos3 = obtener_datos_valladolid()
    nuevos_datos_valladolid = [dato for dato in datos3 if dato]
    equipo_valladolid = 'Real Valladolid'
    tabla_partidos_valladolid = {}
    # Iteramos sobre cada jornada y partido
    for jornada in datos3:
        for partido in jornada['partidos']:
            equipo_local = partido['local']
            equipo_visitante = partido['visitante']
            resultado_local = partido['resultadoA']
            resultado_visitante = partido['resultadoB']           
            # Verificamos si el Real Valladolid está jugando
            if equipo_local == equipo_valladolid or equipo_visitante == equipo_valladolid:
                # Determinamos el equipo contrario y los resultados
                if equipo_local == equipo_valladolid:
                    equipo_contrario = equipo_visitante
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_valladolid = 'C'
                else:
                    equipo_contrario = equipo_local
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_valladolid = 'F'
                # Verificamos si el equipo contrario no está en la tabla
                if equipo_contrario not in tabla_partidos_valladolid:
                    tabla_partidos_valladolid[equipo_contrario] = {'jornadas': {}}                       
                # Verificamos si es el primer o segundo enfrentamiento
                if 'primer_enfrentamiento' not in tabla_partidos_valladolid[equipo_contrario]:
                    tabla_partidos_valladolid[equipo_contrario]['primer_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_valladolid[equipo_contrario]['resultadoA'] = resultado_a
                    tabla_partidos_valladolid[equipo_contrario]['resultadoB'] = resultado_b
                elif 'segundo_enfrentamiento' not in tabla_partidos_valladolid[equipo_contrario]:
                    tabla_partidos_valladolid[equipo_contrario]['segundo_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_valladolid[equipo_contrario]['resultadoAA'] = resultado_a
                    tabla_partidos_valladolid[equipo_contrario]['resultadoBB'] = resultado_b  
                # Agregamos la jornada y resultados
                if jornada['nombre'] not in tabla_partidos_valladolid[equipo_contrario]['jornadas']:
                    tabla_partidos_valladolid[equipo_contrario]['jornadas'][jornada['nombre']] = {
                        'resultadoA': resultado_a,
                        'resultadoB': resultado_b,
                        'rol_valladolid': rol_valladolid
                    }
                # Asignamos los resultados según el rol del Real Valladolid
                if equipo_local == equipo_contrario or equipo_visitante == equipo_contrario:
                  if not tabla_partidos_valladolid[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA']:
                    tabla_partidos_valladolid[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA'] = resultado_a
                    tabla_partidos_valladolid[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoB'] = resultado_b
                    tabla_partidos_valladolid[equipo_contrario]['jornadas'][jornada['nombre']]['rol_valladolid'] = rol_valladolid
                  else:
                    tabla_partidos_valladolid[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_valladolid[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_valladolid[equipo_contrario]['jornadas'][jornada['nombre']]['rol_valladolid'] = rol_valladolid
                else:
                  if not tabla_partidos_valladolid[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA']:
                    tabla_partidos_valladolid[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_valladolid[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_valladolid[equipo_contrario]['jornadas'][jornada['nombre']]['rol_valladolid'] = rol_valladolid
                  else:
                    tabla_partidos_valladolid[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_valladolid[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_valladolid[equipo_contrario]['jornadas'][jornada['nombre']]['rol_valladolid'] = rol_valladolid
    return render_template('equipos_futbol/calendario_vallad.html', tabla_partidos_valladolid=tabla_partidos_valladolid, nuevos_datos_valladolid=nuevos_datos_valladolid)
# Crear la clasificación del Real Valladolid
def generar_clasificacion_analisis_futbol_valladolid(data):
    default_dict = defaultdict(lambda: {})
    clasificacion = defaultdict(lambda: {'puntos': 0,'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'favor': 0, 'contra': 0, 'diferencia_goles': 0})
    print(clasificacion)
    for jornada in data:
        for partido in jornada['partidos']:
            equipo_local = partido['local']
            equipo_visitante = partido['visitante']
            try:
                resultado_local = int(partido['resultadoA'])
                resultado_visitante = int(partido['resultadoB'])
            except ValueError:
                print(f"Error al convertir resultados a enteros en el partido {partido}")
                continue
            if clasificacion[equipo_local]['jugados'] > 0:
                promedio_favor_local = clasificacion[equipo_local]['favor'] / clasificacion[equipo_local]['jugados']
            else:
                promedio_favor_local = 0
            # Ajusta la lógica según tus reglas para asignar puntos y calcular estadísticas en baloncesto
            if resultado_local > resultado_visitante:
                clasificacion[equipo_local]['puntos'] += 3
                clasificacion[equipo_local]['ganados'] += 1
                clasificacion[equipo_visitante]['perdidos'] += 1
            elif resultado_local < resultado_visitante:
                clasificacion[equipo_local]['puntos'] += 0
                clasificacion[equipo_local]['perdidos'] += 1
                clasificacion[equipo_visitante]['puntos'] += 3
                clasificacion[equipo_visitante]['ganados'] += 1
            else:
                clasificacion[equipo_local]['puntos'] += 1
                clasificacion[equipo_local]['empatados'] += 1
                clasificacion[equipo_visitante]['puntos'] += 1
                clasificacion[equipo_visitante]['empatados'] += 1
            clasificacion[equipo_local]['jugados'] += 1
            clasificacion[equipo_visitante]['jugados'] += 1
            clasificacion[equipo_local]['favor'] += resultado_local
            clasificacion[equipo_local]['contra'] += resultado_visitante
            clasificacion[equipo_visitante]['favor'] += resultado_visitante
            clasificacion[equipo_visitante]['contra'] += resultado_local
            clasificacion[equipo_local]['diferencia_goles'] += resultado_local - resultado_visitante
            clasificacion[equipo_visitante]['diferencia_goles'] += resultado_visitante - resultado_local
    # Ordena la clasificación por puntos y diferencia de canastas
    clasificacion_ordenada = [{'equipo': equipo, 'datos': datos} for equipo, datos in sorted(clasificacion.items(), key=lambda x: (x[1]['puntos'], x[1]['diferencia_goles']), reverse=True)]
    print(generar_clasificacion_analisis_futbol_valladolid)
    return clasificacion_ordenada
# Ruta para mostrar la clasificación y análisis del Real Valladolid
@app.route('/equipos_futbol/clasi_analis_vallad/')
def clasif_analisis_valladolid():
    data3 = obtener_datos_valladolid()
    # Genera la clasificación y análisis actual
    clasificacion_analisis_valladolid = generar_clasificacion_analisis_futbol_valladolid(data3)    
    # Obtén los equipos de la jornada 0
    clubs_valladolid = obtener_clubs_valladolid()
    # Inicializa las estadísticas de los equipos de la jornada 0 si no están ya en la clasificación
    for club in clubs_valladolid:
        if not any(equipo['equipo'] == club['nombre'] for equipo in clasificacion_analisis_valladolid):
            equipo = {
                'equipo': club['nombre'],
                'datos': {
                    'puntos': 0,
                    'jugados': 0,
                    'ganados': 0,
                    'empatados': 0,
                    'perdidos': 0,
                    'favor': 0,
                    'contra': 0,
                    'diferencia_goles': 0
                }
            }
            clasificacion_analisis_valladolid.append(equipo)
    return render_template('equipos_futbol/clasi_analis_vallad.html', clasificacion_analisis_valladolid=clasificacion_analisis_valladolid)
# Crear la Jornada 0, inscribir a los club participantes
def obtener_clubs_valladolid():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM valladolid_clubs")
    clubs = cur.fetchall()
    cur.close()
    return [{'id': club['id'], 'nombre': club['nombre']} for club in clubs]
@app.route('/admin/jornada0_valladolid', methods=['GET', 'POST'])
def jornada0_valladolid():
    if request.method == 'POST':
        if 'equipo' in request.form:
            club = request.form['equipo']
            if club:
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO valladolid_clubs (nombre) VALUES (%s)", (club,))
                mysql.connection.commit()
                cur.close()
            return redirect(url_for('jornada0_valladolid'))
        elif 'index' in request.form:
            index = int(request.form['index'])
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM valladolid_clubs WHERE id = %s", (index + 1,))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('jornada0_valladolid'))
    clubs = obtener_clubs_valladolid()
    return render_template('admin/clubs_valladolid.html', clubs=clubs, indices=range(len(clubs)))
@app.route('/admin/eliminar_club_valladolid/<string:club_id>', methods=['POST'])
def eliminar_club_valladolid(club_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM valladolid_clubs WHERE id = %s", (club_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('jornada0_valladolid'))
# Fin proceso Real Valladolid

#Todo el proceso de calendario y clasificación del Promesas
# Ruta de partidos Promesas
# Ingresar los resultados de los partidos del Promesas
@app.route('/admin/crear_calendario_promesas', methods=['POST'])
def ingresar_resul_promesas():
    if request.method == 'POST':
        nombre_jornada = request.form['nombre']
        num_partidos = int(request.form['num_partidos'])       
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO jornadas_promesas (nombre) VALUES (%s)', (nombre_jornada,))
        jornada_id = cur.lastrowid        
        for i in range(num_partidos):
            fecha = request.form[f'fecha{i}']
            hora = request.form[f'hora{i}']
            local = request.form[f'local{i}']
            resultadoA = request.form[f'resultadoA{i}']
            resultadoB = request.form[f'resultadoB{i}']
            visitante = request.form[f'visitante{i}']          
            cur.execute('INSERT INTO promesas_partidos (jornada_id, fecha, hora, local, resultadoA, resultadoB, visitante) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                        (jornada_id, fecha, hora, local, resultadoA, resultadoB, visitante))       
        mysql.connection.commit()
        cur.close()
    return redirect(url_for('calend_promesas')) 
# Partidos Promesas
@app.route('/admin/calend_promesas')
def calend_promesas():
    cur = mysql.connection.cursor()
    cur.execute('SELECT id, nombre FROM jornadas_promesas')
    jornadas = cur.fetchall()
    for jornada in jornadas:
        cur.execute('SELECT id, fecha, hora, local, resultadoA, resultadoB, visitante FROM promesas_partidos WHERE jornada_id = %s', (jornada['id'],))
        partidos = cur.fetchall()
        jornada['partidos'] = partidos
    cur.close()
    return render_template('admin/calend_promesas.html', jornadas=jornadas)
# Modificar los partidos de cada jornada
@app.route('/modificar_jornada_promesas/<string:id>', methods=['POST'])
def modificar_jorn_promesas(id):
    nombre_jornada = request.form['nombre']
    num_partidos = int(request.form['num_partidos'])
    cur = mysql.connection.cursor()
    # Actualizar la jornada
    cur.execute('UPDATE jornadas_promesas SET nombre = %s WHERE id = %s', (nombre_jornada, id))
    # Actualizar los partidos de la jornada
    for i in range(num_partidos):
        partido_id = request.form[f'partido_id{i}']
        fecha = request.form[f'fecha{i}']
        hora = request.form[f'hora{i}']
        local = request.form[f'local{i}']
        resultadoA = request.form[f'resultadoA{i}']
        resultadoB = request.form[f'resultadoB{i}']
        visitante = request.form[f'visitante{i}']   
        cur.execute('UPDATE promesas_partidos SET fecha = %s, hora = %s, local = %s, resultadoA = %s, resultadoB = %s, visitante = %s WHERE id = %s',
                    (fecha, hora, local, resultadoA, resultadoB, visitante, partido_id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('calend_promesas'))        
# Ruta para borrar jornadas
@app.route('/eliminar_jorn_promesas/<string:id>', methods=['POST'])
def eliminar_jorn_promesas(id):
    cur = mysql.connection.cursor()
    # Eliminar los partidos asociados a la jornada
    cur.execute('DELETE FROM promesas_partidos WHERE jornada_id = %s', (id,))
    # Eliminar la jornada
    cur.execute('DELETE FROM jornadas_promesas WHERE id = %s', (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('calend_promesas')) 
# Obtener datos para Real Valladolid Promesas
def obtener_datos_promesas():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM jornadas_promesas")
    jornadas = cur.fetchall()
    jornadas_con_partidos = []
    for jornada in jornadas:
        cur.execute("SELECT * FROM promesas_partidos WHERE jornada_id = %s", (jornada['id'],))
        partidos = cur.fetchall()
        jornada_con_partidos = {
            'nombre': jornada['nombre'],
            'partidos': partidos
        }       
        jornadas_con_partidos.append(jornada_con_partidos)
    cur.close()
    return jornadas_con_partidos
# Ruta y creación del calendario individual del Promesas
@app.route('/equipos_futbol/calendario_promesas')
def calendarios_promesas():
    print("Se llamo a la ruta/'equipo_futbol/calendario_promesas")
    datos4 = obtener_datos_promesas()
    nuevos_datos_promesas = [dato for dato in datos4 if dato]
    equipo_promesas = 'Real Valladolid B'
    tabla_partidos_promesas = {}
    # Iteramos sobre cada jornada y partido
    for jornada in datos4:
        for partido in jornada['partidos']:
            equipo_local = partido['local']
            equipo_visitante = partido['visitante']
            resultado_local = partido['resultadoA']
            resultado_visitante = partido['resultadoB']           
            # Verificamos si el Promesas está jugando
            if equipo_local == equipo_promesas or equipo_visitante == equipo_promesas:
                # Determinamos el equipo contrario y los resultados
                if equipo_local == equipo_promesas:
                    equipo_contrario = equipo_visitante
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_promesas = 'C'
                else:
                    equipo_contrario = equipo_local
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_promesas = 'F'
                # Verificamos si el equipo contrario no está en la tabla
                if equipo_contrario not in tabla_partidos_promesas:
                    tabla_partidos_promesas[equipo_contrario] = {'jornadas': {}}                       
                # Verificamos si es el primer o segundo enfrentamiento
                if 'primer_enfrentamiento' not in tabla_partidos_promesas[equipo_contrario]:
                    tabla_partidos_promesas[equipo_contrario]['primer_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_promesas[equipo_contrario]['resultadoA'] = resultado_a
                    tabla_partidos_promesas[equipo_contrario]['resultadoB'] = resultado_b
                elif 'segundo_enfrentamiento' not in tabla_partidos_promesas[equipo_contrario]:
                    tabla_partidos_promesas[equipo_contrario]['segundo_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_promesas[equipo_contrario]['resultadoAA'] = resultado_a
                    tabla_partidos_promesas[equipo_contrario]['resultadoBB'] = resultado_b  
                # Agregamos la jornada y resultados
                if jornada['nombre'] not in tabla_partidos_promesas[equipo_contrario]['jornadas']:
                    tabla_partidos_promesas[equipo_contrario]['jornadas'][jornada['nombre']] = {
                        'resultadoA': resultado_a,
                        'resultadoB': resultado_b,
                        'rol_promesas': rol_promesas
                    }
                # Asignamos los resultados según el rol del Real Valladolid
                if equipo_local == equipo_contrario or equipo_visitante == equipo_contrario:
                  if not tabla_partidos_promesas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA']:
                    tabla_partidos_promesas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA'] = resultado_a
                    tabla_partidos_promesas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoB'] = resultado_b
                    tabla_partidos_promesas[equipo_contrario]['jornadas'][jornada['nombre']]['rol_promesas'] = rol_promesas
                  else:
                    tabla_partidos_promesas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_promesas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_promesas[equipo_contrario]['jornadas'][jornada['nombre']]['rol_promesas'] = rol_promesas
                else:
                  if not tabla_partidos_promesas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA']:
                    tabla_partidos_promesas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_promesas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_promesas[equipo_contrario]['jornadas'][jornada['nombre']]['rol_promesas'] = rol_promesas
                  else:
                    tabla_partidos_promesas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_promesas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_promesas[equipo_contrario]['jornadas'][jornada['nombre']]['rol_promesas'] = rol_promesas
    return render_template('equipos_futbol/calendario_promesas.html', tabla_partidos_promesas=tabla_partidos_promesas, nuevos_datos_promesas=nuevos_datos_promesas)
# Crear la clasificación del Promesas
def generar_clasificacion_analisis_futbol_promesas(data):
    default_dict = defaultdict(lambda: {})
    clasificacion = defaultdict(lambda: {'puntos': 0,'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'favor': 0, 'contra': 0, 'diferencia_goles': 0})
    print(clasificacion)
    for jornada in data:
        for partido in jornada['partidos']:
            equipo_local = partido['local']
            equipo_visitante = partido['visitante']
            try:
                resultado_local = int(partido['resultadoA'])
                resultado_visitante = int(partido['resultadoB'])
            except ValueError:
                print(f"Error al convertir resultados a enteros en el partido {partido}")
                continue
            if clasificacion[equipo_local]['jugados'] > 0:
                promedio_favor_local = clasificacion[equipo_local]['favor'] / clasificacion[equipo_local]['jugados']
            else:
                promedio_favor_local = 0
            # Ajusta la lógica según tus reglas para asignar puntos y calcular estadísticas en baloncesto
            if resultado_local > resultado_visitante:
                clasificacion[equipo_local]['puntos'] += 3
                clasificacion[equipo_local]['ganados'] += 1
                clasificacion[equipo_visitante]['perdidos'] += 1
            elif resultado_local < resultado_visitante:
                clasificacion[equipo_local]['puntos'] += 0
                clasificacion[equipo_local]['perdidos'] += 1
                clasificacion[equipo_visitante]['puntos'] += 3
                clasificacion[equipo_visitante]['ganados'] += 1
            else:
                clasificacion[equipo_local]['puntos'] += 1
                clasificacion[equipo_local]['empatados'] += 1
                clasificacion[equipo_visitante]['puntos'] += 1
                clasificacion[equipo_visitante]['empatados'] += 1
            clasificacion[equipo_local]['jugados'] += 1
            clasificacion[equipo_visitante]['jugados'] += 1
            clasificacion[equipo_local]['favor'] += resultado_local
            clasificacion[equipo_local]['contra'] += resultado_visitante
            clasificacion[equipo_visitante]['favor'] += resultado_visitante
            clasificacion[equipo_visitante]['contra'] += resultado_local
            clasificacion[equipo_local]['diferencia_goles'] += resultado_local - resultado_visitante
            clasificacion[equipo_visitante]['diferencia_goles'] += resultado_visitante - resultado_local
    # Ordena la clasificación por puntos y diferencia de canastas
    clasificacion_ordenada = [{'equipo': equipo, 'datos': datos} for equipo, datos in sorted(clasificacion.items(), key=lambda x: (x[1]['puntos'], x[1]['diferencia_goles']), reverse=True)]
    print(generar_clasificacion_analisis_futbol_promesas)
    return clasificacion_ordenada  
# Ruta para mostrar la clasificación y análisis del Promesas
@app.route('/equipos_futbol/clasi_analis_prome/')
def clasif_analisis_promesas():
    data4 = obtener_datos_promesas()
    # Genera la clasificación y análisis actual
    clasificacion_analisis_promesas = generar_clasificacion_analisis_futbol_promesas(data4)    
    # Obtén los equipos de la jornada 0
    clubs_promesas = obtener_clubs_promesas()
    # Inicializa las estadísticas de los equipos de la jornada 0 si no están ya en la clasificación
    for club in clubs_promesas:
        if not any(equipo['equipo'] == club['nombre'] for equipo in clasificacion_analisis_promesas):
            equipo = {
                'equipo': club['nombre'],
                'datos': {
                    'puntos': 0,
                    'jugados': 0,
                    'ganados': 0,
                    'empatados': 0,
                    'perdidos': 0,
                    'favor': 0,
                    'contra': 0,
                    'diferencia_goles': 0
                }
            }
            clasificacion_analisis_promesas.append(equipo)
    return render_template('equipos_futbol/clasi_analis_prome.html', clasificacion_analisis_promesas=clasificacion_analisis_promesas) 
# Crear la Jornada 0, inscribir a los club participantes
def obtener_clubs_promesas():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM promesas_clubs")
    clubs = cur.fetchall()
    cur.close()
    return [{'id': club['id'], 'nombre': club['nombre']} for club in clubs]
@app.route('/admin/jornada0_promesas', methods=['GET', 'POST'])
def jornada0_promesas():
    if request.method == 'POST':
        if 'equipo' in request.form:
            club = request.form['equipo']
            if club:
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO promesas_clubs (nombre) VALUES (%s)", (club,))
                mysql.connection.commit()
                cur.close()
            return redirect(url_for('jornada0_promesas'))
        elif 'index' in request.form:
            index = int(request.form['index'])
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM promesas_clubs WHERE id = %s", (index + 1,))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('jornada0_promesas'))
    clubs = obtener_clubs_promesas()
    return render_template('admin/clubs_promesas.html', clubs=clubs, indices=range(len(clubs)))
@app.route('/admin/eliminar_club_promesas/<string:club_id>', methods=['POST'])
def eliminar_club_promesas(club_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM promesas_clubs WHERE id = %s", (club_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('jornada0_promesas'))
# Fin proceso Real Valladolid Promesas

#Todo el proceso de calendario y clasificación del RV Simancas
# Ruta de partidos RV Simancas 
# Ingresar los resultados de los partidos del V Simancas
@app.route('/admin/crear_calendario_simancas', methods=['POST'])
def ingresar_resul_simancas():
    if request.method == 'POST':
        nombre_jornada = request.form['nombre']
        num_partidos = int(request.form['num_partidos'])       
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO jornadas_simancas (nombre) VALUES (%s)', (nombre_jornada,))
        jornada_id = cur.lastrowid        
        for i in range(num_partidos):
            fecha = request.form[f'fecha{i}']
            hora = request.form[f'hora{i}']
            local = request.form[f'local{i}']
            resultadoA = request.form[f'resultadoA{i}']
            resultadoB = request.form[f'resultadoB{i}']
            visitante = request.form[f'visitante{i}']          
            cur.execute('INSERT INTO simancas_partidos (jornada_id, fecha, hora, local, resultadoA, resultadoB, visitante) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                        (jornada_id, fecha, hora, local, resultadoA, resultadoB, visitante))       
        mysql.connection.commit()
        cur.close()
    return redirect(url_for('calend_simancas'))
# Partidos RV Simancas
@app.route('/admin/calend_simancas')
def calend_simancas():
    cur = mysql.connection.cursor()
    cur.execute('SELECT id, nombre FROM jornadas_simancas')
    jornadas = cur.fetchall()
    for jornada in jornadas:
        cur.execute('SELECT id, fecha, hora, local, resultadoA, resultadoB, visitante FROM simancas_partidos WHERE jornada_id = %s', (jornada['id'],))
        partidos = cur.fetchall()
        jornada['partidos'] = partidos
    cur.close()
    return render_template('admin/calend_simancas.html', jornadas=jornadas)
# Modificar los partidos de cada jornada
@app.route('/modificar_jornada_simancas/<string:id>', methods=['POST'])
def modificar_jorn_simancas(id):
    nombre_jornada = request.form['nombre']
    num_partidos = int(request.form['num_partidos'])
    cur = mysql.connection.cursor()
    # Actualizar la jornada
    cur.execute('UPDATE jornadas_simancas SET nombre = %s WHERE id = %s', (nombre_jornada, id))
    # Actualizar los partidos de la jornada
    for i in range(num_partidos):
        partido_id = request.form[f'partido_id{i}']
        fecha = request.form[f'fecha{i}']
        hora = request.form[f'hora{i}']
        local = request.form[f'local{i}']
        resultadoA = request.form[f'resultadoA{i}']
        resultadoB = request.form[f'resultadoB{i}']
        visitante = request.form[f'visitante{i}']   
        cur.execute('UPDATE simancas_partidos SET fecha = %s, hora = %s, local = %s, resultadoA = %s, resultadoB = %s, visitante = %s WHERE id = %s',
                    (fecha, hora, local, resultadoA, resultadoB, visitante, partido_id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('calend_simancas'))
# Ruta para borrar jornadas
@app.route('/eliminar_jorn_simancas/<string:id>', methods=['POST'])
def eliminar_jorn_simancas(id):
    cur = mysql.connection.cursor()
    # Eliminar los partidos asociados a la jornada
    cur.execute('DELETE FROM simancas_partidos WHERE jornada_id = %s', (id,))
    # Eliminar la jornada
    cur.execute('DELETE FROM jornadas_simancas WHERE id = %s', (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('calend_simancas'))
# Obtener datos para Real Valladolid Simancas
def obtener_datos_simancas():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM jornadas_simancas")
    jornadas = cur.fetchall()
    jornadas_con_partidos = []
    for jornada in jornadas:
        cur.execute("SELECT * FROM simancas_partidos WHERE jornada_id = %s", (jornada['id'],))
        partidos = cur.fetchall()
        jornada_con_partidos = {
            'nombre': jornada['nombre'],
            'partidos': partidos
        }       
        jornadas_con_partidos.append(jornada_con_partidos)
    cur.close()
    return jornadas_con_partidos
# Ruta y creación del calendario individual del RV Simancas
@app.route('/equipos_futbol/calendario_simancas')
def calendarios_simancas():
    datos5 = obtener_datos_simancas()
    nuevos_datos_simancas = [dato for dato in datos5 if dato]
    equipo_simancas = 'Real Valladolid Fem.'
    tabla_partidos_simancas = {}
    # Iteramos sobre cada jornada y partido
    for jornada in datos5:
        for partido in jornada['partidos']:
            equipo_local = partido['local']
            equipo_visitante = partido['visitante']
            resultado_local = partido['resultadoA']
            resultado_visitante = partido['resultadoB']           
            # Verificamos si el Simancas está jugando
            if equipo_local == equipo_simancas or equipo_visitante == equipo_simancas:
                # Determinamos el equipo contrario y los resultados
                if equipo_local == equipo_simancas:
                    equipo_contrario = equipo_visitante
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_simancas = 'C'
                else:
                    equipo_contrario = equipo_local
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_simancas = 'F'
                # Verificamos si el equipo contrario no está en la tabla
                if equipo_contrario not in tabla_partidos_simancas:
                    tabla_partidos_simancas[equipo_contrario] = {'jornadas': {}}                       
                # Verificamos si es el primer o segundo enfrentamiento
                if 'primer_enfrentamiento' not in tabla_partidos_simancas[equipo_contrario]:
                    tabla_partidos_simancas[equipo_contrario]['primer_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_simancas[equipo_contrario]['resultadoA'] = resultado_a
                    tabla_partidos_simancas[equipo_contrario]['resultadoB'] = resultado_b
                elif 'segundo_enfrentamiento' not in tabla_partidos_simancas[equipo_contrario]:
                    tabla_partidos_simancas[equipo_contrario]['segundo_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_simancas[equipo_contrario]['resultadoAA'] = resultado_a
                    tabla_partidos_simancas[equipo_contrario]['resultadoBB'] = resultado_b  
                # Agregamos la jornada y resultados
                if jornada['nombre'] not in tabla_partidos_simancas[equipo_contrario]['jornadas']:
                    tabla_partidos_simancas[equipo_contrario]['jornadas'][jornada['nombre']] = {
                        'resultadoA': resultado_a,
                        'resultadoB': resultado_b,
                        'rol_simancas': rol_simancas
                    }
                # Asignamos los resultados según el rol del Real Valladolid
                if equipo_local == equipo_contrario or equipo_visitante == equipo_contrario:
                  if not tabla_partidos_simancas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA']:
                    tabla_partidos_simancas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA'] = resultado_a
                    tabla_partidos_simancas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoB'] = resultado_b
                    tabla_partidos_simancas[equipo_contrario]['jornadas'][jornada['nombre']]['rol_simancas'] = rol_simancas
                  else:
                    tabla_partidos_simancas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_simancas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_simancas[equipo_contrario]['jornadas'][jornada['nombre']]['rol_simanca'] = rol_simancas
                else:
                  if not tabla_partidos_simancas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA']:
                    tabla_partidos_simancas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_simancas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_simancas[equipo_contrario]['jornadas'][jornada['nombre']]['rol_simancas'] = rol_simancas
                  else:
                    tabla_partidos_simancas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_simancas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_simancas[equipo_contrario]['jornadas'][jornada['nombre']]['rol_simancas'] = rol_simancas
    return render_template('equipos_futbol/calendario_simancas.html', tabla_partidos_simancas=tabla_partidos_simancas, nuevos_datos_simancas=nuevos_datos_simancas)
# Crear la clasificación del V Simancas
def generar_clasificacion_analisis_futbol_simancas(data):
    default_dict = defaultdict(lambda: {})
    clasificacion = defaultdict(lambda: {'puntos': 0,'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'favor': 0, 'contra': 0, 'diferencia_goles': 0})
    print(clasificacion)
    for jornada in data:
        for partido in jornada['partidos']:
            equipo_local = partido['local']
            equipo_visitante = partido['visitante']
            try:
                resultado_local = int(partido['resultadoA'])
                resultado_visitante = int(partido['resultadoB'])
            except ValueError:
                print(f"Error al convertir resultados a enteros en el partido {partido}")
                continue
            if clasificacion[equipo_local]['jugados'] > 0:
                promedio_favor_local = clasificacion[equipo_local]['favor'] / clasificacion[equipo_local]['jugados']
            else:
                promedio_favor_local = 0
            # Ajusta la lógica según tus reglas para asignar puntos y calcular estadísticas en baloncesto
            if resultado_local > resultado_visitante:
                clasificacion[equipo_local]['puntos'] += 3
                clasificacion[equipo_local]['ganados'] += 1
                clasificacion[equipo_visitante]['perdidos'] += 1
            elif resultado_local < resultado_visitante:
                clasificacion[equipo_local]['puntos'] += 0
                clasificacion[equipo_local]['perdidos'] += 1
                clasificacion[equipo_visitante]['puntos'] += 3
                clasificacion[equipo_visitante]['ganados'] += 1
            else:
                clasificacion[equipo_local]['puntos'] += 1
                clasificacion[equipo_local]['empatados'] += 1
                clasificacion[equipo_visitante]['puntos'] += 1
                clasificacion[equipo_visitante]['empatados'] += 1
            clasificacion[equipo_local]['jugados'] += 1
            clasificacion[equipo_visitante]['jugados'] += 1
            clasificacion[equipo_local]['favor'] += resultado_local
            clasificacion[equipo_local]['contra'] += resultado_visitante
            clasificacion[equipo_visitante]['favor'] += resultado_visitante
            clasificacion[equipo_visitante]['contra'] += resultado_local
            clasificacion[equipo_local]['diferencia_goles'] += resultado_local - resultado_visitante
            clasificacion[equipo_visitante]['diferencia_goles'] += resultado_visitante - resultado_local
    # Ordena la clasificación por puntos y diferencia de canastas
    clasificacion_ordenada = [{'equipo': equipo, 'datos': datos} for equipo, datos in sorted(clasificacion.items(), key=lambda x: (x[1]['puntos'], x[1]['diferencia_goles']), reverse=True)]
    print(generar_clasificacion_analisis_futbol_simancas)
    return clasificacion_ordenada
# Ruta para mostrar la clasificación y análisis del RV Simancas
@app.route('/equipos_futbol/clasi_analis_siman/')
def clasif_analisis_simancas():
    data5 = obtener_datos_simancas()
    # Genera la clasificación y análisis actual
    clasificacion_analisis_simancas = generar_clasificacion_analisis_futbol_simancas(data5)    
    # Obtén los equipos de la jornada 0
    clubs_simancas = obtener_clubs_simancas()
    # Inicializa las estadísticas de los equipos de la jornada 0 si no están ya en la clasificación
    for club in clubs_simancas:
        if not any(equipo['equipo'] == club['nombre'] for equipo in clasificacion_analisis_simancas):
            equipo = {
                'equipo': club['nombre'],
                'datos': {
                    'puntos': 0,
                    'jugados': 0,
                    'ganados': 0,
                    'empatados': 0,
                    'perdidos': 0,
                    'favor': 0,
                    'contra': 0,
                    'diferencia_goles': 0
                }
            }
            clasificacion_analisis_simancas.append(equipo)
    return render_template('equipos_futbol/clasi_analis_siman.html', clasificacion_analisis_simancas=clasificacion_analisis_simancas)
# Crear la Jornada 0, inscribir a los club participantes
def obtener_clubs_simancas():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM simancas_clubs")
    clubs = cur.fetchall()
    cur.close()
    return [{'id': club['id'], 'nombre': club['nombre']} for club in clubs]
@app.route('/admin/jornada0_simancas', methods=['GET', 'POST'])
def jornada0_simancas():
    if request.method == 'POST':
        if 'equipo' in request.form:
            club = request.form['equipo']
            if club:
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO simancas_clubs (nombre) VALUES (%s)", (club,))
                mysql.connection.commit()
                cur.close()
            return redirect(url_for('jornada0_simancas'))
        elif 'index' in request.form:
            index = int(request.form['index'])
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM simancas_clubs WHERE id = %s", (index + 1,))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('jornada0_simancas'))
    clubs = obtener_clubs_simancas()
    return render_template('admin/clubs_simancas.html', clubs=clubs, indices=range(len(clubs)))
@app.route('/admin/eliminar_club_simancas/<string:club_id>', methods=['POST'])
def eliminar_club_simancas(club_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM simancas_clubs WHERE id = %s", (club_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('jornada0_simancas'))
# Fin proceso RV Simancas

#Todo el proceso de calendario y clasificación del CD Parquesol
# Ruta de partidos CD Parquesol
# Ingresar los resultados de los partidos del CD Parquesol
@app.route('/admin/crear_calendario_parquesol', methods=['POST'])
def ingresar_resul_parquesol():
    if request.method == 'POST':
        nombre_jornada = request.form['nombre']
        num_partidos = int(request.form['num_partidos'])       
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO jornadas_parquesol (nombre) VALUES (%s)', (nombre_jornada,))
        jornada_id = cur.lastrowid        
        for i in range(num_partidos):
            fecha = request.form[f'fecha{i}']
            hora = request.form[f'hora{i}']
            local = request.form[f'local{i}']
            resultadoA = request.form[f'resultadoA{i}']
            resultadoB = request.form[f'resultadoB{i}']
            visitante = request.form[f'visitante{i}']          
            cur.execute('INSERT INTO parquesol_partidos (jornada_id, fecha, hora, local, resultadoA, resultadoB, visitante) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                        (jornada_id, fecha, hora, local, resultadoA, resultadoB, visitante))       
        mysql.connection.commit()
        cur.close()
    return redirect(url_for('calend_parquesol'))
# Partidos CD Parquesol
@app.route('/admin/calend_parquesol')
def calend_parquesol():
    cur = mysql.connection.cursor()
    cur.execute('SELECT id, nombre FROM jornadas_parquesol')
    jornadas = cur.fetchall()
    for jornada in jornadas:
        cur.execute('SELECT id, fecha, hora, local, resultadoA, resultadoB, visitante FROM parquesol_partidos WHERE jornada_id = %s', (jornada['id'],))
        partidos = cur.fetchall()
        jornada['partidos'] = partidos
    cur.close()
    return render_template('admin/calend_parquesol.html', jornadas=jornadas)
# Modificar los partidos de cada jornada
@app.route('/modificar_jorn_parquesol/<string:id>', methods=['POST'])
def modificar_jorn_parquesol(id):
    nombre_jornada = request.form['nombre']
    num_partidos = int(request.form['num_partidos'])
    cur = mysql.connection.cursor()
    # Actualizar la jornada
    cur.execute('UPDATE jornadas_parquesol SET nombre = %s WHERE id = %s', (nombre_jornada, id))
    # Actualizar los partidos de la jornada
    for i in range(num_partidos):
        partido_id = request.form[f'partido_id{i}']
        fecha = request.form[f'fecha{i}']
        hora = request.form[f'hora{i}']
        local = request.form[f'local{i}']
        resultadoA = request.form[f'resultadoA{i}']
        resultadoB = request.form[f'resultadoB{i}']
        visitante = request.form[f'visitante{i}']   
        cur.execute('UPDATE parquesol_partidos SET fecha = %s, hora = %s, local = %s, resultadoA = %s, resultadoB = %s, visitante = %s WHERE id = %s',
                    (fecha, hora, local, resultadoA, resultadoB, visitante, partido_id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('calend_parquesol'))
# Ruta para borrar jornadas
@app.route('/eliminar_jorn_parquesol/<string:id>', methods=['POST'])
def eliminar_jorn_parquesol(id):
    cur = mysql.connection.cursor()
    # Eliminar los partidos asociados a la jornada
    cur.execute('DELETE FROM parquesol_partidos WHERE jornada_id = %s', (id,))
    # Eliminar la jornada
    cur.execute('DELETE FROM jornadas_parquesol WHERE id = %s', (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('calend_parquesol')) 
# Obtener datos para CD Parquesol
def obtener_datos_parquesol():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM jornadas_parquesol")
    jornadas = cur.fetchall()
    jornadas_con_partidos = []
    for jornada in jornadas:
        cur.execute("SELECT * FROM parquesol_partidos WHERE jornada_id = %s", (jornada['id'],))
        partidos = cur.fetchall()
        jornada_con_partidos = {
            'nombre': jornada['nombre'],
            'partidos': partidos
        }       
        jornadas_con_partidos.append(jornada_con_partidos)
    cur.close()
    return jornadas_con_partidos
# Ruta y creación del calendario individual del CD Parquesol
@app.route('/equipos_futbol/calendario_parquesol')
def calendarios_parquesol():
    datos6 = obtener_datos_parquesol()
    nuevos_datos_parquesol = [dato for dato in datos6 if dato]
    equipo_parquesol = 'CD Parquesol'
    tabla_partidos_parquesol = {}
    # Iteramos sobre cada jornada y partido
    for jornada in datos6:
        for partido in jornada['partidos']:
            equipo_local = partido['local']
            equipo_visitante = partido['visitante']
            resultado_local = partido['resultadoA']
            resultado_visitante = partido['resultadoB']           
            # Verificamos si el Simancas está jugando
            if equipo_local == equipo_parquesol or equipo_visitante == equipo_parquesol:
                # Determinamos el equipo contrario y los resultados
                if equipo_local == equipo_parquesol:
                    equipo_contrario = equipo_visitante
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_parquesol = 'C'
                else:
                    equipo_contrario = equipo_local
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_parquesol = 'F'
                # Verificamos si el equipo contrario no está en la tabla
                if equipo_contrario not in tabla_partidos_parquesol:
                    tabla_partidos_parquesol[equipo_contrario] = {'jornadas': {}}                       
                # Verificamos si es el primer o segundo enfrentamiento
                if 'primer_enfrentamiento' not in tabla_partidos_parquesol[equipo_contrario]:
                    tabla_partidos_parquesol[equipo_contrario]['primer_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_parquesol[equipo_contrario]['resultadoA'] = resultado_a
                    tabla_partidos_parquesol[equipo_contrario]['resultadoB'] = resultado_b
                elif 'segundo_enfrentamiento' not in tabla_partidos_parquesol[equipo_contrario]:
                    tabla_partidos_parquesol[equipo_contrario]['segundo_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_parquesol[equipo_contrario]['resultadoAA'] = resultado_a
                    tabla_partidos_parquesol[equipo_contrario]['resultadoBB'] = resultado_b  
                # Agregamos la jornada y resultados
                if jornada['nombre'] not in tabla_partidos_parquesol[equipo_contrario]['jornadas']:
                    tabla_partidos_parquesol[equipo_contrario]['jornadas'][jornada['nombre']] = {
                        'resultadoA': resultado_a,
                        'resultadoB': resultado_b,
                        'rol_parquesol': rol_parquesol
                    }
                # Asignamos los resultados según el rol del Real Valladolid
                if equipo_local == equipo_contrario or equipo_visitante == equipo_contrario:
                  if not tabla_partidos_parquesol[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA']:
                    tabla_partidos_parquesol[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA'] = resultado_a
                    tabla_partidos_parquesol[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoB'] = resultado_b
                    tabla_partidos_parquesol[equipo_contrario]['jornadas'][jornada['nombre']]['rol_parquesol'] = rol_parquesol
                  else:
                    tabla_partidos_parquesol[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_parquesol[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_parquesol[equipo_contrario]['jornadas'][jornada['nombre']]['rol_parquesol'] = rol_parquesol
                else:
                  if not tabla_partidos_parquesol[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA']:
                    tabla_partidos_parquesol[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_parquesol[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_parquesol[equipo_contrario]['jornadas'][jornada['nombre']]['rol_parquesol'] = rol_parquesol
                  else:
                    tabla_partidos_parquesol[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_parquesol[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_parquesol[equipo_contrario]['jornadas'][jornada['nombre']]['rol_parquesol'] = rol_parquesol
    return render_template('equipos_futbol/calendario_parquesol.html', tabla_partidos_parquesol=tabla_partidos_parquesol, nuevos_datos_parquesol=nuevos_datos_parquesol)        
# Crear la clasificación del CD Parquesol
def generar_clasificacion_analisis_futbol_parquesol(data):
    default_dict = defaultdict(lambda: {})
    clasificacion = defaultdict(lambda: {'puntos': 0,'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'favor': 0, 'contra': 0, 'diferencia_goles': 0})
    for jornada in data:
        for partido in jornada['partidos']:
            equipo_local = partido['local']
            equipo_visitante = partido['visitante']
            try:
                resultado_local = int(partido['resultadoA'])
                resultado_visitante = int(partido['resultadoB'])
            except ValueError:
                print(f"Error al convertir resultados a enteros en el partido {partido}")
                continue
            if clasificacion[equipo_local]['jugados'] > 0:
                promedio_favor_local = clasificacion[equipo_local]['favor'] / clasificacion[equipo_local]['jugados']
            else:
                promedio_favor_local = 0
            # Ajusta la lógica según tus reglas para asignar puntos y calcular estadísticas en baloncesto
            if resultado_local > resultado_visitante:
                clasificacion[equipo_local]['puntos'] += 3
                clasificacion[equipo_local]['ganados'] += 1
                clasificacion[equipo_visitante]['perdidos'] += 1
            elif resultado_local < resultado_visitante:
                clasificacion[equipo_local]['puntos'] += 0
                clasificacion[equipo_local]['perdidos'] += 1
                clasificacion[equipo_visitante]['puntos'] += 3
                clasificacion[equipo_visitante]['ganados'] += 1
            else:
                clasificacion[equipo_local]['puntos'] += 1
                clasificacion[equipo_local]['empatados'] += 1
                clasificacion[equipo_visitante]['puntos'] += 1
                clasificacion[equipo_visitante]['empatados'] += 1
            clasificacion[equipo_local]['jugados'] += 1
            clasificacion[equipo_visitante]['jugados'] += 1
            clasificacion[equipo_local]['favor'] += resultado_local
            clasificacion[equipo_local]['contra'] += resultado_visitante
            clasificacion[equipo_visitante]['favor'] += resultado_visitante
            clasificacion[equipo_visitante]['contra'] += resultado_local
            clasificacion[equipo_local]['diferencia_goles'] += resultado_local - resultado_visitante
            clasificacion[equipo_visitante]['diferencia_goles'] += resultado_visitante - resultado_local
    # Ordena la clasificación por puntos y diferencia de canastas
    clasificacion_ordenada = [{'equipo': equipo, 'datos': datos} for equipo, datos in sorted(clasificacion.items(), key=lambda x: (x[1]['puntos'], x[1]['diferencia_goles']), reverse=True)]
    print(generar_clasificacion_analisis_futbol_parquesol)
    return clasificacion_ordenada
# Ruta para mostrar la clasificación y análisis del CD Parquesol
@app.route('/equipos_futbol/clasi_analis_parque/')
def clasif_analisis_parquesol():
    data6 = obtener_datos_parquesol()
    # Genera la clasificación y análisis actual
    clasificacion_analisis_parquesol = generar_clasificacion_analisis_futbol_parquesol(data6)    
    # Obtén los equipos de la jornada 0
    clubs_parquesol = obtener_clubs_parquesol()
    # Inicializa las estadísticas de los equipos de la jornada 0 si no están ya en la clasificación
    for club in clubs_parquesol:
        if not any(equipo['equipo'] == club['nombre'] for equipo in clasificacion_analisis_parquesol):
            equipo = {
                'equipo': club['nombre'],
                'datos': {
                    'puntos': 0,
                    'jugados': 0,
                    'ganados': 0,
                    'empatados': 0,
                    'perdidos': 0,
                    'favor': 0,
                    'contra': 0,
                    'diferencia_goles': 0
                }
            }
            clasificacion_analisis_parquesol.append(equipo)
    return render_template('equipos_futbol/clasi_analis_parque.html', clasificacion_analisis_parquesol=clasificacion_analisis_parquesol)         
# Crear la Jornada 0, inscribir a los club participantes
def obtener_clubs_parquesol():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM parquesol_clubs")
    clubs = cur.fetchall()
    cur.close()
    return [{'id': club['id'], 'nombre': club['nombre']} for club in clubs]
@app.route('/admin/jornada0_parquesol', methods=['GET', 'POST'])
def jornada0_parquesol():
    if request.method == 'POST':
        if 'equipo' in request.form:
            club = request.form['equipo']
            if club:
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO parquesol_clubs (nombre) VALUES (%s)", (club,))
                mysql.connection.commit()
                cur.close()
            return redirect(url_for('jornada0_parquesol'))
        elif 'index' in request.form:
            index = int(request.form['index'])
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM parquesol_clubs WHERE id = %s", (index + 1,))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('jornada0_parquesol'))
    clubs = obtener_clubs_parquesol()
    return render_template('admin/clubs_parquesol.html', clubs=clubs, indices=range(len(clubs)))
@app.route('/admin/eliminar_club_parquesol/<string:club_id>', methods=['POST'])
def eliminar_club_parquesol(club_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM parquesol_clubs WHERE id = %s", (club_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('jornada0_parquesol'))
# Fin proceso CD Parquesol               

# EQUIPOS FÚTBOL SALA
#Todo el proceso de calendario y clasificación del Valladolid FS            
# Ingresar los resultados de los partidos del Valladolid FS
@app.route('/admin/crear_calendario_valladolid_fs', methods=['POST'])
def ingresar_resul_valladolid_fs():
    if request.method == 'POST':
        nombre_jornada = request.form['nombre']
        num_partidos = int(request.form['num_partidos'])       
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO jornadas_fsvalladolid (nombre) VALUES (%s)', (nombre_jornada,))
        jornada_id = cur.lastrowid        
        for i in range(num_partidos):
            fecha = request.form[f'fecha{i}']
            hora = request.form[f'hora{i}']
            local = request.form[f'local{i}']
            resultadoA = request.form[f'resultadoA{i}']
            resultadoB = request.form[f'resultadoB{i}']
            visitante = request.form[f'visitante{i}']          
            cur.execute('INSERT INTO fsvalladolid_partidos (jornada_id, fecha, hora, local, resultadoA, resultadoB, visitante) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                        (jornada_id, fecha, hora, local, resultadoA, resultadoB, visitante))       
        mysql.connection.commit()
        cur.close()
    return redirect(url_for('calend_valladolid_fs')) 
# Partidos Valladolid FS
@app.route('/admin/calend_valladolid_fs')
def calend_valladolid_fs():
    cur = mysql.connection.cursor()
    cur.execute('SELECT id, nombre FROM jornadas_fsvalladolid')
    jornadas = cur.fetchall()
    for jornada in jornadas:
        cur.execute('SELECT id, fecha, hora, local, resultadoA, resultadoB, visitante FROM fsvalladolid_partidos WHERE jornada_id = %s', (jornada['id'],))
        partidos = cur.fetchall()
        jornada['partidos'] = partidos
    cur.close()
    return render_template('admin/calend_vallad_fs.html', jornadas=jornadas)
# Modificar los partidos de cada jornada
@app.route('/modificar_jornada_valladolid_fs/<string:id>', methods=['POST'])
def modificar_jorn_valladolid_fs(id):
    nombre_jornada = request.form['nombre']
    num_partidos = int(request.form['num_partidos'])
    cur = mysql.connection.cursor()
    # Actualizar la jornada
    cur.execute('UPDATE jornadas_fsvalladolid SET nombre = %s WHERE id = %s', (nombre_jornada, id))
    # Actualizar los partidos de la jornada
    for i in range(num_partidos):
        partido_id = request.form[f'partido_id{i}']
        fecha = request.form[f'fecha{i}']
        hora = request.form[f'hora{i}']
        local = request.form[f'local{i}']
        resultadoA = request.form[f'resultadoA{i}']
        resultadoB = request.form[f'resultadoB{i}']
        visitante = request.form[f'visitante{i}']   
        cur.execute('UPDATE fsvalladolid_partidos SET fecha = %s, hora = %s, local = %s, resultadoA = %s, resultadoB = %s, visitante = %s WHERE id = %s',
                    (fecha, hora, local, resultadoA, resultadoB, visitante, partido_id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('calend_valladolid_fs'))
# Ruta para borrar jornadas
@app.route('/eliminar_jorn_valladolid_fs/<string:id>', methods=['POST'])
def eliminar_jorn_valladolid_fs(id):
    cur = mysql.connection.cursor()
    # Eliminar los partidos asociados a la jornada
    cur.execute('DELETE FROM fsvalladolid_partidos WHERE jornada_id = %s', (id,))
    # Eliminar la jornada
    cur.execute('DELETE FROM jornadas_fsvalladolid WHERE id = %s', (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('calend_valladolid_fs'))    
# Obtener datos para CD Parquesol
def obtener_datos_valladolid_fs():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM jornadas_fsvalladolid")
    jornadas = cur.fetchall()
    jornadas_con_partidos = []
    for jornada in jornadas:
        cur.execute("SELECT * FROM fsvalladolid_partidos WHERE jornada_id = %s", (jornada['id'],))
        partidos = cur.fetchall()
        jornada_con_partidos = {
            'nombre': jornada['nombre'],
            'partidos': partidos
        }       
        jornadas_con_partidos.append(jornada_con_partidos)
    cur.close()
    return jornadas_con_partidos       
# Ruta y creación del calendario individual del Valladolid FS
@app.route('/equipos_futbol_sala/calendario_vallad_fs')
def calendarios_valladolid_fs():
    datos16 = obtener_datos_valladolid_fs()
    nuevos_datos_valladolid_fs = [dato for dato in datos16 if dato]
    equipo_valladolid_fs = 'Valladolid FS'
    tabla_partidos_valladolid_fs = {}
    # Iteramos sobre cada jornada y partido
    for jornada in datos16:
        for partido in jornada['partidos']:
            equipo_local = partido['local']
            equipo_visitante = partido['visitante']
            resultado_local = partido['resultadoA']
            resultado_visitante = partido['resultadoB']           
            # Verificamos si el Simancas está jugando
            if equipo_local == equipo_valladolid_fs or equipo_visitante == equipo_valladolid_fs:
                # Determinamos el equipo contrario y los resultados
                if equipo_local == equipo_valladolid_fs:
                    equipo_contrario = equipo_visitante
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_valladolid_fs = 'C'
                else:
                    equipo_contrario = equipo_local
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_valladolid_fs = 'F'
                # Verificamos si el equipo contrario no está en la tabla
                if equipo_contrario not in tabla_partidos_valladolid_fs:
                    tabla_partidos_valladolid_fs[equipo_contrario] = {'jornadas': {}}                       
                # Verificamos si es el primer o segundo enfrentamiento
                if 'primer_enfrentamiento' not in tabla_partidos_valladolid_fs[equipo_contrario]:
                    tabla_partidos_valladolid_fs[equipo_contrario]['primer_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_valladolid_fs[equipo_contrario]['resultadoA'] = resultado_a
                    tabla_partidos_valladolid_fs[equipo_contrario]['resultadoB'] = resultado_b
                elif 'segundo_enfrentamiento' not in tabla_partidos_valladolid_fs[equipo_contrario]:
                    tabla_partidos_valladolid_fs[equipo_contrario]['segundo_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_valladolid_fs[equipo_contrario]['resultadoAA'] = resultado_a
                    tabla_partidos_valladolid_fs[equipo_contrario]['resultadoBB'] = resultado_b  
                # Agregamos la jornada y resultados
                if jornada['nombre'] not in tabla_partidos_valladolid_fs[equipo_contrario]['jornadas']:
                    tabla_partidos_valladolid_fs[equipo_contrario]['jornadas'][jornada['nombre']] = {
                        'resultadoA': resultado_a,
                        'resultadoB': resultado_b,
                        'rol_valladolid_fs': rol_valladolid_fs
                    }
                # Asignamos los resultados según el rol del Valladolid FS
                if equipo_local == equipo_contrario or equipo_visitante == equipo_contrario:
                  if not tabla_partidos_valladolid_fs[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA']:
                    tabla_partidos_valladolid_fs[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA'] = resultado_a
                    tabla_partidos_valladolid_fs[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoB'] = resultado_b
                    tabla_partidos_valladolid_fs[equipo_contrario]['jornadas'][jornada['nombre']]['rol_valladolid_fs'] = rol_valladolid_fs
                  else:
                    tabla_partidos_valladolid_fs[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_valladolid_fs[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_valladolid_fs[equipo_contrario]['jornadas'][jornada['nombre']]['rol_valladolid_fs'] = rol_valladolid_fs
                else:
                  if not tabla_partidos_valladolid_fs[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA']:
                    tabla_partidos_valladolid_fs[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_valladolid_fs[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_valladolid_fs[equipo_contrario]['jornadas'][jornada['nombre']]['rol_valladolid_fs'] = rol_valladolid_fs
                  else:
                    tabla_partidos_valladolid_fs[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_valladolid_fs[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_valladolid_fs[equipo_contrario]['jornadas'][jornada['nombre']]['rol_valladolid_fs'] = rol_valladolid_fs
    return render_template('equipos_futbol_sala/calendario_vallad_fs.html', tabla_partidos_valladolid_fs=tabla_partidos_valladolid_fs, nuevos_datos_valladolid_fs=nuevos_datos_valladolid_fs)
# Crear la clasificación del Valladolid FS
def generar_clasificacion_analisis_futsal_valladolid_fs(data):
    default_dict = defaultdict(lambda: {})
    clasificacion = defaultdict(lambda: {'puntos': 0,'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'favor': 0, 'contra': 0, 'diferencia_goles': 0})
    for jornada in data:
        for partido in jornada['partidos']:
            equipo_local = partido['local']
            equipo_visitante = partido['visitante']
            try:
                resultado_local = int(partido['resultadoA'])
                resultado_visitante = int(partido['resultadoB'])
            except ValueError:
                print(f"Error al convertir resultados a enteros en el partido {partido}")
                continue
            if clasificacion[equipo_local]['jugados'] > 0:
                promedio_favor_local = clasificacion[equipo_local]['favor'] / clasificacion[equipo_local]['jugados']
            else:
                promedio_favor_local = 0
            # Ajusta la lógica según tus reglas para asignar puntos y calcular estadísticas en baloncesto
            if resultado_local > resultado_visitante:
                clasificacion[equipo_local]['puntos'] += 3
                clasificacion[equipo_local]['ganados'] += 1
                clasificacion[equipo_visitante]['perdidos'] += 1
            elif resultado_local < resultado_visitante:
                clasificacion[equipo_local]['puntos'] += 0
                clasificacion[equipo_local]['perdidos'] += 1
                clasificacion[equipo_visitante]['puntos'] += 3
                clasificacion[equipo_visitante]['ganados'] += 1
            else:
                clasificacion[equipo_local]['puntos'] += 1
                clasificacion[equipo_local]['empatados'] += 1
                clasificacion[equipo_visitante]['puntos'] += 1
                clasificacion[equipo_visitante]['empatados'] += 1
            clasificacion[equipo_local]['jugados'] += 1
            clasificacion[equipo_visitante]['jugados'] += 1
            clasificacion[equipo_local]['favor'] += resultado_local
            clasificacion[equipo_local]['contra'] += resultado_visitante
            clasificacion[equipo_visitante]['favor'] += resultado_visitante
            clasificacion[equipo_visitante]['contra'] += resultado_local
            clasificacion[equipo_local]['diferencia_goles'] += resultado_local - resultado_visitante
            clasificacion[equipo_visitante]['diferencia_goles'] += resultado_visitante - resultado_local
    # Ordena la clasificación por puntos y diferencia de canastas
    clasificacion_ordenada = [{'equipo': equipo, 'datos': datos} for equipo, datos in sorted(clasificacion.items(), key=lambda x: (x[1]['puntos'], x[1]['diferencia_goles']), reverse=True)]
    print(generar_clasificacion_analisis_futsal_valladolid_fs)
    return clasificacion_ordenada
# Ruta para mostrar la clasificación y análisis del Valladolid FS
@app.route('/equipos_futbol_sala/clasi_analis_vallad_fs/')
def clasif_analisis_valladolid_fs():
    data7 = obtener_datos_valladolid_fs()
    # Genera la clasificación y análisis actual
    clasificacion_analisis_fsvalladolid = generar_clasificacion_analisis_futsal_valladolid_fs(data7)    
    # Obtén los equipos de la jornada 0
    clubs_fsvalladolid = obtener_clubs_fsvalladolid()
    # Inicializa las estadísticas de los equipos de la jornada 0 si no están ya en la clasificación
    for club in clubs_fsvalladolid:
        if not any(equipo['equipo'] == club['nombre'] for equipo in clasificacion_analisis_fsvalladolid):
            equipo = {
                'equipo': club['nombre'],
                'datos': {
                    'puntos': 0,
                    'jugados': 0,
                    'ganados': 0,
                    'empatados': 0,
                    'perdidos': 0,
                    'favor': 0,
                    'contra': 0,
                    'diferencia_goles': 0
                }
            }
            clasificacion_analisis_fsvalladolid.append(equipo)
    return render_template('equipos_futbol_sala/clasi_analis_vallad_fs.html', clasificacion_analisis_fsvalladolid=clasificacion_analisis_fsvalladolid)
# Crear la Jornada 0, inscribir a los club participantes
def obtener_clubs_fsvalladolid():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM fsvalladolid_clubs")
    clubs = cur.fetchall()
    cur.close()
    return [{'id': club['id'], 'nombre': club['nombre']} for club in clubs]
@app.route('/admin/jornada0_fsvalladolid', methods=['GET', 'POST'])
def jornada0_fsvalladolid():
    if request.method == 'POST':
        if 'equipo' in request.form:
            club = request.form['equipo']
            if club:
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO fsvalladolid_clubs (nombre) VALUES (%s)", (club,))
                mysql.connection.commit()
                cur.close()
            return redirect(url_for('jornada0_fsvalladolid'))
        elif 'index' in request.form:
            index = int(request.form['index'])
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM fsvalladolid_clubs WHERE id = %s", (index + 1,))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('jornada0_fsvalladolid'))
    clubs = obtener_clubs_fsvalladolid()
    return render_template('admin/clubs_valladolid_fs.html', clubs=clubs, indices=range(len(clubs)))
@app.route('/admin/eliminar_club_fsvalladolid/<string:club_id>', methods=['POST'])
def eliminar_club_fsvalladolid(club_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM fsvalladolid_clubs WHERE id = %s", (club_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('jornada0_fsvalladolid'))
# Fin proceso Valladolid FS

#Todo el proceso de calendario y clasificación del Universidad Valladolid
# Ruta de partidos Universidad Valladolid
# Ingresar los resultados de los partidos del Universidad Valladolid
@app.route('/admin/crear_calendario_universidad', methods=['POST'])
def ingresar_resul_universidad():
    if request.method == 'POST':
        nombre_jornada = request.form['nombre']
        num_partidos = int(request.form['num_partidos'])       
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO jornadas_universidad (nombre) VALUES (%s)', (nombre_jornada,))
        jornada_id = cur.lastrowid        
        for i in range(num_partidos):
            fecha = request.form[f'fecha{i}']
            hora = request.form[f'hora{i}']
            local = request.form[f'local{i}']
            resultadoA = request.form[f'resultadoA{i}']
            resultadoB = request.form[f'resultadoB{i}']
            visitante = request.form[f'visitante{i}']          
            cur.execute('INSERT INTO universidad_partidos (jornada_id, fecha, hora, local, resultadoA, resultadoB, visitante) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                        (jornada_id, fecha, hora, local, resultadoA, resultadoB, visitante))       
        mysql.connection.commit()
        cur.close()
    return redirect(url_for('calend_universidad')) 
# Partidos Universidad Valladolid
@app.route('/admin/calend_universidad')
def calend_universidad():
    cur = mysql.connection.cursor()
    cur.execute('SELECT id, nombre FROM jornadas_universidad')
    jornadas = cur.fetchall()
    for jornada in jornadas:
        cur.execute('SELECT id, fecha, hora, local, resultadoA, resultadoB, visitante FROM universidad_partidos WHERE jornada_id = %s', (jornada['id'],))
        partidos = cur.fetchall()
        jornada['partidos'] = partidos
    cur.close()
    return render_template('admin/calend_universidad.html', jornadas=jornadas)
# Modificar los partidos de cada jornada
@app.route('/modificar_jornada_universidad/<string:id>', methods=['POST'])
def modificar_jorn_universidad(id):
    nombre_jornada = request.form['nombre']
    num_partidos = int(request.form['num_partidos'])
    cur = mysql.connection.cursor()
    # Actualizar la jornada
    cur.execute('UPDATE jornadas_universidad SET nombre = %s WHERE id = %s', (nombre_jornada, id))
    # Actualizar los partidos de la jornada
    for i in range(num_partidos):
        partido_id = request.form[f'partido_id{i}']
        fecha = request.form[f'fecha{i}']
        hora = request.form[f'hora{i}']
        local = request.form[f'local{i}']
        resultadoA = request.form[f'resultadoA{i}']
        resultadoB = request.form[f'resultadoB{i}']
        visitante = request.form[f'visitante{i}']   
        cur.execute('UPDATE universidad_partidos SET fecha = %s, hora = %s, local = %s, resultadoA = %s, resultadoB = %s, visitante = %s WHERE id = %s',
                    (fecha, hora, local, resultadoA, resultadoB, visitante, partido_id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('calend_universidad'))
# Ruta para borrar jornadas
@app.route('/eliminar_jorn_universidad/<string:id>', methods=['POST'])
def eliminar_jorn_universidad(id):
    cur = mysql.connection.cursor()
    # Eliminar los partidos asociados a la jornada
    cur.execute('DELETE FROM universidad_partidos WHERE jornada_id = %s', (id,))
    # Eliminar la jornada
    cur.execute('DELETE FROM jornadas_universidad WHERE id = %s', (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('calend_universidad'))
# Obtener datos para CD Parquesol
def obtener_datos_universidad():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM jornadas_universidad")
    jornadas = cur.fetchall()
    jornadas_con_partidos = []
    for jornada in jornadas:
        cur.execute("SELECT * FROM universidad_partidos WHERE jornada_id = %s", (jornada['id'],))
        partidos = cur.fetchall()
        jornada_con_partidos = {
            'nombre': jornada['nombre'],
            'partidos': partidos
        }       
        jornadas_con_partidos.append(jornada_con_partidos)
    cur.close()
    return jornadas_con_partidos
# Ruta y creación del calendario individual del Universidad Valladolid
@app.route('/equipos_futbol_sala/calendario_universidad')
def calendarios_universidad():
    datos17 = obtener_datos_universidad()
    nuevos_datos_universidad = [dato for dato in datos17 if dato]
    equipo_universidad = 'C.D.Univ. Valladolid'
    tabla_partidos_universidad = {}
    # Iteramos sobre cada jornada y partido
    for jornada in datos17:
        for partido in jornada['partidos']:
            equipo_local = partido['local']
            equipo_visitante = partido['visitante']
            resultado_local = partido['resultadoA']
            resultado_visitante = partido['resultadoB']           
            # Verificamos si el Simancas está jugando
            if equipo_local == equipo_universidad or equipo_visitante == equipo_universidad:
                # Determinamos el equipo contrario y los resultados
                if equipo_local == equipo_universidad:
                    equipo_contrario = equipo_visitante
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_universidad = 'C'
                else:
                    equipo_contrario = equipo_local
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_universidad = 'F'
                # Verificamos si el equipo contrario no está en la tabla
                if equipo_contrario not in tabla_partidos_universidad:
                    tabla_partidos_universidad[equipo_contrario] = {'jornadas': {}}                       
                # Verificamos si es el primer o segundo enfrentamiento
                if 'primer_enfrentamiento' not in tabla_partidos_universidad[equipo_contrario]:
                    tabla_partidos_universidad[equipo_contrario]['primer_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_universidad[equipo_contrario]['resultadoA'] = resultado_a
                    tabla_partidos_universidad[equipo_contrario]['resultadoB'] = resultado_b
                elif 'segundo_enfrentamiento' not in tabla_partidos_universidad[equipo_contrario]:
                    tabla_partidos_universidad[equipo_contrario]['segundo_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_universidad[equipo_contrario]['resultadoAA'] = resultado_a
                    tabla_partidos_universidad[equipo_contrario]['resultadoBB'] = resultado_b  
                # Agregamos la jornada y resultados
                if jornada['nombre'] not in tabla_partidos_universidad[equipo_contrario]['jornadas']:
                    tabla_partidos_universidad[equipo_contrario]['jornadas'][jornada['nombre']] = {
                        'resultadoA': resultado_a,
                        'resultadoB': resultado_b,
                        'rol_universidad': rol_universidad
                    }
                # Asignamos los resultados según el rol del Universidad Valladolid
                if equipo_local == equipo_contrario or equipo_visitante == equipo_contrario:
                  if not tabla_partidos_universidad[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA']:
                    tabla_partidos_universidad[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA'] = resultado_a
                    tabla_partidos_universidad[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoB'] = resultado_b
                    tabla_partidos_universidad[equipo_contrario]['jornadas'][jornada['nombre']]['rol_universidad'] = rol_universidad
                  else:
                    tabla_partidos_universidad[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_universidad[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_universidad[equipo_contrario]['jornadas'][jornada['nombre']]['rol_universidad'] = rol_universidad
                else:
                  if not tabla_partidos_universidad[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA']:
                    tabla_partidos_universidad[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_universidad[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_universidad[equipo_contrario]['jornadas'][jornada['nombre']]['rol_universidad'] = rol_universidad
                  else:
                    tabla_partidos_universidad[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_universidad[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_universidad[equipo_contrario]['jornadas'][jornada['nombre']]['rol_universidad'] = rol_universidad
    return render_template('equipos_futbol_sala/calendario_universidad.html', tabla_partidos_universidad=tabla_partidos_universidad, nuevos_datos_universidad=nuevos_datos_universidad)
# Crear la clasificación del Universidad Valladolid
def generar_clasificacion_analisis_futsal_universidad(data):
    default_dict = defaultdict(lambda: {})
    clasificacion = defaultdict(lambda: {'puntos': 0,'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'favor': 0, 'contra': 0, 'diferencia_goles': 0})
    for jornada in data:
        for partido in jornada['partidos']:
            equipo_local = partido['local']
            equipo_visitante = partido['visitante']
            try:
                resultado_local = int(partido['resultadoA'])
                resultado_visitante = int(partido['resultadoB'])
            except ValueError:
                print(f"Error al convertir resultados a enteros en el partido {partido}")
                continue
            if clasificacion[equipo_local]['jugados'] > 0:
                promedio_favor_local = clasificacion[equipo_local]['favor'] / clasificacion[equipo_local]['jugados']
            else:
                promedio_favor_local = 0
            # Ajusta la lógica según tus reglas para asignar puntos y calcular estadísticas en baloncesto
            if resultado_local > resultado_visitante:
                clasificacion[equipo_local]['puntos'] += 3
                clasificacion[equipo_local]['ganados'] += 1
                clasificacion[equipo_visitante]['perdidos'] += 1
            elif resultado_local < resultado_visitante:
                clasificacion[equipo_local]['puntos'] += 0
                clasificacion[equipo_local]['perdidos'] += 1
                clasificacion[equipo_visitante]['puntos'] += 3
                clasificacion[equipo_visitante]['ganados'] += 1
            else:
                clasificacion[equipo_local]['puntos'] += 1
                clasificacion[equipo_local]['empatados'] += 1
                clasificacion[equipo_visitante]['puntos'] += 1
                clasificacion[equipo_visitante]['empatados'] += 1
            clasificacion[equipo_local]['jugados'] += 1
            clasificacion[equipo_visitante]['jugados'] += 1
            clasificacion[equipo_local]['favor'] += resultado_local
            clasificacion[equipo_local]['contra'] += resultado_visitante
            clasificacion[equipo_visitante]['favor'] += resultado_visitante
            clasificacion[equipo_visitante]['contra'] += resultado_local
            clasificacion[equipo_local]['diferencia_goles'] += resultado_local - resultado_visitante
            clasificacion[equipo_visitante]['diferencia_goles'] += resultado_visitante - resultado_local
    # Ordena la clasificación por puntos y diferencia de canastas
    clasificacion_ordenada = [{'equipo': equipo, 'datos': datos} for equipo, datos in sorted(clasificacion.items(), key=lambda x: (x[1]['puntos'], x[1]['diferencia_goles']), reverse=True)]
    print(generar_clasificacion_analisis_futsal_universidad)
    return clasificacion_ordenada 
# Ruta para mostrar la clasificación y análisis del Universidad Valladolid
@app.route('/equipos_futbol_sala/clasi_analis_universidad/')
def clasif_analisis_universidad():
    data7 = obtener_datos_universidad()
    # Genera la clasificación y análisis actual
    clasificacion_analisis_universidad = generar_clasificacion_analisis_futsal_universidad(data7)    
    # Obtén los equipos de la jornada 0
    clubs_universidad = obtener_clubs_universidad()
    # Inicializa las estadísticas de los equipos de la jornada 0 si no están ya en la clasificación
    for club in clubs_universidad:
        if not any(equipo['equipo'] == club['nombre'] for equipo in clasificacion_analisis_universidad):
            equipo = {
                'equipo': club['nombre'],
                'datos': {
                    'puntos': 0,
                    'jugados': 0,
                    'ganados': 0,
                    'empatados': 0,
                    'perdidos': 0,
                    'favor': 0,
                    'contra': 0,
                    'diferencia_goles': 0
                }
            }
            clasificacion_analisis_universidad.append(equipo)
    return render_template('equipos_futbol_sala/clasi_analis_universidad.html', clasificacion_analisis_universidad=clasificacion_analisis_universidad)
# Crear la Jornada 0, inscribir a los club participantes
def obtener_clubs_universidad():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM universidad_clubs")
    clubs = cur.fetchall()
    cur.close()
    return [{'id': club['id'], 'nombre': club['nombre']} for club in clubs]
@app.route('/admin/jornada0_universidad', methods=['GET', 'POST'])
def jornada0_universidad():
    if request.method == 'POST':
        if 'equipo' in request.form:
            club = request.form['equipo']
            if club:
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO universidad_clubs (nombre) VALUES (%s)", (club,))
                mysql.connection.commit()
                cur.close()
            return redirect(url_for('jornada0_universidad'))
        elif 'index' in request.form:
            index = int(request.form['index'])
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM universidad_clubs WHERE id = %s", (index + 1,))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('jornada0_universidad'))
    clubs = obtener_clubs_universidad()
    return render_template('admin/clubs_universidad.html', clubs=clubs, indices=range(len(clubs)))
@app.route('/admin/eliminar_club_universidad/<string:club_id>', methods=['POST'])
def eliminar_club_universidad(club_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM universidad_clubs WHERE id = %s", (club_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('jornada0_universidad'))
# Fin proceso Universidad Valladolid

# EQUIPOS BALONMANO
#Todo el proceso de calendario y clasificación del Aula Valladolid
# Ingresar los resultados de los partidos del Aula Valladolid
@app.route('/admin/crear_calendario_aula', methods=['POST'])
def ingresar_resul_aula():
    if request.method == 'POST':
        nombre_jornada = request.form['nombre']
        num_partidos = int(request.form['num_partidos'])       
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO jornadas_aula (nombre) VALUES (%s)', (nombre_jornada,))
        jornada_id = cur.lastrowid        
        for i in range(num_partidos):
            fecha = request.form[f'fecha{i}']
            hora = request.form[f'hora{i}']
            local = request.form[f'local{i}']
            resultadoA = request.form[f'resultadoA{i}']
            resultadoB = request.form[f'resultadoB{i}']
            visitante = request.form[f'visitante{i}']          
            cur.execute('INSERT INTO aula_partidos (jornada_id, fecha, hora, local, resultadoA, resultadoB, visitante) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                        (jornada_id, fecha, hora, local, resultadoA, resultadoB, visitante))       
        mysql.connection.commit()
        cur.close()
    return redirect(url_for('calend_aula')) 
# Partidos Aula
@app.route('/admin/calend_aula')
def calend_aula():
    cur = mysql.connection.cursor()
    cur.execute('SELECT id, nombre FROM jornadas_aula')
    jornadas = cur.fetchall()
    for jornada in jornadas:
        cur.execute('SELECT id, fecha, hora, local, resultadoA, resultadoB, visitante FROM aula_partidos WHERE jornada_id = %s', (jornada['id'],))
        partidos = cur.fetchall()
        jornada['partidos'] = partidos
    cur.close()
    return render_template('admin/calend_aula.html', jornadas=jornadas)
# Modificar los partidos de cada jornada
@app.route('/modificar_jornada_aula/<string:id>', methods=['POST'])
def modificar_jorn_aula(id):
    nombre_jornada = request.form['nombre']
    num_partidos = int(request.form['num_partidos'])
    cur = mysql.connection.cursor()
    # Actualizar la jornada
    cur.execute('UPDATE jornadas_aula SET nombre = %s WHERE id = %s', (nombre_jornada, id))
    # Actualizar los partidos de la jornada
    for i in range(num_partidos):
        partido_id = request.form[f'partido_id{i}']
        fecha = request.form[f'fecha{i}']
        hora = request.form[f'hora{i}']
        local = request.form[f'local{i}']
        resultadoA = request.form[f'resultadoA{i}']
        resultadoB = request.form[f'resultadoB{i}']
        visitante = request.form[f'visitante{i}']   
        cur.execute('UPDATE aula_partidos SET fecha = %s, hora = %s, local = %s, resultadoA = %s, resultadoB = %s, visitante = %s WHERE id = %s',
                    (fecha, hora, local, resultadoA, resultadoB, visitante, partido_id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('calend_aula'))
# Ruta para borrar jornadas
@app.route('/eliminar_jorn_aula/<string:id>', methods=['POST'])
def eliminar_jorn_aula(id):
    cur = mysql.connection.cursor()
    # Eliminar los partidos asociados a la jornada
    cur.execute('DELETE FROM aula_partidos WHERE jornada_id = %s', (id,))
    # Eliminar la jornada
    cur.execute('DELETE FROM jornadas_aula WHERE id = %s', (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('calend_aula'))
# Obtener datos para CD Parquesol
def obtener_datos_aula():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM jornadas_aula")
    jornadas = cur.fetchall()
    jornadas_con_partidos = []
    for jornada in jornadas:
        cur.execute("SELECT * FROM aula_partidos WHERE jornada_id = %s", (jornada['id'],))
        partidos = cur.fetchall()
        jornada_con_partidos = {
            'nombre': jornada['nombre'],
            'partidos': partidos
        }       
        jornadas_con_partidos.append(jornada_con_partidos)
    cur.close()
    return jornadas_con_partidos 
# Ruta y creación del calendario individual del Aula Valladolid
@app.route('/equipos_balonmano/calendario_aula')
def calendarios_aula():
    datos7 = obtener_datos_aula()
    nuevos_datos_aula = [dato for dato in datos7 if dato]
    equipo_aula = 'Aula Valladolid F'
    tabla_partidos_aula = {}
    # Iteramos sobre cada jornada y partido
    for jornada in datos7:
        for partido in jornada['partidos']:
            equipo_local = partido['local']
            equipo_visitante = partido['visitante']
            resultado_local = partido['resultadoA']
            resultado_visitante = partido['resultadoB']          
            # Verificamos si el Simancas está jugando
            if equipo_local == equipo_aula or equipo_visitante == equipo_aula:
                # Determinamos el equipo contrario y los resultados
                if equipo_local == equipo_aula:
                    equipo_contrario = equipo_visitante
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_aula = 'C'
                else:
                    equipo_contrario = equipo_local
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_aula = 'F'
                # Verificamos si el equipo contrario no está en la tabla
                if equipo_contrario not in tabla_partidos_aula:
                    tabla_partidos_aula[equipo_contrario] = {'jornadas': {}}                       
                # Verificamos si es el primer o segundo enfrentamiento
                if 'primer_enfrentamiento' not in tabla_partidos_aula[equipo_contrario]:
                    tabla_partidos_aula[equipo_contrario]['primer_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_aula[equipo_contrario]['resultadoA'] = resultado_a
                    tabla_partidos_aula[equipo_contrario]['resultadoB'] = resultado_b
                elif 'segundo_enfrentamiento' not in tabla_partidos_aula[equipo_contrario]:
                    tabla_partidos_aula[equipo_contrario]['segundo_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_aula[equipo_contrario]['resultadoAA'] = resultado_a
                    tabla_partidos_aula[equipo_contrario]['resultadoBB'] = resultado_b  
                # Agregamos la jornada y resultados
                if jornada['nombre'] not in tabla_partidos_aula[equipo_contrario]['jornadas']:
                    tabla_partidos_aula[equipo_contrario]['jornadas'][jornada['nombre']] = {
                        'resultadoA': resultado_a,
                        'resultadoB': resultado_b,
                        'rol_aula': rol_aula
                    }
                # Asignamos los resultados según el rol del Real Valladolid
                if equipo_local == equipo_contrario or equipo_visitante == equipo_contrario:
                  if not tabla_partidos_aula[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA']:
                    tabla_partidos_aula[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA'] = resultado_a
                    tabla_partidos_aula[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoB'] = resultado_b
                    tabla_partidos_aula[equipo_contrario]['jornadas'][jornada['nombre']]['rol_aula'] = rol_aula
                  else:
                    tabla_partidos_aula[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_aula[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_aula[equipo_contrario]['jornadas'][jornada['nombre']]['rol_aula'] = rol_aula
                else:
                  if not tabla_partidos_aula[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA']:
                    tabla_partidos_aula[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_aula[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_aula[equipo_contrario]['jornadas'][jornada['nombre']]['rol_aula'] = rol_aula
                  else:
                    tabla_partidos_aula[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_aula[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_aula[equipo_contrario]['jornadas'][jornada['nombre']]['rol_aula'] = rol_aula
    return render_template('equipos_balonmano/calendario_aula.html', tabla_partidos_aula=tabla_partidos_aula, nuevos_datos_aula=nuevos_datos_aula)
# Crear la clasificación del Aula Valladolid
def generar_clasificacion_analisis_balonmano_aula(data):
    default_dict = defaultdict(lambda: {})
    clasificacion = defaultdict(lambda: {'puntos': 0,'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'favor': 0, 'contra': 0, 'diferencia_goles': 0})
    for jornada in data:
        for partido in jornada['partidos']:
            equipo_local = partido['local']
            equipo_visitante = partido['visitante']
            try:
                resultado_local = int(partido['resultadoA'])
                resultado_visitante = int(partido['resultadoB'])
            except ValueError:
                print(f"Error al convertir resultados a enteros en el partido {partido}")
                continue
            if clasificacion[equipo_local]['jugados'] > 0:
                promedio_favor_local = clasificacion[equipo_local]['favor'] / clasificacion[equipo_local]['jugados']
            else:
                promedio_favor_local = 0
            # Ajusta la lógica según tus reglas para asignar puntos y calcular estadísticas en baloncesto
            if resultado_local > resultado_visitante:
                clasificacion[equipo_local]['puntos'] += 2
                clasificacion[equipo_local]['ganados'] += 1
                clasificacion[equipo_visitante]['perdidos'] += 1
            elif resultado_local < resultado_visitante:
                clasificacion[equipo_local]['puntos'] += 0
                clasificacion[equipo_local]['perdidos'] += 1
                clasificacion[equipo_visitante]['puntos'] += 2
                clasificacion[equipo_visitante]['ganados'] += 1
            else:
                clasificacion[equipo_local]['puntos'] += 1
                clasificacion[equipo_local]['empatados'] += 1
                clasificacion[equipo_visitante]['puntos'] += 1
                clasificacion[equipo_visitante]['empatados'] += 1
            clasificacion[equipo_local]['jugados'] += 1
            clasificacion[equipo_visitante]['jugados'] += 1
            clasificacion[equipo_local]['favor'] += resultado_local
            clasificacion[equipo_local]['contra'] += resultado_visitante
            clasificacion[equipo_visitante]['favor'] += resultado_visitante
            clasificacion[equipo_visitante]['contra'] += resultado_local
            clasificacion[equipo_local]['diferencia_goles'] += resultado_local - resultado_visitante
            clasificacion[equipo_visitante]['diferencia_goles'] += resultado_visitante - resultado_local
    # Ordena la clasificación por puntos y diferencia de canastas
    clasificacion_ordenada = [{'equipo': equipo, 'datos': datos} for equipo, datos in sorted(clasificacion.items(), key=lambda x: (x[1]['puntos'], x[1]['diferencia_goles']), reverse=True)]
    print(generar_clasificacion_analisis_balonmano_aula)
    return clasificacion_ordenada
# Ruta para mostrar la clasificación y análisis del Aula Valladolid
@app.route('/equipos_balonmano/clasi_analis_aula/')
def clasif_analisis_aula():
    data8 = obtener_datos_aula()
    # Genera la clasificación y análisis actual
    clasificacion_analisis_aula = generar_clasificacion_analisis_balonmano_aula(data8)    
    # Obtén los equipos de la jornada 0
    clubs_aula = obtener_clubs_aula()
    # Inicializa las estadísticas de los equipos de la jornada 0 si no están ya en la clasificación
    for club in clubs_aula:
        if not any(equipo['equipo'] == club['nombre'] for equipo in clasificacion_analisis_aula):
            equipo = {
                'equipo': club['nombre'],
                'datos': {
                    'puntos': 0,
                    'jugados': 0,
                    'ganados': 0,
                    'empatados': 0,
                    'perdidos': 0,
                    'favor': 0,
                    'contra': 0,
                    'diferencia_goles': 0
                }
            }
            clasificacion_analisis_aula.append(equipo)       
    return render_template('equipos_balonmano/clasi_analis_aula.html', clasificacion_analisis_aula=clasificacion_analisis_aula)
# Crear la Jornada 0, inscribir a los club participantes
def obtener_clubs_aula():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM aula_clubs")
    clubs = cur.fetchall()
    cur.close()
    return [{'id': club['id'], 'nombre': club['nombre']} for club in clubs]
@app.route('/admin/jornada0_aula', methods=['GET', 'POST'])
def jornada0_aula():
    if request.method == 'POST':
        if 'equipo' in request.form:
            club = request.form['equipo']
            if club:
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO aula_clubs (nombre) VALUES (%s)", (club,))
                mysql.connection.commit()
                cur.close()
            return redirect(url_for('jornada0_aula'))
        elif 'index' in request.form:
            index = int(request.form['index'])
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM aula_clubs WHERE id = %s", (index + 1,))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('jornada0_aula'))
    clubs = obtener_clubs_aula()
    return render_template('admin/clubs_aula.html', clubs=clubs, indices=range(len(clubs)))
@app.route('/admin/eliminar_club_aula/<string:club_id>', methods=['POST'])
def eliminar_club_aula(club_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM aula_clubs WHERE id = %s", (club_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('jornada0_aula'))
# Fin proceso Aula Valladolid F

#Todo el proceso de calendario y clasificación del Atlético Valladolid
# Ruta de partidos Atlético Valladolid
# Ingresar los resultados de los partidos del Atlético Valladolid
@app.route('/admin/crear_calendario_recoletas', methods=['POST'])
def ingresar_resul_recoletas():
    if request.method == 'POST':
        nombre_jornada = request.form['nombre']
        num_partidos = int(request.form['num_partidos'])       
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO jornadas_recoletas (nombre) VALUES (%s)', (nombre_jornada,))
        jornada_id = cur.lastrowid        
        for i in range(num_partidos):
            fecha = request.form[f'fecha{i}']
            hora = request.form[f'hora{i}']
            local = request.form[f'local{i}']
            resultadoA = request.form[f'resultadoA{i}']
            resultadoB = request.form[f'resultadoB{i}']
            visitante = request.form[f'visitante{i}']          
            cur.execute('INSERT INTO recoletas_partidos (jornada_id, fecha, hora, local, resultadoA, resultadoB, visitante) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                        (jornada_id, fecha, hora, local, resultadoA, resultadoB, visitante))       
        mysql.connection.commit()
        cur.close()
    return redirect(url_for('calend_recoletas')) 
# Partidos Atlético Valladolid
@app.route('/admin/calend_recoletas')
def calend_recoletas():
    cur = mysql.connection.cursor()
    cur.execute('SELECT id, nombre FROM jornadas_recoletas')
    jornadas = cur.fetchall()
    for jornada in jornadas:
        cur.execute('SELECT id, fecha, hora, local, resultadoA, resultadoB, visitante FROM recoletas_partidos WHERE jornada_id = %s', (jornada['id'],))
        partidos = cur.fetchall()
        jornada['partidos'] = partidos
    cur.close()
    return render_template('admin/calend_recoletas.html', jornadas=jornadas)
# Modificar los partidos de cada jornada
@app.route('/modificar_jornada_recoletas/<string:id>', methods=['POST'])
def modificar_jorn_recoletas(id):
    nombre_jornada = request.form['nombre']
    num_partidos = int(request.form['num_partidos'])
    cur = mysql.connection.cursor()
    # Actualizar la jornada
    cur.execute('UPDATE jornadas_recoletas SET nombre = %s WHERE id = %s', (nombre_jornada, id))
    # Actualizar los partidos de la jornada
    for i in range(num_partidos):
        partido_id = request.form[f'partido_id{i}']
        fecha = request.form[f'fecha{i}']
        hora = request.form[f'hora{i}']
        local = request.form[f'local{i}']
        resultadoA = request.form[f'resultadoA{i}']
        resultadoB = request.form[f'resultadoB{i}']
        visitante = request.form[f'visitante{i}']   
        cur.execute('UPDATE recoletas_partidos SET fecha = %s, hora = %s, local = %s, resultadoA = %s, resultadoB = %s, visitante = %s WHERE id = %s',
                    (fecha, hora, local, resultadoA, resultadoB, visitante, partido_id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('calend_recoletas'))
# Ruta para borrar jornadas
@app.route('/eliminar_jorn_recoletas/<string:id>', methods=['POST'])
def eliminar_jorn_recoletas(id):
    cur = mysql.connection.cursor()
    # Eliminar los partidos asociados a la jornada
    cur.execute('DELETE FROM recoletas_partidos WHERE jornada_id = %s', (id,))
    # Eliminar la jornada
    cur.execute('DELETE FROM jornadas_recoletas WHERE id = %s', (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('calend_recoletas'))
# Obtener datos para CD Atl. Valladolid
def obtener_datos_recoletas():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM jornadas_recoletas")
    jornadas = cur.fetchall()
    jornadas_con_partidos = []
    for jornada in jornadas:
        cur.execute("SELECT * FROM recoletas_partidos WHERE jornada_id = %s", (jornada['id'],))
        partidos = cur.fetchall()
        jornada_con_partidos = {
            'nombre': jornada['nombre'],
            'partidos': partidos
        }       
        jornadas_con_partidos.append(jornada_con_partidos)
    cur.close()
    return jornadas_con_partidos
# Ruta y creación del calendario individual del Aula Valladolid
@app.route('/equipos_balonmano/calendario_recoletas')
def calendarios_recoletas():
    datos8 = obtener_datos_recoletas()
    nuevos_datos_recoletas = [dato for dato in datos8 if dato]
    equipo_recoletas = 'Atl.Valladolid'
    tabla_partidos_recoletas = {}
    # Iteramos sobre cada jornada y partido
    for jornada in datos8:
        for partido in jornada['partidos']:
            equipo_local = partido['local']
            equipo_visitante = partido['visitante']
            resultado_local = partido['resultadoA']
            resultado_visitante = partido['resultadoB']           
            # Verificamos si el Simancas está jugando
            if equipo_local == equipo_recoletas or equipo_visitante == equipo_recoletas:
                # Determinamos el equipo contrario y los resultados
                if equipo_local == equipo_recoletas:
                    equipo_contrario = equipo_visitante
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_recoletas = 'C'
                else:
                    equipo_contrario = equipo_local
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_recoletas = 'F'
                # Verificamos si el equipo contrario no está en la tabla
                if equipo_contrario not in tabla_partidos_recoletas:
                    tabla_partidos_recoletas[equipo_contrario] = {'jornadas': {}}                       
                # Verificamos si es el primer o segundo enfrentamiento
                if 'primer_enfrentamiento' not in tabla_partidos_recoletas[equipo_contrario]:
                    tabla_partidos_recoletas[equipo_contrario]['primer_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_recoletas[equipo_contrario]['resultadoA'] = resultado_a
                    tabla_partidos_recoletas[equipo_contrario]['resultadoB'] = resultado_b
                elif 'segundo_enfrentamiento' not in tabla_partidos_recoletas[equipo_contrario]:
                    tabla_partidos_recoletas[equipo_contrario]['segundo_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_recoletas[equipo_contrario]['resultadoAA'] = resultado_a
                    tabla_partidos_recoletas[equipo_contrario]['resultadoBB'] = resultado_b  
                # Agregamos la jornada y resultados
                if jornada['nombre'] not in tabla_partidos_recoletas[equipo_contrario]['jornadas']:
                    tabla_partidos_recoletas[equipo_contrario]['jornadas'][jornada['nombre']] = {
                        'resultadoA': resultado_a,
                        'resultadoB': resultado_b,
                        'rol_recoletas': rol_recoletas
                    }
                # Asignamos los resultados según el rol del Real Valladolid
                if equipo_local == equipo_contrario or equipo_visitante == equipo_contrario:
                  if not tabla_partidos_recoletas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA']:
                    tabla_partidos_recoletas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA'] = resultado_a
                    tabla_partidos_recoletas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoB'] = resultado_b
                    tabla_partidos_recoletas[equipo_contrario]['jornadas'][jornada['nombre']]['rol_recoletas'] = rol_recoletas
                  else:
                    tabla_partidos_recoletas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_recoletas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_recoletas[equipo_contrario]['jornadas'][jornada['nombre']]['rol_recoletas'] = rol_recoletas
                else:
                  if not tabla_partidos_recoletas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA']:
                    tabla_partidos_recoletas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_recoletas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_recoletas[equipo_contrario]['jornadas'][jornada['nombre']]['rol_recoletas'] = rol_recoletas
                  else:
                    tabla_partidos_recoletas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_recoletas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_recoletas[equipo_contrario]['jornadas'][jornada['nombre']]['rol_recoletas'] = rol_recoletas
    return render_template('equipos_balonmano/calendario_recoletas.html', tabla_partidos_recoletas=tabla_partidos_recoletas, nuevos_datos_recoletas=nuevos_datos_recoletas)
# Crear la clasificación del Atlético Valladolid
def generar_clasificacion_analisis_balonmano_recoletas(data):
    default_dict = defaultdict(lambda: {})
    clasificacion = defaultdict(lambda: {'puntos': 0,'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'favor': 0, 'contra': 0, 'diferencia_goles': 0})
    for jornada in data:
        for partido in jornada['partidos']:
            equipo_local = partido['local']
            equipo_visitante = partido['visitante']
            try:
                resultado_local = int(partido['resultadoA'])
                resultado_visitante = int(partido['resultadoB'])
            except ValueError:
                print(f"Error al convertir resultados a enteros en el partido {partido}")
                continue
            if clasificacion[equipo_local]['jugados'] > 0:
                promedio_favor_local = clasificacion[equipo_local]['favor'] / clasificacion[equipo_local]['jugados']
            else:
                promedio_favor_local = 0
            # Ajusta la lógica según tus reglas para asignar puntos y calcular estadísticas en baloncesto
            if resultado_local > resultado_visitante:
                clasificacion[equipo_local]['puntos'] += 2
                clasificacion[equipo_local]['ganados'] += 1
                clasificacion[equipo_visitante]['perdidos'] += 1
            elif resultado_local < resultado_visitante:
                clasificacion[equipo_local]['puntos'] += 0
                clasificacion[equipo_local]['perdidos'] += 1
                clasificacion[equipo_visitante]['puntos'] += 2
                clasificacion[equipo_visitante]['ganados'] += 1
            else:
                clasificacion[equipo_local]['puntos'] += 1
                clasificacion[equipo_local]['empatados'] += 1
                clasificacion[equipo_visitante]['puntos'] += 1
                clasificacion[equipo_visitante]['empatados'] += 1
            clasificacion[equipo_local]['jugados'] += 1
            clasificacion[equipo_visitante]['jugados'] += 1
            clasificacion[equipo_local]['favor'] += resultado_local
            clasificacion[equipo_local]['contra'] += resultado_visitante
            clasificacion[equipo_visitante]['favor'] += resultado_visitante
            clasificacion[equipo_visitante]['contra'] += resultado_local
            clasificacion[equipo_local]['diferencia_goles'] += resultado_local - resultado_visitante
            clasificacion[equipo_visitante]['diferencia_goles'] += resultado_visitante - resultado_local
    # Ordena la clasificación por puntos y diferencia de canastas
    clasificacion_ordenada = [{'equipo': equipo, 'datos': datos} for equipo, datos in sorted(clasificacion.items(), key=lambda x: (x[1]['puntos'], x[1]['diferencia_goles']), reverse=True)]
    print(generar_clasificacion_analisis_balonmano_recoletas)
    return clasificacion_ordenada
# Ruta para mostrar la clasificación y análisis del Aula Valladolid
@app.route('/equipos_balonmano/clasi_analis_recoletas/')
def clasif_analisis_recoletas():
    data9 = obtener_datos_recoletas()
    # Genera la clasificación y análisis actual
    clasificacion_analisis_recoletas = generar_clasificacion_analisis_balonmano_recoletas(data9)    
    # Obtén los equipos de la jornada 0
    clubs_recoletas = obtener_clubs_recoletas()
    # Inicializa las estadísticas de los equipos de la jornada 0 si no están ya en la clasificación
    for club in clubs_recoletas:
        if not any(equipo['equipo'] == club['nombre'] for equipo in clasificacion_analisis_recoletas):
            equipo = {
                'equipo': club['nombre'],
                'datos': {
                    'puntos': 0,
                    'jugados': 0,
                    'ganados': 0,
                    'empatados': 0,
                    'perdidos': 0,
                    'favor': 0,
                    'contra': 0,
                    'diferencia_goles': 0
                }
            }
            clasificacion_analisis_recoletas.append(equipo)        
    return render_template('equipos_balonmano/clasi_analis_recoletas.html', clasificacion_analisis_recoletas=clasificacion_analisis_recoletas)
# Crear la Jornada 0, inscribir a los club participantes
def obtener_clubs_recoletas():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM recoletas_clubs")
    clubs = cur.fetchall()
    cur.close()
    return [{'id': club['id'], 'nombre': club['nombre']} for club in clubs]
@app.route('/admin/jornada0_recoletas', methods=['GET', 'POST'])
def jornada0_recoletas():
    if request.method == 'POST':
        if 'equipo' in request.form:
            club = request.form['equipo']
            if club:
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO recoletas_clubs (nombre) VALUES (%s)", (club,))
                mysql.connection.commit()
                cur.close()
            return redirect(url_for('jornada0_recoletas'))
        elif 'index' in request.form:
            index = int(request.form['index'])
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM recoletas_clubs WHERE id = %s", (index + 1,))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('jornada0_recoletas'))
    clubs = obtener_clubs_recoletas()
    return render_template('admin/clubs_recoletas.html', clubs=clubs, indices=range(len(clubs)))
@app.route('/admin/eliminar_club_recoletas/<string:club_id>', methods=['POST'])
def eliminar_club_recoletas(club_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM recoletas_clubs WHERE id = %s", (club_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('jornada0_recoletas'))
#Fin proceso Atlético Valladolid

#EQUIPOS RUGBY
#Todo el proceso de calendario y clasificación del El Salvador
# Ingresar los resultados de los partidos de El Salvador
@app.route('/admin/crear_calendario_salvador', methods=['POST'])
def ingresar_resul_salvador():
    if request.method == 'POST':
        nombre_jornada = request.form['nombre']
        num_partidos = int(request.form['num_partidos'])       
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO jornadas_salvador (nombre) VALUES (%s)', (nombre_jornada,))
        jornada_id = cur.lastrowid        
        for i in range(num_partidos):
            fecha = request.form[f'fecha{i}']
            hora = request.form[f'hora{i}']
            local = request.form[f'local{i}']
            bonusA = request.form[f'bonusA{i}']
            resultadoA = request.form[f'resultadoA{i}']
            resultadoB = request.form[f'resultadoB{i}']
            bonusB = request.form[f'bonusB{i}']
            visitante = request.form[f'visitante{i}']          
            cur.execute('INSERT INTO salvador_partidos (jornada_id, fecha, hora, local, bonusA ,resultadoA, resultadoB, bonusB, visitante) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                        (jornada_id, fecha, hora, local, bonusA , resultadoA, resultadoB, bonusB,visitante))       
        mysql.connection.commit()
        cur.close()
    return redirect(url_for('calend_salvador'))
# Partidos El Salvador
@app.route('/admin/calend_salvador')
def calend_salvador():
    cur = mysql.connection.cursor()
    cur.execute('SELECT id, nombre FROM jornadas_salvador')
    jornadas = cur.fetchall()
    for jornada in jornadas:
        cur.execute('SELECT id, fecha, hora, local, bonusA, resultadoA, resultadoB, bonusB, visitante FROM salvador_partidos WHERE jornada_id = %s', (jornada['id'],))
        partidos = cur.fetchall()
        jornada['partidos'] = partidos
    cur.close()
    return render_template('admin/calend_salvador.html', jornadas=jornadas)
# Modificar los partidos de cada jornada
@app.route('/modificar_jornada_salvador/<string:id>', methods=['POST'])
def modificar_jorn_salvador(id):
    nombre_jornada = request.form['nombre']
    num_partidos = int(request.form['num_partidos'])
    cur = mysql.connection.cursor()
    # Actualizar la jornada
    cur.execute('UPDATE jornadas_salvador SET nombre = %s WHERE id = %s', (nombre_jornada, id))
    # Actualizar los partidos de la jornada
    for i in range(num_partidos):
        partido_id = request.form[f'partido_id{i}']
        fecha = request.form[f'fecha{i}']
        hora = request.form[f'hora{i}']
        local = request.form[f'local{i}']
        bonusA = request.form[f'bonusA{i}']
        resultadoA = request.form[f'resultadoA{i}']
        resultadoB = request.form[f'resultadoB{i}']
        bonusB = request.form[f'bonusB{i}']
        visitante = request.form[f'visitante{i}']   
        cur.execute('UPDATE salvador_partidos SET fecha = %s, hora = %s, local = %s, bonusA = %s, resultadoA = %s, resultadoB = %s, bonusB = %s ,visitante = %s WHERE id = %s',
                    (fecha, hora, local, bonusA,resultadoA, resultadoB, bonusB,visitante, partido_id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('calend_salvador'))
# Ruta para borrar jornadas
@app.route('/eliminar_jorn_salvador/<string:id>', methods=['POST'])
def eliminar_jorn_salvador(id):
    cur = mysql.connection.cursor()
    # Eliminar los partidos asociados a la jornada
    cur.execute('DELETE FROM salvador_partidos WHERE jornada_id = %s', (id,))
    # Eliminar la jornada
    cur.execute('DELETE FROM jornadas_salvador WHERE id = %s', (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('calend_salvador'))
# Obtener datos para CR El Salvador
def obtener_datos_salvador():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM jornadas_salvador")
    jornadas = cur.fetchall()
    jornadas_con_partidos = []
    for jornada in jornadas:
        cur.execute("SELECT * FROM salvador_partidos WHERE jornada_id = %s", (jornada['id'],))
        partidos = cur.fetchall()
        jornada_con_partidos = {
            'nombre': jornada['nombre'],
            'partidos': partidos
        }       
        jornadas_con_partidos.append(jornada_con_partidos)
    cur.close()
    return jornadas_con_partidos
total_partidos_temporada_salvador = 11
total_partidos_temporada_grupos_salvador = 5
# Ruta y creación del calendario individual de El Salvador
@app.route('/equipos_rugby/calendario_salvador')
def calendarios_salvador():
    datos11 = obtener_datos_salvador()
    nuevos_datos_salvador = [dato for dato in datos11 if dato]
    equipo_salvador = 'CR El Salvador'
    tabla_partidos_salvador = {}
    # Iteramos sobre cada jornada y partido
    for jornada in datos11:
        for partido in jornada['partidos']:
            equipo_local = partido['local']
            equipo_visitante = partido['visitante']
            resultado_local = partido['resultadoA']
            resultado_visitante = partido['resultadoB']           
            # Verificamos si El Salvador está jugando
            if equipo_local == equipo_salvador or equipo_visitante == equipo_salvador:
                # Determinamos el equipo contrario y los resultados
                if equipo_local == equipo_salvador:
                    equipo_contrario = equipo_visitante
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_salvador = 'C'
                else:
                    equipo_contrario = equipo_local
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_salvador = 'F'
                # Verificamos si el equipo contrario no está en la tabla
                if equipo_contrario not in tabla_partidos_salvador:
                    tabla_partidos_salvador[equipo_contrario] = {'jornadas': {}}                       
                # Verificamos si es el primer o segundo enfrentamiento
                if 'primer_enfrentamiento' not in tabla_partidos_salvador[equipo_contrario]:
                    tabla_partidos_salvador[equipo_contrario]['primer_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_salvador[equipo_contrario]['resultadoA'] = resultado_a
                    tabla_partidos_salvador[equipo_contrario]['resultadoB'] = resultado_b
                elif 'segundo_enfrentamiento' not in tabla_partidos_salvador[equipo_contrario]:
                    tabla_partidos_salvador[equipo_contrario]['segundo_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_salvador[equipo_contrario]['resultadoAA'] = resultado_a
                    tabla_partidos_salvador[equipo_contrario]['resultadoBB'] = resultado_b  
                # Agregamos la jornada y resultados
                if jornada['nombre'] not in tabla_partidos_salvador[equipo_contrario]['jornadas']:
                    tabla_partidos_salvador[equipo_contrario]['jornadas'][jornada['nombre']] = {
                        'resultadoA': resultado_a,
                        'resultadoB': resultado_b,
                        'rol_salvador': rol_salvador
                    }
                # Asignamos los resultados según el rol del Real Valladolid
                if equipo_local == equipo_contrario or equipo_visitante == equipo_contrario:
                  if not tabla_partidos_salvador[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA']:
                    tabla_partidos_salvador[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA'] = resultado_a
                    tabla_partidos_salvador[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoB'] = resultado_b
                    tabla_partidos_salvador[equipo_contrario]['jornadas'][jornada['nombre']]['rol_salvador'] = rol_salvador
                  else:
                    tabla_partidos_salvador[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_salvador[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_salvador[equipo_contrario]['jornadas'][jornada['nombre']]['rol_salvador'] = rol_salvador
                else:
                  if not tabla_partidos_salvador[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA']:
                    tabla_partidos_salvador[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_salvador[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_salvador[equipo_contrario]['jornadas'][jornada['nombre']]['rol_salvador'] = rol_salvador
                  else:
                    tabla_partidos_salvador[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_salvador[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_salvador[equipo_contrario]['jornadas'][jornada['nombre']]['rol_salvador'] = rol_salvador
    return render_template('equipos_rugby/calendario_salvador.html', tabla_partidos_salvador=tabla_partidos_salvador, nuevos_datos_salvador=nuevos_datos_salvador)
# Crear la clasificación de El Salvador
def generar_clasificacion_analisis_rugby_salvador(data,total_partidos):
    default_dict = defaultdict(lambda: {})
    clasificacion = defaultdict(lambda: {'puntos': 0,'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'favor': 0, 'contra': 0, 'diferencia_goles': 0, 'bonus': 0})
    for jornada in data[:total_partidos]:
        for partido in jornada['partidos']:
            equipo_local = partido['local']
            equipo_visitante = partido['visitante']
            try:
                bonus_local = int(partido['bonusA'])
                resultado_local = int(partido['resultadoA'])
                resultado_visitante = int(partido['resultadoB'])
                bonus_visitante = int(partido['bonusB'])
            except ValueError:
                print(f"Error al convertir resultados a enteros en el partido {partido}")
                continue
            if clasificacion[equipo_local]['jugados'] > 0:
                promedio_favor_local = clasificacion[equipo_local]['favor'] / clasificacion[equipo_local]['jugados']
            else:
                promedio_favor_local = 0
            # Ajusta la lógica según tus reglas para asignar puntos y calcular estadísticas en baloncesto
            if resultado_local > resultado_visitante:
                clasificacion[equipo_local]['puntos'] += 4 + bonus_local
                clasificacion[equipo_local]['ganados'] += 1
                clasificacion[equipo_visitante]['puntos'] += 0 + bonus_visitante
                clasificacion[equipo_visitante]['perdidos'] += 1
            elif resultado_local < resultado_visitante:
                clasificacion[equipo_local]['puntos'] += 0 + bonus_local
                clasificacion[equipo_local]['perdidos'] += 1
                clasificacion[equipo_visitante]['puntos'] += 4 + bonus_visitante
                clasificacion[equipo_visitante]['ganados'] += 1
            else:
                clasificacion[equipo_local]['puntos'] += 2 + bonus_local
                clasificacion[equipo_local]['empatados'] += 1
                clasificacion[equipo_visitante]['puntos'] += 2 + bonus_visitante
                clasificacion[equipo_visitante]['empatados'] += 1                    
            # Calcula los bonus
            clasificacion[equipo_local]['bonus'] += bonus_local
            clasificacion[equipo_visitante]['bonus'] += bonus_visitante    
            clasificacion[equipo_local]['jugados'] += 1
            clasificacion[equipo_visitante]['jugados'] += 1
            clasificacion[equipo_local]['favor'] += resultado_local
            clasificacion[equipo_local]['contra'] += resultado_visitante
            clasificacion[equipo_visitante]['favor'] += resultado_visitante
            clasificacion[equipo_visitante]['contra'] += resultado_local
            clasificacion[equipo_local]['diferencia_goles'] += resultado_local - resultado_visitante
            clasificacion[equipo_visitante]['diferencia_goles'] += resultado_visitante - resultado_local
    # Ordena la clasificación por puntos y diferencia de canastas
    clasificacion_ordenada = [{'equipo': equipo, 'datos': datos} for equipo, datos in sorted(clasificacion.items(), key=lambda x: (x[1]['puntos'], x[1]['diferencia_goles']), reverse=True)]
    return clasificacion_ordenada 
# Crear la clasificación para el GrupoA1 y GrupoB1 de El Salvador
def generar_clasificacion_grupoA1_grupoB1(data, total_partidos):
    clasificacion = defaultdict(lambda: {'puntos': 0, 'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'favor': 0, 'contra': 0, 'diferencia_goles': 0, 'bonus': 0})
    for jornada in data[:total_partidos]:
        for partido in jornada['partidos']:
            equipo_local = partido['local']
            equipo_visitante = partido['visitante']
            try:
                bonus_local = int(partido['bonusA'])
                resultado_local = int(partido['resultadoA'])
                resultado_visitante = int(partido['resultadoB'])
                bonus_visitante = int(partido['bonusB'])
            except ValueError:
                print(f"Error al convertir resultados a enteros en el partido {partido}")
                continue
            if resultado_local > resultado_visitante:
                clasificacion[equipo_local]['puntos'] += 4 + bonus_local
                clasificacion[equipo_local]['ganados'] += 1
                clasificacion[equipo_visitante]['puntos'] += 0 + bonus_visitante
                clasificacion[equipo_visitante]['perdidos'] += 1
            elif resultado_local < resultado_visitante:
                clasificacion[equipo_local]['puntos'] += 0 + bonus_local
                clasificacion[equipo_local]['perdidos'] += 1
                clasificacion[equipo_visitante]['puntos'] += 4 + bonus_visitante
                clasificacion[equipo_visitante]['ganados'] += 1
            else:
                clasificacion[equipo_local]['puntos'] += 2 + bonus_local
                clasificacion[equipo_visitante]['puntos'] += 2 + bonus_visitante
                clasificacion[equipo_local]['empatados'] += 1
                clasificacion[equipo_visitante]['empatados'] += 1
            clasificacion[equipo_local]['bonus'] += bonus_local
            clasificacion[equipo_visitante]['bonus'] += bonus_visitante
            clasificacion[equipo_local]['jugados'] += 1
            clasificacion[equipo_visitante]['jugados'] += 1
            clasificacion[equipo_local]['favor'] += resultado_local
            clasificacion[equipo_local]['contra'] += resultado_visitante
            clasificacion[equipo_visitante]['favor'] += resultado_visitante
            clasificacion[equipo_visitante]['contra'] += resultado_local
            clasificacion[equipo_local]['diferencia_goles'] += resultado_local - resultado_visitante
            clasificacion[equipo_visitante]['diferencia_goles'] += resultado_visitante - resultado_local
    # Ordena la clasificación por puntos y diferencia de goles
    clasificacion_ordenada = [{'equipo': equipo, 'datos': datos} for equipo, datos in sorted(clasificacion.items(), key=lambda x: (x[1]['puntos'], x[1]['diferencia_goles']), reverse=True)]
    # Divide la clasificación en Grupo A y Grupo B
    grupoA1 = clasificacion_ordenada[:6]
    grupoB1 = clasificacion_ordenada[6:12]
    return grupoA1, grupoB1
# Ruta para mostrar la clasificación de El Salvador
@app.route('/equipos_rugby/clasi_analis_salvador/')
def clasif_analisis_salvador():
    data10 = obtener_datos_salvador()
    clasificacion_analisis_salvador = generar_clasificacion_analisis_rugby_salvador(data10, total_partidos_temporada_salvador)
    clubs_salvador = obtener_clubs_salvador()
    clubs_set = {club['equipo'] for club in clasificacion_analisis_salvador}
    for club in clubs_salvador:
        if club['nombre'] not in clubs_set:
            clasificacion_analisis_salvador.append({
                'equipo': club['nombre'],
                'datos': {
                    'puntos': 0,
                    'jugados': 0,
                    'ganados': 0,
                    'empatados': 0,
                    'perdidos': 0,
                    'favor': 0,
                    'contra': 0,
                    'diferencia_goles': 0,
                    'bonus': 0
                }
            })
    clasificacion_analisis_salvador = sorted(clasificacion_analisis_salvador, key=lambda x: (x['datos']['puntos'], x['datos']['diferencia_goles']), reverse=True)
    clasificacion_analisis_salvador_indexed = [{'index': i + 1, 'equipo': equipo['equipo'], 'datos': equipo['datos']} for i, equipo in enumerate(clasificacion_analisis_salvador)]
    data11 = obtener_datos_salvador()  # Asumiendo que usas la misma función para obtener los datos de los grupos
    grupoA1, grupoB1 = generar_clasificacion_grupoA1_grupoB1(data11, total_partidos_temporada_grupos_salvador)
    grupoA1_indexed = [{'index': i + 1, 'equipo': equipo['equipo'], 'datos': equipo['datos']} for i, equipo in enumerate(grupoA1)]
    grupoB1_indexed = [{'index': i + 7, 'equipo': equipo['equipo'], 'datos': equipo['datos']} for i, equipo in enumerate(grupoB1)]
    return render_template('equipos_rugby/clasi_analis_salvador.html', clasificacion_analisis_salvador=clasificacion_analisis_salvador_indexed, grupoA1=grupoA1_indexed, grupoB1=grupoB1_indexed)
# Crear la Jornada 0, inscribir a los club participantes
def obtener_clubs_salvador():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM salvador_clubs")
    clubs = cur.fetchall()
    cur.close()
    return [{'id': club['id'], 'nombre': club['nombre']} for club in clubs]
@app.route('/admin/jornada0_salvador', methods=['GET', 'POST'])
def jornada0_salvador():
    if request.method == 'POST':
        if 'equipo' in request.form:
            club = request.form['equipo']
            if club:
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO salvador_clubs (nombre) VALUES (%s)", (club,))
                mysql.connection.commit()
                cur.close()
            return redirect(url_for('jornada0_salvador'))
        elif 'index' in request.form:
            index = int(request.form['index'])
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM salvador_clubs WHERE id = %s", (index + 1,))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('jornada0_salvador'))
    clubs = obtener_clubs_salvador()
    return render_template('admin/clubs_salvador.html', clubs=clubs, indices=range(len(clubs)))
@app.route('/admin/eliminar_club_salvador/<string:club_id>', methods=['POST'])
def eliminar_club_salvador(club_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM salvador_clubs WHERE id = %s", (club_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('jornada0_salvador'))
#Fin proceso CR El Salvador

#Todo el proceso de calendario y clasificación del VRAC
# Ruta de partidos VRAC
# Ingresar los resultados de los partidos del VRAC
@app.route('/admin/crear_calendario_vrac', methods=['POST'])
def ingresar_resul_vrac():
    if request.method == 'POST':
        nombre_jornada = request.form['nombre']
        num_partidos = int(request.form['num_partidos'])       
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO jornadas_vrac (nombre) VALUES (%s)', (nombre_jornada,))
        jornada_id = cur.lastrowid        
        for i in range(num_partidos):
            fecha = request.form[f'fecha{i}']
            hora = request.form[f'hora{i}']
            local = request.form[f'local{i}']
            bonusA = request.form[f'bonusA{i}']
            resultadoA = request.form[f'resultadoA{i}']
            resultadoB = request.form[f'resultadoB{i}']
            bonusB = request.form[f'bonusB{i}']
            visitante = request.form[f'visitante{i}']          
            cur.execute('INSERT INTO vrac_partidos (jornada_id, fecha, hora, local, bonusA ,resultadoA, resultadoB, bonusB, visitante) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                        (jornada_id, fecha, hora, local, bonusA , resultadoA, resultadoB, bonusB,visitante))       
        mysql.connection.commit()
        cur.close()
    return redirect(url_for('calend_vrac'))
# Partidos VRAC
@app.route('/admin/calend_vrac')
def calend_vrac():
    cur = mysql.connection.cursor()
    cur.execute('SELECT id, nombre FROM jornadas_vrac')
    jornadas = cur.fetchall()
    for jornada in jornadas:
        cur.execute('SELECT id, fecha, hora, local, bonusA, resultadoA, resultadoB, bonusB, visitante FROM vrac_partidos WHERE jornada_id = %s', (jornada['id'],))
        partidos = cur.fetchall()
        jornada['partidos'] = partidos
    cur.close()
    return render_template('admin/calend_vrac.html', jornadas=jornadas)
# Modificar los partidos de cada jornada
@app.route('/modificar_jornada_vrac/<string:id>', methods=['POST'])
def modificar_jorn_vrac(id):
    nombre_jornada = request.form['nombre']
    num_partidos = int(request.form['num_partidos'])
    cur = mysql.connection.cursor()
    # Actualizar la jornada
    cur.execute('UPDATE jornadas_vrac SET nombre = %s WHERE id = %s', (nombre_jornada, id))
    # Actualizar los partidos de la jornada
    for i in range(num_partidos):
        partido_id = request.form[f'partido_id{i}']
        fecha = request.form[f'fecha{i}']
        hora = request.form[f'hora{i}']
        local = request.form[f'local{i}']
        bonusA = request.form[f'bonusA{i}']
        resultadoA = request.form[f'resultadoA{i}']
        resultadoB = request.form[f'resultadoB{i}']
        bonusB = request.form[f'bonusB{i}']
        visitante = request.form[f'visitante{i}']   
        cur.execute('UPDATE vrac_partidos SET fecha = %s, hora = %s, local = %s, bonusA = %s, resultadoA = %s, resultadoB = %s, bonusB = %s ,visitante = %s WHERE id = %s',
                    (fecha, hora, local, bonusA,resultadoA, resultadoB, bonusB,visitante, partido_id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('calend_vrac'))
# Ruta para borrar jornadas
@app.route('/eliminar_jorn_vrac/<string:id>', methods=['POST'])
def eliminar_jorn_vrac(id):
    cur = mysql.connection.cursor()
    # Eliminar los partidos asociados a la jornada
    cur.execute('DELETE FROM vrac_partidos WHERE jornada_id = %s', (id,))
    # Eliminar la jornada
    cur.execute('DELETE FROM jornadas_vrac WHERE id = %s', (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('calend_vrac'))
def obtener_datos_vrac():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM jornadas_vrac")
    jornadas = cur.fetchall()
    jornadas_con_partidos = []
    for jornada in jornadas:
        cur.execute("SELECT * FROM vrac_partidos WHERE jornada_id = %s", (jornada['id'],))
        partidos = cur.fetchall()
        jornada_con_partidos = {
            'nombre': jornada['nombre'],
            'partidos': partidos
        }       
        jornadas_con_partidos.append(jornada_con_partidos)
    cur.close()
    return jornadas_con_partidos
total_partidos_temporada_vrac = 11
total_partidos_temporada_grupos_vrac = 5
# Ruta y creación del calendario individual de El Salvador
@app.route('/equipos_rugby/calendario_vrac')
def calendarios_vrac():
    datos12 = obtener_datos_vrac()
    nuevos_datos_vrac = [dato for dato in datos12 if dato]
    equipo_vrac = 'VRAC Quesos Entrepinares'
    tabla_partidos_vrac = {}
    # Iteramos sobre cada jornada y partido
    for jornada in datos12:
        for partido in jornada['partidos']:
            equipo_local = partido['local']
            equipo_visitante = partido['visitante']
            resultado_local = partido['resultadoA']
            resultado_visitante = partido['resultadoB']           
            # Verificamos si El Salvador está jugando
            if equipo_local == equipo_vrac or equipo_visitante == equipo_vrac:
                # Determinamos el equipo contrario y los resultados
                if equipo_local == equipo_vrac:
                    equipo_contrario = equipo_visitante
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_vrac = 'C'
                else:
                    equipo_contrario = equipo_local
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_vrac = 'F'
                # Verificamos si el equipo contrario no está en la tabla
                if equipo_contrario not in tabla_partidos_vrac:
                    tabla_partidos_vrac[equipo_contrario] = {'jornadas': {}}                       
                # Verificamos si es el primer o segundo enfrentamiento
                if 'primer_enfrentamiento' not in tabla_partidos_vrac[equipo_contrario]:
                    tabla_partidos_vrac[equipo_contrario]['primer_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_vrac[equipo_contrario]['resultadoA'] = resultado_a
                    tabla_partidos_vrac[equipo_contrario]['resultadoB'] = resultado_b
                elif 'segundo_enfrentamiento' not in tabla_partidos_vrac[equipo_contrario]:
                    tabla_partidos_vrac[equipo_contrario]['segundo_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_vrac[equipo_contrario]['resultadoAA'] = resultado_a
                    tabla_partidos_vrac[equipo_contrario]['resultadoBB'] = resultado_b  
                # Agregamos la jornada y resultados
                if jornada['nombre'] not in tabla_partidos_vrac[equipo_contrario]['jornadas']:
                    tabla_partidos_vrac[equipo_contrario]['jornadas'][jornada['nombre']] = {
                        'resultadoA': resultado_a,
                        'resultadoB': resultado_b,
                        'rol_vrac': rol_vrac
                    }
                # Asignamos los resultados según el rol del Real Valladolid
                if equipo_local == equipo_contrario or equipo_visitante == equipo_contrario:
                  if not tabla_partidos_vrac[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA']:
                    tabla_partidos_vrac[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA'] = resultado_a
                    tabla_partidos_vrac[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoB'] = resultado_b
                    tabla_partidos_vrac[equipo_contrario]['jornadas'][jornada['nombre']]['rol_vrac'] = rol_vrac
                  else:
                    tabla_partidos_vrac[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_vrac[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_vrac[equipo_contrario]['jornadas'][jornada['nombre']]['rol_vrac'] = rol_vrac
                else:
                  if not tabla_partidos_vrac[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA']:
                    tabla_partidos_vrac[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_vrac[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_vrac[equipo_contrario]['jornadas'][jornada['nombre']]['rol_vrac'] = rol_vrac
                  else:
                    tabla_partidos_vrac[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_vrac[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_vrac[equipo_contrario]['jornadas'][jornada['nombre']]['rol_vrac'] = rol_vrac
    return render_template('equipos_rugby/calendario_vrac.html', tabla_partidos_vrac=tabla_partidos_vrac, nuevos_datos_vrac=nuevos_datos_vrac)
# Crear la clasificación del VRAC
def generar_clasificacion_analisis_rugby_vrac(data,total_partidos):
    default_dict = defaultdict(lambda: {})
    clasificacion = defaultdict(lambda: {'puntos': 0,'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'favor': 0, 'contra': 0, 'diferencia_goles': 0, 'bonus': 0})
    for jornada in data[:total_partidos]:
        for partido in jornada['partidos']:
            equipo_local = partido['local']
            equipo_visitante = partido['visitante']
            try:
                bonus_local = int(partido['bonusA'])
                resultado_local = int(partido['resultadoA'])
                resultado_visitante = int(partido['resultadoB'])
                bonus_visitante = int(partido['bonusB'])
            except ValueError:
                print(f"Error al convertir resultados a enteros en el partido {partido}")
                continue
            if clasificacion[equipo_local]['jugados'] > 0:
                promedio_favor_local = clasificacion[equipo_local]['favor'] / clasificacion[equipo_local]['jugados']
            else:
                promedio_favor_local = 0
            # Ajusta la lógica según tus reglas para asignar puntos y calcular estadísticas en baloncesto
            if resultado_local > resultado_visitante:
                clasificacion[equipo_local]['puntos'] += 4 + bonus_local
                clasificacion[equipo_local]['ganados'] += 1
                clasificacion[equipo_visitante]['puntos'] += 0 + bonus_visitante
                clasificacion[equipo_visitante]['perdidos'] += 1
            elif resultado_local < resultado_visitante:
                clasificacion[equipo_local]['puntos'] += 0 + bonus_local
                clasificacion[equipo_local]['perdidos'] += 1
                clasificacion[equipo_visitante]['puntos'] += 4 + bonus_visitante
                clasificacion[equipo_visitante]['ganados'] += 1
            else:
                clasificacion[equipo_local]['puntos'] += 2 + bonus_local
                clasificacion[equipo_local]['empatados'] += 1
                clasificacion[equipo_visitante]['puntos'] += 2 + bonus_visitante
                clasificacion[equipo_visitante]['empatados'] += 1                    
            # Calcula los bonus
            clasificacion[equipo_local]['bonus'] += bonus_local
            clasificacion[equipo_visitante]['bonus'] += bonus_visitante    
            clasificacion[equipo_local]['jugados'] += 1
            clasificacion[equipo_visitante]['jugados'] += 1
            clasificacion[equipo_local]['favor'] += resultado_local
            clasificacion[equipo_local]['contra'] += resultado_visitante
            clasificacion[equipo_visitante]['favor'] += resultado_visitante
            clasificacion[equipo_visitante]['contra'] += resultado_local
            clasificacion[equipo_local]['diferencia_goles'] += resultado_local - resultado_visitante
            clasificacion[equipo_visitante]['diferencia_goles'] += resultado_visitante - resultado_local
    # Ordena la clasificación por puntos y diferencia de canastas
    clasificacion_ordenada = [{'equipo': equipo, 'datos': datos} for equipo, datos in sorted(clasificacion.items(), key=lambda x: (x[1]['puntos'], x[1]['diferencia_goles']), reverse=True)]
    return clasificacion_ordenada
# Crear la clasificación para el GrupoA2 y GrupoB2 del VRAC
def generar_clasificacion_grupoA2_grupoB2(data, total_partidos):
    clasificacion = defaultdict(lambda: {'puntos': 0, 'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'favor': 0, 'contra': 0, 'diferencia_goles': 0, 'bonus': 0})
    for jornada in data[:total_partidos]:
        for partido in jornada['partidos']:
            equipo_local = partido['local']
            equipo_visitante = partido['visitante']
            try:
                bonus_local = int(partido['bonusA'])
                resultado_local = int(partido['resultadoA'])
                resultado_visitante = int(partido['resultadoB'])
                bonus_visitante = int(partido['bonusB'])
            except ValueError:
                print(f"Error al convertir resultados a enteros en el partido {partido}")
                continue
            if resultado_local > resultado_visitante:
                clasificacion[equipo_local]['puntos'] += 4 + bonus_local
                clasificacion[equipo_local]['ganados'] += 1
                clasificacion[equipo_visitante]['puntos'] += 0 + bonus_visitante
                clasificacion[equipo_visitante]['perdidos'] += 1
            elif resultado_local < resultado_visitante:
                clasificacion[equipo_local]['puntos'] += 0 + bonus_local
                clasificacion[equipo_local]['perdidos'] += 1
                clasificacion[equipo_visitante]['puntos'] += 4 + bonus_visitante
                clasificacion[equipo_visitante]['ganados'] += 1
            else:
                clasificacion[equipo_local]['puntos'] += 2 + bonus_local
                clasificacion[equipo_visitante]['puntos'] += 2 + bonus_visitante
                clasificacion[equipo_local]['empatados'] += 1
                clasificacion[equipo_visitante]['empatados'] += 1
            clasificacion[equipo_local]['bonus'] += bonus_local
            clasificacion[equipo_visitante]['bonus'] += bonus_visitante
            clasificacion[equipo_local]['jugados'] += 1
            clasificacion[equipo_visitante]['jugados'] += 1
            clasificacion[equipo_local]['favor'] += resultado_local
            clasificacion[equipo_local]['contra'] += resultado_visitante
            clasificacion[equipo_visitante]['favor'] += resultado_visitante
            clasificacion[equipo_visitante]['contra'] += resultado_local
            clasificacion[equipo_local]['diferencia_goles'] += resultado_local - resultado_visitante
            clasificacion[equipo_visitante]['diferencia_goles'] += resultado_visitante - resultado_local
    # Ordena la clasificación por puntos y diferencia de goles
    clasificacion_ordenada = [{'equipo': equipo, 'datos': datos} for equipo, datos in sorted(clasificacion.items(), key=lambda x: (x[1]['puntos'], x[1]['diferencia_goles']), reverse=True)]
    # Divide la clasificación en Grupo A y Grupo B
    grupoA2 = clasificacion_ordenada[:6]
    grupoB2 = clasificacion_ordenada[6:12]
    return grupoA2, grupoB2
# Ruta para mostrar la clasificación del VRAC
@app.route('/equipos_rugby/clasi_analis_vrac/')
def clasif_analisis_vrac():
    data12 = obtener_datos_vrac()
    clasificacion_analisis_vrac = generar_clasificacion_analisis_rugby_vrac(data12, total_partidos_temporada_vrac)
    clubs_vrac = obtener_clubs_vrac()
    clubs_set = {club['equipo'] for club in clasificacion_analisis_vrac}
    for club in clubs_vrac:
        if club['nombre'] not in clubs_set:
            clasificacion_analisis_vrac.append({
                'equipo': club['nombre'],
                'datos': {
                    'puntos': 0,
                    'jugados': 0,
                    'ganados': 0,
                    'empatados': 0,
                    'perdidos': 0,
                    'favor': 0,
                    'contra': 0,
                    'diferencia_goles': 0,
                    'bonus': 0
                }
            })
    clasificacion_analisis_vrac = sorted(clasificacion_analisis_vrac, key=lambda x: (x['datos']['puntos'], x['datos']['diferencia_goles']), reverse=True)
    clasificacion_analisis_vrac_indexed = [{'index': i + 1, 'equipo': equipo['equipo'], 'datos': equipo['datos']} for i, equipo in enumerate(clasificacion_analisis_vrac)]
    data13 = obtener_datos_vrac()  # Asumiendo que usas la misma función para obtener los datos de los grupos
    grupoA2, grupoB2 = generar_clasificacion_grupoA2_grupoB2(data13, total_partidos_temporada_grupos_vrac)
    grupoA2_indexed = [{'index': i + 1, 'equipo': equipo['equipo'], 'datos': equipo['datos']} for i, equipo in enumerate(grupoA2)]
    grupoB2_indexed = [{'index': i + 7, 'equipo': equipo['equipo'], 'datos': equipo['datos']} for i, equipo in enumerate(grupoB2)]
    return render_template('equipos_rugby/clasi_analis_vrac.html', clasificacion_analisis_vrac=clasificacion_analisis_vrac_indexed, grupoA2=grupoA2_indexed, grupoB2=grupoB2_indexed)
# Crear la Jornada 0, inscribir a los club participantes
def obtener_clubs_vrac():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM vrac_clubs")
    clubs = cur.fetchall()
    cur.close()
    return [{'id': club['id'], 'nombre': club['nombre']} for club in clubs]
@app.route('/admin/jornada0_vrac', methods=['GET', 'POST'])
def jornada0_vrac():
    if request.method == 'POST':
        if 'equipo' in request.form:
            club = request.form['equipo']
            if club:
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO vrac_clubs (nombre) VALUES (%s)", (club,))
                mysql.connection.commit()
                cur.close()
            return redirect(url_for('jornada0_vrac'))
        elif 'index' in request.form:
            index = int(request.form['index'])
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM vrac_clubs WHERE id = %s", (index + 1,))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('jornada0_vrac'))
    clubs = obtener_clubs_vrac()
    return render_template('admin/clubs_vrac.html', clubs=clubs, indices=range(len(clubs)))
@app.route('/admin/eliminar_club_vrac/<string:club_id>', methods=['POST'])
def eliminar_club_vrac(club_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM vrac_clubs WHERE id = %s", (club_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('jornada0_vrac'))
#Fin proceso del VRAC

#Todo el proceso de calendario y clasificación del El Salvador Fem.
# Ruta de partidos El Salvador Fem.
# Ingresar los resultados de los partidos de El Salvador Fem.
@app.route('/admin/crear_calendario_salvador_fem', methods=['POST'])
def ingresar_resul_salvador_fem():
    if request.method == 'POST':
        nombre_jornada = request.form['nombre']
        num_partidos = int(request.form['num_partidos'])       
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO jornadas_salvador_fem (nombre) VALUES (%s)', (nombre_jornada,))
        jornada_id = cur.lastrowid        
        for i in range(num_partidos):
            fecha = request.form[f'fecha{i}']
            hora = request.form[f'hora{i}']
            local = request.form[f'local{i}']
            bonusA = request.form[f'bonusA{i}']
            resultadoA = request.form[f'resultadoA{i}']
            resultadoB = request.form[f'resultadoB{i}']
            bonusB = request.form[f'bonusB{i}']
            visitante = request.form[f'visitante{i}']          
            cur.execute('INSERT INTO salvador_fem_partidos (jornada_id, fecha, hora, local, bonusA ,resultadoA, resultadoB, bonusB, visitante) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                        (jornada_id, fecha, hora, local, bonusA , resultadoA, resultadoB, bonusB,visitante))       
        mysql.connection.commit()
        cur.close()
    return redirect(url_for('calend_salvador_fem'))
# Partidos El Salvador
@app.route('/admin/calend_salvador_fem')
def calend_salvador_fem():
    cur = mysql.connection.cursor()
    cur.execute('SELECT id, nombre FROM jornadas_salvador_fem')
    jornadas = cur.fetchall()
    for jornada in jornadas:
        cur.execute('SELECT id, fecha, hora, local, bonusA, resultadoA, resultadoB, bonusB, visitante FROM salvador_fem_partidos WHERE jornada_id = %s', (jornada['id'],))
        partidos = cur.fetchall()
        jornada['partidos'] = partidos
    cur.close()
    return render_template('admin/calend_salvador_fem.html', jornadas=jornadas)
# Modificar los partidos de cada jornada
@app.route('/modificar_jornada_salvador_fem/<string:id>', methods=['POST'])
def modificar_jorn_salvador_fem(id):
    nombre_jornada = request.form['nombre']
    num_partidos = int(request.form['num_partidos'])
    cur = mysql.connection.cursor()
    # Actualizar la jornada
    cur.execute('UPDATE jornadas_salvador_fem SET nombre = %s WHERE id = %s', (nombre_jornada, id))
    # Actualizar los partidos de la jornada
    for i in range(num_partidos):
        partido_id = request.form[f'partido_id{i}']
        fecha = request.form[f'fecha{i}']
        hora = request.form[f'hora{i}']
        local = request.form[f'local{i}']
        bonusA = request.form[f'bonusA{i}']
        resultadoA = request.form[f'resultadoA{i}']
        resultadoB = request.form[f'resultadoB{i}']
        bonusB = request.form[f'bonusB{i}']
        visitante = request.form[f'visitante{i}']   
        cur.execute('UPDATE salvador_fem_partidos SET fecha = %s, hora = %s, local = %s, bonusA = %s, resultadoA = %s, resultadoB = %s, bonusB = %s ,visitante = %s WHERE id = %s',
                    (fecha, hora, local, bonusA,resultadoA, resultadoB, bonusB,visitante, partido_id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('calend_salvador_fem'))
# Ruta para borrar jornadas
@app.route('/eliminar_jorn_salvador_fem/<string:id>', methods=['POST'])
def eliminar_jorn_salvador_fem(id):
    cur = mysql.connection.cursor()
    # Eliminar los partidos asociados a la jornada
    cur.execute('DELETE FROM salvador_fem_partidos WHERE jornada_id = %s', (id,))
    # Eliminar la jornada
    cur.execute('DELETE FROM jornadas_salvador_fem WHERE id = %s', (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('calend_salvador_fem'))
def obtener_datos_salvador_fem():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM jornadas_salvador_fem")
    jornadas = cur.fetchall()
    jornadas_con_partidos = []
    for jornada in jornadas:
        cur.execute("SELECT * FROM salvador_fem_partidos WHERE jornada_id = %s", (jornada['id'],))
        partidos = cur.fetchall()
        jornada_con_partidos = {
            'nombre': jornada['nombre'],
            'partidos': partidos
        }       
        jornadas_con_partidos.append(jornada_con_partidos)
    cur.close()
    return jornadas_con_partidos
total_partidos_temporada_salvador_fem = 7
total_partidos_temporada_grupos_salvador_fem = 3
# Ruta y creación del calendario individual de El Salvador Fem.
@app.route('/equipos_rugby/calendario_salvador_fem')
def calendarios_salvador_fem():
    datos14 = obtener_datos_salvador_fem()
    nuevos_datos_salvador_fem = [dato for dato in datos14 if dato]
    equipo_salvador_fem = 'CR El Salvador Fem.'
    tabla_partidos_salvador_fem = {}
    # Iteramos sobre cada jornada y partido
    for jornada in datos14:
        for partido in jornada['partidos']:
            equipo_local = partido['local']
            equipo_visitante = partido['visitante']
            resultado_local = partido['resultadoA']
            resultado_visitante = partido['resultadoB']           
            # Verificamos si El Salvador está jugando
            if equipo_local == equipo_salvador_fem or equipo_visitante == equipo_salvador_fem:
                # Determinamos el equipo contrario y los resultados
                if equipo_local == equipo_salvador_fem:
                    equipo_contrario = equipo_visitante
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_salvador_fem = 'C'
                else:
                    equipo_contrario = equipo_local
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_salvador_fem = 'F'
                # Verificamos si el equipo contrario no está en la tabla
                if equipo_contrario not in tabla_partidos_salvador_fem:
                    tabla_partidos_salvador_fem[equipo_contrario] = {'jornadas': {}}                       
                # Verificamos si es el primer o segundo enfrentamiento
                if 'primer_enfrentamiento' not in tabla_partidos_salvador_fem[equipo_contrario]:
                    tabla_partidos_salvador_fem[equipo_contrario]['primer_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_salvador_fem[equipo_contrario]['resultadoA'] = resultado_a
                    tabla_partidos_salvador_fem[equipo_contrario]['resultadoB'] = resultado_b
                elif 'segundo_enfrentamiento' not in tabla_partidos_salvador_fem[equipo_contrario]:
                    tabla_partidos_salvador_fem[equipo_contrario]['segundo_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_salvador_fem[equipo_contrario]['resultadoAA'] = resultado_a
                    tabla_partidos_salvador_fem[equipo_contrario]['resultadoBB'] = resultado_b  
                # Agregamos la jornada y resultados
                if jornada['nombre'] not in tabla_partidos_salvador_fem[equipo_contrario]['jornadas']:
                    tabla_partidos_salvador_fem[equipo_contrario]['jornadas'][jornada['nombre']] = {
                        'resultadoA': resultado_a,
                        'resultadoB': resultado_b,
                        'rol_salvador_fem': rol_salvador_fem
                    }
                # Asignamos los resultados según el rol del CR El Salvador Fem.
                if equipo_local == equipo_contrario or equipo_visitante == equipo_contrario:
                  if not tabla_partidos_salvador_fem[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA']:
                    tabla_partidos_salvador_fem[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA'] = resultado_a
                    tabla_partidos_salvador_fem[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoB'] = resultado_b
                    tabla_partidos_salvador_fem[equipo_contrario]['jornadas'][jornada['nombre']]['rol_salvador'] = rol_salvador_fem
                  else:
                    tabla_partidos_salvador_fem[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_salvador_fem[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_salvador_fem[equipo_contrario]['jornadas'][jornada['nombre']]['rol_salvador'] = rol_salvador_fem
                else:
                  if not tabla_partidos_salvador_fem[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA']:
                    tabla_partidos_salvador_fem[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_salvador_fem[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_salvador_fem[equipo_contrario]['jornadas'][jornada['nombre']]['rol_salvador'] = rol_salvador_fem
                  else:
                    tabla_partidos_salvador_fem[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_salvador_fem[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_salvador_fem[equipo_contrario]['jornadas'][jornada['nombre']]['rol_salvador'] = rol_salvador_fem
    return render_template('equipos_rugby/calendario_salvador_fem.html', tabla_partidos_salvador_fem=tabla_partidos_salvador_fem, nuevos_datos_salvador_fem=nuevos_datos_salvador_fem)
# Crear la clasificación de El Salvador Fem.
def generar_clasificacion_analisis_rugby_salvador_fem(data,total_partidos):
    default_dict = defaultdict(lambda: {})
    clasificacion = defaultdict(lambda: {'puntos': 0,'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'favor': 0, 'contra': 0, 'diferencia_goles': 0, 'bonus': 0})
    for jornada in data[:total_partidos]:
        for partido in jornada['partidos']:
            equipo_local = partido['local']
            equipo_visitante = partido['visitante']
            try:
                bonus_local = int(partido['bonusA'])
                resultado_local = int(partido['resultadoA'])
                resultado_visitante = int(partido['resultadoB'])
                bonus_visitante = int(partido['bonusB'])
            except ValueError:
                print(f"Error al convertir resultados a enteros en el partido {partido}")
                continue
            if clasificacion[equipo_local]['jugados'] > 0:
                promedio_favor_local = clasificacion[equipo_local]['favor'] / clasificacion[equipo_local]['jugados']
            else:
                promedio_favor_local = 0
            # Ajusta la lógica según tus reglas para asignar puntos y calcular estadísticas en rugby
            if resultado_local > resultado_visitante:
                clasificacion[equipo_local]['puntos'] += 4 + bonus_local
                clasificacion[equipo_local]['ganados'] += 1
                clasificacion[equipo_visitante]['puntos'] += 0 + bonus_visitante
                clasificacion[equipo_visitante]['perdidos'] += 1
            elif resultado_local < resultado_visitante:
                clasificacion[equipo_local]['puntos'] += 0 + bonus_local
                clasificacion[equipo_local]['perdidos'] += 1
                clasificacion[equipo_visitante]['puntos'] += 4 + bonus_visitante
                clasificacion[equipo_visitante]['ganados'] += 1
            else:
                clasificacion[equipo_local]['puntos'] += 2 + bonus_local
                clasificacion[equipo_local]['empatados'] += 1
                clasificacion[equipo_visitante]['puntos'] += 2 + bonus_visitante
                clasificacion[equipo_visitante]['empatados'] += 1                    
            # Calcula los bonus
            clasificacion[equipo_local]['bonus'] += bonus_local
            clasificacion[equipo_visitante]['bonus'] += bonus_visitante    
            clasificacion[equipo_local]['jugados'] += 1
            clasificacion[equipo_visitante]['jugados'] += 1
            clasificacion[equipo_local]['favor'] += resultado_local
            clasificacion[equipo_local]['contra'] += resultado_visitante
            clasificacion[equipo_visitante]['favor'] += resultado_visitante
            clasificacion[equipo_visitante]['contra'] += resultado_local
            clasificacion[equipo_local]['diferencia_goles'] += resultado_local - resultado_visitante
            clasificacion[equipo_visitante]['diferencia_goles'] += resultado_visitante - resultado_local
    # Ordena la clasificación por puntos y diferencia de canastas
    clasificacion_ordenada = [{'equipo': equipo, 'datos': datos} for equipo, datos in sorted(clasificacion.items(), key=lambda x: (x[1]['puntos'], x[1]['diferencia_goles']), reverse=True)]
    return clasificacion_ordenada 
# Crear la clasificación para el GrupoA3 y GrupoB3 de El Salvador Fem.
def generar_clasificacion_grupoA3_grupoB3(data, total_partidos):
    clasificacion = defaultdict(lambda: {'puntos': 0, 'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'favor': 0, 'contra': 0, 'diferencia_goles': 0, 'bonus': 0})
    for jornada in data[:total_partidos]:
        for partido in jornada['partidos']:
            equipo_local = partido['local']
            equipo_visitante = partido['visitante']
            try:
                bonus_local = int(partido['bonusA'])
                resultado_local = int(partido['resultadoA'])
                resultado_visitante = int(partido['resultadoB'])
                bonus_visitante = int(partido['bonusB'])
            except ValueError:
                print(f"Error al convertir resultados a enteros en el partido {partido}")
                continue
            if resultado_local > resultado_visitante:
                clasificacion[equipo_local]['puntos'] += 4 + bonus_local
                clasificacion[equipo_local]['ganados'] += 1
                clasificacion[equipo_visitante]['puntos'] += 0 + bonus_visitante
                clasificacion[equipo_visitante]['perdidos'] += 1
            elif resultado_local < resultado_visitante:
                clasificacion[equipo_local]['puntos'] += 0 + bonus_local
                clasificacion[equipo_local]['perdidos'] += 1
                clasificacion[equipo_visitante]['puntos'] += 4 + bonus_visitante
                clasificacion[equipo_visitante]['ganados'] += 1
            else:
                clasificacion[equipo_local]['puntos'] += 2 + bonus_local
                clasificacion[equipo_visitante]['puntos'] += 2 + bonus_visitante
                clasificacion[equipo_local]['empatados'] += 1
                clasificacion[equipo_visitante]['empatados'] += 1
            clasificacion[equipo_local]['bonus'] += bonus_local
            clasificacion[equipo_visitante]['bonus'] += bonus_visitante
            clasificacion[equipo_local]['jugados'] += 1
            clasificacion[equipo_visitante]['jugados'] += 1
            clasificacion[equipo_local]['favor'] += resultado_local
            clasificacion[equipo_local]['contra'] += resultado_visitante
            clasificacion[equipo_visitante]['favor'] += resultado_visitante
            clasificacion[equipo_visitante]['contra'] += resultado_local
            clasificacion[equipo_local]['diferencia_goles'] += resultado_local - resultado_visitante
            clasificacion[equipo_visitante]['diferencia_goles'] += resultado_visitante - resultado_local
    # Ordena la clasificación por puntos y diferencia de goles
    clasificacion_ordenada = [{'equipo': equipo, 'datos': datos} for equipo, datos in sorted(clasificacion.items(), key=lambda x: (x[1]['puntos'], x[1]['diferencia_goles']), reverse=True)]
    # Divide la clasificación en Grupo A y Grupo B
    grupoA3 = clasificacion_ordenada[:4]
    grupoB3 = clasificacion_ordenada[4:8]
    return grupoA3, grupoB3
# Ruta para mostrar la clasificación de El Salvador
@app.route('/equipos_rugby/clasi_analis_salvador_fem/')
def clasif_analisis_salvador_fem():
    data15 = obtener_datos_salvador_fem()
    clasificacion_analisis_salvador_fem = generar_clasificacion_analisis_rugby_salvador_fem(data15, total_partidos_temporada_salvador_fem)
    clubs_salvador_fem = obtener_clubs_salvador_fem()
    clubs_set = {club['equipo'] for club in clasificacion_analisis_salvador_fem}
    for club in clubs_salvador_fem:
        if club['nombre'] not in clubs_set:
            clasificacion_analisis_salvador.append({
                'equipo': club['nombre'],
                'datos': {
                    'puntos': 0,
                    'jugados': 0,
                    'ganados': 0,
                    'empatados': 0,
                    'perdidos': 0,
                    'favor': 0,
                    'contra': 0,
                    'diferencia_goles': 0,
                    'bonus': 0
                }
            })
    clasificacion_analisis_salvador_fem = sorted(clasificacion_analisis_salvador_fem, key=lambda x: (x['datos']['puntos'], x['datos']['diferencia_goles']), reverse=True)
    clasificacion_analisis_salvador_fem_indexed = [{'index': i + 1, 'equipo': equipo['equipo'], 'datos': equipo['datos']} for i, equipo in enumerate(clasificacion_analisis_salvador_fem)]
    data16 = obtener_datos_salvador_fem()  # Asumiendo que usas la misma función para obtener los datos de los grupos
    grupoA3, grupoB3 = generar_clasificacion_grupoA3_grupoB3(data16, total_partidos_temporada_grupos_salvador_fem)
    grupoA3_indexed = [{'index': i + 1, 'equipo': equipo['equipo'], 'datos': equipo['datos']} for i, equipo in enumerate(grupoA3)]
    grupoB3_indexed = [{'index': i + 7, 'equipo': equipo['equipo'], 'datos': equipo['datos']} for i, equipo in enumerate(grupoB3)]
    return render_template('equipos_rugby/clasi_analis_salvador_fem.html', clasificacion_analisis_salvador_fem=clasificacion_analisis_salvador_fem_indexed, grupoA3=grupoA3_indexed, grupoB3=grupoB3_indexed)
# Crear la Jornada 0, inscribir a los club participantes
def obtener_clubs_salvador_fem():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM salvador_fem_clubs")
    clubs = cur.fetchall()
    cur.close()
    return [{'id': club['id'], 'nombre': club['nombre']} for club in clubs]
@app.route('/admin/jornada0_salvador_fem', methods=['GET', 'POST'])
def jornada0_salvador_fem():
    if request.method == 'POST':
        if 'equipo' in request.form:
            club = request.form['equipo']
            if club:
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO salvador_fem_clubs (nombre) VALUES (%s)", (club,))
                mysql.connection.commit()
                cur.close()
            return redirect(url_for('jornada0_salvador_fem'))
        elif 'index' in request.form:
            index = int(request.form['index'])
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM salvador_fem_clubs WHERE id = %s", (index + 1,))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('jornada0_salvador_fem'))
    clubs = obtener_clubs_salvador_fem()
    return render_template('admin/clubs_salvador_fem.html', clubs=clubs, indices=range(len(clubs)))
@app.route('/admin/eliminar_club_salvador_fem/<string:club_id>', methods=['POST'])
def eliminar_club_salvador_fem(club_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM salvador_fem_clubs WHERE id = %s", (club_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('jornada0_salvador_fem'))
#Fin proceso El Salvador Fem.

#EQUIPOS HOCKEY
#Todo el proceso de calendario y clasificación del CPLV Caja Rural
# Ingresar los resultados de los partidos de CPLV Caja Rural
@app.route('/admin/crear_calendario_caja', methods=['POST'])
def ingresar_resul_caja():
    if request.method == 'POST':
        nombre_jornada = request.form['nombre']
        num_partidos = int(request.form['num_partidos'])       
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO jornadas_caja (nombre) VALUES (%s)', (nombre_jornada,))
        jornada_id = cur.lastrowid        
        for i in range(num_partidos):
            fecha = request.form[f'fecha{i}']
            hora = request.form[f'hora{i}']
            local = request.form[f'local{i}']
            bonusA = request.form[f'bonusA{i}']
            resultadoA = request.form[f'resultadoA{i}']
            resultadoB = request.form[f'resultadoB{i}']
            bonusB = request.form[f'bonusB{i}']
            visitante = request.form[f'visitante{i}']          
            cur.execute('INSERT INTO caja_partidos (jornada_id, fecha, hora, local, bonusA ,resultadoA, resultadoB, bonusB, visitante) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                        (jornada_id, fecha, hora, local, bonusA , resultadoA, resultadoB, bonusB,visitante))       
        mysql.connection.commit()
        cur.close()
    return redirect(url_for('calend_caja'))
# Partidos Caja Rural CPLV
@app.route('/admin/calend_caja')
def calend_caja():
    cur = mysql.connection.cursor()
    cur.execute('SELECT id, nombre FROM jornadas_caja')
    jornadas = cur.fetchall()
    for jornada in jornadas:
        cur.execute('SELECT id, fecha, hora, local, bonusA, resultadoA, resultadoB, bonusB, visitante FROM caja_partidos WHERE jornada_id = %s', (jornada['id'],))
        partidos = cur.fetchall()
        jornada['partidos'] = partidos
    cur.close()
    return render_template('admin/calend_caja.html', jornadas=jornadas)
# Modificar los partidos de cada jornada
@app.route('/modificar_jornada_caja/<string:id>', methods=['POST'])
def modificar_jorn_caja(id):
    nombre_jornada = request.form['nombre']
    num_partidos = int(request.form['num_partidos'])
    cur = mysql.connection.cursor()
    # Actualizar la jornada
    cur.execute('UPDATE jornadas_caja SET nombre = %s WHERE id = %s', (nombre_jornada, id))
    # Actualizar los partidos de la jornada
    for i in range(num_partidos):
        partido_id = request.form[f'partido_id{i}']
        fecha = request.form[f'fecha{i}']
        hora = request.form[f'hora{i}']
        local = request.form[f'local{i}']
        bonusA = request.form[f'bonusA{i}']
        resultadoA = request.form[f'resultadoA{i}']
        resultadoB = request.form[f'resultadoB{i}']
        bonusB = request.form[f'bonusB{i}']
        visitante = request.form[f'visitante{i}']   
        cur.execute('UPDATE caja_partidos SET fecha = %s, hora = %s, local = %s, bonusA = %s, resultadoA = %s, resultadoB = %s, bonusB = %s ,visitante = %s WHERE id = %s',
                    (fecha, hora, local, bonusA,resultadoA, resultadoB, bonusB,visitante, partido_id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('calend_caja'))
# Ruta para borrar jornadas
@app.route('/eliminar_jorn_caja/<string:id>', methods=['POST'])
def eliminar_jorn_caja(id):
    cur = mysql.connection.cursor()
    # Eliminar los partidos asociados a la jornada
    cur.execute('DELETE FROM caja_partidos WHERE jornada_id = %s', (id,))
    # Eliminar la jornada
    cur.execute('DELETE FROM jornadas_caja WHERE id = %s', (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('calend_caja'))
def obtener_datos_caja():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM jornadas_caja")
    jornadas = cur.fetchall()
    jornadas_con_partidos = []
    for jornada in jornadas:
        cur.execute("SELECT * FROM caja_partidos WHERE jornada_id = %s", (jornada['id'],))
        partidos = cur.fetchall()
        jornada_con_partidos = {
            'nombre': jornada['nombre'],
            'partidos': partidos
        }       
        jornadas_con_partidos.append(jornada_con_partidos)
    cur.close()
    return jornadas_con_partidos
# Ruta y creación del calendario individual del CPLV Caja Rural
@app.route('/equipos_hockey/calendario_caja')
def calendarios_caja():
    datos17 = obtener_datos_caja()
    nuevos_datos_caja = [dato for dato in datos17 if dato]
    equipo_caja = 'CPLV Caja Rural'
    tabla_partidos_caja = {}
    # Iteramos sobre cada jornada y partido
    for jornada in datos17:
        for partido in jornada['partidos']:
            equipo_local = partido['local']
            equipo_visitante = partido['visitante']
            resultado_local = partido['resultadoA']
            resultado_visitante = partido['resultadoB']           
            # Verificamos si El Salvador está jugando
            if equipo_local == equipo_caja or equipo_visitante == equipo_caja:
                # Determinamos el equipo contrario y los resultados
                if equipo_local == equipo_caja:
                    equipo_contrario = equipo_visitante
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_caja = 'C'
                else:
                    equipo_contrario = equipo_local
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_caja = 'F'
                # Verificamos si el equipo contrario no está en la tabla
                if equipo_contrario not in tabla_partidos_caja:
                    tabla_partidos_caja[equipo_contrario] = {'jornadas': {}}                       
                # Verificamos si es el primer o segundo enfrentamiento
                if 'primer_enfrentamiento' not in tabla_partidos_caja[equipo_contrario]:
                    tabla_partidos_caja[equipo_contrario]['primer_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_caja[equipo_contrario]['resultadoA'] = resultado_a
                    tabla_partidos_caja[equipo_contrario]['resultadoB'] = resultado_b
                elif 'segundo_enfrentamiento' not in tabla_partidos_caja[equipo_contrario]:
                    tabla_partidos_caja[equipo_contrario]['segundo_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_caja[equipo_contrario]['resultadoAA'] = resultado_a
                    tabla_partidos_caja[equipo_contrario]['resultadoBB'] = resultado_b  
                # Agregamos la jornada y resultados
                if jornada['nombre'] not in tabla_partidos_caja[equipo_contrario]['jornadas']:
                    tabla_partidos_caja[equipo_contrario]['jornadas'][jornada['nombre']] = {
                        'resultadoA': resultado_a,
                        'resultadoB': resultado_b,
                        'rol_caja': rol_caja
                    }
                # Asignamos los resultados según el rol del Real Valladolid
                if equipo_local == equipo_contrario or equipo_visitante == equipo_contrario:
                  if not tabla_partidos_caja[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA']:
                    tabla_partidos_caja[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA'] = resultado_a
                    tabla_partidos_caja[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoB'] = resultado_b
                    tabla_partidos_caja[equipo_contrario]['jornadas'][jornada['nombre']]['rol_caja'] = rol_caja
                  else:
                    tabla_partidos_caja[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_caja[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_caja[equipo_contrario]['jornadas'][jornada['nombre']]['rol_caja'] = rol_caja
                else:
                  if not tabla_partidos_caja[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA']:
                    tabla_partidos_caja[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_caja[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_caja[equipo_contrario]['jornadas'][jornada['nombre']]['rol_caja'] = rol_caja
                  else:
                    tabla_partidos_caja[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_caja[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_caja[equipo_contrario]['jornadas'][jornada['nombre']]['rol_caja'] = rol_caja
    return render_template('equipos_hockey/calendario_caja.html', tabla_partidos_caja=tabla_partidos_caja, nuevos_datos_caja=nuevos_datos_caja)
# Crear la clasificación de CPLV Caja Rural
def generar_clasificacion_analisis_hockey_caja(data):
    default_dict = defaultdict(lambda: {})
    clasificacion = defaultdict(lambda: {'puntos': 0,'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'favor': 0, 'contra': 0, 'diferencia_goles': 0, 'bonus': 0})
    for jornada in data:
        for partido in jornada['partidos']:
            equipo_local = partido['local']
            equipo_visitante = partido['visitante']
            try:
                bonus_local = int(partido['bonusA'])
                resultado_local = int(partido['resultadoA'])
                resultado_visitante = int(partido['resultadoB'])
                bonus_visitante = int(partido['bonusB'])
            except ValueError:
                print(f"Error al convertir resultados a enteros en el partido {partido}")
                continue
            if clasificacion[equipo_local]['jugados'] > 0:
                promedio_favor_local = clasificacion[equipo_local]['favor'] / clasificacion[equipo_local]['jugados']
            else:
                promedio_favor_local = 0
            # Ajusta la lógica según tus reglas para asignar puntos y calcular estadísticas en baloncesto
            if resultado_local > resultado_visitante:
                clasificacion[equipo_local]['puntos'] += 3
                clasificacion[equipo_local]['ganados'] += 1
                clasificacion[equipo_visitante]['puntos'] += 0
                clasificacion[equipo_visitante]['perdidos'] += 1
            elif resultado_local < resultado_visitante:
                clasificacion[equipo_local]['puntos'] += 0
                clasificacion[equipo_local]['perdidos'] += 1
                clasificacion[equipo_visitante]['puntos'] += 3
                clasificacion[equipo_visitante]['ganados'] += 1
            else:
                clasificacion[equipo_local]['puntos'] += 1 + bonus_local
                clasificacion[equipo_local]['empatados'] += 1
                clasificacion[equipo_visitante]['puntos'] += 1 + bonus_visitante
                clasificacion[equipo_visitante]['empatados'] += 1                    
            # Calcula los bonus
            clasificacion[equipo_local]['bonus'] += bonus_local
            clasificacion[equipo_visitante]['bonus'] += bonus_visitante    
            clasificacion[equipo_local]['jugados'] += 1
            clasificacion[equipo_visitante]['jugados'] += 1
            clasificacion[equipo_local]['favor'] += resultado_local
            clasificacion[equipo_local]['contra'] += resultado_visitante
            clasificacion[equipo_visitante]['favor'] += resultado_visitante
            clasificacion[equipo_visitante]['contra'] += resultado_local
            clasificacion[equipo_local]['diferencia_goles'] += resultado_local - resultado_visitante
            clasificacion[equipo_visitante]['diferencia_goles'] += resultado_visitante - resultado_local
    # Ordena la clasificación por puntos y diferencia de canastas
    clasificacion_ordenada = [{'equipo': equipo, 'datos': datos} for equipo, datos in sorted(clasificacion.items(), key=lambda x: (x[1]['puntos'], x[1]['diferencia_goles']), reverse=True)]
    print(generar_clasificacion_analisis_hockey_caja)
    return clasificacion_ordenada
# Ruta para mostrar la clasificación y analisis del CPLV Caja Rural
@app.route('/equipos_hockey/clasi_analis_caja/')
def clasif_analisis_caja():
    data17 = obtener_datos_caja()
    # Genera la clasificación y análisis actual
    clasificacion_analisis_caja = generar_clasificacion_analisis_hockey_caja(data17)    
    # Obtén los equipos de la jornada 0
    clubs_caja = obtener_clubs_caja()
    # Inicializa las estadísticas de los equipos de la jornada 0 si no están ya en la clasificación
    for club in clubs_caja:
        if not any(equipo['equipo'] == club['nombre'] for equipo in clasificacion_analisis_caja):
            equipo = {
                'equipo': club['nombre'],
                'datos': {
                    'puntos': 0,
                    'jugados': 0,
                    'ganados': 0,
                    'empatados': 0,
                    'perdidos': 0,
                    'favor': 0,
                    'contra': 0,
                    'diferencia_goles': 0,
                    'bonus': 0
                }
            }
            clasificacion_analisis_caja.append(equipo) 
    return render_template('equipos_hockey/clasi_analis_caja.html', clasificacion_analisis_caja=clasificacion_analisis_caja)
# Crear la Jornada 0, inscribir a los club participantes
def obtener_clubs_caja():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM caja_clubs")
    clubs = cur.fetchall()
    cur.close()
    return [{'id': club['id'], 'nombre': club['nombre']} for club in clubs]
@app.route('/admin/jornada0_caja', methods=['GET', 'POST'])
def jornada0_caja():
    if request.method == 'POST':
        if 'equipo' in request.form:
            club = request.form['equipo']
            if club:
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO caja_clubs (nombre) VALUES (%s)", (club,))
                mysql.connection.commit()
                cur.close()
            return redirect(url_for('jornada0_caja'))
        elif 'index' in request.form:
            index = int(request.form['index'])
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM caja_clubs WHERE id = %s", (index + 1,))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('jornada0_caja'))
    clubs = obtener_clubs_caja()
    return render_template('admin/clubs_caja.html', clubs=clubs, indices=range(len(clubs)))
@app.route('/admin/eliminar_club_caja/<string:club_id>', methods=['POST'])
def eliminar_club_caja(club_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM caja_clubs WHERE id = %s", (club_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('jornada0_caja'))
#Fin proceso CPLV Caja Rural

#Todo el proceso de calendario y clasificación del CPLV Munia Panteras
# Ruta de partidos CPLV Munia Panteras
# Ingresar los resultados de los partidos de CPLV Munia Panteras
@app.route('/admin/crear_calendario_panteras', methods=['POST'])
def ingresar_resul_panteras():
    data18 = obtener_datos_panteras()
    if request.method == 'POST':
        nombre_jornada = request.form['nombre']
        num_partidos = int(request.form['num_partidos'])       
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO jornadas_panteras (nombre) VALUES (%s)', (nombre_jornada,))
        jornada_id = cur.lastrowid        
        for i in range(num_partidos):
            fecha = request.form[f'fecha{i}']
            hora = request.form[f'hora{i}']
            local = request.form[f'local{i}']
            bonusA = request.form[f'bonusA{i}']
            resultadoA = request.form[f'resultadoA{i}']
            resultadoB = request.form[f'resultadoB{i}']
            bonusB = request.form[f'bonusB{i}']
            visitante = request.form[f'visitante{i}']          
            cur.execute('INSERT INTO panteras_partidos (jornada_id, fecha, hora, local, bonusA ,resultadoA, resultadoB, bonusB, visitante) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                        (jornada_id, fecha, hora, local, bonusA , resultadoA, resultadoB, bonusB,visitante))       
        mysql.connection.commit()
        cur.close()
    return redirect(url_for('calend_panteras'))
# Partidos CPLV Munia Panteras
@app.route('/admin/calend_panteras')
def calend_panteras():
    cur = mysql.connection.cursor()
    cur.execute('SELECT id, nombre FROM jornadas_panteras')
    jornadas = cur.fetchall()
    for jornada in jornadas:
        cur.execute('SELECT id, fecha, hora, local, bonusA, resultadoA, resultadoB, bonusB, visitante FROM panteras_partidos WHERE jornada_id = %s', (jornada['id'],))
        partidos = cur.fetchall()
        jornada['partidos'] = partidos
    cur.close()
    return render_template('admin/calend_panteras.html', jornadas=jornadas)
# Modificar los partidos de cada jornada
@app.route('/modificar_jornada_panteras/<string:id>', methods=['POST'])
def modificar_jorn_panteras(id):
    nombre_jornada = request.form['nombre']
    num_partidos = int(request.form['num_partidos'])
    cur = mysql.connection.cursor()
    # Actualizar la jornada
    cur.execute('UPDATE jornadas_panteras SET nombre = %s WHERE id = %s', (nombre_jornada, id))
    # Actualizar los partidos de la jornada
    for i in range(num_partidos):
        partido_id = request.form[f'partido_id{i}']
        fecha = request.form[f'fecha{i}']
        hora = request.form[f'hora{i}']
        local = request.form[f'local{i}']
        bonusA = request.form[f'bonusA{i}']
        resultadoA = request.form[f'resultadoA{i}']
        resultadoB = request.form[f'resultadoB{i}']
        bonusB = request.form[f'bonusB{i}']
        visitante = request.form[f'visitante{i}']   
        cur.execute('UPDATE panteras_partidos SET fecha = %s, hora = %s, local = %s, bonusA = %s, resultadoA = %s, resultadoB = %s, bonusB = %s ,visitante = %s WHERE id = %s',
                    (fecha, hora, local, bonusA,resultadoA, resultadoB, bonusB,visitante, partido_id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('calend_panteras'))
# Ruta para borrar jornadas
@app.route('/eliminar_jorn_panteras/<string:id>', methods=['POST'])
def eliminar_jorn_panteras(id):
    cur = mysql.connection.cursor()
    # Eliminar los partidos asociados a la jornada
    cur.execute('DELETE FROM panteras_partidos WHERE jornada_id = %s', (id,))
    # Eliminar la jornada
    cur.execute('DELETE FROM jornadas_panteras WHERE id = %s', (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('calend_panteras'))
def obtener_datos_panteras():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM jornadas_panteras")
    jornadas = cur.fetchall()
    jornadas_con_partidos = []
    for jornada in jornadas:
        cur.execute("SELECT * FROM panteras_partidos WHERE jornada_id = %s", (jornada['id'],))
        partidos = cur.fetchall()
        jornada_con_partidos = {
            'nombre': jornada['nombre'],
            'partidos': partidos
        }       
        jornadas_con_partidos.append(jornada_con_partidos)
    cur.close()
    return jornadas_con_partidos
# Ruta y creación del calendario individual del CPLV Munia Panteras
@app.route('/equipos_hockey/calendario_panteras')
def calendarios_panteras():
    datos18 = obtener_datos_panteras()
    nuevos_datos_panteras = [dato for dato in datos18 if dato]
    equipo_panteras = 'CPLV Munia Panteras'
    tabla_partidos_panteras = {}
    # Iteramos sobre cada jornada y partido
    for jornada in datos18:
        for partido in jornada['partidos']:
            equipo_local = partido['local']
            equipo_visitante = partido['visitante']
            resultado_local = partido['resultadoA']
            resultado_visitante = partido['resultadoB']           
            # Verificamos si El Salvador está jugando
            if equipo_local == equipo_panteras or equipo_visitante == equipo_panteras:
                # Determinamos el equipo contrario y los resultados
                if equipo_local == equipo_panteras:
                    equipo_contrario = equipo_visitante
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_panteras = 'C'
                else:
                    equipo_contrario = equipo_local
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_panteras = 'F'
                # Verificamos si el equipo contrario no está en la tabla
                if equipo_contrario not in tabla_partidos_panteras:
                    tabla_partidos_panteras[equipo_contrario] = {'jornadas': {}}                       
                # Verificamos si es el primer o segundo enfrentamiento
                if 'primer_enfrentamiento' not in tabla_partidos_panteras[equipo_contrario]:
                    tabla_partidos_panteras[equipo_contrario]['primer_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_panteras[equipo_contrario]['resultadoA'] = resultado_a
                    tabla_partidos_panteras[equipo_contrario]['resultadoB'] = resultado_b
                elif 'segundo_enfrentamiento' not in tabla_partidos_panteras[equipo_contrario]:
                    tabla_partidos_panteras[equipo_contrario]['segundo_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_panteras[equipo_contrario]['resultadoAA'] = resultado_a
                    tabla_partidos_panteras[equipo_contrario]['resultadoBB'] = resultado_b  
                # Agregamos la jornada y resultados
                if jornada['nombre'] not in tabla_partidos_panteras[equipo_contrario]['jornadas']:
                    tabla_partidos_panteras[equipo_contrario]['jornadas'][jornada['nombre']] = {
                        'resultadoA': resultado_a,
                        'resultadoB': resultado_b,
                        'rol_panteras': rol_panteras
                    }
                # Asignamos los resultados según el rol del Real Valladolid
                if equipo_local == equipo_contrario or equipo_visitante == equipo_contrario:
                  if not tabla_partidos_panteras[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA']:
                    tabla_partidos_panteras[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA'] = resultado_a
                    tabla_partidos_panteras[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoB'] = resultado_b
                    tabla_partidos_panteras[equipo_contrario]['jornadas'][jornada['nombre']]['rol_panteras'] = rol_panteras
                  else:
                    tabla_partidos_panteras[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_panteras[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_panteras[equipo_contrario]['jornadas'][jornada['nombre']]['rol_panteras'] = rol_panteras
                else:
                  if not tabla_partidos_panteras[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA']:
                    tabla_partidos_panteras[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_panteras[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_panteras[equipo_contrario]['jornadas'][jornada['nombre']]['rol_panteras'] = rol_panteras
                  else:
                    tabla_partidos_panteras[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_panteras[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_panteras[equipo_contrario]['jornadas'][jornada['nombre']]['rol_panteras'] = rol_panteras
    return render_template('equipos_hockey/calendario_panteras.html', tabla_partidos_panteras=tabla_partidos_panteras, nuevos_datos_panteras=nuevos_datos_panteras)
# Crear la clasificación de CPLV Munia Panteras
def generar_clasificacion_analisis_hockey_panteras(data):
    default_dict = defaultdict(lambda: {})
    clasificacion = defaultdict(lambda: {'puntos': 0,'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'favor': 0, 'contra': 0, 'diferencia_goles': 0, 'bonus': 0})
    for jornada in data:
        for partido in jornada['partidos']:
            equipo_local = partido['local']
            equipo_visitante = partido['visitante']
            try:
                bonus_local = int(partido['bonusA'])
                resultado_local = int(partido['resultadoA'])
                resultado_visitante = int(partido['resultadoB'])
                bonus_visitante = int(partido['bonusB'])
            except ValueError:
                print(f"Error al convertir resultados a enteros en el partido {partido}")
                continue
            if clasificacion[equipo_local]['jugados'] > 0:
                promedio_favor_local = clasificacion[equipo_local]['favor'] / clasificacion[equipo_local]['jugados']
            else:
                promedio_favor_local = 0
            # Ajusta la lógica según tus reglas para asignar puntos y calcular estadísticas en baloncesto
            if resultado_local > resultado_visitante:
                clasificacion[equipo_local]['puntos'] += 3
                clasificacion[equipo_local]['ganados'] += 1
                clasificacion[equipo_visitante]['puntos'] += 0
                clasificacion[equipo_visitante]['perdidos'] += 1
            elif resultado_local < resultado_visitante:
                clasificacion[equipo_local]['puntos'] += 0
                clasificacion[equipo_local]['perdidos'] += 1
                clasificacion[equipo_visitante]['puntos'] += 3
                clasificacion[equipo_visitante]['ganados'] += 1
            else:
                clasificacion[equipo_local]['puntos'] += 1 + bonus_local
                clasificacion[equipo_local]['empatados'] += 1
                clasificacion[equipo_visitante]['puntos'] += 1 + bonus_visitante
                clasificacion[equipo_visitante]['empatados'] += 1                    
            # Calcula los bonus
            clasificacion[equipo_local]['bonus'] += bonus_local
            clasificacion[equipo_visitante]['bonus'] += bonus_visitante    
            clasificacion[equipo_local]['jugados'] += 1
            clasificacion[equipo_visitante]['jugados'] += 1
            clasificacion[equipo_local]['favor'] += resultado_local
            clasificacion[equipo_local]['contra'] += resultado_visitante
            clasificacion[equipo_visitante]['favor'] += resultado_visitante
            clasificacion[equipo_visitante]['contra'] += resultado_local
            clasificacion[equipo_local]['diferencia_goles'] += resultado_local - resultado_visitante
            clasificacion[equipo_visitante]['diferencia_goles'] += resultado_visitante - resultado_local
    # Ordena la clasificación por puntos y diferencia de canastas
    clasificacion_ordenada = [{'equipo': equipo, 'datos': datos} for equipo, datos in sorted(clasificacion.items(), key=lambda x: (x[1]['puntos'], x[1]['diferencia_goles']), reverse=True)]
    print(generar_clasificacion_analisis_hockey_panteras)
    return clasificacion_ordenada
# Ruta para mostrar la clasificación y analisis del CPLV Munia Panteras
@app.route('/equipos_hockey/clasi_analis_panteras/')
def clasif_analisis_panteras():
    data18 = obtener_datos_panteras()
    # Genera la clasificación y análisis actual
    clasificacion_analisis_panteras = generar_clasificacion_analisis_hockey_panteras(data18)    
    # Obtén los equipos de la jornada 0
    clubs_panteras = obtener_clubs_panteras()
    # Inicializa las estadísticas de los equipos de la jornada 0 si no están ya en la clasificación
    for club in clubs_panteras:
        if not any(equipo['equipo'] == club['nombre'] for equipo in clasificacion_analisis_panteras):
            equipo = {
                'equipo': club['nombre'],
                'datos': {
                    'puntos': 0,
                    'jugados': 0,
                    'ganados': 0,
                    'empatados': 0,
                    'perdidos': 0,
                    'favor': 0,
                    'contra': 0,
                    'diferencia_goles': 0,
                    'bonus': 0
                }
            }
            clasificacion_analisis_panteras.append(equipo)
    return render_template('equipos_hockey/clasi_analis_pante.html', clasificacion_analisis_panteras=clasificacion_analisis_panteras)
# Crear la Jornada 0, inscribir a los club participantes
def obtener_clubs_panteras():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM panteras_clubs")
    clubs = cur.fetchall()
    cur.close()
    return [{'id': club['id'], 'nombre': club['nombre']} for club in clubs]
@app.route('/admin/jornada0_panteras', methods=['GET', 'POST'])
def jornada0_panteras():
    if request.method == 'POST':
        if 'equipo' in request.form:
            club = request.form['equipo']
            if club:
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO panteras_clubs (nombre) VALUES (%s)", (club,))
                mysql.connection.commit()
                cur.close()
            return redirect(url_for('jornada0_panteras'))
        elif 'index' in request.form:
            index = int(request.form['index'])
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM panteras_clubs WHERE id = %s", (index + 1,))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('jornada0_panteras'))
    clubs = obtener_clubs_panteras()
    return render_template('admin/clubs_panteras.html', clubs=clubs, indices=range(len(clubs)))
@app.route('/admin/eliminar_club_panteras/<string:club_id>', methods=['POST'])
def eliminar_club_panteras(club_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM panteras_clubs WHERE id = %s", (club_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('jornada0_panteras'))
#Fin proceso CPLV Munia Panteras

#EQUIPOS VOLEIBOL
#Todo el proceso de calendario y clasificación del Univ. Valladolid VCV
# Ingresar los resultados de los partidos de Univ. Valladolid VCV
@app.route('/admin/crear_calendario_vcv', methods=['POST'])
def ingresar_resul_vcv():
    data19 = obtener_datos_vcv()
    if request.method == 'POST':
        nombre_jornada = request.form['nombre']
        num_partidos = int(request.form['num_partidos'])       
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO jornadas_vcv (nombre) VALUES (%s)', (nombre_jornada,))
        jornada_id = cur.lastrowid        
        for i in range(num_partidos):
            fecha = request.form[f'fecha{i}']
            hora = request.form[f'hora{i}']
            local = request.form[f'local{i}']
            resultadoA = request.form[f'resultadoA{i}']
            resultadoB = request.form[f'resultadoB{i}']
            visitante = request.form[f'visitante{i}']          
            cur.execute('INSERT INTO vcv_partidos (jornada_id, fecha, hora, local ,resultadoA, resultadoB, visitante) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                        (jornada_id, fecha, hora, local, resultadoA, resultadoB, visitante))       
        mysql.connection.commit()
        cur.close()
    return redirect(url_for('calend_vcv'))
# Partidos Univ. Valladolid VCV
@app.route('/admin/calend_vcv')
def calend_vcv():
    cur = mysql.connection.cursor()
    cur.execute('SELECT id, nombre FROM jornadas_vcv')
    jornadas = cur.fetchall()
    for jornada in jornadas:
        cur.execute('SELECT id, fecha, hora, local, resultadoA, resultadoB, visitante FROM vcv_partidos WHERE jornada_id = %s', (jornada['id'],))
        partidos = cur.fetchall()
        jornada['partidos'] = partidos
    cur.close()
    return render_template('admin/calend_vcv.html', jornadas=jornadas)
# Modificar los partidos de cada jornada
@app.route('/modificar_jornada_vcv/<string:id>', methods=['POST'])
def modificar_jorn_vcv(id):
    nombre_jornada = request.form['nombre']
    num_partidos = int(request.form['num_partidos'])
    cur = mysql.connection.cursor()
    # Actualizar la jornada
    cur.execute('UPDATE jornadas_vcv SET nombre = %s WHERE id = %s', (nombre_jornada, id))
    # Actualizar los partidos de la jornada
    for i in range(num_partidos):
        partido_id = request.form[f'partido_id{i}']
        fecha = request.form[f'fecha{i}']
        hora = request.form[f'hora{i}']
        local = request.form[f'local{i}']
        resultadoA = request.form[f'resultadoA{i}']
        resultadoB = request.form[f'resultadoB{i}']
        visitante = request.form[f'visitante{i}']   
        cur.execute('UPDATE vcv_partidos SET fecha = %s, hora = %s, local = %s, resultadoA = %s, resultadoB = %s, visitante = %s WHERE id = %s',
                    (fecha, hora, local, resultadoA, resultadoB, visitante, partido_id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('calend_vcv'))
# Ruta para borrar jornadas
@app.route('/eliminar_jorn_vcv/<string:id>', methods=['POST'])
def eliminar_jorn_vcv(id):
    cur = mysql.connection.cursor()
    # Eliminar los partidos asociados a la jornada
    cur.execute('DELETE FROM vcv_partidos WHERE jornada_id = %s', (id,))
    # Eliminar la jornada
    cur.execute('DELETE FROM jornadas_vcv WHERE id = %s', (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('calend_vcv'))
def obtener_datos_vcv():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM jornadas_vcv")
    jornadas = cur.fetchall()
    jornadas_con_partidos = []
    for jornada in jornadas:
        cur.execute("SELECT * FROM vcv_partidos WHERE jornada_id = %s", (jornada['id'],))
        partidos = cur.fetchall()
        jornada_con_partidos = {
            'nombre': jornada['nombre'],
            'partidos': partidos
        }       
        jornadas_con_partidos.append(jornada_con_partidos)
    cur.close()
    return jornadas_con_partidos
# Ruta y creación del calendario individual del Univ. Valladolid VCV
@app.route('/equipos_voleibol/calendario_vcv')
def calendarios_vcv():
    datos19 = obtener_datos_vcv()
    nuevos_datos_vcv = [dato for dato in datos19 if dato]
    equipo_vcv = 'Univ.Valladolid VCV'
    tabla_partidos_vcv = {}
    # Iteramos sobre cada jornada y partido
    for jornada in datos19:
        for partido in jornada['partidos']:
            equipo_local = partido['local']
            equipo_visitante = partido['visitante']
            resultado_local = partido['resultadoA']
            resultado_visitante = partido['resultadoB']           
            # Verificamos si El Salvador está jugando
            if equipo_local == equipo_vcv or equipo_visitante == equipo_vcv:
                # Determinamos el equipo contrario y los resultados
                if equipo_local == equipo_vcv:
                    equipo_contrario = equipo_visitante
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_vcv = 'C'
                else:
                    equipo_contrario = equipo_local
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_vcv = 'F'
                # Verificamos si el equipo contrario no está en la tabla
                if equipo_contrario not in tabla_partidos_vcv:
                    tabla_partidos_vcv[equipo_contrario] = {'jornadas': {}}                       
                # Verificamos si es el primer o segundo enfrentamiento
                if 'primer_enfrentamiento' not in tabla_partidos_vcv[equipo_contrario]:
                    tabla_partidos_vcv[equipo_contrario]['primer_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_vcv[equipo_contrario]['resultadoA'] = resultado_a
                    tabla_partidos_vcv[equipo_contrario]['resultadoB'] = resultado_b
                elif 'segundo_enfrentamiento' not in tabla_partidos_vcv[equipo_contrario]:
                    tabla_partidos_vcv[equipo_contrario]['segundo_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_vcv[equipo_contrario]['resultadoAA'] = resultado_a
                    tabla_partidos_vcv[equipo_contrario]['resultadoBB'] = resultado_b  
                # Agregamos la jornada y resultados
                if jornada['nombre'] not in tabla_partidos_vcv[equipo_contrario]['jornadas']:
                    tabla_partidos_vcv[equipo_contrario]['jornadas'][jornada['nombre']] = {
                        'resultadoA': resultado_a,
                        'resultadoB': resultado_b,
                        'rol_vcv': rol_vcv
                    }
                # Asignamos los resultados según el rol del Univ. Valladolid VCV
                if equipo_local == equipo_contrario or equipo_visitante == equipo_contrario:
                  if not tabla_partidos_vcv[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA']:
                    tabla_partidos_vcv[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA'] = resultado_a
                    tabla_partidos_vcv[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoB'] = resultado_b
                    tabla_partidos_vcv[equipo_contrario]['jornadas'][jornada['nombre']]['rol_vcv'] = rol_vcv
                  else:
                    tabla_partidos_vcv[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_vcv[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_vcv[equipo_contrario]['jornadas'][jornada['nombre']]['rol_vcv'] = rol_vcv
                else:
                  if not tabla_partidos_vcv[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA']:
                    tabla_partidos_vcv[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_vcv[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_vcv[equipo_contrario]['jornadas'][jornada['nombre']]['rol_vcv'] = rol_vcv
                  else:
                    tabla_partidos_vcv[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_vcv[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_vcv[equipo_contrario]['jornadas'][jornada['nombre']]['rol_vcv'] = rol_vcv
    return render_template('equipos_voleibol/calendario_vcv.html', tabla_partidos_vcv=tabla_partidos_vcv, nuevos_datos_vcv=nuevos_datos_vcv)
# Crear la clasificación de Univ. Valladolid VCV
def generar_clasificacion_analisis_voley_vcv(data):
    clasificacion = defaultdict(lambda: {'puntos': 0, 'jugados': 0, 'ganados3': 0, 'ganados2': 0, 'perdidos1': 0, 'perdidos0': 0, 'favor': 0, 'contra': 0, 'diferencia_sets': 0})
    for jornada in data:
        for partido in jornada['partidos']:
            equipo_local = partido['local']
            equipo_visitante = partido['visitante']
            try:
                resultado_local = int(partido['resultadoA'])
                resultado_visitante = int(partido['resultadoB'])
            except ValueError:
                print(f"Error al convertir resultados a enteros en el partido {partido}")
                continue
            clasificacion[equipo_local]['jugados'] += 1
            clasificacion[equipo_visitante]['jugados'] += 1           
            clasificacion[equipo_local]['favor'] += resultado_local
            clasificacion[equipo_local]['contra'] += resultado_visitante
            clasificacion[equipo_visitante]['favor'] += resultado_visitante
            clasificacion[equipo_visitante]['contra'] += resultado_local           
            if resultado_local > resultado_visitante:  # Equipo local gana
                if resultado_local == 3 and resultado_visitante <= 1:  # 3-0 ó 3-1
                    clasificacion[equipo_local]['puntos'] += 3
                    clasificacion[equipo_local]['ganados3'] += 1
                    clasificacion[equipo_visitante]['puntos'] += 0
                    clasificacion[equipo_visitante]['perdidos0'] += 1
                else:
                    clasificacion[equipo_local]['puntos'] += 2  # 3-2
                    clasificacion[equipo_local]['ganados2'] += 1
                    clasificacion[equipo_visitante]['puntos'] += 1
                    clasificacion[equipo_visitante]['perdidos1'] += 1
            elif resultado_local < resultado_visitante:  # Equipo visitante gana
                if resultado_visitante == 3 and resultado_local <= 1:  # 3-0 ó 3-1
                    clasificacion[equipo_visitante]['puntos'] += 3
                    clasificacion[equipo_visitante]['ganados3'] += 1
                    clasificacion[equipo_local]['puntos'] += 0
                    clasificacion[equipo_local]['perdidos0'] += 1
                else:
                    clasificacion[equipo_visitante]['puntos'] += 2  # 3-2
                    clasificacion[equipo_visitante]['ganados2'] += 1
                    clasificacion[equipo_local]['puntos'] += 1
                    clasificacion[equipo_local]['perdidos1'] += 1
    # Ordena la clasificación por puntos y diferencia de goles
    clasificacion_ordenada = [{'equipo': equipo, 'datos': datos} for equipo, datos in sorted(clasificacion.items(), key=lambda x: (x[1]['puntos'], x[1]['favor'] - x[1]['contra']), reverse=True)]
    return clasificacion_ordenada
# Ruta para mostrar la clasificación y analisis del Univ. Valladolid VCV
@app.route('/equipos_voleibol/clasi_analis_vcv/')
def clasif_analisis_vcv():
    data19 = obtener_datos_vcv()
    # Genera la clasificación y análisis actual
    clasificacion_analisis_vcv = generar_clasificacion_analisis_voley_vcv(data19)    
    # Obtén los equipos de la jornada 0
    clubs_vcv = obtener_clubs_vcv()
    # Inicializa las estadísticas de los equipos de la jornada 0 si no están ya en la clasificación
    for club in clubs_vcv:
        if not any(equipo['equipo'] == club['nombre'] for equipo in clasificacion_analisis_vcv):
            equipo = {
                'equipo': club['nombre'],
                'datos': {
                    'puntos': 0,
                    'jugados': 0,
                    'ganados3': 0,
                    'ganados2': 0,
                    'perdidos1': 0,
                    'perdidos0': 0,
                    'favor': 0,
                    'contra': 0,
                    'diferencia_sets': 0,
                }
            }
            clasificacion_analisis_vcv.append(equipo)
    return render_template('equipos_voleibol/clasi_analis_vcv.html', clasificacion_analisis_vcv=clasificacion_analisis_vcv)
# Crear la Jornada 0, inscribir a los club participantes
def obtener_clubs_vcv():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM vcv_clubs")
    clubs = cur.fetchall()
    cur.close()
    return [{'id': club['id'], 'nombre': club['nombre']} for club in clubs]
@app.route('/admin/jornada0_vcv', methods=['GET', 'POST'])
def jornada0_vcv():
    if request.method == 'POST':
        if 'equipo' in request.form:
            club = request.form['equipo']
            if club:
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO vcv_clubs (nombre) VALUES (%s)", (club,))
                mysql.connection.commit()
                cur.close()
            return redirect(url_for('jornada0_vcv'))
        elif 'index' in request.form:
            index = int(request.form['index'])
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM vcv_clubs WHERE id = %s", (index + 1,))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('jornada0_vcv'))
    clubs = obtener_clubs_vcv()
    return render_template('admin/clubs_vcv.html', clubs=clubs, indices=range(len(clubs)))
@app.route('/admin/eliminar_club_vcv/<string:club_id>', methods=['POST'])
def eliminar_club_vcv(club_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM vcv_clubs WHERE id = %s", (club_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('jornada0_vcv'))
#Fin proceso Univ. Valladolid VCV

# COPA DEL REY Y COPA DE LA REINA
# Crear formulario para los playoff Real Valladolid
@app.route('/admin/crear_copa_valladolid', methods=['GET', 'POST'])
def crear_copa_valladolid():
    if request.method == 'POST':
        eliminatoria = request.form.get('eliminatoria')       
        # Determinar el máximo de partidos permitidos para la eliminatoria
        max_partidos = {
            'ronda1': 55,
            'ronda2': 28,
            'ronda3': 16,
            'octavos': 8,
            'cuartos': 4,
            'semifinales': 4,
            'final': 1
        }.get(eliminatoria, 0)        
        # Obtener el número de partidos del formulario
        num_partidos_str = request.form.get('num_partidos', '0').strip()
        num_partidos = int(num_partidos_str) if num_partidos_str else 0        
        # Validar el número de partidos
        if num_partidos < 0 or num_partidos > max_partidos:
            return "Número de partidos no válido"                
        # Crear un cursor para ejecutar consultas SQL
        cur = mysql.connection.cursor()
        # Iterar sobre los datos del formulario para insertar los partidos
        for i in range(num_partidos):
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            local = request.form.get(f'local{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            visitante = request.form.get(f'visitante{i}')          
            # Verificar si algún campo es None y asignar valores por defecto
            if fecha is None:
                fecha = ''
            if hora is None:
                hora = ''
            if local is None:
                local = ''
            if resultadoA is None:
                resultadoA = ''
            if resultadoB is None:
                resultadoB = ''
            if visitante is None:
                visitante = ''           
            # Insertar el partido en la tabla copa_valladolid
            cur.execute("""
                INSERT INTO copa_valladolid (eliminatoria, fecha, hora, local, resultadoA, resultadoB, visitante)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (eliminatoria, fecha, hora, local, resultadoA, resultadoB, visitante))       
        # Confirmar los cambios en la base de datos
        mysql.connection.commit()        
        # Cerrar el cursor
        cur.close()        
        # Redireccionar a la vista de la copa_valladolid
        return redirect(url_for('ver_copa_valladolid'))
    # Renderizar el formulario para crear la copa_valladolid
    return render_template('admin/copa_valladolid.html')
# Ruta para ver las eliminatorias en el Admin
@app.route('/admin/copa_valladolid/')
def ver_copa_valladolid():
    cursor = mysql.connection.cursor()
    eliminatorias = ['ronda1', 'ronda2', 'ronda3', 'octavos', 'cuartos', 'semifinales', 'final']
    datos_eliminatorias = {}
    for eliminatoria in eliminatorias:
        cursor.execute("SELECT * FROM copa_valladolid WHERE eliminatoria = %s", [eliminatoria])
        partidos = cursor.fetchall()
        datos_eliminatorias[eliminatoria] = partidos
    cursor.close()
    return render_template('admin/copa_valladolid.html', datos_eliminatorias=datos_eliminatorias)
# Ruta para modificar las eliminatorias
@app.route('/modificar_copa_valladolid/<string:id>', methods=['POST'])
def modificar_copa_valladolid(id):
    eliminatoria = request.form['eliminatoria']
    num_partidos = int(request.form['num_partidos'])
    cur = mysql.connection.cursor()
    # Actualizar la jornada
    cur.execute('UPDATE copa_valladolid SET eliminatoria = %s WHERE id = %s', (eliminatoria, id))
    # Actualizar los partidos de la jornada
    for i in range(num_partidos):
        partido_id = request.form.get(f'partido_id{i}')
        fecha = request.form.get(f'fecha{i}')
        hora = request.form.get(f'hora{i}')
        local = request.form.get(f'local{i}')
        resultadoA = request.form.get(f'resultadoA{i}')
        resultadoB = request.form.get(f'resultadoB{i}')
        visitante = request.form.get(f'visitante{i}')
        # Verificar que los campos obligatorios tienen valores válidos
        if all([partido_id, local, visitante]):
        # Asignar valores predeterminados si los campos opcionales están vacíos
            if fecha is None:
                fecha = ''
            if hora is None:
                hora = ''
            if local is None:
                local = ''
            if resultadoA is None:
                resultadoA = ''
            if resultadoB is None:
                resultadoB = ''
            if visitante is None:
                visitante = ''
        # Verificar que todos los campos están presentes
        cur.execute('UPDATE copa_valladolid SET fecha = %s, hora = %s, local = %s, resultadoA = %s, resultadoB = %s, visitante = %s WHERE id = %s',
            (fecha, hora, local, resultadoA, resultadoB, visitante, partido_id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('ver_copa_valladolid')) 
# Ruta para eliminar las eliminatorias
@app.route('/eliminar_copa_valladolid/<string:eliminatoria>', methods=['POST'])
def eliminar_copa_valladolid(eliminatoria):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM copa_valladolid WHERE eliminatoria = %s', [eliminatoria])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('ver_copa_valladolid'))
# Ruta para ver las eliminatorias en Inicio
@app.route('/copa_valladolid/')
def copas_valladolid():
    # Obtener datos de las eliminatorias
    cursor = mysql.connection.cursor()
    eliminatorias = ['ronda1', 'ronda2', 'ronda3', 'octavos', 'cuartos', 'semifinales', 'final']
    datos_copa = {}
    for eliminatoria in eliminatorias:
        cursor.execute("SELECT * FROM copa_valladolid WHERE eliminatoria = %s", [eliminatoria])
        partidos = cursor.fetchall()
        datos_copa[eliminatoria] = partidos
    cursor.close()
    return render_template('copas/valladolid_copa.html', datos_copa=datos_copa)
# Fin copa Real Valladolid

# Copa Aula Valladolid
# Crear formulario para los playoff
@app.route('/admin/crear_copa_aula', methods=['GET', 'POST'])
def crear_copa_aula():
    if request.method == 'POST':
        eliminatoria = request.form.get('eliminatoria')       
        # Determinar el máximo de partidos permitidos para la eliminatoria
        max_partidos = {
            'fase1': 6,
            'fase2': 6,
            'cuartos': 4,
            'semifinales': 2,
            'final': 1
        }.get(eliminatoria, 0)        
        # Obtener el número de partidos del formulario
        num_partidos_str = request.form.get('num_partidos', '0').strip()
        num_partidos = int(num_partidos_str) if num_partidos_str else 0        
        # Validar el número de partidos
        if num_partidos < 0 or num_partidos > max_partidos:
            return "Número de partidos no válido"                
        # Crear un cursor para ejecutar consultas SQL
        cur = mysql.connection.cursor()
        # Iterar sobre los datos del formulario para insertar los partidos
        for i in range(num_partidos):
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            local = request.form.get(f'local{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            visitante = request.form.get(f'visitante{i}')          
            # Verificar si algún campo es None y asignar valores por defecto
            if fecha is None:
                fecha = ''
            if hora is None:
                hora = ''
            if local is None:
                local = ''
            if resultadoA is None:
                resultadoA = ''
            if resultadoB is None:
                resultadoB = ''
            if visitante is None:
                visitante = ''           
            # Insertar el partido en la tabla copa_valladolid
            cur.execute("""
                INSERT INTO copa_aula (eliminatoria, fecha, hora, local, resultadoA, resultadoB, visitante)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (eliminatoria, fecha, hora, local, resultadoA, resultadoB, visitante))       
        # Confirmar los cambios en la base de datos
        mysql.connection.commit()        
        # Cerrar el cursor
        cur.close()        
        # Redireccionar a la vista de la copa_valladolid
        return redirect(url_for('ver_copa_aula'))
    # Renderizar el formulario para crear la copa_valladolid
    return render_template('admin/copa_aula.html')
# Crear formulario para las eliminatorias
@app.route('/admin/copa_aula/')
def ver_copa_aula():
    cursor = mysql.connection.cursor()
    eliminatorias = ['fase1', 'fase2', 'cuartos', 'semifinales', 'final']
    datos_eliminatorias = {}
    for eliminatoria in eliminatorias:
        cursor.execute("SELECT * FROM copa_aula WHERE eliminatoria = %s", [eliminatoria])
        partidos = cursor.fetchall()
        datos_eliminatorias[eliminatoria] = partidos
    cursor.close()
    return render_template('admin/copa_aula.html', datos_eliminatorias=datos_eliminatorias)
# Modificar los partidos de los playoff
@app.route('/modificar_copa_aula/<string:id>', methods=['GET', 'POST'])
def modificar_copa_aula(id):
    eliminatoria = request.form['eliminatoria']
    num_partidos = int(request.form['num_partidos'])
    cur = mysql.connection.cursor()
    # Actualizar la jornada
    cur.execute('UPDATE copa_aula SET eliminatoria = %s WHERE id = %s', (eliminatoria, id))
    # Actualizar los partidos de la jornada
    for i in range(num_partidos):
        partido_id = request.form.get(f'partido_id{i}')
        fecha = request.form.get(f'fecha{i}')
        hora = request.form.get(f'hora{i}')
        local = request.form.get(f'local{i}')
        resultadoA = request.form.get(f'resultadoA{i}')
        resultadoB = request.form.get(f'resultadoB{i}')
        visitante = request.form.get(f'visitante{i}')
        # Verificar que los campos obligatorios tienen valores válidos
        if all([partido_id, local, visitante]):
        # Asignar valores predeterminados si los campos opcionales están vacíos
            if fecha is None:
                fecha = ''
            if hora is None:
                hora = ''
            if local is None:
                local = ''
            if resultadoA is None:
                resultadoA = ''
            if resultadoB is None:
                resultadoB = ''
            if visitante is None:
                visitante = ''
        # Verificar que todos los campos están presentes
        cur.execute('UPDATE copa_aula SET fecha = %s, hora = %s, local = %s, resultadoA = %s, resultadoB = %s, visitante = %s WHERE id = %s',
            (fecha, hora, local, resultadoA, resultadoB, visitante, partido_id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('ver_copa_aula'))
# Ruta para eliminar las eliminatorias
@app.route('/eliminar_copa_aula/<string:eliminatoria>', methods=['POST'])
def eliminar_copa_aula(eliminatoria):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM copa_aula WHERE eliminatoria = %s', [eliminatoria])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('ver_copa_aula'))
# Ruta para mostrar la copa Aula Valladolid
@app.route('/copa_aula/')
def copas_aula():
    # Obtener datos de las eliminatorias
    cursor = mysql.connection.cursor()
    eliminatorias = ['fase1', 'fase2', 'cuartos', 'semifinales', 'final']
    datos_copa = {}
    for eliminatoria in eliminatorias:
        cursor.execute("SELECT * FROM copa_aula WHERE eliminatoria = %s", [eliminatoria])
        partidos = cursor.fetchall()
        datos_copa[eliminatoria] = partidos
    cursor.close()
    return render_template('copas/aula_copa.html', datos_copa=datos_copa)
# Fin copa Aula Valladolid

# Copa Recoletas Atl. Valladolid
# Crear formulario para los playoff
@app.route('/admin/crear_copa_recoletas', methods=['GET', 'POST'])
def crear_copa_recoletas():
    if request.method == 'POST':
        eliminatoria = request.form.get('eliminatoria')       
        # Determinar el máximo de partidos permitidos para la eliminatoria
        max_partidos = {
            'ronda1': 12,
            'ronda2': 6,
            'octavos': 6,
            'cuartos': 4,
            'semifinales': 2,
            'final': 1
        }.get(eliminatoria, 0)        
        # Obtener el número de partidos del formulario
        num_partidos_str = request.form.get('num_partidos', '0').strip()
        num_partidos = int(num_partidos_str) if num_partidos_str else 0        
        # Validar el número de partidos
        if num_partidos < 0 or num_partidos > max_partidos:
            return "Número de partidos no válido"                
        # Crear un cursor para ejecutar consultas SQL
        cur = mysql.connection.cursor()
        # Iterar sobre los datos del formulario para insertar los partidos
        for i in range(num_partidos):
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            local = request.form.get(f'local{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            visitante = request.form.get(f'visitante{i}')          
            # Verificar si algún campo es None y asignar valores por defecto
            if fecha is None:
                fecha = ''
            if hora is None:
                hora = ''
            if local is None:
                local = ''
            if resultadoA is None:
                resultadoA = ''
            if resultadoB is None:
                resultadoB = ''
            if visitante is None:
                visitante = ''           
            # Insertar el partido en la tabla copa_recoletas
            cur.execute("""
                INSERT INTO copa_recoletas (eliminatoria, fecha, hora, local, resultadoA, resultadoB, visitante)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (eliminatoria, fecha, hora, local, resultadoA, resultadoB, visitante))       
        # Confirmar los cambios en la base de datos
        mysql.connection.commit()        
        # Cerrar el cursor
        cur.close()        
        # Redireccionar a la vista de la copa_recoletas
        return redirect(url_for('ver_copa_recoletas'))
    # Renderizar el formulario para crear la copa_recoletas
    return render_template('admin/copa_recoleas.html')
# Crear formulario para las eliminatorias
@app.route('/admin/copa_recoletas/')
def ver_copa_recoletas():
    cursor = mysql.connection.cursor()
    eliminatorias = ['ronda1', 'ronda2', 'octavos','cuartos', 'semifinales', 'final']
    datos_eliminatorias = {}
    for eliminatoria in eliminatorias:
        cursor.execute("SELECT * FROM copa_recoletas WHERE eliminatoria = %s", [eliminatoria])
        partidos = cursor.fetchall()
        datos_eliminatorias[eliminatoria] = partidos
    cursor.close()
    return render_template('admin/copa_recoletas.html', datos_eliminatorias=datos_eliminatorias)
# Modificar los partidos de los playoff
@app.route('/modificar_copa_recoletas/<string:id>', methods=['GET', 'POST'])
def modificar_copa_recoletas(id):
    eliminatoria = request.form['eliminatoria']
    num_partidos = int(request.form['num_partidos'])
    cur = mysql.connection.cursor()
    # Actualizar la jornada
    cur.execute('UPDATE copa_recoletas SET eliminatoria = %s WHERE id = %s', (eliminatoria, id))
    # Actualizar los partidos de la jornada
    for i in range(num_partidos):
        partido_id = request.form.get(f'partido_id{i}')
        fecha = request.form.get(f'fecha{i}')
        hora = request.form.get(f'hora{i}')
        local = request.form.get(f'local{i}')
        resultadoA = request.form.get(f'resultadoA{i}')
        resultadoB = request.form.get(f'resultadoB{i}')
        visitante = request.form.get(f'visitante{i}')
        # Verificar que los campos obligatorios tienen valores válidos
        if all([partido_id, local, visitante]):
        # Asignar valores predeterminados si los campos opcionales están vacíos
            if fecha is None:
                fecha = ''
            if hora is None:
                hora = ''
            if local is None:
                local = ''
            if resultadoA is None:
                resultadoA = ''
            if resultadoB is None:
                resultadoB = ''
            if visitante is None:
                visitante = ''
        # Verificar que todos los campos están presentes
        cur.execute('UPDATE copa_recoletas SET fecha = %s, hora = %s, local = %s, resultadoA = %s, resultadoB = %s, visitante = %s WHERE id = %s',
            (fecha, hora, local, resultadoA, resultadoB, visitante, partido_id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('ver_copa_recoletas'))
# Ruta para eliminar las eliminatorias
@app.route('/eliminar_copa_recoletas/<string:eliminatoria>', methods=['POST'])
def eliminar_copa_recoletas(eliminatoria):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM copa_recoletas WHERE eliminatoria = %s', [eliminatoria])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('ver_copa_recoletas'))
# Ruta para mostrar la copa Recoletas Atl. Valladolid
@app.route('/copa_recoletas/')
def copas_recoletas():
    # Obtener datos de las eliminatorias
    cursor = mysql.connection.cursor()
    eliminatorias = ['ronda1', 'ronda2', 'octavos','cuartos', 'semifinales', 'final']
    datos_copa = {}
    for eliminatoria in eliminatorias:
        cursor.execute("SELECT * FROM copa_recoletas WHERE eliminatoria = %s", [eliminatoria])
        partidos = cursor.fetchall()
        datos_copa[eliminatoria] = partidos
    cursor.close()
    return render_template('copas/recoletas_copa.html', datos_copa=datos_copa)
# Fin copa Recoletas Atl. Valladolid

# Copa Fundación Aliados
# Crear formulario para los playoff
@app.route('/admin/crear_copa_aliados', methods=['GET', 'POST'])
def crear_copa_aliados():
    if request.method == 'POST':
        eliminatoria = request.form.get('eliminatoria')       
        # Determinar el máximo de partidos permitidos para la eliminatoria
        max_partidos = {
            'cuartos': 4,
            'semifinales': 2,
            'eliminados': 2,
            'final': 1
        }.get(eliminatoria, 0)        
        # Obtener el número de partidos del formulario
        num_partidos_str = request.form.get('num_partidos', '0').strip()
        num_partidos = int(num_partidos_str) if num_partidos_str else 0        
        # Validar el número de partidos
        if num_partidos < 0 or num_partidos > max_partidos:
            return "Número de partidos no válido"                
        # Crear un cursor para ejecutar consultas SQL
        cur = mysql.connection.cursor()
        # Iterar sobre los datos del formulario para insertar los partidos
        for i in range(num_partidos):
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            local = request.form.get(f'local{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            visitante = request.form.get(f'visitante{i}')          
            # Verificar si algún campo es None y asignar valores por defecto
            if fecha is None:
                fecha = ''
            if hora is None:
                hora = ''
            if local is None:
                local = ''
            if resultadoA is None:
                resultadoA = ''
            if resultadoB is None:
                resultadoB = ''
            if visitante is None:
                visitante = ''           
            # Insertar el partido en la tabla copa_recoletas
            cur.execute("""
                INSERT INTO copa_aliados (eliminatoria, fecha, hora, local, resultadoA, resultadoB, visitante)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (eliminatoria, fecha, hora, local, resultadoA, resultadoB, visitante))       
        # Confirmar los cambios en la base de datos
        mysql.connection.commit()        
        # Cerrar el cursor
        cur.close()        
        # Redireccionar a la vista de la copa_recoletas
        return redirect(url_for('ver_copa_aliados'))
    # Renderizar el formulario para crear la copa_recoletas
    return render_template('admin/copa_aliados.html')
# Crear formulario para los playoff
@app.route('/admin/copa_aliados/')
def ver_copa_aliados():
    cursor = mysql.connection.cursor()
    eliminatorias = ['cuartos', 'semifinales', 'eliminados','final']
    datos_eliminatorias = {}
    for eliminatoria in eliminatorias:
        cursor.execute("SELECT * FROM copa_aliados WHERE eliminatoria = %s", [eliminatoria])
        partidos = cursor.fetchall()
        datos_eliminatorias[eliminatoria] = partidos
    cursor.close()
    return render_template('admin/copa_aliados.html', datos_eliminatorias=datos_eliminatorias)
# Modificar los partidos de los playoff
@app.route('/modificar_copa_aliados/<string:id>', methods=['GET', 'POST'])
def modificar_copa_aliados(id):
    eliminatoria = request.form['eliminatoria']
    num_partidos = int(request.form['num_partidos'])
    cur = mysql.connection.cursor()
    # Actualizar la jornada
    cur.execute('UPDATE copa_aliados SET eliminatoria = %s WHERE id = %s', (eliminatoria, id))
    # Actualizar los partidos de la jornada
    for i in range(num_partidos):
        partido_id = request.form.get(f'partido_id{i}')
        fecha = request.form.get(f'fecha{i}')
        hora = request.form.get(f'hora{i}')
        local = request.form.get(f'local{i}')
        resultadoA = request.form.get(f'resultadoA{i}')
        resultadoB = request.form.get(f'resultadoB{i}')
        visitante = request.form.get(f'visitante{i}')
        # Verificar que los campos obligatorios tienen valores válidos
        if all([partido_id, local, visitante]):
        # Asignar valores predeterminados si los campos opcionales están vacíos
            if fecha is None:
                fecha = ''
            if hora is None:
                hora = ''
            if local is None:
                local = ''
            if resultadoA is None:
                resultadoA = ''
            if resultadoB is None:
                resultadoB = ''
            if visitante is None:
                visitante = ''
        # Verificar que todos los campos están presentes
        cur.execute('UPDATE copa_aliados SET fecha = %s, hora = %s, local = %s, resultadoA = %s, resultadoB = %s, visitante = %s WHERE id = %s',
            (fecha, hora, local, resultadoA, resultadoB, visitante, partido_id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('ver_copa_aliados')) 
# Ruta para eliminar las eliminatorias
@app.route('/eliminar_copa_aliados/<string:eliminatoria>', methods=['POST'])
def eliminar_copa_aliados(eliminatoria):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM copa_aliados WHERE eliminatoria = %s', [eliminatoria])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('ver_copa_aliados'))
# Ruta para mostrar la copa Fundación Aliados
@app.route('/copa_aliados/')
def copas_aliados():
    # Obtener datos de las eliminatorias
    cursor = mysql.connection.cursor()
    eliminatorias = ['cuartos', 'semifinales', 'eliminados', 'final']
    datos_copa = {}
    for eliminatoria in eliminatorias:
        cursor.execute("SELECT * FROM copa_aliados WHERE eliminatoria = %s", [eliminatoria])
        partidos = cursor.fetchall()
        datos_copa[eliminatoria] = partidos
    cursor.close()
    return render_template('copas/aliados_copa.html', datos_copa=datos_copa)
# Fin copa Fundación Aliados

# Copa CD Parquesol
# Crear formulario para la copa
@app.route('/admin/crear_copa_parquesol', methods=['GET', 'POST'])
def crear_copa_parquesol():
    if request.method == 'POST':
        eliminatoria = request.form.get('eliminatoria')       
        # Determinar el máximo de partidos permitidos para la eliminatoria
        max_partidos = {
            'primera': 16,
            'segunda': 8,
            'tercera': 8,
            'octavos': 8,
            'cuartos': 4,
            'semifinales': 4,
            'final': 1
        }.get(eliminatoria, 0)        
        # Obtener el número de partidos del formulario
        num_partidos_str = request.form.get('num_partidos', '0').strip()
        num_partidos = int(num_partidos_str) if num_partidos_str else 0        
        # Validar el número de partidos
        if num_partidos < 0 or num_partidos > max_partidos:
            return "Número de partidos no válido"                
        # Crear un cursor para ejecutar consultas SQL
        cur = mysql.connection.cursor()
        # Iterar sobre los datos del formulario para insertar los partidos
        for i in range(num_partidos):
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            local = request.form.get(f'local{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            visitante = request.form.get(f'visitante{i}')          
            # Verificar si algún campo es None y asignar valores por defecto
            if fecha is None:
                fecha = ''
            if hora is None:
                hora = ''
            if local is None:
                local = ''
            if resultadoA is None:
                resultadoA = ''
            if resultadoB is None:
                resultadoB = ''
            if visitante is None:
                visitante = ''           
            # Insertar el partido en la tabla copa_recoletas
            cur.execute("""
                INSERT INTO copa_parquesol (eliminatoria, fecha, hora, local, resultadoA, resultadoB, visitante)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (eliminatoria, fecha, hora, local, resultadoA, resultadoB, visitante))       
        # Confirmar los cambios en la base de datos
        mysql.connection.commit()        
        # Cerrar el cursor
        cur.close()        
        # Redireccionar a la vista de la copa_recoletas
        return redirect(url_for('ver_copa_parquesol'))
    # Renderizar el formulario para crear la copa_recoletas
    return render_template('admin/copa_parquesol.html')
# Crear formulario para la copa
@app.route('/admin/copa_parquesol/')
def ver_copa_parquesol():
    cursor = mysql.connection.cursor()
    eliminatorias = ['primera', 'segunda', 'tercera','octavos','cuartos', 'semifinales', 'eliminados','final']
    datos_eliminatorias = {}
    for eliminatoria in eliminatorias:
        cursor.execute("SELECT * FROM copa_parquesol WHERE eliminatoria = %s", [eliminatoria])
        partidos = cursor.fetchall()
        datos_eliminatorias[eliminatoria] = partidos
    cursor.close()
    return render_template('admin/copa_parquesol.html', datos_eliminatorias=datos_eliminatorias)
# Modificar los partidos de los playoff
@app.route('/modificar_copa_parquesol/<string:id>', methods=['POST'])
def modificar_copa_parquesol(id):
    eliminatoria = request.form['eliminatoria']
    num_partidos = int(request.form['num_partidos'])
    cur = mysql.connection.cursor()
    # Actualizar la jornada
    cur.execute('UPDATE copa_parquesol SET eliminatoria = %s WHERE id = %s', (eliminatoria, id))
    # Actualizar los partidos de la jornada
    for i in range(num_partidos):
        partido_id = request.form.get(f'partido_id{i}')
        fecha = request.form.get(f'fecha{i}')
        hora = request.form.get(f'hora{i}')
        local = request.form.get(f'local{i}')
        resultadoA = request.form.get(f'resultadoA{i}')
        resultadoB = request.form.get(f'resultadoB{i}')
        visitante = request.form.get(f'visitante{i}')
        # Verificar que los campos obligatorios tienen valores válidos
        if all([partido_id, local, visitante]):
        # Asignar valores predeterminados si los campos opcionales están vacíos
            if fecha is None:
                fecha = ''
            if hora is None:
                hora = ''
            if local is None:
                local = ''
            if resultadoA is None:
                resultadoA = ''
            if resultadoB is None:
                resultadoB = ''
            if visitante is None:
                visitante = ''
        # Verificar que todos los campos están presentes
        cur.execute('UPDATE copa_parquesol SET fecha = %s, hora = %s, local = %s, resultadoA = %s, resultadoB = %s, visitante = %s WHERE id = %s',
            (fecha, hora, local, resultadoA, resultadoB, visitante, partido_id))
    mysql.connection.commit()
    cur.close()       
    # Redireccionar a la página de visualización de copa
    return redirect(url_for('ver_copa_parquesol')) 
# Ruta para eliminar las eliminatorias
@app.route('/eliminar_copa_parquesol/<string:eliminatoria>', methods=['POST'])
def eliminar_copa_parquesol(eliminatoria):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM copa_parquesol WHERE eliminatoria = %s', [eliminatoria])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('ver_copa_parquesol'))
# Ruta para mostrar la copa CD Parquesol
@app.route('/copa_parquesol/')
def copas_parquesol():
    # Obtener datos de las eliminatorias
    cursor = mysql.connection.cursor()
    eliminatorias = ['primera', 'segunda', 'tercera', 'octavos','cuartos', 'semifinales', 'eliminados', 'final']
    datos_copa = {}
    for eliminatoria in eliminatorias:
        cursor.execute("SELECT * FROM copa_parquesol WHERE eliminatoria = %s", [eliminatoria])
        partidos = cursor.fetchall()
        datos_copa[eliminatoria] = partidos
    cursor.close()
    return render_template('copas/parquesol_copa.html', datos_copa=datos_copa)
# Fin copa CD Parquesol

# Copa CPLV Munia Panteras
# Crear formulario para los playoff
@app.route('/admin/crear_copa_panteras', methods=['GET', 'POST'])
def crear_copa_panteras():
    if request.method == 'POST':
        eliminatoria = request.form.get('eliminatoria')       
        # Determinar el máximo de partidos permitidos para la eliminatoria
        max_partidos = {
            'cuartos': 3,
            'semifinales': 2,
            'final': 1
        }.get(eliminatoria, 0)        
        # Obtener el número de partidos del formulario
        num_partidos_str = request.form.get('num_partidos', '0').strip()
        num_partidos = int(num_partidos_str) if num_partidos_str else 0        
        # Validar el número de partidos
        if num_partidos < 0 or num_partidos > max_partidos:
            return "Número de partidos no válido"                
        # Crear un cursor para ejecutar consultas SQL
        cur = mysql.connection.cursor()
        # Iterar sobre los datos del formulario para insertar los partidos
        for i in range(num_partidos):
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            local = request.form.get(f'local{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            visitante = request.form.get(f'visitante{i}')          
            # Verificar si algún campo es None y asignar valores por defecto
            if fecha is None:
                fecha = ''
            if hora is None:
                hora = ''
            if local is None:
                local = ''
            if resultadoA is None:
                resultadoA = ''
            if resultadoB is None:
                resultadoB = ''
            if visitante is None:
                visitante = ''           
            # Insertar el partido en la tabla copa_recoletas
            cur.execute("""
                INSERT INTO copa_panteras (eliminatoria, fecha, hora, local, resultadoA, resultadoB, visitante)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (eliminatoria, fecha, hora, local, resultadoA, resultadoB, visitante))       
        # Confirmar los cambios en la base de datos
        mysql.connection.commit()        
        # Cerrar el cursor
        cur.close()        
        # Redireccionar a la vista de la copa_recoletas
        return redirect(url_for('ver_copa_panteras'))
    # Si no es una solicitud POST, renderizar el formulario
    return render_template('admin/copa_panteras.html')
# Crear formulario para los playoff
@app.route('/admin/copa_panteras/')
def ver_copa_panteras():
    cursor = mysql.connection.cursor()
    eliminatorias = ['cuartos', 'semifinales', 'final']
    datos_eliminatorias = {}
    for eliminatoria in eliminatorias:
        cursor.execute("SELECT * FROM copa_panteras WHERE eliminatoria = %s", [eliminatoria])
        partidos = cursor.fetchall()
        datos_eliminatorias[eliminatoria] = partidos
    cursor.close()
    return render_template('admin/copa_panteras.html', datos_eliminatorias=datos_eliminatorias)
# Modificar los partidos de los playoff
@app.route('/modificar_copa_panteras/<string:id>', methods=['POST'])
def modificar_copa_panteras(id):
    eliminatoria = request.form['eliminatoria']
    num_partidos = int(request.form['num_partidos'])
    cur = mysql.connection.cursor()
    # Actualizar la jornada
    cur.execute('UPDATE copa_panteras SET eliminatoria = %s WHERE id = %s', (eliminatoria, id))
    # Actualizar los partidos de la jornada
    for i in range(num_partidos):
        partido_id = request.form.get(f'partido_id{i}')
        fecha = request.form.get(f'fecha{i}')
        hora = request.form.get(f'hora{i}')
        local = request.form.get(f'local{i}')
        resultadoA = request.form.get(f'resultadoA{i}')
        resultadoB = request.form.get(f'resultadoB{i}')
        visitante = request.form.get(f'visitante{i}')
        # Verificar que los campos obligatorios tienen valores válidos
        if all([partido_id, local, visitante]):
        # Asignar valores predeterminados si los campos opcionales están vacíos
            if fecha is None:
                fecha = ''
            if hora is None:
                hora = ''
            if local is None:
                local = ''
            if resultadoA is None:
                resultadoA = ''
            if resultadoB is None:
                resultadoB = ''
            if visitante is None:
                visitante = ''
        # Verificar que todos los campos están presentes
        cur.execute('UPDATE copa_panteras SET fecha = %s, hora = %s, local = %s, resultadoA = %s, resultadoB = %s, visitante = %s WHERE id = %s',
            (fecha, hora, local, resultadoA, resultadoB, visitante, partido_id))
    mysql.connection.commit()
    cur.close()       
    # Redireccionar a la página de visualización de copa
    return redirect(url_for('ver_copa_panteras')) 
# Ruta para eliminar las eliminatorias
@app.route('/eliminar_copa_panteras/<string:eliminatoria>', methods=['POST'])
def eliminar_copa_panteras(eliminatoria):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM copa_panteras WHERE eliminatoria = %s', [eliminatoria])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('ver_copa_panteras'))
# Ruta para mostrar la copa CPLV Munia Panteras
@app.route('/copa_panteras/')
def copas_panteras():
    # Obtener datos de las eliminatorias
    cursor = mysql.connection.cursor()
    eliminatorias = ['cuartos', 'semifinales', 'final']
    datos_copa = {}
    for eliminatoria in eliminatorias:
        cursor.execute("SELECT * FROM copa_panteras WHERE eliminatoria = %s", [eliminatoria])
        partidos = cursor.fetchall()
        datos_copa[eliminatoria] = partidos
    cursor.close()
    return render_template('copas/panteras_copa.html', datos_copa=datos_copa)
# Fin copa CPLV Munia Panteras

# Copa CPLV Caja Rural
# Crear formulario para los playoff
@app.route('/admin/crear_copa_caja', methods=['GET', 'POST'])
def crear_copa_caja():
    if request.method == 'POST':
        eliminatoria = request.form.get('eliminatoria')       
        # Determinar el máximo de partidos permitidos para la eliminatoria
        max_partidos = {
            'cuartos': 3,
            'semifinales': 2,
            'final': 1
        }.get(eliminatoria, 0)        
        # Obtener el número de partidos del formulario
        num_partidos_str = request.form.get('num_partidos', '0').strip()
        num_partidos = int(num_partidos_str) if num_partidos_str else 0        
        # Validar el número de partidos
        if num_partidos < 0 or num_partidos > max_partidos:
            return "Número de partidos no válido"                
        # Crear un cursor para ejecutar consultas SQL
        cur = mysql.connection.cursor()
        # Iterar sobre los datos del formulario para insertar los partidos
        for i in range(num_partidos):
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            local = request.form.get(f'local{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            visitante = request.form.get(f'visitante{i}')          
            # Verificar si algún campo es None y asignar valores por defecto
            if fecha is None:
                fecha = ''
            if hora is None:
                hora = ''
            if local is None:
                local = ''
            if resultadoA is None:
                resultadoA = ''
            if resultadoB is None:
                resultadoB = ''
            if visitante is None:
                visitante = ''           
            # Insertar el partido en la tabla copa_recoletas
            cur.execute("""
                INSERT INTO copa_caja (eliminatoria, fecha, hora, local, resultadoA, resultadoB, visitante)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (eliminatoria, fecha, hora, local, resultadoA, resultadoB, visitante))       
        # Confirmar los cambios en la base de datos
        mysql.connection.commit()        
        # Cerrar el cursor
        cur.close()        
        # Redireccionar a la vista de la copa_recoletas
        return redirect(url_for('ver_copa_caja'))
    # Si no es una solicitud POST, renderizar el formulario
    return render_template('admin/copa_caja.html')
# Crear formulario para los playoff
@app.route('/admin/copa_caja/')
def ver_copa_caja():
    cursor = mysql.connection.cursor()
    eliminatorias = ['cuartos', 'semifinales', 'final']
    datos_eliminatorias = {}
    for eliminatoria in eliminatorias:
        cursor.execute("SELECT * FROM copa_caja WHERE eliminatoria = %s", [eliminatoria])
        partidos = cursor.fetchall()
        datos_eliminatorias[eliminatoria] = partidos
    cursor.close()
    return render_template('admin/copa_caja.html', datos_eliminatorias=datos_eliminatorias)
# Modificar los partidos de los playoff
@app.route('/modificar_copa_caja/<string:id>', methods=['GET', 'POST'])
def modificar_copa_caja(id):
    eliminatoria = request.form['eliminatoria']
    num_partidos = int(request.form['num_partidos'])
    cur = mysql.connection.cursor()
    # Actualizar la jornada
    cur.execute('UPDATE copa_caja SET eliminatoria = %s WHERE id = %s', (eliminatoria, id))
    # Actualizar los partidos de la jornada
    for i in range(num_partidos):
        partido_id = request.form.get(f'partido_id{i}')
        fecha = request.form.get(f'fecha{i}')
        hora = request.form.get(f'hora{i}')
        local = request.form.get(f'local{i}')
        resultadoA = request.form.get(f'resultadoA{i}')
        resultadoB = request.form.get(f'resultadoB{i}')
        visitante = request.form.get(f'visitante{i}')
        # Verificar que los campos obligatorios tienen valores válidos
        if all([partido_id, local, visitante]):
        # Asignar valores predeterminados si los campos opcionales están vacíos
            if fecha is None:
                fecha = ''
            if hora is None:
                hora = ''
            if local is None:
                local = ''
            if resultadoA is None:
                resultadoA = ''
            if resultadoB is None:
                resultadoB = ''
            if visitante is None:
                visitante = ''
        # Verificar que todos los campos están presentes
        cur.execute('UPDATE copa_caja SET fecha = %s, hora = %s, local = %s, resultadoA = %s, resultadoB = %s, visitante = %s WHERE id = %s',
            (fecha, hora, local, resultadoA, resultadoB, visitante, partido_id))
    mysql.connection.commit()
    cur.close()       
    # Redireccionar a la página de visualización de copa
    return redirect(url_for('ver_copa_caja'))
# Ruta para eliminar las eliminatorias
@app.route('/eliminar_copa_caja/<string:eliminatoria>', methods=['POST'])
def eliminar_copa_caja(eliminatoria):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM copa_caja WHERE eliminatoria = %s', [eliminatoria])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('ver_copa_caja'))
# Ruta para mostrar la copa CPLV Caja Rural
@app.route('/copa_caja/')
def copas_caja():
    # Obtener datos de las eliminatorias
    cursor = mysql.connection.cursor()
    eliminatorias = ['cuartos', 'semifinales', 'final']
    datos_copa = {}
    for eliminatoria in eliminatorias:
        cursor.execute("SELECT * FROM copa_caja WHERE eliminatoria = %s", [eliminatoria])
        partidos = cursor.fetchall()
        datos_copa[eliminatoria] = partidos
    cursor.close()
    return render_template('copas/caja_copa.html', datos_copa=datos_copa)
# Fin copa CPLV Caja Rural

# Copa CR El Salvador Fem
# Crear formulario para los playoff
@app.route('/admin/crear_copa_salvador_fem', methods=['GET', 'POST'])
def crear_copa_salvador_fem():
    if request.method == 'POST':
        encuentros = request.form.get('encuentros')
        print(f"Encuentros: {encuentros}")
        num_partidos = int(request.form.get('num_partidos', 0))
        cur = mysql.connection.cursor()
        for i in range(num_partidos):
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            local = request.form.get(f'local{i}')
            bonus_local = request.form.get(f'bonusA{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            bonus_visitante = request.form.get(f'bonusB{i}')
            visitante = request.form.get(f'visitante{i}')
            # Verificar si algún campo es None y asignar valores por defecto
            if fecha is None:
                fecha = ''
            if hora is None:
                hora = ''
            if local is None:
                local = ''
            if bonus_local is None:
                bonus_local = ''    
            if resultadoA is None:
                resultadoA = ''
            if resultadoB is None:
                resultadoB = ''
            if bonus_visitante is None:
                bonus_visitante = ''    
            if visitante is None:
                visitante = ''
            if encuentros is None:
                encuentros = '' 
            cur.execute("""
                INSERT INTO copa_salvador_fem (encuentros, fecha, hora, local, bonusA, resultadoA, resultadoB, bonusB, visitante)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (encuentros, fecha, hora, local, bonus_local, resultadoA, resultadoB, bonus_visitante, visitante))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('ver_copa_salvador_fem'))
    # Renderizar el formulario para crear la Cops Europa Caja
    return render_template('admin/crear_copa_salvador_fem.html')
    # Renderizar el formulario para crear la copa UEMC
    return render_template('admin/crear_copa_salvador_fem.html')
# Actualizar clasificación de los grupos
def actualizar_clasificacion_salvador_fem(clasificacion_por_grupo_salvador_fem, local, bonus_local ,resultado_local, resultado_visitante, bonus_visitante, visitante):
    resultado_local = int(resultado_local) if resultado_local.isdigit() else None
    resultado_visitante = int(resultado_visitante) if resultado_visitante.isdigit() else None
    # Asegurarse de que cada grupo tenga una entrada en la clasificación
    if grupo not in clasificacion_por_grupo_salvador_fem:
        clasificacion_por_grupo_salvador_fem[grupo] = {}
    if local not in clasificacion_por_grupo_salvador_fem[grupo]:
        clasificacion_por_grupo_salvador_fem[grupo][local] = {'nombre': local, 'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0,'puntos': 0, 'bonus': 0}
    if visitante not in clasificacion_por_grupo_salvador_fem[grupo]:
        clasificacion_por_grupo_salvador_fem[grupo][visitante] = {'nombre': visitante, 'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'puntos': 0, 'bonus': 0}
    # Actualizar los partidos jugados
    if resultado_local is not None and resultado_visitante is not None:
        clasificacion_por_grupo_salvador_fem[grupo][local]['jugados'] += 1
        clasificacion_por_grupo_salvador_fem[grupo][visitante]['jugados'] += 1
        # Determinar el resultado del partido
        if resultado_local > resultado_visitante:
            clasificacion_por_grupo_salvador_fem[grupo][local]['ganados'] += 1
            clasificacion_por_grupo_salvador_fem[grupo][local]['puntos'] += 4 + bonus_local
            clasificacion_por_grupo_salvador_fem[grupo][visitante]['perdidos'] += 1
            clasificacion_por_grupo_salvador_fem[grupo][visitante]['puntos'] += 0 + bonus_visitante
        elif resultado_local < resultado_visitante:
            clasificacion_por_grupo_salvador_fem[grupo][visitante]['ganados'] += 1
            clasificacion_por_grupo_salvador_fem[grupo][visitante]['puntos'] += 4 + bonus_visitante
            clasificacion_por_grupo_salvador_fem[grupo][local]['perdidos'] += 1
            clasificacion_por_grupo_salvador_fem[grupo][local]['puntos'] += 0 + bonus_local
        elif resultado_local == resultado_visitante:
            clasificacion_por_grupo_salvador_fem[grupo][visitante]['empatados'] += 1
            clasificacion_por_grupo_salvador_fem[grupo][visitante]['puntos'] += 2 + bonus_visitante
            clasificacion_por_grupo_salvador_fem[grupo][local]['empatados'] += 1
            clasificacion_por_grupo_salvador_fem[grupo][local]['puntos'] += 2 + bonus_local   
        clasificaciones_salvador_fem[grupo][local]['bonus'] += bonus_local
        clasificaciones_salvador_fem[grupo][visitante]['bonus'] += bonus_visitante 
    return clasificacion_por_grupo_salvador_fem
# Recalcular clasificación
def recalcular_clasificaciones_salvador_fem(partidos):
    clasificaciones_salvador_fem = {}
    enfrentamientos_directos_salvador_fem = {}
    for partido in partidos:
        grupo = partido.get('encuentros')
        local = partido['local']
        visitante = partido['visitante']
        resultado_local = int(partido['resultadoA']) if partido['resultadoA'].isdigit() else None
        resultado_visitante = int(partido['resultadoB']) if partido['resultadoB'].isdigit() else None
        bonus_local = int(partido['bonusA']) if partido['bonusA'].isdigit() else None
        bonus_visitante = int(partido['bonusB']) if partido['bonusB'].isdigit() else None
        if grupo not in clasificaciones_salvador_fem:
            clasificaciones_salvador_fem[grupo] = {}
        # Inicializar equipos si no existen
        if local not in clasificaciones_salvador_fem[grupo]:
            clasificaciones_salvador_fem[grupo][local] = {'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'puntos': 0, 'bonus': 0}
        if visitante not in clasificaciones_salvador_fem[grupo]:
            clasificaciones_salvador_fem[grupo][visitante] = {'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'puntos': 0, 'bonus': 0}
        # Actualizar estadísticas de partidos
        if resultado_local is not None and resultado_visitante is not None:
            clasificaciones_salvador_fem[grupo][local]['jugados'] += 1
            clasificaciones_salvador_fem[grupo][visitante]['jugados'] += 1
            if resultado_local > resultado_visitante:
                clasificaciones_salvador_fem[grupo][local]['ganados'] += 1
                clasificaciones_salvador_fem[grupo][local]['puntos'] += 4 + bonus_local
                clasificaciones_salvador_fem[grupo][visitante]['perdidos'] += 1
                clasificaciones_salvador_fem[grupo][visitante]['puntos'] += 0 + bonus_visitante
            elif resultado_local < resultado_visitante:
                clasificaciones_salvador_fem[grupo][visitante]['ganados'] += 1
                clasificaciones_salvador_fem[grupo][visitante]['puntos'] += 4 + bonus_visitante
                clasificaciones_salvador_fem[grupo][local]['perdidos'] += 1
                clasificaciones_salvador_fem[grupo][local]['puntos'] += 0 + bonus_local
            elif resultado_local == resultado_visitante:
                clasificaciones_salvador_fem[grupo][visitante]['empatados'] += 1
                clasificaciones_salvador_fem[grupo][visitante]['puntos'] += 2 + bonus_visitante
                clasificaciones_salvador_fem[grupo][local]['empatados'] += 1 
                clasificaciones_salvador_fem[grupo][local]['puntos'] += 2 + bonus_local  
            
            clasificaciones_salvador_fem[grupo][local]['bonus'] += bonus_local
            clasificaciones_salvador_fem[grupo][visitante]['bonus'] += bonus_visitante 

        # Almacenar el resultado del enfrentamiento directo
        if local not in enfrentamientos_directos_salvador_fem:
            enfrentamientos_directos_salvador_fem[local] = {}
        if visitante not in enfrentamientos_directos_salvador_fem:
            enfrentamientos_directos_salvador_fem[visitante] = {}
        if resultado_local is not None and resultado_visitante is not None:
            enfrentamientos_directos_salvador_fem[local][visitante] = resultado_local - resultado_visitante
            enfrentamientos_directos_salvador_fem[visitante][local] = resultado_visitante - resultado_local        
    return clasificaciones_salvador_fem, enfrentamientos_directos_salvador_fem
# Función para obtener equipos desde la base de datos
def obtener_equipos_desde_bd_salvador_fem():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, encuentros, fecha, hora, local, bonusA, resultadoA, resultadoB, bonusB, visitante FROM copa_salvador_fem")
    partidos = cur.fetchall()
    cur.close()
    # Definir los grupos y fases de eliminatorias
    grupos_salvador_fem = {'grupoA', 'grupoB', 'grupoC', 'grupoD'}
    fases_eliminatorias_salvador_fem = {'semifinales', 'final'}
    equipos_por_encuentros_salvador_fem = {}
    eliminatorias_salvador_fem = {'semifinales': {'partidos': []}, 'final': {'partidos': []}}
    for partido in partidos:
        grupo_o_fase = partido.get('encuentros')
        if grupo_o_fase in fases_eliminatorias_salvador_fem:
            # Añadir partidos a la fase de eliminación correspondiente
            eliminatorias_salvador_fem[grupo_o_fase]['partidos'].append(partido)
        elif grupo_o_fase in grupos_salvador_fem:
            # Añadir equipos y partidos a los grupos
            if grupo_o_fase not in equipos_por_encuentros_salvador_fem:
                equipos_por_encuentros_salvador_fem[grupo_o_fase] = {'equipos': [], 'partidos': []}
            local = {'nombre': partido['local'], 'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'puntos': 0, 'bonus': 0}
            visitante = {'nombre': partido['visitante'], 'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'puntos': 0, 'bonus': 0}
            # Añadir equipos si no existen en la lista de equipos del grupo
            if not any(e['nombre'] == local['nombre'] for e in equipos_por_encuentros_salvador_fem[grupo_o_fase]['equipos']):
                equipos_por_encuentros_salvador_fem[grupo_o_fase]['equipos'].append(local)
            if not any(e['nombre'] == visitante['nombre'] for e in equipos_por_encuentros_salvador_fem[grupo_o_fase]['equipos']):
                equipos_por_encuentros_salvador_fem[grupo_o_fase]['equipos'].append(visitante)
            equipos_por_encuentros_salvador_fem[grupo_o_fase]['partidos'].append(partido)
        else:
            print(f"Grupo o fase no reconocido: {grupo_o_fase}")
    return equipos_por_encuentros_salvador_fem, eliminatorias_salvador_fem
#Obtener equipos Copa copa CPLV salvador_fem Rural
def obtener_equipos_por_encuentros_salvador_fem(partidos):
    equipos_por_encuentros_salvador_fem = {}
    eliminatorias_salvador_fem = {'semifinales': {'partidos': []}, 'final': {'partidos': []}}
    # Clasificar partidos en grupos o eliminatorias
    for partido in partidos:
        grupo_o_fase = partido.get('encuentros')
        if grupo_o_fase in eliminatorias_salvador_fem:
            eliminatorias_salvador_fem[grupo_o_fase]['partidos'].append(partido)
        else:
            if grupo_o_fase not in equipos_por_encuentros_salvador_fem:
                equipos_por_encuentros_salvador_fem[grupo_o_fase] = {'equipos': [], 'partidos': []}
            # Añadir equipos si no existen en la lista de equipos del grupo
            local = {'nombre': partido['local'], 'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'puntos': 0, 'bonus': 0}
            visitante = {'nombre': partido['visitante'], 'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'puntos': 0, 'bonus':0}
            if not any(e['nombre'] == local['nombre'] for e in equipos_por_encuentros_salvador_fem[grupo_o_fase]['equipos']):
                equipos_por_encuentros_salvador_fem[grupo_o_fase]['equipos'].append(local)
            if not any(e['nombre'] == visitante['nombre'] for e in equipos_por_encuentros_salvador_fem[grupo_o_fase]['equipos']):
                equipos_por_encuentros_salvador_fem[grupo_o_fase]['equipos'].append(visitante)
            equipos_por_encuentros_salvador_fem[grupo_o_fase]['partidos'].append(partido)
    return equipos_por_encuentros_salvador_fem, eliminatorias_salvador_fem
# Obtener la información de la tabla copa_salvador_fem
def obtener_copa_salvador_fem():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, encuentros, fecha, hora, local, bonusA, resultadoA, resultadoB, bonusB, visitante FROM copa_salvador_fem")
    partidos = cur.fetchall()
    cur.close()
    print("Partidos desde la BD:", partidos)  # Añadir esta línea para depuración
    return partidos
# Formatear partidos por grupo
def formatear_partidos_por_encuentros_salvador_fem(partidos):
    encuentros_salvador_fem = {
        'grupoA': {'id': 1, 'encuentros': 'grupoA', 'partidos': []},
        'grupoB': {'id': 2, 'encuentros': 'grupoB', 'partidos': []},
        'grupoC': {'id': 3, 'encuentros': 'grupoC', 'partidos': []},
        'grupoD': {'id': 4, 'encuentros': 'grupoD', 'partidos': []},
        'semifinales': {'id': 5, 'encuentros': 'semifinales', 'partidos': []},
        'final': {'id': 6, 'encuentros': 'final', 'partidos': []}
    }
    for partido in partidos:
        grupo = partido.get('encuentros', '')
        if grupo in encuentros_salvador_fem:
            encuentros_salvador_fem[grupo]['partidos'].append(partido)
        else:
            print(f"Grupo no encontrado: {grupo}")            
    return encuentros_salvador_fem
# Crear formulario para los grupos y eliminatorias salvador_fem
@app.route('/admin/copa_salvador_fem/')
def ver_copa_salvador_fem():
    try:
        # Obtener todos los partidos de los Playoff salvador_fem
        partidos = obtener_copa_salvador_fem()
        # Formatear los partidos por grupos y eliminatorias
        dats9 = formatear_partidos_por_encuentros_salvador_fem(partidos)
        # Imprimir para depuración
        print(dats9)
        # Renderizar la plantilla con los datos formateados
        return render_template('admin/copa_salvador_fem.html', dats9=dats9)
    except Exception as e:
        print(f"Error al obtener o formatear los datos de Copa copa salvador_fem: {e}")
        # Renderizar una plantilla de error o manejar el error de alguna manera
        return render_template('error.html')
# Modificar los partidos de los playoff
@app.route('/modificar_copa_salvador_fem/<int:id>', methods=['POST'])
def modificar_copa_salvador_fem(id):
    if request.method == 'POST':
        encuentros = request.form.get('encuentros')
        num_partidos = int(request.form.get('num_partidos', 0))
        try:
            cur = mysql.connection.cursor()
            # Actualizar la eliminatoria de la jornada
            cur.execute('UPDATE copa_salvador_fem SET encuentros = %s WHERE id = %s', (encuentros, id))
            print(f"Consulta para actualizar la eliminatoria ejecutada para id {id}")
            # Actualizar los detalles de cada partido
            for i in range(num_partidos):
                partido_id = request.form.get(f'partido_id{i}')
                fecha = request.form.get(f'fecha{i}')
                hora = request.form.get(f'hora{i}')
                local = request.form.get(f'local{i}')
                bonusA = request.form.get(f'bonusA{i}')
                resultadoA = request.form.get(f'resultadoA{i}')
                resultadoB = request.form.get(f'resultadoB{i}')
                bonusB = request.form.get(f'bonusB{i}')
                visitante = request.form.get(f'visitante{i}')
                # Verificar que los campos obligatorios tienen valores válidos
                if all([partido_id, local, visitante]):
                    # Asignar valores predeterminados si los campos opcionales están vacíos
                    if fecha is None:
                        fecha = ''
                    if hora is None:
                        hora = ''
                    if local is None:
                        local = ''
                    if bonusA is None:
                        bonusA = ''    
                    if resultadoA is None:
                        resultadoA = ''
                    if resultadoB is None:
                        resultadoB = ''
                    if bonusB is None:
                        bonusB = ''    
                    if visitante is None:
                        visitante = ''
                    # Actualizar el partido en la base de datos
                    cur.execute('UPDATE copa_salvador_fem SET fecha = %s, hora = %s, local = %s, bonusA = %s, resultadoA = %s, resultadoB = %s, bonusB = %s, visitante = %s WHERE id = %s',
                                (fecha, hora, local, bonusA, resultadoA, resultadoB, bonusB, visitante, partido_id))
                    print(f"Consulta para actualizar el partido ejecutada para id {partido_id}")
            # Commit de la transacción
            mysql.connection.commit()
        except MySQLdb.Error as e:
            print(f"Error en la base de datos: {e}")
            mysql.connection.rollback()  # Revertir cambios en caso de error
        finally:
            if 'cur' in locals() and cur:
                cur.close()  # Cerrar cursor
        return redirect(url_for('ver_copa_salvador_fem'))
    return render_template('tu_template.html')
#Eliminar partidos Copa copa CPLV salvador_fem Rural
@app.route('/eliminar_copa_salvador_fem/<string:identificador>', methods=['POST'])
def eliminar_copa_salvador_fem(identificador):
    cur = mysql.connection.cursor()
    try:
        if identificador.startswith('grupo') or identificador in ['finalA', 'finalB']:
            cur.execute('DELETE FROM copa_salvador_fem WHERE encuentros = %s', [identificador])
            mysql.connection.commit()
            flash('Partidos eliminados correctamente', 'success')
        else:
            flash('Identificador de encuentros no válido', 'error')
    except Exception as e:
        flash(f'Error al eliminar partidos: {str(e)}', 'error')
    finally:
        cur.close()
    return redirect(url_for('ver_copa_salvador_fem'))
# Ruta para mostrar la Copa copa CPLV salvador_fem Rural
@app.route('/copa_salvador_fem/')
def copa_salvador_fem():
    partidos = obtener_copa_salvador_fem()
    equipos_por_encuentros, eliminatorias = obtener_equipos_por_encuentros_salvador_fem(partidos)
    clasificaciones, enfrentamientos_directos = recalcular_clasificaciones_salvador_fem(partidos)
    # Convertir clasificaciones a una estructura adecuada para la vista
    data_clasificaciones = {}
    for grupo, equipos in clasificaciones.items():
        # Ordenar equipos primero por puntos, luego por victorias, derrotas, y partidos jugados
        equipos_ordenados = sorted(equipos.items(), key=lambda item: (-item[1]['puntos'], item[1]['ganados'], item[1]['perdidos'], -item[1]['jugados']))      
        # Aplicar el criterio de desempate basado en enfrentamientos directos
        def criterio_enfrentamientos_directos(equipo1, equipo2):
            if equipo1 in enfrentamientos_directos and equipo2 in enfrentamientos_directos[equipo1]:
                resultado_directo = enfrentamientos_directos[equipo1][equipo2]
                return resultado_directo  # Resultado positivo indica que equipo1 ganó
            return 0
        # Crear una lista ordenada usando el criterio de desempate de enfrentamientos directos
        equipos_ordenados = sorted(equipos_ordenados, key=lambda item: (
            -item[1]['puntos'], 
            item[1]['ganados'], 
            item[1]['perdidos'], 
            -item[1]['jugados'],
            -criterio_enfrentamientos_directos(item[0], item[0])
        ))
        # Ajustar el orden para el desempate directo
        for i in range(len(equipos_ordenados)):
            for j in range(i + 1, len(equipos_ordenados)):
                equipo_a, stats_a = equipos_ordenados[i]
                equipo_b, stats_b = equipos_ordenados[j]
                if stats_a['puntos'] == stats_b['puntos'] and stats_a['ganados'] == stats_b['ganados'] and stats_a['perdidos'] == stats_b['perdidos']:
                    resultado_directo = criterio_enfrentamientos_directos(equipo_a, equipo_b)
                    if resultado_directo > 0:  # equipo_a ganó el enfrentamiento directo
                        # Intercambiar posiciones para que equipo_a quede por encima de equipo_b
                        equipos_ordenados[i], equipos_ordenados[j] = equipos_ordenados[j], equipos_ordenados[i]
                    elif resultado_directo < 0:  # equipo_b ganó el enfrentamiento directo
                        # Intercambiar posiciones para que equipo_b quede por encima de equipo_a
                        equipos_ordenados[i], equipos_ordenados[j] = equipos_ordenados[j], equipos_ordenados[i]
        data_clasificaciones[grupo] = equipos_ordenados
    return render_template('copas/salvador_fem_copa.html', equipos_por_encuentros=equipos_por_encuentros, eliminatorias=eliminatorias, clasificaciones=data_clasificaciones)
# Fin copa CR El Salvador Fem

# Copa CR El Salvador
# Crear formulario para los playoff
@app.route('/admin/crear_copa_salvador', methods=['GET', 'POST'])
def crear_copa_salvador():
    if request.method == 'POST':
        encuentros = request.form.get('encuentros')
        print(f"Encuentros: {encuentros}")
        num_partidos = int(request.form.get('num_partidos', 0))
        cur = mysql.connection.cursor()
        for i in range(num_partidos):
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            local = request.form.get(f'local{i}')
            bonus_local = request.form.get(f'bonusA{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            bonus_visitante = request.form.get(f'bonusB{i}')
            visitante = request.form.get(f'visitante{i}')
            # Verificar si algún campo es None y asignar valores por defecto
            if fecha is None:
                fecha = ''
            if hora is None:
                hora = ''
            if local is None:
                local = ''
            if bonus_local is None:
                bonus_local = ''    
            if resultadoA is None:
                resultadoA = ''
            if resultadoB is None:
                resultadoB = ''
            if bonus_visitante is None:
                bonus_visitante = ''    
            if visitante is None:
                visitante = ''
            if encuentros is None:
                encuentros = '' 
            cur.execute("""
                INSERT INTO copa_salvador (encuentros, fecha, hora, local, bonusA, resultadoA, resultadoB, bonusB, visitante)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (encuentros, fecha, hora, local, bonus_local, resultadoA, resultadoB, bonus_visitante, visitante))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('ver_copa_salvador'))
    # Renderizar el formulario para crear la Cops Europa Caja
    return render_template('admin/crear_copa_salvador.html')
    # Renderizar el formulario para crear la copa UEMC
    return render_template('admin/crear_copa_salvador.html')
# Actualizar clasificación de los grupos
def actualizar_clasificacion_salvador(clasificacion_por_grupo_salvador, local, bonus_local ,resultado_local, resultado_visitante, bonus_visitante, visitante):
    resultado_local = int(resultado_local) if resultado_local.isdigit() else None
    resultado_visitante = int(resultado_visitante) if resultado_visitante.isdigit() else None
    # Asegurarse de que cada grupo tenga una entrada en la clasificación
    if grupo not in clasificacion_por_grupo_salvador:
        clasificacion_por_grupo_salvador[grupo] = {}
    if local not in clasificacion_por_grupo_salvador[grupo]:
        clasificacion_por_grupo_salvador[grupo][local] = {'nombre': local, 'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0,'puntos': 0, 'bonus': 0}
    if visitante not in clasificacion_por_grupo_salvador[grupo]:
        clasificacion_por_grupo_salvador[grupo][visitante] = {'nombre': visitante, 'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'puntos': 0, 'bonus': 0}
    # Actualizar los partidos jugados
    if resultado_local is not None and resultado_visitante is not None:
        clasificacion_por_grupo_salvador[grupo][local]['jugados'] += 1
        clasificacion_por_grupo_salvador[grupo][visitante]['jugados'] += 1
        # Determinar el resultado del partido
        if resultado_local > resultado_visitante:
            clasificacion_por_grupo_salvador[grupo][local]['ganados'] += 1
            clasificacion_por_grupo_salvador[grupo][local]['puntos'] += 4 + bonus_local
            clasificacion_por_grupo_salvador[grupo][visitante]['perdidos'] += 1
            clasificacion_por_grupo_salvador[grupo][visitante]['puntos'] += 0 + bonus_visitante
        elif resultado_local < resultado_visitante:
            clasificacion_por_grupo_salvador[grupo][visitante]['ganados'] += 1
            clasificacion_por_grupo_salvador[grupo][visitante]['puntos'] += 4 + bonus_visitante
            clasificacion_por_grupo_salvador[grupo][local]['perdidos'] += 1
            clasificacion_por_grupo_salvador[grupo][local]['puntos'] += 0 + bonus_local
        elif resultado_local == resultado_visitante:
            clasificacion_por_grupo_salvador[grupo][visitante]['empatados'] += 1
            clasificacion_por_grupo_salvador[grupo][visitante]['puntos'] += 2 + bonus_visitante
            clasificacion_por_grupo_salvador[grupo][local]['empatados'] += 1
            clasificacion_por_grupo_salvador[grupo][local]['puntos'] += 2 + bonus_local   
        clasificaciones_salvador[grupo][local]['bonus'] += bonus_local
        clasificaciones_salvador[grupo][visitante]['bonus'] += bonus_visitante 
    return clasificacion_por_grupo_salvador
# Recalcular clasificación
def recalcular_clasificaciones_salvador(partidos):
    clasificaciones_salvador = {}
    enfrentamientos_directos_salvador = {}
    for partido in partidos:
        grupo = partido.get('encuentros')
        local = partido['local']
        visitante = partido['visitante']
        resultado_local = int(partido['resultadoA']) if partido['resultadoA'].isdigit() else None
        resultado_visitante = int(partido['resultadoB']) if partido['resultadoB'].isdigit() else None
        bonus_local = int(partido['bonusA']) if partido['bonusA'].isdigit() else None
        bonus_visitante = int(partido['bonusB']) if partido['bonusB'].isdigit() else None
        if grupo not in clasificaciones_salvador:
            clasificaciones_salvador[grupo] = {}
        # Inicializar equipos si no existen
        if local not in clasificaciones_salvador[grupo]:
            clasificaciones_salvador[grupo][local] = {'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'puntos': 0, 'bonus': 0}
        if visitante not in clasificaciones_salvador[grupo]:
            clasificaciones_salvador[grupo][visitante] = {'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'puntos': 0, 'bonus': 0}
        # Actualizar estadísticas de partidos
        if resultado_local is not None and resultado_visitante is not None:
            clasificaciones_salvador[grupo][local]['jugados'] += 1
            clasificaciones_salvador[grupo][visitante]['jugados'] += 1
            if resultado_local > resultado_visitante:
                clasificaciones_salvador[grupo][local]['ganados'] += 1
                clasificaciones_salvador[grupo][local]['puntos'] += 4 + bonus_local
                clasificaciones_salvador[grupo][visitante]['perdidos'] += 1
                clasificaciones_salvador[grupo][visitante]['puntos'] += 0 + bonus_visitante
            elif resultado_local < resultado_visitante:
                clasificaciones_salvador[grupo][visitante]['ganados'] += 1
                clasificaciones_salvador[grupo][visitante]['puntos'] += 4 + bonus_visitante
                clasificaciones_salvador[grupo][local]['perdidos'] += 1
                clasificaciones_salvador[grupo][local]['puntos'] += 0 + bonus_local
            elif resultado_local == resultado_visitante:
                clasificaciones_salvador[grupo][visitante]['empatados'] += 1
                clasificaciones_salvador[grupo][visitante]['puntos'] += 2 + bonus_visitante
                clasificaciones_salvador[grupo][local]['empatados'] += 1 
                clasificaciones_salvador[grupo][local]['puntos'] += 2 + bonus_local  
            
            clasificaciones_salvador[grupo][local]['bonus'] += bonus_local
            clasificaciones_salvador[grupo][visitante]['bonus'] += bonus_visitante 

        # Almacenar el resultado del enfrentamiento directo
        if local not in enfrentamientos_directos_salvador:
            enfrentamientos_directos_salvador[local] = {}
        if visitante not in enfrentamientos_directos_salvador:
            enfrentamientos_directos_salvador[visitante] = {}
        if resultado_local is not None and resultado_visitante is not None:
            enfrentamientos_directos_salvador[local][visitante] = resultado_local - resultado_visitante
            enfrentamientos_directos_salvador[visitante][local] = resultado_visitante - resultado_local        
    return clasificaciones_salvador, enfrentamientos_directos_salvador
# Función para obtener equipos desde la base de datos
def obtener_equipos_desde_bd_salvador():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, encuentros, fecha, hora, local, bonusA, resultadoA, resultadoB, bonusB, visitante FROM copa_salvador")
    partidos = cur.fetchall()
    cur.close()
    # Definir los grupos y fases de eliminatorias
    grupos_salvador = {'grupoA', 'grupoB', 'grupoC', 'grupoD'}
    fases_eliminatorias_salvador = {'semifinales', 'final'}
    equipos_por_encuentros_salvador = {}
    eliminatorias_salvador = {'semifinales': {'partidos': []}, 'final': {'partidos': []}}
    for partido in partidos:
        grupo_o_fase = partido.get('encuentros')
        if grupo_o_fase in fases_eliminatorias_salvador:
            # Añadir partidos a la fase de eliminación correspondiente
            eliminatorias_salvador[grupo_o_fase]['partidos'].append(partido)
        elif grupo_o_fase in grupos_salvador:
            # Añadir equipos y partidos a los grupos
            if grupo_o_fase not in equipos_por_encuentros_salvador:
                equipos_por_encuentros_salvador[grupo_o_fase] = {'equipos': [], 'partidos': []}
            local = {'nombre': partido['local'], 'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'puntos': 0, 'bonus': 0}
            visitante = {'nombre': partido['visitante'], 'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'puntos': 0, 'bonus': 0}
            # Añadir equipos si no existen en la lista de equipos del grupo
            if not any(e['nombre'] == local['nombre'] for e in equipos_por_encuentros_salvador[grupo_o_fase]['equipos']):
                equipos_por_encuentros_salvador[grupo_o_fase]['equipos'].append(local)
            if not any(e['nombre'] == visitante['nombre'] for e in equipos_por_encuentros_salvador[grupo_o_fase]['equipos']):
                equipos_por_encuentros_salvador[grupo_o_fase]['equipos'].append(visitante)
            equipos_por_encuentros_salvador[grupo_o_fase]['partidos'].append(partido)
        else:
            print(f"Grupo o fase no reconocido: {grupo_o_fase}")
    return equipos_por_encuentros_salvador, eliminatorias_salvador
#Obtener equipos Copa copa CPLV salvador Rural
def obtener_equipos_por_encuentros_salvador(partidos):
    equipos_por_encuentros_salvador = {}
    eliminatorias_salvador = {'semifinales': {'partidos': []}, 'final': {'partidos': []}}
    # Clasificar partidos en grupos o eliminatorias
    for partido in partidos:
        grupo_o_fase = partido.get('encuentros')
        if grupo_o_fase in eliminatorias_salvador:
            eliminatorias_salvador[grupo_o_fase]['partidos'].append(partido)
        else:
            if grupo_o_fase not in equipos_por_encuentros_salvador:
                equipos_por_encuentros_salvador[grupo_o_fase] = {'equipos': [], 'partidos': []}
            # Añadir equipos si no existen en la lista de equipos del grupo
            local = {'nombre': partido['local'], 'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'puntos': 0, 'bonus': 0}
            visitante = {'nombre': partido['visitante'], 'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'puntos': 0, 'bonus':0}
            if not any(e['nombre'] == local['nombre'] for e in equipos_por_encuentros_salvador[grupo_o_fase]['equipos']):
                equipos_por_encuentros_salvador[grupo_o_fase]['equipos'].append(local)
            if not any(e['nombre'] == visitante['nombre'] for e in equipos_por_encuentros_salvador[grupo_o_fase]['equipos']):
                equipos_por_encuentros_salvador[grupo_o_fase]['equipos'].append(visitante)
            equipos_por_encuentros_salvador[grupo_o_fase]['partidos'].append(partido)
    return equipos_por_encuentros_salvador, eliminatorias_salvador
# Obtener la información de la tabla copa_salvador
def obtener_copa_salvador():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, encuentros, fecha, hora, local, bonusA, resultadoA, resultadoB, bonusB, visitante FROM copa_salvador")
    partidos = cur.fetchall()
    cur.close()
    print("Partidos desde la BD:", partidos)  # Añadir esta línea para depuración
    return partidos
# Formatear partidos por grupo
def formatear_partidos_por_encuentros_salvador(partidos):
    encuentros_salvador = {
        'grupoA': {'id': 1, 'encuentros': 'grupoA', 'partidos': []},
        'grupoB': {'id': 2, 'encuentros': 'grupoB', 'partidos': []},
        'grupoC': {'id': 3, 'encuentros': 'grupoC', 'partidos': []},
        'grupoD': {'id': 4, 'encuentros': 'grupoD', 'partidos': []},
        'semifinales': {'id': 5, 'encuentros': 'semifinales', 'partidos': []},
        'final': {'id': 6, 'encuentros': 'final', 'partidos': []}
    }
    for partido in partidos:
        grupo = partido.get('encuentros', '')
        if grupo in encuentros_salvador:
            encuentros_salvador[grupo]['partidos'].append(partido)
        else:
            print(f"Grupo no encontrado: {grupo}")            
    return encuentros_salvador
# Crear formulario para los grupos y eliminatorias salvador
@app.route('/admin/copa_salvador/')
def ver_copa_salvador():
    try:
        # Obtener todos los partidos de los Playoff salvador
        partidos = obtener_copa_salvador()
        # Formatear los partidos por grupos y eliminatorias
        dats10 = formatear_partidos_por_encuentros_salvador(partidos)
        # Imprimir para depuración
        print(dats10)
        # Renderizar la plantilla con los datos formateados
        return render_template('admin/copa_salvador.html', dats10=dats10)
    except Exception as e:
        print(f"Error al obtener o formatear los datos de Copa copa salvador: {e}")
        # Renderizar una plantilla de error o manejar el error de alguna manera
        return render_template('error.html')
# Modificar los partidos de los playoff
@app.route('/modificar_copa_salvador/<int:id>', methods=['POST'])
def modificar_copa_salvador(id):
    if request.method == 'POST':
        encuentros = request.form.get('encuentros')
        num_partidos = int(request.form.get('num_partidos', 0))
        try:
            cur = mysql.connection.cursor()
            # Actualizar la eliminatoria de la jornada
            cur.execute('UPDATE copa_salvador SET encuentros = %s WHERE id = %s', (encuentros, id))
            print(f"Consulta para actualizar la eliminatoria ejecutada para id {id}")
            # Actualizar los detalles de cada partido
            for i in range(num_partidos):
                partido_id = request.form.get(f'partido_id{i}')
                fecha = request.form.get(f'fecha{i}')
                hora = request.form.get(f'hora{i}')
                local = request.form.get(f'local{i}')
                bonusA = request.form.get(f'bonusA{i}')
                resultadoA = request.form.get(f'resultadoA{i}')
                resultadoB = request.form.get(f'resultadoB{i}')
                bonusB = request.form.get(f'bonusB{i}')
                visitante = request.form.get(f'visitante{i}')
                # Verificar que los campos obligatorios tienen valores válidos
                if all([partido_id, local, visitante]):
                    # Asignar valores predeterminados si los campos opcionales están vacíos
                    if fecha is None:
                        fecha = ''
                    if hora is None:
                        hora = ''
                    if local is None:
                        local = ''
                    if bonusA is None:
                        bonusA = ''    
                    if resultadoA is None:
                        resultadoA = ''
                    if resultadoB is None:
                        resultadoB = ''
                    if bonusB is None:
                        bonusB = ''    
                    if visitante is None:
                        visitante = ''
                    # Actualizar el partido en la base de datos
                    cur.execute('UPDATE copa_salvador SET fecha = %s, hora = %s, local = %s, bonusA = %s, resultadoA = %s, resultadoB = %s, bonusB = %s, visitante = %s WHERE id = %s',
                                (fecha, hora, local, bonusA, resultadoA, resultadoB, bonusB, visitante, partido_id))
                    print(f"Consulta para actualizar el partido ejecutada para id {partido_id}")
            # Commit de la transacción
            mysql.connection.commit()
        except MySQLdb.Error as e:
            print(f"Error en la base de datos: {e}")
            mysql.connection.rollback()  # Revertir cambios en caso de error
        finally:
            if 'cur' in locals() and cur:
                cur.close()  # Cerrar cursor
        return redirect(url_for('ver_copa_salvador'))
    return render_template('tu_template.html')
#Eliminar partidos Copa copa CPLV salvador Rural
@app.route('/eliminar_copa_salvador/<string:identificador>', methods=['POST'])
def eliminar_copa_salvador(identificador):
    cur = mysql.connection.cursor()
    try:
        if identificador.startswith('grupo') or identificador in ['finalA', 'finalB']:
            cur.execute('DELETE FROM copa_salvador WHERE encuentros = %s', [identificador])
            mysql.connection.commit()
            flash('Partidos eliminados correctamente', 'success')
        else:
            flash('Identificador de encuentros no válido', 'error')
    except Exception as e:
        flash(f'Error al eliminar partidos: {str(e)}', 'error')
    finally:
        cur.close()
    return redirect(url_for('ver_copa_salvador'))
# Ruta para mostrar la Copa copa CPLV salvador Rural
@app.route('/copa_salvador/')
def copa_salvador():
    partidos = obtener_copa_salvador()
    equipos_por_encuentros, eliminatorias = obtener_equipos_por_encuentros_salvador(partidos)
    clasificaciones, enfrentamientos_directos = recalcular_clasificaciones_salvador(partidos)
    # Convertir clasificaciones a una estructura adecuada para la vista
    data_clasificaciones = {}
    for grupo, equipos in clasificaciones.items():
        # Ordenar equipos primero por puntos, luego por victorias, derrotas, y partidos jugados
        equipos_ordenados = sorted(equipos.items(), key=lambda item: (-item[1]['puntos'], item[1]['ganados'], item[1]['perdidos'], -item[1]['jugados']))      
        # Aplicar el criterio de desempate basado en enfrentamientos directos
        def criterio_enfrentamientos_directos(equipo1, equipo2):
            if equipo1 in enfrentamientos_directos and equipo2 in enfrentamientos_directos[equipo1]:
                resultado_directo = enfrentamientos_directos[equipo1][equipo2]
                return resultado_directo  # Resultado positivo indica que equipo1 ganó
            return 0
        # Crear una lista ordenada usando el criterio de desempate de enfrentamientos directos
        equipos_ordenados = sorted(equipos_ordenados, key=lambda item: (
            -item[1]['puntos'], 
            item[1]['ganados'], 
            item[1]['perdidos'], 
            -item[1]['jugados'],
            -criterio_enfrentamientos_directos(item[0], item[0])
        ))
        # Ajustar el orden para el desempate directo
        for i in range(len(equipos_ordenados)):
            for j in range(i + 1, len(equipos_ordenados)):
                equipo_a, stats_a = equipos_ordenados[i]
                equipo_b, stats_b = equipos_ordenados[j]
                if stats_a['puntos'] == stats_b['puntos'] and stats_a['ganados'] == stats_b['ganados'] and stats_a['perdidos'] == stats_b['perdidos']:
                    resultado_directo = criterio_enfrentamientos_directos(equipo_a, equipo_b)
                    if resultado_directo > 0:  # equipo_a ganó el enfrentamiento directo
                        # Intercambiar posiciones para que equipo_a quede por encima de equipo_b
                        equipos_ordenados[i], equipos_ordenados[j] = equipos_ordenados[j], equipos_ordenados[i]
                    elif resultado_directo < 0:  # equipo_b ganó el enfrentamiento directo
                        # Intercambiar posiciones para que equipo_b quede por encima de equipo_a
                        equipos_ordenados[i], equipos_ordenados[j] = equipos_ordenados[j], equipos_ordenados[i]
        data_clasificaciones[grupo] = equipos_ordenados
    return render_template('copas/salvador_copa.html', equipos_por_encuentros=equipos_por_encuentros, eliminatorias=eliminatorias, clasificaciones=data_clasificaciones)
# Fin copa CR El Salvador

# Copa VRAC
# Crear formulario para los playoff
@app.route('/admin/crear_copa_vrac', methods=['GET', 'POST'])
def crear_copa_vrac():
    if request.method == 'POST':
        encuentros = request.form.get('encuentros')
        print(f"Encuentros: {encuentros}")
        num_partidos = int(request.form.get('num_partidos', 0))
        cur = mysql.connection.cursor()
        for i in range(num_partidos):
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            local = request.form.get(f'local{i}')
            bonus_local = request.form.get(f'bonusA{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            bonus_visitante = request.form.get(f'bonusB{i}')
            visitante = request.form.get(f'visitante{i}')
            # Verificar si algún campo es None y asignar valores por defecto
            if fecha is None:
                fecha = ''
            if hora is None:
                hora = ''
            if local is None:
                local = ''
            if bonus_local is None:
                bonus_local = ''    
            if resultadoA is None:
                resultadoA = ''
            if resultadoB is None:
                resultadoB = ''
            if bonus_visitante is None:
                bonus_visitante = ''    
            if visitante is None:
                visitante = ''
            if encuentros is None:
                encuentros = '' 
            cur.execute("""
                INSERT INTO copa_vrac (encuentros, fecha, hora, local, bonusA, resultadoA, resultadoB, bonusB, visitante)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (encuentros, fecha, hora, local, bonus_local, resultadoA, resultadoB, bonus_visitante, visitante))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('ver_copa_vrac'))
    # Renderizar el formulario para crear la Cops Europa Caja
    return render_template('admin/crear_copa_vrac.html')
    # Renderizar el formulario para crear la copa UEMC
    return render_template('admin/crear_copa_vrac.html')
# Actualizar clasificación de los grupos
def actualizar_clasificacion_vrac(clasificacion_por_grupo_vrac, local, bonus_local ,resultado_local, resultado_visitante, bonus_visitante, visitante):
    resultado_local = int(resultado_local) if resultado_local.isdigit() else None
    resultado_visitante = int(resultado_visitante) if resultado_visitante.isdigit() else None
    # Asegurarse de que cada grupo tenga una entrada en la clasificación
    if grupo not in clasificacion_por_grupo_vrac:
        clasificacion_por_grupo_vrac[grupo] = {}
    if local not in clasificacion_por_grupo_vrac[grupo]:
        clasificacion_por_grupo_vrac[grupo][local] = {'nombre': local, 'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0,'puntos': 0, 'bonus': 0}
    if visitante not in clasificacion_por_grupo_vrac[grupo]:
        clasificacion_por_grupo_vrac[grupo][visitante] = {'nombre': visitante, 'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'puntos': 0, 'bonus': 0}
    # Actualizar los partidos jugados
    if resultado_local is not None and resultado_visitante is not None:
        clasificacion_por_grupo_vrac[grupo][local]['jugados'] += 1
        clasificacion_por_grupo_vrac[grupo][visitante]['jugados'] += 1
        # Determinar el resultado del partido
        if resultado_local > resultado_visitante:
            clasificacion_por_grupo_vrac[grupo][local]['ganados'] += 1
            clasificacion_por_grupo_vrac[grupo][local]['puntos'] += 4 + bonus_local
            clasificacion_por_grupo_vrac[grupo][visitante]['perdidos'] += 1
            clasificacion_por_grupo_vrac[grupo][visitante]['puntos'] += 0 + bonus_visitante
        elif resultado_local < resultado_visitante:
            clasificacion_por_grupo_vrac[grupo][visitante]['ganados'] += 1
            clasificacion_por_grupo_vrac[grupo][visitante]['puntos'] += 4 + bonus_visitante
            clasificacion_por_grupo_vrac[grupo][local]['perdidos'] += 1
            clasificacion_por_grupo_vrac[grupo][local]['puntos'] += 0 + bonus_local
        elif resultado_local == resultado_visitante:
            clasificacion_por_grupo_vrac[grupo][visitante]['empatados'] += 1
            clasificacion_por_grupo_vrac[grupo][visitante]['puntos'] += 2 + bonus_visitante
            clasificacion_por_grupo_vrac[grupo][local]['empatados'] += 1
            clasificacion_por_grupo_vrac[grupo][local]['puntos'] += 2 + bonus_local   
        clasificaciones_vrac[grupo][local]['bonus'] += bonus_local
        clasificaciones_vrac[grupo][visitante]['bonus'] += bonus_visitante 
    return clasificacion_por_grupo_vrac
# Recalcular clasificación
def recalcular_clasificaciones_vrac(partidos):
    clasificaciones_vrac = {}
    enfrentamientos_directos_vrac = {}
    for partido in partidos:
        grupo = partido.get('encuentros')
        local = partido['local']
        visitante = partido['visitante']
        resultado_local = int(partido['resultadoA']) if partido['resultadoA'].isdigit() else None
        resultado_visitante = int(partido['resultadoB']) if partido['resultadoB'].isdigit() else None
        bonus_local = int(partido['bonusA']) if partido['bonusA'].isdigit() else None
        bonus_visitante = int(partido['bonusB']) if partido['bonusB'].isdigit() else None
        if grupo not in clasificaciones_vrac:
            clasificaciones_vrac[grupo] = {}
        # Inicializar equipos si no existen
        if local not in clasificaciones_vrac[grupo]:
            clasificaciones_vrac[grupo][local] = {'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'puntos': 0, 'bonus': 0}
        if visitante not in clasificaciones_vrac[grupo]:
            clasificaciones_vrac[grupo][visitante] = {'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'puntos': 0, 'bonus': 0}
        # Actualizar estadísticas de partidos
        if resultado_local is not None and resultado_visitante is not None:
            clasificaciones_vrac[grupo][local]['jugados'] += 1
            clasificaciones_vrac[grupo][visitante]['jugados'] += 1
            if resultado_local > resultado_visitante:
                clasificaciones_vrac[grupo][local]['ganados'] += 1
                clasificaciones_vrac[grupo][local]['puntos'] += 4 + bonus_local
                clasificaciones_vrac[grupo][visitante]['perdidos'] += 1
                clasificaciones_vrac[grupo][visitante]['puntos'] += 0 + bonus_visitante
            elif resultado_local < resultado_visitante:
                clasificaciones_vrac[grupo][visitante]['ganados'] += 1
                clasificaciones_vrac[grupo][visitante]['puntos'] += 4 + bonus_visitante
                clasificaciones_vrac[grupo][local]['perdidos'] += 1
                clasificaciones_vrac[grupo][local]['puntos'] += 0 + bonus_local
            elif resultado_local == resultado_visitante:
                clasificaciones_vrac[grupo][visitante]['empatados'] += 1
                clasificaciones_vrac[grupo][visitante]['puntos'] += 2 + bonus_visitante
                clasificaciones_vrac[grupo][local]['empatados'] += 1 
                clasificaciones_vrac[grupo][local]['puntos'] += 2 + bonus_local              
            clasificaciones_vrac[grupo][local]['bonus'] += bonus_local
            clasificaciones_vrac[grupo][visitante]['bonus'] += bonus_visitante 
        # Almacenar el resultado del enfrentamiento directo
        if local not in enfrentamientos_directos_vrac:
            enfrentamientos_directos_vrac[local] = {}
        if visitante not in enfrentamientos_directos_vrac:
            enfrentamientos_directos_vrac[visitante] = {}
        if resultado_local is not None and resultado_visitante is not None:
            enfrentamientos_directos_vrac[local][visitante] = resultado_local - resultado_visitante
            enfrentamientos_directos_vrac[visitante][local] = resultado_visitante - resultado_local        
    return clasificaciones_vrac, enfrentamientos_directos_vrac
# Función para obtener equipos desde la base de datos
def obtener_equipos_desde_bd_vrac():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, encuentros, fecha, hora, local, bonusA, resultadoA, resultadoB, bonusB, visitante FROM copa_vrac")
    partidos = cur.fetchall()
    cur.close()
    # Definir los grupos y fases de eliminatorias
    grupos_vrac = {'grupoA', 'grupoB', 'grupoC', 'grupoD'}
    fases_eliminatorias_vrac = {'semifinales', 'final'}
    equipos_por_encuentros_vrac = {}
    eliminatorias_vrac = {'semifinales': {'partidos': []}, 'final': {'partidos': []}}
    for partido in partidos:
        grupo_o_fase = partido.get('encuentros')
        if grupo_o_fase in fases_eliminatorias_vrac:
            # Añadir partidos a la fase de eliminación correspondiente
            eliminatorias_vrac[grupo_o_fase]['partidos'].append(partido)
        elif grupo_o_fase in grupos_vrac:
            # Añadir equipos y partidos a los grupos
            if grupo_o_fase not in equipos_por_encuentros_vrac:
                equipos_por_encuentros_vrac[grupo_o_fase] = {'equipos': [], 'partidos': []}
            local = {'nombre': partido['local'], 'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'puntos': 0, 'bonus': 0}
            visitante = {'nombre': partido['visitante'], 'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'puntos': 0, 'bonus': 0}
            # Añadir equipos si no existen en la lista de equipos del grupo
            if not any(e['nombre'] == local['nombre'] for e in equipos_por_encuentros_vrac[grupo_o_fase]['equipos']):
                equipos_por_encuentros_vrac[grupo_o_fase]['equipos'].append(local)
            if not any(e['nombre'] == visitante['nombre'] for e in equipos_por_encuentros_vrac[grupo_o_fase]['equipos']):
                equipos_por_encuentros_vrac[grupo_o_fase]['equipos'].append(visitante)
            equipos_por_encuentros_vrac[grupo_o_fase]['partidos'].append(partido)
        else:
            print(f"Grupo o fase no reconocido: {grupo_o_fase}")
    return equipos_por_encuentros_vrac, eliminatorias_vrac
#Obtener equipos Copa copa CPLV vrac Rural
def obtener_equipos_por_encuentros_vrac(partidos):
    equipos_por_encuentros_vrac = {}
    eliminatorias_vrac = {'semifinales': {'partidos': []}, 'final': {'partidos': []}}
    # Clasificar partidos en grupos o eliminatorias
    for partido in partidos:
        grupo_o_fase = partido.get('encuentros')
        if grupo_o_fase in eliminatorias_vrac:
            eliminatorias_vrac[grupo_o_fase]['partidos'].append(partido)
        else:
            if grupo_o_fase not in equipos_por_encuentros_vrac:
                equipos_por_encuentros_vrac[grupo_o_fase] = {'equipos': [], 'partidos': []}
            # Añadir equipos si no existen en la lista de equipos del grupo
            local = {'nombre': partido['local'], 'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'puntos': 0, 'bonus': 0}
            visitante = {'nombre': partido['visitante'], 'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'puntos': 0, 'bonus':0}
            if not any(e['nombre'] == local['nombre'] for e in equipos_por_encuentros_vrac[grupo_o_fase]['equipos']):
                equipos_por_encuentros_vrac[grupo_o_fase]['equipos'].append(local)
            if not any(e['nombre'] == visitante['nombre'] for e in equipos_por_encuentros_vrac[grupo_o_fase]['equipos']):
                equipos_por_encuentros_vrac[grupo_o_fase]['equipos'].append(visitante)
            equipos_por_encuentros_vrac[grupo_o_fase]['partidos'].append(partido)
    return equipos_por_encuentros_vrac, eliminatorias_vrac
# Obtener la información de la tabla copa_vrac
def obtener_copa_vrac():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, encuentros, fecha, hora, local, bonusA, resultadoA, resultadoB, bonusB, visitante FROM copa_vrac")
    partidos = cur.fetchall()
    cur.close()
    print("Partidos desde la BD:", partidos)  # Añadir esta línea para depuración
    return partidos
# Formatear partidos por grupo
def formatear_partidos_por_encuentros_vrac(partidos):
    encuentros_vrac = {
        'grupoA': {'id': 1, 'encuentros': 'grupoA', 'partidos': []},
        'grupoB': {'id': 2, 'encuentros': 'grupoB', 'partidos': []},
        'grupoC': {'id': 3, 'encuentros': 'grupoC', 'partidos': []},
        'grupoD': {'id': 4, 'encuentros': 'grupoD', 'partidos': []},
        'semifinales': {'id': 5, 'encuentros': 'semifinales', 'partidos': []},
        'final': {'id': 6, 'encuentros': 'final', 'partidos': []}
    }
    for partido in partidos:
        grupo = partido.get('encuentros', '')
        if grupo in encuentros_vrac:
            encuentros_vrac[grupo]['partidos'].append(partido)
        else:
            print(f"Grupo no encontrado: {grupo}")            
    return encuentros_vrac
# Crear formulario para los grupos y eliminatorias vrac
@app.route('/admin/copa_vrac/')
def ver_copa_vrac():
    try:
        # Obtener todos los partidos de los Playoff vrac
        partidos = obtener_copa_vrac()
        # Formatear los partidos por grupos y eliminatorias
        dats11 = formatear_partidos_por_encuentros_vrac(partidos)
        # Imprimir para depuración
        print(dats11)
        # Renderizar la plantilla con los datos formateados
        return render_template('admin/copa_vrac.html', dats11=dats11)
    except Exception as e:
        print(f"Error al obtener o formatear los datos de Copa copa vrac: {e}")
        # Renderizar una plantilla de error o manejar el error de alguna manera
        return render_template('error.html')
# Modificar los partidos de los playoff
@app.route('/modificar_copa_vrac/<int:id>', methods=['POST'])
def modificar_copa_vrac(id):
    if request.method == 'POST':
        encuentros = request.form.get('encuentros')
        num_partidos = int(request.form.get('num_partidos', 0))
        try:
            cur = mysql.connection.cursor()
            # Actualizar la eliminatoria de la jornada
            cur.execute('UPDATE copa_vrac SET encuentros = %s WHERE id = %s', (encuentros, id))
            print(f"Consulta para actualizar la eliminatoria ejecutada para id {id}")
            # Actualizar los detalles de cada partido
            for i in range(num_partidos):
                partido_id = request.form.get(f'partido_id{i}')
                fecha = request.form.get(f'fecha{i}')
                hora = request.form.get(f'hora{i}')
                local = request.form.get(f'local{i}')
                bonusA = request.form.get(f'bonusA{i}')
                resultadoA = request.form.get(f'resultadoA{i}')
                resultadoB = request.form.get(f'resultadoB{i}')
                bonusB = request.form.get(f'bonusB{i}')
                visitante = request.form.get(f'visitante{i}')
                # Verificar que los campos obligatorios tienen valores válidos
                if all([partido_id, local, visitante]):
                    # Asignar valores predeterminados si los campos opcionales están vacíos
                    if fecha is None:
                        fecha = ''
                    if hora is None:
                        hora = ''
                    if local is None:
                        local = ''
                    if bonusA is None:
                        bonusA = ''    
                    if resultadoA is None:
                        resultadoA = ''
                    if resultadoB is None:
                        resultadoB = ''
                    if bonusB is None:
                        bonusB = ''    
                    if visitante is None:
                        visitante = ''
                    # Actualizar el partido en la base de datos
                    cur.execute('UPDATE copa_vrac SET fecha = %s, hora = %s, local = %s, bonusA = %s, resultadoA = %s, resultadoB = %s, bonusB = %s, visitante = %s WHERE id = %s',
                                (fecha, hora, local, bonusA, resultadoA, resultadoB, bonusB, visitante, partido_id))
                    print(f"Consulta para actualizar el partido ejecutada para id {partido_id}")
            # Commit de la transacción
            mysql.connection.commit()
        except MySQLdb.Error as e:
            print(f"Error en la base de datos: {e}")
            mysql.connection.rollback()  # Revertir cambios en caso de error
        finally:
            if 'cur' in locals() and cur:
                cur.close()  # Cerrar cursor
        return redirect(url_for('ver_copa_vrac'))
    return render_template('tu_template.html')
#Eliminar partidos Copa copa CPLV vrac Rural
@app.route('/eliminar_copa_vrac/<string:identificador>', methods=['POST'])
def eliminar_copa_vrac(identificador):
    cur = mysql.connection.cursor()
    try:
        if identificador.startswith('grupo') or identificador in ['finalA', 'finalB']:
            cur.execute('DELETE FROM copa_vrac WHERE encuentros = %s', [identificador])
            mysql.connection.commit()
            flash('Partidos eliminados correctamente', 'success')
        else:
            flash('Identificador de encuentros no válido', 'error')
    except Exception as e:
        flash(f'Error al eliminar partidos: {str(e)}', 'error')
    finally:
        cur.close()
    return redirect(url_for('ver_copa_vrac'))
# Ruta para mostrar la Copa copa CPLV vrac Rural
@app.route('/copa_vrac/')
def copa_vrac():
    partidos = obtener_copa_vrac()
    equipos_por_encuentros, eliminatorias = obtener_equipos_por_encuentros_vrac(partidos)
    clasificaciones, enfrentamientos_directos = recalcular_clasificaciones_vrac(partidos)
    # Convertir clasificaciones a una estructura adecuada para la vista
    data_clasificaciones = {}
    for grupo, equipos in clasificaciones.items():
        # Ordenar equipos primero por puntos, luego por victorias, derrotas, y partidos jugados
        equipos_ordenados = sorted(equipos.items(), key=lambda item: (-item[1]['puntos'], item[1]['ganados'], item[1]['perdidos'], -item[1]['jugados']))      
        # Aplicar el criterio de desempate basado en enfrentamientos directos
        def criterio_enfrentamientos_directos(equipo1, equipo2):
            if equipo1 in enfrentamientos_directos and equipo2 in enfrentamientos_directos[equipo1]:
                resultado_directo = enfrentamientos_directos[equipo1][equipo2]
                return resultado_directo  # Resultado positivo indica que equipo1 ganó
            return 0
        # Crear una lista ordenada usando el criterio de desempate de enfrentamientos directos
        equipos_ordenados = sorted(equipos_ordenados, key=lambda item: (
            -item[1]['puntos'], 
            item[1]['ganados'], 
            item[1]['perdidos'], 
            -item[1]['jugados'],
            -criterio_enfrentamientos_directos(item[0], item[0])
        ))
        # Ajustar el orden para el desempate directo
        for i in range(len(equipos_ordenados)):
            for j in range(i + 1, len(equipos_ordenados)):
                equipo_a, stats_a = equipos_ordenados[i]
                equipo_b, stats_b = equipos_ordenados[j]
                if stats_a['puntos'] == stats_b['puntos'] and stats_a['ganados'] == stats_b['ganados'] and stats_a['perdidos'] == stats_b['perdidos']:
                    resultado_directo = criterio_enfrentamientos_directos(equipo_a, equipo_b)
                    if resultado_directo > 0:  # equipo_a ganó el enfrentamiento directo
                        # Intercambiar posiciones para que equipo_a quede por encima de equipo_b
                        equipos_ordenados[i], equipos_ordenados[j] = equipos_ordenados[j], equipos_ordenados[i]
                    elif resultado_directo < 0:  # equipo_b ganó el enfrentamiento directo
                        # Intercambiar posiciones para que equipo_b quede por encima de equipo_a
                        equipos_ordenados[i], equipos_ordenados[j] = equipos_ordenados[j], equipos_ordenados[i]
        data_clasificaciones[grupo] = equipos_ordenados
    return render_template('copas/vrac_copa.html', equipos_por_encuentros=equipos_por_encuentros, eliminatorias=eliminatorias, clasificaciones=data_clasificaciones)
# Fin copa VRAC

# Copa UEMC Valladolid
# Crear formulario para los grupos de la Copa UEMC
@app.route('/admin/crear_copa_uemc', methods=['GET', 'POST'])
def crear_copa_uemc():
    if request.method == 'POST':
        encuentros = request.form.get('encuentros')
        print(f"Encuentros: {encuentros}")
        num_partidos = int(request.form.get('num_partidos', 0))
        cur = mysql.connection.cursor()
        for i in range(num_partidos):
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            local = request.form.get(f'local{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            visitante = request.form.get(f'visitante{i}')
            # Verificar si algún campo es None y asignar valores por defecto
            if fecha is None:
                fecha = ''
            if hora is None:
                hora = ''
            if local is None:
                local = ''
            if resultadoA is None:
                resultadoA = ''
            if resultadoB is None:
                resultadoB = ''
            if visitante is None:
                visitante = ''
            if encuentros is None:
                encuentros = '' 
            cur.execute("""
                INSERT INTO copa_uemc (encuentros, fecha, hora, local, resultadoA, resultadoB, visitante)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (encuentros, fecha, hora, local, resultadoA, resultadoB, visitante))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('ver_copa_uemc'))
    # Renderizar el formulario para crear la copa UEMC
    return render_template('admin/crear_copa_uemc.html')
# Actualizar clasificación de los grupos
def actualizar_clasificacion(clasificacion_por_grupo, local, resultado_local, resultado_visitante, visitante):
    resultado_local = int(resultado_local) if resultado_local.isdigit() else None
    resultado_visitante = int(resultado_visitante) if resultado_visitante.isdigit() else None
    # Asegurarse de que cada grupo tenga una entrada en la clasificación
    if grupo not in clasificacion_por_grupo:
        clasificacion_por_grupo[grupo] = {}
    if local not in clasificacion_por_grupo[grupo]:
        clasificacion_por_grupo[grupo][local] = {'nombre': local, 'jugados': 0, 'ganados': 0, 'perdidos': 0,'puntos': 0}
    if visitante not in clasificacion_por_grupo[grupo]:
        clasificacion_por_grupo[grupo][visitante] = {'nombre': visitante, 'jugados': 0, 'ganados': 0, 'perdidos': 0, 'puntos': 0}
    # Actualizar los partidos jugados
    if resultado_local is not None and resultado_visitante is not None:
        clasificacion_por_grupo[grupo][local]['jugados'] += 1
        clasificacion_por_grupo[grupo][visitante]['jugados'] += 1
        # Determinar el resultado del partido
        if resultado_local > resultado_visitante:
            clasificacion_por_grupo[grupo][local]['ganados'] += 1
            clasificacion_por_grupo[grupo][local]['puntos'] += 2
            clasificacion_por_grupo[grupo][visitante]['perdidos'] += 1
            clasificacion_por_grupo[grupo][visitante]['puntos'] += 1
        elif resultado_local < resultado_visitante:
            clasificacion_por_grupo[grupo][visitante]['ganados'] += 1
            clasificacion_por_grupo[grupo][visitante]['puntos'] += 2
            clasificacion_por_grupo[grupo][local]['perdidos'] += 1
            clasificacion_por_grupo[grupo][local]['puntos'] += 1
        else:
            clasificacion_por_grupo[grupo][local]['puntos'] += 1
            clasificacion_por_grupo[grupo][visitante]['puntos'] += 1
    return clasificacion_por_grupo
# Recalcular clasificación
def recalcular_clasificaciones(partidos):
    clasificaciones = {}
    enfrentamientos_directos = {}
    for partido in partidos:
        grupo = partido.get('encuentros')
        local = partido['local']
        visitante = partido['visitante']
        resultado_local = int(partido['resultadoA']) if partido['resultadoA'].isdigit() else None
        resultado_visitante = int(partido['resultadoB']) if partido['resultadoB'].isdigit() else None
        if grupo not in clasificaciones:
            clasificaciones[grupo] = {}
        # Inicializar equipos si no existen
        if local not in clasificaciones[grupo]:
            clasificaciones[grupo][local] = {'jugados': 0, 'ganados': 0, 'perdidos': 0, 'puntos': 0}
        if visitante not in clasificaciones[grupo]:
            clasificaciones[grupo][visitante] = {'jugados': 0, 'ganados': 0, 'perdidos': 0, 'puntos': 0}
        # Actualizar estadísticas de partidos
        if resultado_local is not None and resultado_visitante is not None:
            clasificaciones[grupo][local]['jugados'] += 1
            clasificaciones[grupo][visitante]['jugados'] += 1
            if resultado_local > resultado_visitante:
                clasificaciones[grupo][local]['ganados'] += 1
                clasificaciones[grupo][local]['puntos'] += 2
                clasificaciones[grupo][visitante]['perdidos'] += 1
                clasificaciones[grupo][visitante]['puntos'] += 1
            elif resultado_local < resultado_visitante:
                clasificaciones[grupo][visitante]['ganados'] += 1
                clasificaciones[grupo][visitante]['puntos'] += 2
                clasificaciones[grupo][local]['perdidos'] += 1
                clasificaciones[grupo][local]['puntos'] += 1
            else:
                clasificaciones[grupo][local]['puntos'] += 1
                clasificaciones[grupo][visitante]['puntos'] += 1
        # Almacenar el resultado del enfrentamiento directo
        if local not in enfrentamientos_directos:
            enfrentamientos_directos[local] = {}
        if visitante not in enfrentamientos_directos:
            enfrentamientos_directos[visitante] = {}
        if resultado_local is not None and resultado_visitante is not None:
            enfrentamientos_directos[local][visitante] = resultado_local - resultado_visitante
            enfrentamientos_directos[visitante][local] = resultado_visitante - resultado_local        
    return clasificaciones, enfrentamientos_directos
# Función para obtener equipos desde la base de datos
def obtener_equipos_desde_bd():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, encuentros, fecha, hora, local, resultadoA, resultadoB, visitante FROM copa_uemc")
    partidos = cur.fetchall()
    cur.close()

    # Definir los grupos y fases de eliminatorias
    grupos = {'grupoA', 'grupoB', 'grupoC', 'grupoD', 'grupoE', 'grupoF', 'grupoG', 'grupoH'}
    fases_eliminatorias = {'cuartos', 'semifinales', 'final'}

    equipos_por_encuentros = {}
    eliminatorias = {'cuartos': {'partidos': []}, 'semifinales': {'partidos': []}, 'final': {'partidos': []}}

    for partido in partidos:
        grupo_o_fase = partido.get('encuentros')

        if grupo_o_fase in fases_eliminatorias:
            # Añadir partidos a la fase de eliminación correspondiente
            eliminatorias[grupo_o_fase]['partidos'].append(partido)
        elif grupo_o_fase in grupos:
            # Añadir equipos y partidos a los grupos
            if grupo_o_fase not in equipos_por_encuentros:
                equipos_por_encuentros[grupo_o_fase] = {'equipos': [], 'partidos': []}

            local = {'nombre': partido['local'], 'jugados': 0, 'ganados': 0, 'perdidos': 0, 'puntos': 0}
            visitante = {'nombre': partido['visitante'], 'jugados': 0, 'ganados': 0, 'perdidos': 0, 'puntos': 0}

            # Añadir equipos si no existen en la lista de equipos del grupo
            if not any(e['nombre'] == local['nombre'] for e in equipos_por_encuentros[grupo_o_fase]['equipos']):
                equipos_por_encuentros[grupo_o_fase]['equipos'].append(local)
            if not any(e['nombre'] == visitante['nombre'] for e in equipos_por_encuentros[grupo_o_fase]['equipos']):
                equipos_por_encuentros[grupo_o_fase]['equipos'].append(visitante)

            equipos_por_encuentros[grupo_o_fase]['partidos'].append(partido)
        else:
            print(f"Grupo o fase no reconocido: {grupo_o_fase}")

    return equipos_por_encuentros, eliminatorias
#Obtener equipos Copa Uemc
def obtener_equipos_por_encuentros(partidos):
    equipos_por_encuentros = {}
    eliminatorias = {'cuartos': {'partidos': []}, 'semifinales': {'partidos': []}, 'final': {'partidos': []}}

    # Clasificar partidos en grupos o eliminatorias
    for partido in partidos:
        grupo_o_fase = partido.get('encuentros')

        if grupo_o_fase in eliminatorias:
            eliminatorias[grupo_o_fase]['partidos'].append(partido)
        else:
            if grupo_o_fase not in equipos_por_encuentros:
                equipos_por_encuentros[grupo_o_fase] = {'equipos': [], 'partidos': []}

            # Añadir equipos si no existen en la lista de equipos del grupo
            local = {'nombre': partido['local'], 'jugados': 0, 'ganados': 0, 'perdidos': 0, 'puntos': 0}
            visitante = {'nombre': partido['visitante'], 'jugados': 0, 'ganados': 0, 'perdidos': 0, 'puntos': 0}

            if not any(e['nombre'] == local['nombre'] for e in equipos_por_encuentros[grupo_o_fase]['equipos']):
                equipos_por_encuentros[grupo_o_fase]['equipos'].append(local)
            if not any(e['nombre'] == visitante['nombre'] for e in equipos_por_encuentros[grupo_o_fase]['equipos']):
                equipos_por_encuentros[grupo_o_fase]['equipos'].append(visitante)

            equipos_por_encuentros[grupo_o_fase]['partidos'].append(partido)
    return equipos_por_encuentros, eliminatorias
# Obtener la información de la tabla copa_vrac
def obtener_copa_uemc():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, encuentros, fecha, hora, local, resultadoA, resultadoB, visitante FROM copa_uemc")
    partidos = cur.fetchall()
    cur.close()
    print("Partidos desde la BD:", partidos)  # Añadir esta línea para depuración
    return partidos
# Formatear partidos por grupo
def formatear_partidos_por_encuentros(partidos):
    encuentros = {
        'grupoA': {'id': 1, 'encuentros': 'grupoA', 'partidos': []},
        'grupoB': {'id': 2, 'encuentros': 'grupoB', 'partidos': []},
        'grupoC': {'id': 3, 'encuentros': 'grupoC', 'partidos': []},
        'grupoD': {'id': 4, 'encuentros': 'grupoD', 'partidos': []},
        'grupoE': {'id': 5, 'encuentros': 'grupoE', 'partidos': []},
        'grupoF': {'id': 6, 'encuentros': 'grupoF', 'partidos': []},
        'grupoG': {'id': 7, 'encuentros': 'grupoG', 'partidos': []},
        'grupoH': {'id': 8, 'encuentros': 'grupoH', 'partidos': []},
        'cuartos': {'id': 9, 'encuentros': 'cuartos', 'partidos': []},
        'semifinales': {'id': 10, 'encuentros': 'semifinales', 'partidos': []},
        'final': {'id': 11, 'encuentros': 'final', 'partidos': []}
    }
    for partido in partidos:
        grupo = partido.get('encuentros', '')
        if grupo in encuentros:
            encuentros[grupo]['partidos'].append(partido)
        else:
            print(f"Grupo no encontrado: {grupo}")            
    return encuentros
# Crear formulario para los grupos y eliminatorias UEMC
@app.route('/admin/copa_uemc/')
def ver_copa_uemc():
    try:
        # Obtener todos los partidos de la Copa UEMC
        partidos = obtener_copa_uemc()
        # Formatear los partidos por grupos y eliminatorias
        dats5 = formatear_partidos_por_encuentros(partidos)
        # Imprimir para depuración
        print(dats5)
        # Renderizar la plantilla con los datos formateados
        return render_template('admin/copa_uemc.html', dats5=dats5)
    except Exception as e:
        print(f"Error al obtener o formatear los datos de la Copa VRAC: {e}")
        # Renderizar una plantilla de error o manejar el error de alguna manera
        return render_template('error.html')
# Modificar los partidos de los playoff
@app.route('/modificar_copa_uemc/<int:id>', methods=['POST'])
def modificar_copa_uemc(id):
    if request.method == 'POST':
        encuentros = request.form.get('encuentros')
        num_partidos = int(request.form.get('num_partidos', 0))
        try:
            cur = mysql.connection.cursor()
            # Actualizar la eliminatoria de la jornada
            cur.execute('UPDATE copa_uemc SET encuentros = %s WHERE id = %s', (encuentros, id))
            print(f"Consulta para actualizar la eliminatoria ejecutada para id {id}")
            # Actualizar los detalles de cada partido
            for i in range(num_partidos):
                partido_id = request.form.get(f'partido_id{i}')
                fecha = request.form.get(f'fecha{i}')
                hora = request.form.get(f'hora{i}')
                local = request.form.get(f'local{i}')
                resultadoA = request.form.get(f'resultadoA{i}')
                resultadoB = request.form.get(f'resultadoB{i}')
                visitante = request.form.get(f'visitante{i}')
                # Verificar que los campos obligatorios tienen valores válidos
                if all([partido_id, local, visitante]):
                    # Asignar valores predeterminados si los campos opcionales están vacíos
                    if fecha is None:
                        fecha = ''
                    if hora is None:
                        hora = ''
                    if local is None:
                        local = ''
                    if resultadoA is None:
                        resultadoA = ''
                    if resultadoB is None:
                        resultadoB = ''
                    if visitante is None:
                        visitante = ''
                    # Actualizar el partido en la base de datos
                    cur.execute('UPDATE copa_uemc SET fecha = %s, hora = %s, local = %s, resultadoA = %s, resultadoB = %s, visitante = %s WHERE id = %s',
                                (fecha, hora, local, resultadoA, resultadoB, visitante, partido_id))
                    print(f"Consulta para actualizar el partido ejecutada para id {partido_id}")
            # Commit de la transacción
            mysql.connection.commit()
        except MySQLdb.Error as e:
            print(f"Error en la base de datos: {e}")
            mysql.connection.rollback()  # Revertir cambios en caso de error
        finally:
            if 'cur' in locals() and cur:
                cur.close()  # Cerrar cursor
        return redirect(url_for('ver_copa_uemc'))
    return render_template('tu_template.html')
#Eliminar partidos Copa UEMC
@app.route('/eliminar_copa_uemc/<string:identificador>', methods=['POST'])
def eliminar_copa_uemc(identificador):
    cur = mysql.connection.cursor()
    try:
        if identificador.startswith('grupo') or identificador in ['cuartos', 'semifinales', 'final']:
            cur.execute('DELETE FROM copa_uemc WHERE encuentros = %s', [identificador])
            mysql.connection.commit()
            flash('Partidos eliminados correctamente', 'success')
        else:
            flash('Identificador de encuentros no válido', 'error')
    except Exception as e:
        flash(f'Error al eliminar partidos: {str(e)}', 'error')
    finally:
        cur.close()

    return redirect(url_for('ver_copa_uemc'))
# Ruta para mostrar la copa UEMC
@app.route('/uemc_copa/')
def uemc_copa():
    partidos = obtener_copa_uemc()
    equipos_por_encuentros, eliminatorias = obtener_equipos_por_encuentros(partidos)
    clasificaciones, enfrentamientos_directos = recalcular_clasificaciones(partidos)
    # Convertir clasificaciones a una estructura adecuada para la vista
    data_clasificaciones = {}
    for grupo, equipos in clasificaciones.items():
        # Ordenar equipos primero por puntos, luego por victorias, derrotas, y partidos jugados
        equipos_ordenados = sorted(equipos.items(), key=lambda item: (-item[1]['puntos'], item[1]['ganados'], item[1]['perdidos'], -item[1]['jugados']))      
        # Aplicar el criterio de desempate basado en enfrentamientos directos
        def criterio_enfrentamientos_directos(equipo1, equipo2):
            if equipo1 in enfrentamientos_directos and equipo2 in enfrentamientos_directos[equipo1]:
                resultado_directo = enfrentamientos_directos[equipo1][equipo2]
                return resultado_directo  # Resultado positivo indica que equipo1 ganó
            return 0
        # Crear una lista ordenada usando el criterio de desempate de enfrentamientos directos
        equipos_ordenados = sorted(equipos_ordenados, key=lambda item: (
            -item[1]['puntos'], 
            item[1]['ganados'], 
            item[1]['perdidos'], 
            -item[1]['jugados'],
            -criterio_enfrentamientos_directos(item[0], item[0])
        ))
        # Ajustar el orden para el desempate directo
        for i in range(len(equipos_ordenados)):
            for j in range(i + 1, len(equipos_ordenados)):
                equipo_a, stats_a = equipos_ordenados[i]
                equipo_b, stats_b = equipos_ordenados[j]
                if stats_a['puntos'] == stats_b['puntos'] and stats_a['ganados'] == stats_b['ganados'] and stats_a['perdidos'] == stats_b['perdidos']:
                    resultado_directo = criterio_enfrentamientos_directos(equipo_a, equipo_b)
                    if resultado_directo > 0:  # equipo_a ganó el enfrentamiento directo
                        # Intercambiar posiciones para que equipo_a quede por encima de equipo_b
                        equipos_ordenados[i], equipos_ordenados[j] = equipos_ordenados[j], equipos_ordenados[i]
                    elif resultado_directo < 0:  # equipo_b ganó el enfrentamiento directo
                        # Intercambiar posiciones para que equipo_b quede por encima de equipo_a
                        equipos_ordenados[i], equipos_ordenados[j] = equipos_ordenados[j], equipos_ordenados[i]
        data_clasificaciones[grupo] = equipos_ordenados
    return render_template('copas/uemc_copa.html', equipos_por_encuentros=equipos_por_encuentros, eliminatorias=eliminatorias, clasificaciones=data_clasificaciones)
# Fin copa UEMC Valladolid

# PARTICIPACIÓN EUROPEA MASCULINO Y FEMENINO
# Europa Aula Valladolid
# Crear formulario para EHF Aula Valladolid
@app.route('/admin/crear_europa_aula', methods=['GET', 'POST'])
def crear_europa_aula():
    if request.method == 'POST':
        eliminatoria = request.form.get('eliminatoria')       
        # Determinar el máximo de partidos permitidos para la eliminatoria
        max_partidos = {
            'segunda': 64,
            'tercera': 32,
            'octavos': 16,
            'cuartos': 8,
            'semifinales': 4,
            'final': 2
        }.get(eliminatoria, 0)        
        # Obtener el número de partidos del formulario
        num_partidos_str = request.form.get('num_partidos', '0').strip()
        num_partidos = int(num_partidos_str) if num_partidos_str else 0        
        # Validar el número de partidos
        if num_partidos < 0 or num_partidos > max_partidos:
            return "Número de partidos no válido"                
        # Crear un cursor para ejecutar consultas SQL
        cur = mysql.connection.cursor()
        # Iterar sobre los datos del formulario para insertar los partidos
        for i in range(num_partidos):
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            local = request.form.get(f'local{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            visitante = request.form.get(f'visitante{i}')          
            # Verificar si algún campo es None y asignar valores por defecto
            if fecha is None:
                fecha = ''
            if hora is None:
                hora = ''
            if local is None:
                local = ''
            if resultadoA is None:
                resultadoA = ''
            if resultadoB is None:
                resultadoB = ''
            if visitante is None:
                visitante = ''           
            # Insertar el partido en la tabla copa_recoletas
            cur.execute("""
                INSERT INTO europa_aula (eliminatoria, fecha, hora, local, resultadoA, resultadoB, visitante)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (eliminatoria, fecha, hora, local, resultadoA, resultadoB, visitante))       
        # Confirmar los cambios en la base de datos
        mysql.connection.commit()        
        # Cerrar el cursor
        cur.close()        
        # Redireccionar a la vista de la copa_recoletas
        return redirect(url_for('ver_europa_aula'))
    # Renderizar el formulario para crear la copa_recoletas
    return render_template('admin/europa_aula.html')
# Crear formulario para EHF Aula Valladolid
@app.route('/admin/europa_aula/')
def ver_europa_aula():
    cursor = mysql.connection.cursor()
    eliminatorias = ['segunda', 'tercera','octavos','cuartos', 'semifinales','final']
    datos_eliminatorias = {}
    for eliminatoria in eliminatorias:
        cursor.execute("SELECT * FROM europa_aula WHERE eliminatoria = %s", [eliminatoria])
        partidos = cursor.fetchall()
        datos_eliminatorias[eliminatoria] = partidos
    cursor.close()
    return render_template('admin/europa_aula.html', datos_eliminatorias=datos_eliminatorias)
# Modificar los partidos de EHF Aula Valladolid
@app.route('/modificar_europa_aula/<string:id>', methods=['GET', 'POST'])
def modificar_europa_aula(id):
    eliminatoria = request.form['eliminatoria']
    num_partidos = int(request.form['num_partidos'])
    cur = mysql.connection.cursor()
    # Actualizar la jornada
    cur.execute('UPDATE europa_aula SET eliminatoria = %s WHERE id = %s', (eliminatoria, id))
    # Actualizar los partidos de la jornada
    for i in range(num_partidos):
        partido_id = request.form.get(f'partido_id{i}')
        fecha = request.form.get(f'fecha{i}')
        hora = request.form.get(f'hora{i}')
        local = request.form.get(f'local{i}')
        resultadoA = request.form.get(f'resultadoA{i}')
        resultadoB = request.form.get(f'resultadoB{i}')
        visitante = request.form.get(f'visitante{i}')
        # Verificar que los campos obligatorios tienen valores válidos
        if all([partido_id, local, visitante]):
        # Asignar valores predeterminados si los campos opcionales están vacíos
            if fecha is None:
                fecha = ''
            if hora is None:
                hora = ''
            if local is None:
                local = ''
            if resultadoA is None:
                resultadoA = ''
            if resultadoB is None:
                resultadoB = ''
            if visitante is None:
                visitante = ''
        # Verificar que todos los campos están presentes
        cur.execute('UPDATE europa_aula SET fecha = %s, hora = %s, local = %s, resultadoA = %s, resultadoB = %s, visitante = %s WHERE id = %s',
            (fecha, hora, local, resultadoA, resultadoB, visitante, partido_id))
    mysql.connection.commit()
    cur.close()       
    # Redireccionar a la página de visualización de copa
    return redirect(url_for('ver_europa_aula')) 
# Ruta para eliminar las eliminatorias
@app.route('/eliminar_europa_aula/<string:eliminatoria>', methods=['POST'])
def eliminar_europa_aula(eliminatoria):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM europa_aula WHERE eliminatoria = %s', [eliminatoria])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('ver_europa_aula'))
# Ruta para mostrar la Europa Aula
@app.route('/euro_aula/')
def euro_aula():
    # Obtener datos de las eliminatorias
    cursor = mysql.connection.cursor()
    eliminatorias = ['segunda', 'tercera', 'octavos', 'cuartos', 'semifinales', 'final']
    datos_europa = {}
    for eliminatoria in eliminatorias:
        cursor.execute("SELECT * FROM europa_aula WHERE eliminatoria = %s", [eliminatoria])
        partidos = cursor.fetchall()
        datos_europa[eliminatoria] = partidos
    cursor.close()
    return render_template('europa/aula_europa.html', datos_europa=datos_europa)
# Fin Europa Aula Valladolid

# Europa VRAC
# Crear formulario para Copa Iberica VRAC
@app.route('/admin/crear_europa_vrac', methods=['GET', 'POST'])
def crear_europa_vrac():
    if request.method == 'POST':
        eliminatoria = request.form.get('eliminatoria')       
        # Determinar el máximo de partidos permitidos para la eliminatoria
        max_partidos = {
            'final': 1
        }.get(eliminatoria, 0)        
        # Obtener el número de partidos del formulario
        num_partidos_str = request.form.get('num_partidos', '0').strip()
        num_partidos = int(num_partidos_str) if num_partidos_str else 0        
        # Validar el número de partidos
        if num_partidos < 0 or num_partidos > max_partidos:
            return "Número de partidos no válido"                
        # Crear un cursor para ejecutar consultas SQL
        cur = mysql.connection.cursor()
        # Iterar sobre los datos del formulario para insertar los partidos
        for i in range(num_partidos):
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            local = request.form.get(f'local{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            visitante = request.form.get(f'visitante{i}')          
            # Verificar si algún campo es None y asignar valores por defecto
            if fecha is None:
                fecha = ''
            if hora is None:
                hora = ''
            if local is None:
                local = ''
            if resultadoA is None:
                resultadoA = ''
            if resultadoB is None:
                resultadoB = ''
            if visitante is None:
                visitante = ''           
            # Insertar el partido en la tabla copa_recoletas
            cur.execute("""
                INSERT INTO europa_vrac (eliminatoria, fecha, hora, local, resultadoA, resultadoB, visitante)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (eliminatoria, fecha, hora, local, resultadoA, resultadoB, visitante))       
        # Confirmar los cambios en la base de datos
        mysql.connection.commit()        
        # Cerrar el cursor
        cur.close()        
        # Redireccionar a la vista de la copa_recoletas
        return redirect(url_for('ver_europa_vrac'))
    # Renderizar el formulario para crear la copa_recoletas
    return render_template('admin/europa_vrac.html')
# Crear formulario para EHF Aula Valladolid
@app.route('/admin/europa_vrac/')
def ver_europa_vrac():
    cursor = mysql.connection.cursor()
    eliminatorias = ['final']
    datos_eliminatorias = {}
    for eliminatoria in eliminatorias:
        cursor.execute("SELECT * FROM europa_vrac WHERE eliminatoria = %s", [eliminatoria])
        partidos = cursor.fetchall()
        datos_eliminatorias[eliminatoria] = partidos
    cursor.close()
    return render_template('admin/europa_vrac.html', datos_eliminatorias=datos_eliminatorias)
# Modificar los partidos de EHF Aula Valladolid
@app.route('/modificar_europa_vrac/<string:id>', methods=['GET', 'POST'])
def modificar_europa_vrac(id):
    eliminatoria = request.form['eliminatoria']
    num_partidos = int(request.form['num_partidos'])
    cur = mysql.connection.cursor()
    # Actualizar la jornada
    cur.execute('UPDATE europa_vrac SET eliminatoria = %s WHERE id = %s', (eliminatoria, id))
    # Actualizar los partidos de la jornada
    for i in range(num_partidos):
        partido_id = request.form.get(f'partido_id{i}')
        fecha = request.form.get(f'fecha{i}')
        hora = request.form.get(f'hora{i}')
        local = request.form.get(f'local{i}')
        resultadoA = request.form.get(f'resultadoA{i}')
        resultadoB = request.form.get(f'resultadoB{i}')
        visitante = request.form.get(f'visitante{i}')
        # Verificar que los campos obligatorios tienen valores válidos
        if all([partido_id, local, visitante]):
        # Asignar valores predeterminados si los campos opcionales están vacíos
            if fecha is None:
                fecha = ''
            if hora is None:
                hora = ''
            if local is None:
                local = ''
            if resultadoA is None:
                resultadoA = ''
            if resultadoB is None:
                resultadoB = ''
            if visitante is None:
                visitante = ''
        # Verificar que todos los campos están presentes
        cur.execute('UPDATE europa_vrac SET fecha = %s, hora = %s, local = %s, resultadoA = %s, resultadoB = %s, visitante = %s WHERE id = %s',
            (fecha, hora, local, resultadoA, resultadoB, visitante, partido_id))
    mysql.connection.commit()
    cur.close()       
    # Redireccionar a la página de visualización de copa
    return redirect(url_for('ver_europa_vrac'))
# Ruta para eliminar las eliminatorias
@app.route('/eliminar_europa_vrac/<string:eliminatoria>', methods=['POST'])
def eliminar_europa_vrac(eliminatoria):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM europa_vrac WHERE eliminatoria = %s', [eliminatoria])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('ver_europa_vrac'))
# Ruta para mostrar la Copa Iberica VRAC
@app.route('/euro_vrac/')
def euro_vrac():
    # Obtener datos de las eliminatorias
    cursor = mysql.connection.cursor()
    eliminatorias = ['final']
    datos_europa = {}
    for eliminatoria in eliminatorias:
        cursor.execute("SELECT * FROM europa_vrac WHERE eliminatoria = %s", [eliminatoria])
        partidos = cursor.fetchall()
        datos_europa[eliminatoria] = partidos
    cursor.close()
    return render_template('europa/vrac_europa.html', datos_europa=datos_europa)
# Fin Europa VRAC

# Europa CR El Salvador
# Crear formulario para Copa Iberica CR El Salvador
@app.route('/admin/crear_europa_salvador', methods=['GET', 'POST'])
def crear_europa_salvador():
    if request.method == 'POST':
        eliminatoria = request.form.get('eliminatoria')       
        # Determinar el máximo de partidos permitidos para la eliminatoria
        max_partidos = {
            'final': 1
        }.get(eliminatoria, 0)        
        # Obtener el número de partidos del formulario
        num_partidos_str = request.form.get('num_partidos', '0').strip()
        num_partidos = int(num_partidos_str) if num_partidos_str else 0        
        # Validar el número de partidos
        if num_partidos < 0 or num_partidos > max_partidos:
            return "Número de partidos no válido"                
        # Crear un cursor para ejecutar consultas SQL
        cur = mysql.connection.cursor()
        # Iterar sobre los datos del formulario para insertar los partidos
        for i in range(num_partidos):
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            local = request.form.get(f'local{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            visitante = request.form.get(f'visitante{i}')          
            # Verificar si algún campo es None y asignar valores por defecto
            if fecha is None:
                fecha = ''
            if hora is None:
                hora = ''
            if local is None:
                local = ''
            if resultadoA is None:
                resultadoA = ''
            if resultadoB is None:
                resultadoB = ''
            if visitante is None:
                visitante = ''           
            # Insertar el partido en la tabla copa_recoletas
            cur.execute("""
                INSERT INTO europa_salvador (eliminatoria, fecha, hora, local, resultadoA, resultadoB, visitante)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (eliminatoria, fecha, hora, local, resultadoA, resultadoB, visitante))       
        # Confirmar los cambios en la base de datos
        mysql.connection.commit()        
        # Cerrar el cursor
        cur.close()        
        # Redireccionar a la vista de la copa_recoletas
        return redirect(url_for('ver_europa_salvador'))
    # Si no es una solicitud POST, renderizar el formulario
    return render_template('admin/europa_salvador.html')
# Crear formulario para Copa Ibérica CR El Salvador
@app.route('/admin/europa_salvador/')
def ver_europa_salvador():
    cursor = mysql.connection.cursor()
    eliminatorias = ['final']
    datos_eliminatorias = {}
    for eliminatoria in eliminatorias:
        cursor.execute("SELECT * FROM europa_salvador WHERE eliminatoria = %s", [eliminatoria])
        partidos = cursor.fetchall()
        datos_eliminatorias[eliminatoria] = partidos
    cursor.close()
    return render_template('admin/europa_salvador.html', datos_eliminatorias=datos_eliminatorias)
# Modificar los partidos de EHF Aula Valladolid
@app.route('/modificar_europa_salvador/<string:id>', methods=['GET', 'POST'])
def modificar_europa_salvador(id):
    eliminatoria = request.form['eliminatoria']
    num_partidos = int(request.form['num_partidos'])
    cur = mysql.connection.cursor()
    # Actualizar la jornada
    cur.execute('UPDATE europa_salvador SET eliminatoria = %s WHERE id = %s', (eliminatoria, id))
    # Actualizar los partidos de la jornada
    for i in range(num_partidos):
        partido_id = request.form.get(f'partido_id{i}')
        fecha = request.form.get(f'fecha{i}')
        hora = request.form.get(f'hora{i}')
        local = request.form.get(f'local{i}')
        resultadoA = request.form.get(f'resultadoA{i}')
        resultadoB = request.form.get(f'resultadoB{i}')
        visitante = request.form.get(f'visitante{i}')
        # Verificar que los campos obligatorios tienen valores válidos
        if all([partido_id, local, visitante]):
        # Asignar valores predeterminados si los campos opcionales están vacíos
            if fecha is None:
                fecha = ''
            if hora is None:
                hora = ''
            if local is None:
                local = ''
            if resultadoA is None:
                resultadoA = ''
            if resultadoB is None:
                resultadoB = ''
            if visitante is None:
                visitante = ''
        # Verificar que todos los campos están presentes
        cur.execute('UPDATE europa_salvador SET fecha = %s, hora = %s, local = %s, resultadoA = %s, resultadoB = %s, visitante = %s WHERE id = %s',
            (fecha, hora, local, resultadoA, resultadoB, visitante, partido_id))
    mysql.connection.commit()
    cur.close()       
    # Redireccionar a la página de visualización de copa
    return redirect(url_for('ver_europa_salvador'))
# Ruta para eliminar las eliminatorias
@app.route('/eliminar_europa_salvador/<string:eliminatoria>', methods=['POST'])
def eliminar_europa_salvador(eliminatoria):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM europa_salvador WHERE eliminatoria = %s', [eliminatoria])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('ver_europa_salvador'))
# Ruta para mostrar la Copa Iberica CR El Salvador
@app.route('/euro_salvador/')
def euro_salvador():
    # Obtener datos de las eliminatorias
    cursor = mysql.connection.cursor()
    eliminatorias = ['final']
    datos_europa = {}
    for eliminatoria in eliminatorias:
        cursor.execute("SELECT * FROM europa_salvador WHERE eliminatoria = %s", [eliminatoria])
        partidos = cursor.fetchall()
        datos_europa[eliminatoria] = partidos
    cursor.close()
    return render_template('europa/salvador_europa.html', datos_europa=datos_europa)
# Fin Europa CR El Salvador

# Europa CR El Salvador Fem.
# Crear formulario para Copa Iberica CR El Salvador Fem.
@app.route('/admin/crear_europa_salvador_fem', methods=['GET', 'POST'])
def crear_europa_salvador_fem():
    if request.method == 'POST':
        eliminatoria = request.form.get('eliminatoria')       
        # Determinar el máximo de partidos permitidos para la eliminatoria
        max_partidos = {
            'final': 1
        }.get(eliminatoria, 0)        
        # Obtener el número de partidos del formulario
        num_partidos_str = request.form.get('num_partidos', '0').strip()
        num_partidos = int(num_partidos_str) if num_partidos_str else 0        
        # Validar el número de partidos
        if num_partidos < 0 or num_partidos > max_partidos:
            return "Número de partidos no válido"                
        # Crear un cursor para ejecutar consultas SQL
        cur = mysql.connection.cursor()
        # Iterar sobre los datos del formulario para insertar los partidos
        for i in range(num_partidos):
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            local = request.form.get(f'local{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            visitante = request.form.get(f'visitante{i}')          
            # Verificar si algún campo es None y asignar valores por defecto
            if fecha is None:
                fecha = ''
            if hora is None:
                hora = ''
            if local is None:
                local = ''
            if resultadoA is None:
                resultadoA = ''
            if resultadoB is None:
                resultadoB = ''
            if visitante is None:
                visitante = ''           
            # Insertar el partido en la tabla copa_recoletas
            cur.execute("""
                INSERT INTO europa_salvador_fem (eliminatoria, fecha, hora, local, resultadoA, resultadoB, visitante)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (eliminatoria, fecha, hora, local, resultadoA, resultadoB, visitante))       
        # Confirmar los cambios en la base de datos
        mysql.connection.commit()        
        # Cerrar el cursor
        cur.close()        
        # Redireccionar a la vista de la copa_recoletas
        return redirect(url_for('ver_europa_salvador_fem'))
    # Si no es una solicitud POST, renderizar el formulario
    return render_template('admin/europa_salvador_fem.html')
# Crear formulario para Copa Ibérica CR El Salvador Fem.
@app.route('/admin/europa_salvador_fem/')
def ver_europa_salvador_fem():
    cursor = mysql.connection.cursor()
    eliminatorias = ['final']
    datos_eliminatorias = {}
    for eliminatoria in eliminatorias:
        cursor.execute("SELECT * FROM europa_salvador_fem WHERE eliminatoria = %s", [eliminatoria])
        partidos = cursor.fetchall()
        datos_eliminatorias[eliminatoria] = partidos
    cursor.close()
    return render_template('admin/europa_salvador_fem.html', datos_eliminatorias=datos_eliminatorias)
# Modificar los partidos de Copa Ibérica CR El Salvador Fem.
@app.route('/modificar_europa_salvador_fem/<string:id>', methods=['GET', 'POST'])
def modificar_europa_salvador_fem(id):
    eliminatoria = request.form['eliminatoria']
    num_partidos = int(request.form['num_partidos'])
    cur = mysql.connection.cursor()
    # Actualizar la jornada
    cur.execute('UPDATE europa_salvador_fem SET eliminatoria = %s WHERE id = %s', (eliminatoria, id))
    # Actualizar los partidos de la jornada
    for i in range(num_partidos):
        partido_id = request.form.get(f'partido_id{i}')
        fecha = request.form.get(f'fecha{i}')
        hora = request.form.get(f'hora{i}')
        local = request.form.get(f'local{i}')
        resultadoA = request.form.get(f'resultadoA{i}')
        resultadoB = request.form.get(f'resultadoB{i}')
        visitante = request.form.get(f'visitante{i}')
        # Verificar que los campos obligatorios tienen valores válidos
        if all([partido_id, local, visitante]):
        # Asignar valores predeterminados si los campos opcionales están vacíos
            if fecha is None:
                fecha = ''
            if hora is None:
                hora = ''
            if local is None:
                local = ''
            if resultadoA is None:
                resultadoA = ''
            if resultadoB is None:
                resultadoB = ''
            if visitante is None:
                visitante = ''
        # Verificar que todos los campos están presentes
        cur.execute('UPDATE europa_salvador_fem SET fecha = %s, hora = %s, local = %s, resultadoA = %s, resultadoB = %s, visitante = %s WHERE id = %s',
            (fecha, hora, local, resultadoA, resultadoB, visitante, partido_id))
    mysql.connection.commit()
    cur.close()       
    # Redireccionar a la página de visualización de copa
    return redirect(url_for('ver_europa_salvador_fem')) 
# Ruta para eliminar las eliminatorias
@app.route('/eliminar_europa_salvador_fem/<string:eliminatoria>', methods=['POST'])
def eliminar_europa_salvador_fem(eliminatoria):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM europa_salvador_fem WHERE eliminatoria = %s', [eliminatoria])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('ver_europa_salvador_fem'))
# Ruta para mostrar la Copa Iberica CR El Salvador Fem.
@app.route('/euro_salvador_fem/')
def euro_salvador_fem():
    # Obtener datos de las eliminatorias
    cursor = mysql.connection.cursor()
    eliminatorias = ['final']
    datos_europa = {}
    for eliminatoria in eliminatorias:
        cursor.execute("SELECT * FROM europa_salvador_fem WHERE eliminatoria = %s", [eliminatoria])
        partidos = cursor.fetchall()
        datos_europa[eliminatoria] = partidos
    cursor.close()
    return render_template('europa/salvador_fem_europa.html', datos_europa=datos_europa)
# Fin Europa CR El Salvador Fem.

# Europa CPLV Caja Rural
# Crear formulario para los grupos del playoff Caja Rural
@app.route('/admin/crear_europa_caja', methods=['GET', 'POST'])
def crear_europa_caja():
    if request.method == 'POST':
        encuentros = request.form.get('encuentros')
        print(f"Encuentros: {encuentros}")
        num_partidos = int(request.form.get('num_partidos', 0))
        cur = mysql.connection.cursor()
        for i in range(num_partidos):
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            local = request.form.get(f'local{i}')
            bonus_local = request.form.get(f'bonusA{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            bonus_visitante = request.form.get(f'bonusB{i}')
            visitante = request.form.get(f'visitante{i}')
            # Verificar si algún campo es None y asignar valores por defecto
            if fecha is None:
                fecha = ''
            if hora is None:
                hora = ''
            if local is None:
                local = ''
            if bonus_local is None:
                bonus_local = ''    
            if resultadoA is None:
                resultadoA = ''
            if resultadoB is None:
                resultadoB = ''
            if bonus_visitante is None:
                bonus_visitante = ''    
            if visitante is None:
                visitante = ''
            if encuentros is None:
                encuentros = '' 
            cur.execute("""
                INSERT INTO europa_caja (encuentros, fecha, hora, local, bonusA, resultadoA, resultadoB, bonusB, visitante)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (encuentros, fecha, hora, local, bonus_local, resultadoA, resultadoB, bonus_visitante, visitante))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('ver_europa_caja'))
    # Renderizar el formulario para crear la Cops Europa Caja
    return render_template('admin/crear_europa_caja.html')
# Actualizar clasificación de los grupos
def actualizar_clasificacion_caja(clasificacion_por_grupo_caja, local, bonus_local ,resultado_local, resultado_visitante, bonus_visitante, visitante):
    resultado_local = int(resultado_local) if resultado_local.isdigit() else None
    resultado_visitante = int(resultado_visitante) if resultado_visitante.isdigit() else None
    # Asegurarse de que cada grupo tenga una entrada en la clasificación
    if grupo not in clasificacion_por_grupo_caja:
        clasificacion_por_grupo_caja[grupo] = {}
    if local not in clasificacion_por_grupo_caja[grupo]:
        clasificacion_por_grupo_caja[grupo][local] = {'nombre': local, 'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0,'puntos': 0, 'bonus': 0}
    if visitante not in clasificacion_por_grupo_caja[grupo]:
        clasificacion_por_grupo_caja[grupo][visitante] = {'nombre': visitante, 'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'puntos': 0, 'bonus': 0}
    # Actualizar los partidos jugados
    if resultado_local is not None and resultado_visitante is not None:
        clasificacion_por_grupo_caja[grupo][local]['jugados'] += 1
        clasificacion_por_grupo_caja[grupo][visitante]['jugados'] += 1
        # Determinar el resultado del partido
        if resultado_local > resultado_visitante:
            clasificacion_por_grupo_caja[grupo][local]['ganados'] += 1
            clasificacion_por_grupo_caja[grupo][local]['puntos'] += 3
            clasificacion_por_grupo_caja[grupo][visitante]['perdidos'] += 1
            clasificacion_por_grupo_caja[grupo][visitante]['puntos'] += 0
        elif resultado_local < resultado_visitante:
            clasificacion_por_grupo_caja[grupo][visitante]['ganados'] += 1
            clasificacion_por_grupo_caja[grupo][visitante]['puntos'] += 3
            clasificacion_por_grupo_caja[grupo][local]['perdidos'] += 1
            clasificacion_por_grupo_caja[grupo][local]['puntos'] += 0
        elif resultado_local == resultado_visitante:
            clasificacion_por_grupo_caja[grupo][visitante]['empatados'] += 1
            clasificacion_por_grupo_caja[grupo][visitante]['puntos'] += 1 + bonus_visitante
            clasificacion_por_grupo_caja[grupo][local]['empatados'] += 1
            clasificacion_por_grupo_caja[grupo][local]['puntos'] += 1 + bonus_local   
        clasificaciones_caja[grupo][local]['bonus'] += bonus_local
        clasificaciones_caja[grupo][visitante]['bonus'] += bonus_visitante 
    return clasificacion_por_grupo_caja
# Recalcular clasificación
def recalcular_clasificaciones_caja(partidos):
    clasificaciones_caja = {}
    enfrentamientos_directos_caja = {}
    for partido in partidos:
        grupo = partido.get('encuentros')
        local = partido['local']
        visitante = partido['visitante']
        resultado_local = int(partido['resultadoA']) if partido['resultadoA'].isdigit() else None
        resultado_visitante = int(partido['resultadoB']) if partido['resultadoB'].isdigit() else None
        bonus_local = int(partido['bonusA']) if partido['bonusA'].isdigit() else None
        bonus_visitante = int(partido['bonusB']) if partido['bonusB'].isdigit() else None
        if grupo not in clasificaciones_caja:
            clasificaciones_caja[grupo] = {}
        # Inicializar equipos si no existen
        if local not in clasificaciones_caja[grupo]:
            clasificaciones_caja[grupo][local] = {'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'puntos': 0, 'bonus': 0}
        if visitante not in clasificaciones_caja[grupo]:
            clasificaciones_caja[grupo][visitante] = {'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'puntos': 0, 'bonus': 0}
        # Actualizar estadísticas de partidos
        if resultado_local is not None and resultado_visitante is not None:
            clasificaciones_caja[grupo][local]['jugados'] += 1
            clasificaciones_caja[grupo][visitante]['jugados'] += 1
            if resultado_local > resultado_visitante:
                clasificaciones_caja[grupo][local]['ganados'] += 1
                clasificaciones_caja[grupo][local]['puntos'] += 3
                clasificaciones_caja[grupo][visitante]['perdidos'] += 1
                clasificaciones_caja[grupo][visitante]['puntos'] += 0
            elif resultado_local < resultado_visitante:
                clasificaciones_caja[grupo][visitante]['ganados'] += 1
                clasificaciones_caja[grupo][visitante]['puntos'] += 3
                clasificaciones_caja[grupo][local]['perdidos'] += 1
                clasificaciones_caja[grupo][local]['puntos'] += 0
            elif resultado_local == resultado_visitante:
                clasificaciones_caja[grupo][visitante]['empatados'] += 1
                clasificaciones_caja[grupo][visitante]['puntos'] += 1 + bonus_visitante
                clasificaciones_caja[grupo][local]['empatados'] += 1 
                clasificaciones_caja[grupo][local]['puntos'] += 1 + bonus_local  
            
            clasificaciones_caja[grupo][local]['bonus'] += bonus_local
            clasificaciones_caja[grupo][visitante]['bonus'] += bonus_visitante 

        # Almacenar el resultado del enfrentamiento directo
        if local not in enfrentamientos_directos_caja:
            enfrentamientos_directos_caja[local] = {}
        if visitante not in enfrentamientos_directos_caja:
            enfrentamientos_directos_caja[visitante] = {}
        if resultado_local is not None and resultado_visitante is not None:
            enfrentamientos_directos_caja[local][visitante] = resultado_local - resultado_visitante
            enfrentamientos_directos_caja[visitante][local] = resultado_visitante - resultado_local        
    return clasificaciones_caja, enfrentamientos_directos_caja
# Función para obtener equipos desde la base de datos
def obtener_equipos_desde_bd_caja():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, encuentros, fecha, hora, local, bonusA, resultadoA, resultadoB, bonusB, visitante FROM europa_caja")
    partidos = cur.fetchall()
    cur.close()
    # Definir los grupos y fases de eliminatorias
    grupos_caja = {'grupoA', 'grupoB'}
    fases_eliminatorias_caja = {'semifinales', 'final'}
    equipos_por_encuentros_caja = {}
    eliminatorias_caja = {'semifinales': {'partidos': []}, 'final': {'partidos': []}}
    for partido in partidos:
        grupo_o_fase = partido.get('encuentros')
        if grupo_o_fase in fases_eliminatorias_caja:
            # Añadir partidos a la fase de eliminación correspondiente
            eliminatorias_caja[grupo_o_fase]['partidos'].append(partido)
        elif grupo_o_fase in grupos_caja:
            # Añadir equipos y partidos a los grupos
            if grupo_o_fase not in equipos_por_encuentros_caja:
                equipos_por_encuentros_caja[grupo_o_fase] = {'equipos': [], 'partidos': []}
            local = {'nombre': partido['local'], 'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'puntos': 0, 'bonus': 0}
            visitante = {'nombre': partido['visitante'], 'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'puntos': 0, 'bonus': 0}
            # Añadir equipos si no existen en la lista de equipos del grupo
            if not any(e['nombre'] == local['nombre'] for e in equipos_por_encuentros_caja[grupo_o_fase]['equipos']):
                equipos_por_encuentros_caja[grupo_o_fase]['equipos'].append(local)
            if not any(e['nombre'] == visitante['nombre'] for e in equipos_por_encuentros_caja[grupo_o_fase]['equipos']):
                equipos_por_encuentros_caja[grupo_o_fase]['equipos'].append(visitante)
            equipos_por_encuentros_caja[grupo_o_fase]['partidos'].append(partido)
        else:
            print(f"Grupo o fase no reconocido: {grupo_o_fase}")
    return equipos_por_encuentros_caja, eliminatorias_caja
#Obtener equipos Copa Europa CPLV Caja Rural
def obtener_equipos_por_encuentros_caja(partidos):
    equipos_por_encuentros_caja = {}
    eliminatorias_caja = {'semifinales': {'partidos': []}, 'final': {'partidos': []}}
    # Clasificar partidos en grupos o eliminatorias
    for partido in partidos:
        grupo_o_fase = partido.get('encuentros')
        if grupo_o_fase in eliminatorias_caja:
            eliminatorias_caja[grupo_o_fase]['partidos'].append(partido)
        else:
            if grupo_o_fase not in equipos_por_encuentros_caja:
                equipos_por_encuentros_caja[grupo_o_fase] = {'equipos': [], 'partidos': []}
            # Añadir equipos si no existen en la lista de equipos del grupo
            local = {'nombre': partido['local'], 'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'puntos': 0, 'bonus': 0}
            visitante = {'nombre': partido['visitante'], 'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'puntos': 0, 'bonus':0}
            if not any(e['nombre'] == local['nombre'] for e in equipos_por_encuentros_caja[grupo_o_fase]['equipos']):
                equipos_por_encuentros_caja[grupo_o_fase]['equipos'].append(local)
            if not any(e['nombre'] == visitante['nombre'] for e in equipos_por_encuentros_caja[grupo_o_fase]['equipos']):
                equipos_por_encuentros_caja[grupo_o_fase]['equipos'].append(visitante)
            equipos_por_encuentros_caja[grupo_o_fase]['partidos'].append(partido)
    return equipos_por_encuentros_caja, eliminatorias_caja
# Obtener la información de la tabla europa_caja
def obtener_europa_caja():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, encuentros, fecha, hora, local, bonusA, resultadoA, resultadoB, bonusB, visitante FROM europa_caja")
    partidos = cur.fetchall()
    cur.close()
    print("Partidos desde la BD:", partidos)  # Añadir esta línea para depuración
    return partidos
# Formatear partidos por grupo
def formatear_partidos_por_encuentros_caja(partidos):
    encuentros_caja = {
        'grupoA': {'id': 1, 'encuentros': 'grupoA', 'partidos': []},
        'grupoB': {'id': 2, 'encuentros': 'grupoB', 'partidos': []},
        'semifinales': {'id': 3, 'encuentros': 'semifinales', 'partidos': []},
        'final': {'id': 4, 'encuentros': 'final', 'partidos': []}
    }
    for partido in partidos:
        grupo = partido.get('encuentros', '')
        if grupo in encuentros_caja:
            encuentros_caja[grupo]['partidos'].append(partido)
        else:
            print(f"Grupo no encontrado: {grupo}")            
    return encuentros_caja
# Crear formulario para los grupos y eliminatorias caja
@app.route('/admin/europa_caja/')
def ver_europa_caja():
    try:
        # Obtener todos los partidos de los Playoff caja
        partidos = obtener_europa_caja()
        # Formatear los partidos por grupos y eliminatorias
        dats7 = formatear_partidos_por_encuentros_caja(partidos)
        # Imprimir para depuración
        print(dats7)
        # Renderizar la plantilla con los datos formateados
        return render_template('admin/europa_caja.html', dats7=dats7)
    except Exception as e:
        print(f"Error al obtener o formatear los datos de Copa Europa caja: {e}")
        # Renderizar una plantilla de error o manejar el error de alguna manera
        return render_template('error.html')
# Modificar los partidos de los playoff
@app.route('/modificar_europa_caja/<int:id>', methods=['POST'])
def modificar_europa_caja(id):
    if request.method == 'POST':
        encuentros = request.form.get('encuentros')
        num_partidos = int(request.form.get('num_partidos', 0))
        try:
            cur = mysql.connection.cursor()
            # Actualizar la eliminatoria de la jornada
            cur.execute('UPDATE europa_caja SET encuentros = %s WHERE id = %s', (encuentros, id))
            print(f"Consulta para actualizar la eliminatoria ejecutada para id {id}")
            # Actualizar los detalles de cada partido
            for i in range(num_partidos):
                partido_id = request.form.get(f'partido_id{i}')
                fecha = request.form.get(f'fecha{i}')
                hora = request.form.get(f'hora{i}')
                local = request.form.get(f'local{i}')
                bonusA = request.form.get(f'bonusA{i}')
                resultadoA = request.form.get(f'resultadoA{i}')
                resultadoB = request.form.get(f'resultadoB{i}')
                bonusB = request.form.get(f'bonusB{i}')
                visitante = request.form.get(f'visitante{i}')
                # Verificar que los campos obligatorios tienen valores válidos
                if all([partido_id, local, visitante]):
                    # Asignar valores predeterminados si los campos opcionales están vacíos
                    if fecha is None:
                        fecha = ''
                    if hora is None:
                        hora = ''
                    if local is None:
                        local = ''
                    if bonusA is None:
                        bonusA = ''    
                    if resultadoA is None:
                        resultadoA = ''
                    if resultadoB is None:
                        resultadoB = ''
                    if bonusB is None:
                        bonusB = ''    
                    if visitante is None:
                        visitante = ''
                    # Actualizar el partido en la base de datos
                    cur.execute('UPDATE europa_caja SET fecha = %s, hora = %s, local = %s, bonusA = %s, resultadoA = %s, resultadoB = %s, bonusB = %s, visitante = %s WHERE id = %s',
                                (fecha, hora, local, bonusA, resultadoA, resultadoB, bonusB, visitante, partido_id))
                    print(f"Consulta para actualizar el partido ejecutada para id {partido_id}")
            # Commit de la transacción
            mysql.connection.commit()
        except MySQLdb.Error as e:
            print(f"Error en la base de datos: {e}")
            mysql.connection.rollback()  # Revertir cambios en caso de error
        finally:
            if 'cur' in locals() and cur:
                cur.close()  # Cerrar cursor
        return redirect(url_for('ver_europa_caja'))
    return render_template('tu_template.html')
#Eliminar partidos Copa Europa CPLV Caja Rural
@app.route('/eliminar_europa_caja/<string:identificador>', methods=['POST'])
def eliminar_europa_caja(identificador):
    cur = mysql.connection.cursor()
    try:
        if identificador.startswith('grupo') or identificador in ['finalA', 'finalB']:
            cur.execute('DELETE FROM europa_caja WHERE encuentros = %s', [identificador])
            mysql.connection.commit()
            flash('Partidos eliminados correctamente', 'success')
        else:
            flash('Identificador de encuentros no válido', 'error')
    except Exception as e:
        flash(f'Error al eliminar partidos: {str(e)}', 'error')
    finally:
        cur.close()
    return redirect(url_for('ver_europa_caja'))
# Ruta para mostrar la Copa Europa CPLV Caja Rural
@app.route('/euro_caja/')
def europa_caja():
    partidos = obtener_europa_caja()
    equipos_por_encuentros, eliminatorias = obtener_equipos_por_encuentros_caja(partidos)
    clasificaciones, enfrentamientos_directos = recalcular_clasificaciones_caja(partidos)
    # Convertir clasificaciones a una estructura adecuada para la vista
    data_clasificaciones = {}
    for grupo, equipos in clasificaciones.items():
        # Ordenar equipos primero por puntos, luego por victorias, derrotas, y partidos jugados
        equipos_ordenados = sorted(equipos.items(), key=lambda item: (-item[1]['puntos'], item[1]['ganados'], item[1]['perdidos'], -item[1]['jugados']))      
        # Aplicar el criterio de desempate basado en enfrentamientos directos
        def criterio_enfrentamientos_directos(equipo1, equipo2):
            if equipo1 in enfrentamientos_directos and equipo2 in enfrentamientos_directos[equipo1]:
                resultado_directo = enfrentamientos_directos[equipo1][equipo2]
                return resultado_directo  # Resultado positivo indica que equipo1 ganó
            return 0
        # Crear una lista ordenada usando el criterio de desempate de enfrentamientos directos
        equipos_ordenados = sorted(equipos_ordenados, key=lambda item: (
            -item[1]['puntos'], 
            item[1]['ganados'], 
            item[1]['perdidos'], 
            -item[1]['jugados'],
            -criterio_enfrentamientos_directos(item[0], item[0])
        ))
        # Ajustar el orden para el desempate directo
        for i in range(len(equipos_ordenados)):
            for j in range(i + 1, len(equipos_ordenados)):
                equipo_a, stats_a = equipos_ordenados[i]
                equipo_b, stats_b = equipos_ordenados[j]
                if stats_a['puntos'] == stats_b['puntos'] and stats_a['ganados'] == stats_b['ganados'] and stats_a['perdidos'] == stats_b['perdidos']:
                    resultado_directo = criterio_enfrentamientos_directos(equipo_a, equipo_b)
                    if resultado_directo > 0:  # equipo_a ganó el enfrentamiento directo
                        # Intercambiar posiciones para que equipo_a quede por encima de equipo_b
                        equipos_ordenados[i], equipos_ordenados[j] = equipos_ordenados[j], equipos_ordenados[i]
                    elif resultado_directo < 0:  # equipo_b ganó el enfrentamiento directo
                        # Intercambiar posiciones para que equipo_b quede por encima de equipo_a
                        equipos_ordenados[i], equipos_ordenados[j] = equipos_ordenados[j], equipos_ordenados[i]
        data_clasificaciones[grupo] = equipos_ordenados
    return render_template('europa/caja_europa.html', equipos_por_encuentros=equipos_por_encuentros, eliminatorias=eliminatorias, clasificaciones=data_clasificaciones)
# Fin Copa Europa CPLV Caja Rural

# Europa CPLV Munia Panteras
# Crear formulario para los grupos del playoff panteras
@app.route('/admin/crear_europa_panteras', methods=['GET', 'POST'])
def crear_europa_panteras():
    if request.method == 'POST':
        encuentros = request.form.get('encuentros')
        print(f"Encuentros: {encuentros}")
        num_partidos = int(request.form.get('num_partidos', 0))
        cur = mysql.connection.cursor()
        for i in range(num_partidos):
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            local = request.form.get(f'local{i}')
            bonus_local = request.form.get(f'bonusA{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            bonus_visitante = request.form.get(f'bonusB{i}')
            visitante = request.form.get(f'visitante{i}')
            # Verificar si algún campo es None y asignar valores por defecto
            if fecha is None:
                fecha = ''
            if hora is None:
                hora = ''
            if local is None:
                local = ''
            if bonus_local is None:
                bonus_local = ''    
            if resultadoA is None:
                resultadoA = ''
            if resultadoB is None:
                resultadoB = ''
            if bonus_visitante is None:
                bonus_visitante = ''    
            if visitante is None:
                visitante = ''
            if encuentros is None:
                encuentros = '' 
            cur.execute("""
                INSERT INTO europa_panteras (encuentros, fecha, hora, local, bonusA, resultadoA, resultadoB, bonusB, visitante)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (encuentros, fecha, hora, local, bonus_local, resultadoA, resultadoB, bonus_visitante, visitante))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('ver_europa_panteras'))
    # Renderizar el formulario para crear la copa UEMC
    return render_template('admin/crear_europa_panteras.html')
# Actualizar clasificación de los grupos
def actualizar_clasificacion_panteras(clasificacion_por_grupo_panteras, local, bonus_local ,resultado_local, resultado_visitante, bonus_visitante, visitante):
    resultado_local = int(resultado_local) if resultado_local.isdigit() else None
    resultado_visitante = int(resultado_visitante) if resultado_visitante.isdigit() else None
    # Asegurarse de que cada grupo tenga una entrada en la clasificación
    if grupo not in clasificacion_por_grupo_panteras:
        clasificacion_por_grupo_panteras[grupo] = {}
    if local not in clasificacion_por_grupo_panteras[grupo]:
        clasificacion_por_grupo_panteras[grupo][local] = {'nombre': local, 'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0,'puntos': 0, 'bonus': 0}
    if visitante not in clasificacion_por_grupo_panteras[grupo]:
        clasificacion_por_grupo_panteras[grupo][visitante] = {'nombre': visitante, 'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'puntos': 0, 'bonus': 0}
    # Actualizar los partidos jugados
    if resultado_local is not None and resultado_visitante is not None:
        clasificacion_por_grupo_panteras[grupo][local]['jugados'] += 1
        clasificacion_por_grupo_panteras[grupo][visitante]['jugados'] += 1
        # Determinar el resultado del partido
        if resultado_local > resultado_visitante:
            clasificacion_por_grupo_panteras[grupo][local]['ganados'] += 1
            clasificacion_por_grupo_panteras[grupo][local]['puntos'] += 3
            clasificacion_por_grupo_panteras[grupo][visitante]['perdidos'] += 1
            clasificacion_por_grupo_panteras[grupo][visitante]['puntos'] += 0
        elif resultado_local < resultado_visitante:
            clasificacion_por_grupo_panteras[grupo][visitante]['ganados'] += 1
            clasificacion_por_grupo_panteras[grupo][visitante]['puntos'] += 3
            clasificacion_por_grupo_panteras[grupo][local]['perdidos'] += 1
            clasificacion_por_grupo_panteras[grupo][local]['puntos'] += 0
        elif resultado_local == resultado_visitante:
            clasificacion_por_grupo_panteras[grupo][visitante]['empatados'] += 1
            clasificacion_por_grupo_panteras[grupo][visitante]['puntos'] += 1 + bonus_visitante
            clasificacion_por_grupo_panteras[grupo][local]['empatados'] += 1
            clasificacion_por_grupo_panteras[grupo][local]['puntos'] += 1 + bonus_local   
        clasificaciones_panteras[grupo][local]['bonus'] += bonus_local
        clasificaciones_panteras[grupo][visitante]['bonus'] += bonus_visitante 
    return clasificacion_por_grupo_panteras
# Recalcular clasificación
def recalcular_clasificaciones_panteras(partidos):
    clasificaciones_panteras = {}
    enfrentamientos_directos_panteras = {}
    for partido in partidos:
        grupo = partido.get('encuentros')
        local = partido['local']
        visitante = partido['visitante']
        resultado_local = int(partido['resultadoA']) if partido['resultadoA'].isdigit() else None
        resultado_visitante = int(partido['resultadoB']) if partido['resultadoB'].isdigit() else None
        bonus_local = int(partido['bonusA']) if partido['bonusA'].isdigit() else None
        bonus_visitante = int(partido['bonusB']) if partido['bonusB'].isdigit() else None
        if grupo not in clasificaciones_panteras:
            clasificaciones_panteras[grupo] = {}
        # Inicializar equipos si no existen
        if local not in clasificaciones_panteras[grupo]:
            clasificaciones_panteras[grupo][local] = {'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'puntos': 0, 'bonus': 0}
        if visitante not in clasificaciones_panteras[grupo]:
            clasificaciones_panteras[grupo][visitante] = {'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'puntos': 0, 'bonus': 0}
        # Actualizar estadísticas de partidos
        if resultado_local is not None and resultado_visitante is not None:
            clasificaciones_panteras[grupo][local]['jugados'] += 1
            clasificaciones_panteras[grupo][visitante]['jugados'] += 1
            if resultado_local > resultado_visitante:
                clasificaciones_panteras[grupo][local]['ganados'] += 1
                clasificaciones_panteras[grupo][local]['puntos'] += 3
                clasificaciones_panteras[grupo][visitante]['perdidos'] += 1
                clasificaciones_panteras[grupo][visitante]['puntos'] += 0
            elif resultado_local < resultado_visitante:
                clasificaciones_panteras[grupo][visitante]['ganados'] += 1
                clasificaciones_panteras[grupo][visitante]['puntos'] += 3
                clasificaciones_panteras[grupo][local]['perdidos'] += 1
                clasificaciones_panteras[grupo][local]['puntos'] += 0
            elif resultado_local == resultado_visitante:
                clasificaciones_panteras[grupo][visitante]['empatados'] += 1
                clasificaciones_panteras[grupo][visitante]['puntos'] += 1 + bonus_visitante
                clasificaciones_panteras[grupo][local]['empatados'] += 1 
                clasificaciones_panteras[grupo][local]['puntos'] += 1 + bonus_local  
            
            clasificaciones_panteras[grupo][local]['bonus'] += bonus_local
            clasificaciones_panteras[grupo][visitante]['bonus'] += bonus_visitante 

        # Almacenar el resultado del enfrentamiento directo
        if local not in enfrentamientos_directos_panteras:
            enfrentamientos_directos_panteras[local] = {}
        if visitante not in enfrentamientos_directos_panteras:
            enfrentamientos_directos_panteras[visitante] = {}
        if resultado_local is not None and resultado_visitante is not None:
            enfrentamientos_directos_panteras[local][visitante] = resultado_local - resultado_visitante
            enfrentamientos_directos_panteras[visitante][local] = resultado_visitante - resultado_local        
    return clasificaciones_panteras, enfrentamientos_directos_panteras
# Función para obtener equipos desde la base de datos
def obtener_equipos_desde_bd_panteras():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, encuentros, fecha, hora, local, bonusA, resultadoA, resultadoB, bonusB, visitante FROM europa_panteras")
    partidos = cur.fetchall()
    cur.close()
    # Definir los grupos y fases de eliminatorias
    grupos_panteras = {'grupoA', 'grupoB'}
    fases_eliminatorias_panteras = {'semifinales', 'final'}
    equipos_por_encuentros_panteras = {}
    eliminatorias_panteras = {'semifinales': {'partidos': []}, 'final': {'partidos': []}}
    for partido in partidos:
        grupo_o_fase = partido.get('encuentros')
        if grupo_o_fase in fases_eliminatorias_panteras:
            # Añadir partidos a la fase de eliminación correspondiente
            eliminatorias_panteras[grupo_o_fase]['partidos'].append(partido)
        elif grupo_o_fase in grupos_panteras:
            # Añadir equipos y partidos a los grupos
            if grupo_o_fase not in equipos_por_encuentros_panteras:
                equipos_por_encuentros_panteras[grupo_o_fase] = {'equipos': [], 'partidos': []}
            local = {'nombre': partido['local'], 'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'puntos': 0, 'bonus': 0}
            visitante = {'nombre': partido['visitante'], 'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'puntos': 0, 'bonus': 0}
            # Añadir equipos si no existen en la lista de equipos del grupo
            if not any(e['nombre'] == local['nombre'] for e in equipos_por_encuentros_panteras[grupo_o_fase]['equipos']):
                equipos_por_encuentros_panteras[grupo_o_fase]['equipos'].append(local)
            if not any(e['nombre'] == visitante['nombre'] for e in equipos_por_encuentros_panteras[grupo_o_fase]['equipos']):
                equipos_por_encuentros_panteras[grupo_o_fase]['equipos'].append(visitante)
            equipos_por_encuentros_panteras[grupo_o_fase]['partidos'].append(partido)
        else:
            print(f"Grupo o fase no reconocido: {grupo_o_fase}")
    return equipos_por_encuentros_panteras, eliminatorias_panteras
#Obtener equipos Copa Europa CPLV Munia Panteras
def obtener_equipos_por_encuentros_panteras(partidos):
    equipos_por_encuentros_panteras = {}
    eliminatorias_panteras = {'semifinales': {'partidos': []}, 'final': {'partidos': []}}
    # Clasificar partidos en grupos o eliminatorias
    for partido in partidos:
        grupo_o_fase = partido.get('encuentros')
        if grupo_o_fase in eliminatorias_panteras:
            eliminatorias_panteras[grupo_o_fase]['partidos'].append(partido)
        else:
            if grupo_o_fase not in equipos_por_encuentros_panteras:
                equipos_por_encuentros_panteras[grupo_o_fase] = {'equipos': [], 'partidos': []}
            # Añadir equipos si no existen en la lista de equipos del grupo
            local = {'nombre': partido['local'], 'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'puntos': 0, 'bonus': 0}
            visitante = {'nombre': partido['visitante'], 'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'puntos': 0, 'bonus':0}
            if not any(e['nombre'] == local['nombre'] for e in equipos_por_encuentros_panteras[grupo_o_fase]['equipos']):
                equipos_por_encuentros_panteras[grupo_o_fase]['equipos'].append(local)
            if not any(e['nombre'] == visitante['nombre'] for e in equipos_por_encuentros_panteras[grupo_o_fase]['equipos']):
                equipos_por_encuentros_panteras[grupo_o_fase]['equipos'].append(visitante)
            equipos_por_encuentros_panteras[grupo_o_fase]['partidos'].append(partido)
    return equipos_por_encuentros_panteras, eliminatorias_panteras
# Obtener la información de la tabla europa_panteras
def obtener_europa_panteras():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, encuentros, fecha, hora, local, bonusA, resultadoA, resultadoB, bonusB, visitante FROM europa_panteras")
    partidos = cur.fetchall()
    cur.close()
    print("Partidos desde la BD:", partidos)  # Añadir esta línea para depuración
    return partidos
# Formatear partidos por grupo
def formatear_partidos_por_encuentros_panteras(partidos):
    encuentros_panteras = {
        'grupoA': {'id': 1, 'encuentros': 'grupoA', 'partidos': []},
        'grupoB': {'id': 2, 'encuentros': 'grupoB', 'partidos': []},
        'semifinales': {'id': 3, 'encuentros': 'semifinales', 'partidos': []},
        'final': {'id': 4, 'encuentros': 'final', 'partidos': []}
    }
    for partido in partidos:
        grupo = partido.get('encuentros', '')
        if grupo in encuentros_panteras:
            encuentros_panteras[grupo]['partidos'].append(partido)
        else:
            print(f"Grupo no encontrado: {grupo}")            
    return encuentros_panteras
# Crear formulario para los grupos y eliminatorias panteras
@app.route('/admin/europa_panteras/')
def ver_europa_panteras():
    try:
        # Obtener todos los partidos de los Playoff panteras
        partidos = obtener_europa_panteras()
        # Formatear los partidos por grupos y eliminatorias
        dats7 = formatear_partidos_por_encuentros_panteras(partidos)
        # Imprimir para depuración
        print(dats7)
        # Renderizar la plantilla con los datos formateados
        return render_template('admin/europa_panteras.html', dats7=dats7)
    except Exception as e:
        print(f"Error al obtener o formatear los datos de Copa Europa Panteras: {e}")
        # Renderizar una plantilla de error o manejar el error de alguna manera
        return render_template('error.html')
# Modificar los partidos de los playoff
@app.route('/modificar_europa_panteras/<int:id>', methods=['POST'])
def modificar_europa_panteras(id):
    if request.method == 'POST':
        encuentros = request.form.get('encuentros')
        num_partidos = int(request.form.get('num_partidos', 0))
        try:
            cur = mysql.connection.cursor()
            # Actualizar la eliminatoria de la jornada
            cur.execute('UPDATE europa_panteras SET encuentros = %s WHERE id = %s', (encuentros, id))
            print(f"Consulta para actualizar la eliminatoria ejecutada para id {id}")
            # Actualizar los detalles de cada partido
            for i in range(num_partidos):
                partido_id = request.form.get(f'partido_id{i}')
                fecha = request.form.get(f'fecha{i}')
                hora = request.form.get(f'hora{i}')
                local = request.form.get(f'local{i}')
                bonusA = request.form.get(f'bonusA{i}')
                resultadoA = request.form.get(f'resultadoA{i}')
                resultadoB = request.form.get(f'resultadoB{i}')
                bonusB = request.form.get(f'bonusB{i}')
                visitante = request.form.get(f'visitante{i}')
                # Verificar que los campos obligatorios tienen valores válidos
                if all([partido_id, local, visitante]):
                    # Asignar valores predeterminados si los campos opcionales están vacíos
                    if fecha is None:
                        fecha = ''
                    if hora is None:
                        hora = ''
                    if local is None:
                        local = ''
                    if bonusA is None:
                        bonusA = ''    
                    if resultadoA is None:
                        resultadoA = ''
                    if resultadoB is None:
                        resultadoB = ''
                    if bonusB is None:
                        bonusB = ''    
                    if visitante is None:
                        visitante = ''
                    # Actualizar el partido en la base de datos
                    cur.execute('UPDATE europa_panteras SET fecha = %s, hora = %s, local = %s, bonusA = %s, resultadoA = %s, resultadoB = %s, bonusB = %s, visitante = %s WHERE id = %s',
                                (fecha, hora, local, bonusA, resultadoA, resultadoB, bonusB, visitante, partido_id))
                    print(f"Consulta para actualizar el partido ejecutada para id {partido_id}")
            # Commit de la transacción
            mysql.connection.commit()
        except MySQLdb.Error as e:
            print(f"Error en la base de datos: {e}")
            mysql.connection.rollback()  # Revertir cambios en caso de error
        finally:
            if 'cur' in locals() and cur:
                cur.close()  # Cerrar cursor
        return redirect(url_for('ver_europa_panteras'))
    return render_template('tu_template.html')
#Eliminar partidos Copa Europa CPLV Munia Panteras
@app.route('/eliminar_europa_panteras/<string:identificador>', methods=['POST'])
def eliminar_europa_panteras(identificador):
    cur = mysql.connection.cursor()
    try:
        if identificador.startswith('grupo') or identificador in ['finalA', 'finalB']:
            cur.execute('DELETE FROM europa_panteras WHERE encuentros = %s', [identificador])
            mysql.connection.commit()
            flash('Partidos eliminados correctamente', 'success')
        else:
            flash('Identificador de encuentros no válido', 'error')
    except Exception as e:
        flash(f'Error al eliminar partidos: {str(e)}', 'error')
    finally:
        cur.close()
    return redirect(url_for('ver_europa_panteras'))
# Ruta para mostrar la Copa Europa CPLV Munia Panteras
@app.route('/euro_panteras/')
def europa_panteras():
    partidos = obtener_europa_panteras()
    equipos_por_encuentros, eliminatorias = obtener_equipos_por_encuentros_panteras(partidos)
    clasificaciones, enfrentamientos_directos = recalcular_clasificaciones_panteras(partidos)
    # Convertir clasificaciones a una estructura adecuada para la vista
    data_clasificaciones = {}
    for grupo, equipos in clasificaciones.items():
        # Ordenar equipos primero por puntos, luego por victorias, derrotas, y partidos jugados
        equipos_ordenados = sorted(equipos.items(), key=lambda item: (-item[1]['puntos'], item[1]['ganados'], item[1]['perdidos'], -item[1]['jugados']))      
        # Aplicar el criterio de desempate basado en enfrentamientos directos
        def criterio_enfrentamientos_directos(equipo1, equipo2):
            if equipo1 in enfrentamientos_directos and equipo2 in enfrentamientos_directos[equipo1]:
                resultado_directo = enfrentamientos_directos[equipo1][equipo2]
                return resultado_directo  # Resultado positivo indica que equipo1 ganó
            return 0
        # Crear una lista ordenada usando el criterio de desempate de enfrentamientos directos
        equipos_ordenados = sorted(equipos_ordenados, key=lambda item: (
            -item[1]['puntos'], 
            item[1]['ganados'], 
            item[1]['perdidos'], 
            -item[1]['jugados'],
            -criterio_enfrentamientos_directos(item[0], item[0])
        ))
        # Ajustar el orden para el desempate directo
        for i in range(len(equipos_ordenados)):
            for j in range(i + 1, len(equipos_ordenados)):
                equipo_a, stats_a = equipos_ordenados[i]
                equipo_b, stats_b = equipos_ordenados[j]
                if stats_a['puntos'] == stats_b['puntos'] and stats_a['ganados'] == stats_b['ganados'] and stats_a['perdidos'] == stats_b['perdidos']:
                    resultado_directo = criterio_enfrentamientos_directos(equipo_a, equipo_b)
                    if resultado_directo > 0:  # equipo_a ganó el enfrentamiento directo
                        # Intercambiar posiciones para que equipo_a quede por encima de equipo_b
                        equipos_ordenados[i], equipos_ordenados[j] = equipos_ordenados[j], equipos_ordenados[i]
                    elif resultado_directo < 0:  # equipo_b ganó el enfrentamiento directo
                        # Intercambiar posiciones para que equipo_b quede por encima de equipo_a
                        equipos_ordenados[i], equipos_ordenados[j] = equipos_ordenados[j], equipos_ordenados[i]
        data_clasificaciones[grupo] = equipos_ordenados
    return render_template('europa/panteras_europa.html', equipos_por_encuentros=equipos_por_encuentros, eliminatorias=eliminatorias, clasificaciones=data_clasificaciones)
# Fin Copa Europa CPLV Munia Panteras

# PLAYOFF DE LOS DIFERENTES EQUIPOS
# PlayOff UEMC Valladolid
# Crear formulario para los playoff
@app.route('/admin/crear_playoff_uemc', methods=['GET', 'POST'])
def crear_playoff_uemc():
    if request.method == 'POST':
        eliminatoria = request.form.get('eliminatoria')       
        # Determinar el máximo de partidos permitidos para la eliminatoria
        max_partidos = {
            'cuartos': 20,
            'semifinales': 2,
            'final': 1
        }.get(eliminatoria, 0)        
        # Obtener el número de partidos del formulario
        num_partidos_str = request.form.get('num_partidos', '0').strip()
        num_partidos = int(num_partidos_str) if num_partidos_str else 0        
        # Validar el número de partidos
        if num_partidos < 0 or num_partidos > max_partidos:
            return "Número de partidos no válido"                
        # Crear un cursor para ejecutar consultas SQL
        cur = mysql.connection.cursor()
        # Iterar sobre los datos del formulario para insertar los partidos
        for i in range(num_partidos):
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            local = request.form.get(f'local{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            visitante = request.form.get(f'visitante{i}')          
            # Verificar si algún campo es None y asignar valores por defecto
            if fecha is None:
                fecha = ''
            if hora is None:
                hora = ''
            if local is None:
                local = ''
            if resultadoA is None:
                resultadoA = ''
            if resultadoB is None:
                resultadoB = ''
            if visitante is None:
                visitante = ''           
            # Insertar el partido en la tabla copa_recoletas
            cur.execute("""
                INSERT INTO playoff_uemc (eliminatoria, fecha, hora, local, resultadoA, resultadoB, visitante)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (eliminatoria, fecha, hora, local, resultadoA, resultadoB, visitante))       
        # Confirmar los cambios en la base de datos
        mysql.connection.commit()        
        # Cerrar el cursor
        cur.close()        
        # Redireccionar a la vista de la copa_recoletas
        return redirect(url_for('ver_playoff_uemc'))
    # Renderizar el formulario para crear la copa_recoletas
    return render_template('admin/playoff_uemc.html')
# Crear formulario para los playoff
@app.route('/admin/playoff_uemc/')
def ver_playoff_uemc():
    cursor = mysql.connection.cursor()
    eliminatorias = ['cuartos', 'semifinales','final']
    datos_eliminatorias = {}
    for eliminatoria in eliminatorias:
        cursor.execute("SELECT * FROM playoff_uemc WHERE eliminatoria = %s", [eliminatoria])
        partidos = cursor.fetchall()
        datos_eliminatorias[eliminatoria] = partidos
    cursor.close()
    return render_template('admin/playoff_uemc.html', datos_eliminatorias=datos_eliminatorias)
# Modificar los partidos de los playoff
@app.route('/modificar_playoff_uemc/<string:id>', methods=['GET', 'POST'])
def modificar_playoff_uemc(id):
    eliminatoria = request.form['eliminatoria']
    num_partidos = int(request.form['num_partidos'])
    cur = mysql.connection.cursor()
    # Actualizar la jornada
    cur.execute('UPDATE playoff_uemc SET eliminatoria = %s WHERE id = %s', (eliminatoria, id))
    # Actualizar los partidos de la jornada
    for i in range(num_partidos):
        partido_id = request.form.get(f'partido_id{i}')
        fecha = request.form.get(f'fecha{i}')
        hora = request.form.get(f'hora{i}')
        local = request.form.get(f'local{i}')
        resultadoA = request.form.get(f'resultadoA{i}')
        resultadoB = request.form.get(f'resultadoB{i}')
        visitante = request.form.get(f'visitante{i}')
        # Verificar que los campos obligatorios tienen valores válidos
        if all([partido_id, local, visitante]):
        # Asignar valores predeterminados si los campos opcionales están vacíos
            if fecha is None:
                fecha = ''
            if hora is None:
                hora = ''
            if local is None:
                local = ''
            if resultadoA is None:
                resultadoA = ''
            if resultadoB is None:
                resultadoB = ''
            if visitante is None:
                visitante = ''
        # Verificar que todos los campos están presentes
        cur.execute('UPDATE playoff_uemc SET fecha = %s, hora = %s, local = %s, resultadoA = %s, resultadoB = %s, visitante = %s WHERE id = %s',
            (fecha, hora, local, resultadoA, resultadoB, visitante, partido_id))
    mysql.connection.commit()
    cur.close()       
    # Redireccionar a la página de visualización de copa
    return redirect(url_for('ver_playoff_uemc')) 
# Ruta para eliminar las eliminatorias
@app.route('/eliminar_playoff_uemc/<string:eliminatoria>', methods=['POST'])
def eliminar_playoff_uemc(eliminatoria):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM playoff_uemc WHERE eliminatoria = %s', [eliminatoria])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('ver_playoff_uemc'))
# Ruta para mostrar los playoffs del UEMC Valladolid
@app.route('/playoffs_uemc/')
def playoffs_uemc():
    # Obtener datos de las eliminatorias
    cursor = mysql.connection.cursor()
    eliminatorias = ['cuartos', 'semifinales', 'final']
    datos_europa = {}
    for eliminatoria in eliminatorias:
        cursor.execute("SELECT * FROM playoff_uemc WHERE eliminatoria = %s", [eliminatoria])
        partidos = cursor.fetchall()
        datos_europa[eliminatoria] = partidos
    cursor.close()
    return render_template('playoffs/uemc_playoff.html', datos_europa=datos_europa)
# Fin Playoff UEMC

# PlayOff Fundación Aliados
# Crear formulario para los playoff
@app.route('/admin/crear_playoff_aliados', methods=['GET', 'POST'])
def crear_playoff_aliados():
    if request.method == 'POST':
        eliminatoria = request.form.get('eliminatoria')       
        # Determinar el máximo de partidos permitidos para la eliminatoria
        max_partidos = {
            'semifinales': 2,
            'final': 1
        }.get(eliminatoria, 0)        
        # Obtener el número de partidos del formulario
        num_partidos_str = request.form.get('num_partidos', '0').strip()
        num_partidos = int(num_partidos_str) if num_partidos_str else 0        
        # Validar el número de partidos
        if num_partidos < 0 or num_partidos > max_partidos:
            return "Número de partidos no válido"                
        # Crear un cursor para ejecutar consultas SQL
        cur = mysql.connection.cursor()
        # Iterar sobre los datos del formulario para insertar los partidos
        for i in range(num_partidos):
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            local = request.form.get(f'local{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            visitante = request.form.get(f'visitante{i}')          
            # Verificar si algún campo es None y asignar valores por defecto
            if fecha is None:
                fecha = ''
            if hora is None:
                hora = ''
            if local is None:
                local = ''
            if resultadoA is None:
                resultadoA = ''
            if resultadoB is None:
                resultadoB = ''
            if visitante is None:
                visitante = ''           
            # Insertar el partido en la tabla copa_recoletas
            cur.execute("""
                INSERT INTO playoff_aliados (eliminatoria, fecha, hora, local, resultadoA, resultadoB, visitante)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (eliminatoria, fecha, hora, local, resultadoA, resultadoB, visitante))       
        # Confirmar los cambios en la base de datos
        mysql.connection.commit()        
        # Cerrar el cursor
        cur.close()        
        # Redireccionar a la vista de la copa_recoletas
        return redirect(url_for('ver_playoff_aliados'))
    # Renderizar el formulario para crear la copa_recoletas
    return render_template('admin/playoff_aliados.html')
# Crear formulario para los playoff
@app.route('/admin/playoff_aliados/')
def ver_playoff_aliados():
    cursor = mysql.connection.cursor()
    eliminatorias = ['semifinales','final']
    datos_eliminatorias = {}
    for eliminatoria in eliminatorias:
        cursor.execute("SELECT * FROM playoff_aliados WHERE eliminatoria = %s", [eliminatoria])
        partidos = cursor.fetchall()
        datos_eliminatorias[eliminatoria] = partidos
    cursor.close()
    return render_template('admin/playoff_aliados.html', datos_eliminatorias=datos_eliminatorias)
# Modificar los partidos de los playoff
@app.route('/modificar_playoff_aliados/<string:id>', methods=['GET', 'POST'])
def modificar_playoff_aliados(id):
    eliminatoria = request.form['eliminatoria']
    num_partidos = int(request.form['num_partidos'])
    cur = mysql.connection.cursor()
    # Actualizar la jornada
    cur.execute('UPDATE playoff_aliados SET eliminatoria = %s WHERE id = %s', (eliminatoria, id))
    # Actualizar los partidos de la jornada
    for i in range(num_partidos):
        partido_id = request.form.get(f'partido_id{i}')
        fecha = request.form.get(f'fecha{i}')
        hora = request.form.get(f'hora{i}')
        local = request.form.get(f'local{i}')
        resultadoA = request.form.get(f'resultadoA{i}')
        resultadoB = request.form.get(f'resultadoB{i}')
        visitante = request.form.get(f'visitante{i}')
        # Verificar que los campos obligatorios tienen valores válidos
        if all([partido_id, local, visitante]):
        # Asignar valores predeterminados si los campos opcionales están vacíos
            if fecha is None:
                fecha = ''
            if hora is None:
                hora = ''
            if local is None:
                local = ''
            if resultadoA is None:
                resultadoA = ''
            if resultadoB is None:
                resultadoB = ''
            if visitante is None:
                visitante = ''
        # Verificar que todos los campos están presentes
        cur.execute('UPDATE playoff_aliados SET fecha = %s, hora = %s, local = %s, resultadoA = %s, resultadoB = %s, visitante = %s WHERE id = %s',
            (fecha, hora, local, resultadoA, resultadoB, visitante, partido_id))
    mysql.connection.commit()
    cur.close()       
    # Redireccionar a la página de visualización de copa
    return redirect(url_for('ver_playoff_aliados'))
# Ruta para eliminar las eliminatorias
@app.route('/eliminar_playoff_aliados/<string:eliminatoria>', methods=['POST'])
def eliminar_playoff_aliados(eliminatoria):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM playoff_aliados WHERE eliminatoria = %s', [eliminatoria])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('ver_playoff_aliados'))
# Ruta para mostrar los playoffs de Fundación Aliados
@app.route('/playoffs_aliados/')
def playoffs_aliados():
    # Obtener datos de las eliminatorias
    cursor = mysql.connection.cursor()
    eliminatorias = ['semifinales', 'final']
    datos_europa = {}
    for eliminatoria in eliminatorias:
        cursor.execute("SELECT * FROM playoff_aliados WHERE eliminatoria = %s", [eliminatoria])
        partidos = cursor.fetchall()
        datos_europa[eliminatoria] = partidos
    cursor.close()
    return render_template('playoffs/aliados_playoff.html', datos_europa=datos_europa)
# Fin Playoff Aliados

# PlayOff Valladolid
# Crear formulario para los playoff
@app.route('/admin/crear_playoff_valladolid', methods=['GET', 'POST'])
def crear_playoff_valladolid():
    if request.method == 'POST':
        eliminatoria = request.form.get('eliminatoria')       
        # Determinar el máximo de partidos permitidos para la eliminatoria
        max_partidos = {
            'semifinales': 4,
            'final': 2
        }.get(eliminatoria, 0)        
        # Obtener el número de partidos del formulario
        num_partidos_str = request.form.get('num_partidos', '0').strip()
        num_partidos = int(num_partidos_str) if num_partidos_str else 0        
        # Validar el número de partidos
        if num_partidos < 0 or num_partidos > max_partidos:
            return "Número de partidos no válido"                
        # Crear un cursor para ejecutar consultas SQL
        cur = mysql.connection.cursor()
        # Iterar sobre los datos del formulario para insertar los partidos
        for i in range(num_partidos):
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            local = request.form.get(f'local{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            visitante = request.form.get(f'visitante{i}')          
            # Verificar si algún campo es None y asignar valores por defecto
            if fecha is None:
                fecha = ''
            if hora is None:
                hora = ''
            if local is None:
                local = ''
            if resultadoA is None:
                resultadoA = ''
            if resultadoB is None:
                resultadoB = ''
            if visitante is None:
                visitante = ''           
            # Insertar el partido en la tabla copa_recoletas
            cur.execute("""
                INSERT INTO playoff_valladolid (eliminatoria, fecha, hora, local, resultadoA, resultadoB, visitante)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (eliminatoria, fecha, hora, local, resultadoA, resultadoB, visitante))       
        # Confirmar los cambios en la base de datos
        mysql.connection.commit()        
        # Cerrar el cursor
        cur.close()        
        # Redireccionar a la vista de la copa_recoletas
        return redirect(url_for('ver_playoff_valladolid'))
    # Renderizar el formulario para crear la copa_recoletas
    return render_template('admin/playoff_valladolid.html')
# Crear formulario para los playoff
@app.route('/admin/playoff_valladolid/')
def ver_playoff_valladolid():
    cursor = mysql.connection.cursor()
    eliminatorias = ['semifinales','final']
    datos_playoff = {}
    for eliminatoria in eliminatorias:
        cursor.execute("SELECT * FROM playoff_valladolid WHERE eliminatoria = %s", [eliminatoria])
        partidos = cursor.fetchall()
        datos_playoff[eliminatoria] = partidos
    cursor.close()
    return render_template('admin/playoff_valladolid.html', datos_playoff=datos_playoff)
# Modificar los partidos de los playoff
@app.route('/modificar_playoff_valladolid/<string:id>', methods=['GET', 'POST'])
def modificar_playoff_valladolid(id):
    eliminatoria = request.form['eliminatoria']
    num_partidos = int(request.form['num_partidos'])
    cur = mysql.connection.cursor()
    # Actualizar la jornada
    cur.execute('UPDATE playoff_valladolid SET eliminatoria = %s WHERE id = %s', (eliminatoria, id))
    # Actualizar los partidos de la jornada
    for i in range(num_partidos):
        partido_id = request.form.get(f'partido_id{i}')
        fecha = request.form.get(f'fecha{i}')
        hora = request.form.get(f'hora{i}')
        local = request.form.get(f'local{i}')
        resultadoA = request.form.get(f'resultadoA{i}')
        resultadoB = request.form.get(f'resultadoB{i}')
        visitante = request.form.get(f'visitante{i}')
        # Verificar que los campos obligatorios tienen valores válidos
        if all([partido_id, local, visitante]):
        # Asignar valores predeterminados si los campos opcionales están vacíos
            if fecha is None:
                fecha = ''
            if hora is None:
                hora = ''
            if local is None:
                local = ''
            if resultadoA is None:
                resultadoA = ''
            if resultadoB is None:
                resultadoB = ''
            if visitante is None:
                visitante = ''
        # Verificar que todos los campos están presentes
        cur.execute('UPDATE playoff_valladolid SET fecha = %s, hora = %s, local = %s, resultadoA = %s, resultadoB = %s, visitante = %s WHERE id = %s',
            (fecha, hora, local, resultadoA, resultadoB, visitante, partido_id))
    mysql.connection.commit()
    cur.close()       
    # Redireccionar a la página de visualización de copa
    return redirect(url_for('ver_playoff_valladolid'))
# Ruta para eliminar las eliminatorias
@app.route('/eliminar_playoff_valladolid/<string:eliminatoria>', methods=['POST'])
def eliminar_playoff_valladolid(eliminatoria):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM playoff_valladolid WHERE eliminatoria = %s', [eliminatoria])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('ver_playoff_valladolid'))
# Ruta para mostrar los playoffs del Real Valladolid
@app.route('/playoffs_valladolid/')
def playoffs_valladolid():
    # Obtener datos de las eliminatorias
    cursor = mysql.connection.cursor()
    eliminatorias = ['semifinales', 'final']
    datos_playoff = {}
    for eliminatoria in eliminatorias:
        cursor.execute("SELECT * FROM playoff_valladolid WHERE eliminatoria = %s", [eliminatoria])
        partidos = cursor.fetchall()
        datos_playoff[eliminatoria] = partidos
    cursor.close()
    return render_template('playoffs/valladolid_playoff.html', datos_playoff=datos_playoff)
# Fin Playoff Valladolid

# PlayOff Real Valladolid Promesas
# Crear formulario para los playoff
@app.route('/admin/crear_playoff_promesas', methods=['GET', 'POST'])
def crear_playoff_promesas():
    if request.method == 'POST':
        eliminatoria = request.form.get('eliminatoria')       
        # Determinar el máximo de partidos permitidos para la eliminatoria
        max_partidos = {
            'primera' : 20,
            'semifinales': 10,
            'final': 5
        }.get(eliminatoria, 0)        
        # Obtener el número de partidos del formulario
        num_partidos_str = request.form.get('num_partidos', '0').strip()
        num_partidos = int(num_partidos_str) if num_partidos_str else 0        
        # Validar el número de partidos
        if num_partidos < 0 or num_partidos > max_partidos:
            return "Número de partidos no válido"                
        # Crear un cursor para ejecutar consultas SQL
        cur = mysql.connection.cursor()
        # Iterar sobre los datos del formulario para insertar los partidos
        for i in range(num_partidos):
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            local = request.form.get(f'local{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            visitante = request.form.get(f'visitante{i}')          
            # Verificar si algún campo es None y asignar valores por defecto
            if fecha is None:
                fecha = ''
            if hora is None:
                hora = ''
            if local is None:
                local = ''
            if resultadoA is None:
                resultadoA = ''
            if resultadoB is None:
                resultadoB = ''
            if visitante is None:
                visitante = ''           
            # Insertar el partido en la tabla copa_recoletas
            cur.execute("""
                INSERT INTO playoff_promesas (eliminatoria, fecha, hora, local, resultadoA, resultadoB, visitante)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (eliminatoria, fecha, hora, local, resultadoA, resultadoB, visitante))       
        # Confirmar los cambios en la base de datos
        mysql.connection.commit()        
        # Cerrar el cursor
        cur.close()        
        # Redireccionar a la vista de la copa_recoletas
        return redirect(url_for('ver_playoff_promesas'))
    # Renderizar el formulario para crear la copa_recoletas
    return render_template('admin/playoff_promesas.html')
# Crear formulario para los playoff
@app.route('/admin/playoff_promesas/')
def ver_playoff_promesas():
    cursor = mysql.connection.cursor()
    eliminatorias = ['primera','semifinales','final']
    datos_playoff = {}
    for eliminatoria in eliminatorias:
        cursor.execute("SELECT * FROM playoff_promesas WHERE eliminatoria = %s", [eliminatoria])
        partidos = cursor.fetchall()
        datos_playoff[eliminatoria] = partidos
    cursor.close()
    return render_template('admin/playoff_promesas.html', datos_playoff=datos_playoff)
# Modificar los partidos de los playoff
@app.route('/modificar_playoff_promesas/<string:id>', methods=['GET', 'POST'])
def modificar_playoff_promesas(id):
    eliminatoria = request.form['eliminatoria']
    num_partidos = int(request.form['num_partidos'])
    cur = mysql.connection.cursor()
    # Actualizar la jornada
    cur.execute('UPDATE playoff_promesas SET eliminatoria = %s WHERE id = %s', (eliminatoria, id))
    # Actualizar los partidos de la jornada
    for i in range(num_partidos):
        partido_id = request.form.get(f'partido_id{i}')
        fecha = request.form.get(f'fecha{i}')
        hora = request.form.get(f'hora{i}')
        local = request.form.get(f'local{i}')
        resultadoA = request.form.get(f'resultadoA{i}')
        resultadoB = request.form.get(f'resultadoB{i}')
        visitante = request.form.get(f'visitante{i}')
        # Verificar que los campos obligatorios tienen valores válidos
        if all([partido_id, local, visitante]):
        # Asignar valores predeterminados si los campos opcionales están vacíos
            if fecha is None:
                fecha = ''
            if hora is None:
                hora = ''
            if local is None:
                local = ''
            if resultadoA is None:
                resultadoA = ''
            if resultadoB is None:
                resultadoB = ''
            if visitante is None:
                visitante = ''
        # Verificar que todos los campos están presentes
        cur.execute('UPDATE playoff_promesas SET fecha = %s, hora = %s, local = %s, resultadoA = %s, resultadoB = %s, visitante = %s WHERE id = %s',
            (fecha, hora, local, resultadoA, resultadoB, visitante, partido_id))
    mysql.connection.commit()
    cur.close()       
    # Redireccionar a la página de visualización de copa
    return redirect(url_for('ver_playoff_promesas')) 
# Ruta para eliminar las eliminatorias
@app.route('/eliminar_playoff_promesas/<string:eliminatoria>', methods=['POST'])
def eliminar_playoff_promesas(eliminatoria):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM playoff_promesas WHERE eliminatoria = %s', [eliminatoria])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('ver_playoff_promesas'))
# Ruta para mostrar los playoffs del Real Valladolid Promesas
@app.route('/playoffs_promesas/')
def playoffs_promesas():
    # Obtener datos de las eliminatorias
    cursor = mysql.connection.cursor()
    eliminatorias = ['primera','semifinales', 'final']
    datos_playoff = {}
    for eliminatoria in eliminatorias:
        cursor.execute("SELECT * FROM playoff_promesas WHERE eliminatoria = %s", [eliminatoria])
        partidos = cursor.fetchall()
        datos_playoff[eliminatoria] = partidos
    cursor.close()
    return render_template('playoffs/promesas_playoff.html', datos_playoff=datos_playoff)
# Fin Playoff Promesas

# PlayOff Aula Valladolid
# Crear formulario para los playoff
@app.route('/admin/crear_playoff_aula', methods=['GET', 'POST'])
def crear_playoff_aula():
    if request.method == 'POST':
        eliminatoria = request.form.get('eliminatoria')       
        # Determinar el máximo de partidos permitidos para la eliminatoria
        max_partidos = {
            'cuartos' : 6,
            'septimo': 4,
            'sexto': 2,
            'quinto' : 2,
            'semifinales': 4,
            'tercero': 2,
            'final' : 2
        }.get(eliminatoria, 0)        
        # Obtener el número de partidos del formulario
        num_partidos_str = request.form.get('num_partidos', '0').strip()
        num_partidos = int(num_partidos_str) if num_partidos_str else 0        
        # Validar el número de partidos
        if num_partidos < 0 or num_partidos > max_partidos:
            return "Número de partidos no válido"                
        # Crear un cursor para ejecutar consultas SQL
        cur = mysql.connection.cursor()
        # Iterar sobre los datos del formulario para insertar los partidos
        for i in range(num_partidos):
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            local = request.form.get(f'local{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            visitante = request.form.get(f'visitante{i}')          
            # Verificar si algún campo es None y asignar valores por defecto
            if fecha is None:
                fecha = ''
            if hora is None:
                hora = ''
            if local is None:
                local = ''
            if resultadoA is None:
                resultadoA = ''
            if resultadoB is None:
                resultadoB = ''
            if visitante is None:
                visitante = ''           
            # Insertar el partido en la tabla copa_recoletas
            cur.execute("""
                INSERT INTO playoff_aula (eliminatoria, fecha, hora, local, resultadoA, resultadoB, visitante)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (eliminatoria, fecha, hora, local, resultadoA, resultadoB, visitante))       
        # Confirmar los cambios en la base de datos
        mysql.connection.commit()        
        # Cerrar el cursor
        cur.close()        
        # Redireccionar a la vista de la copa_recoletas
        return redirect(url_for('ver_playoff_aula'))
    # Si no es una solicitud POST, renderizar el formulario
    return render_template('admin/playoff_aula.html')
# Crear formulario para los playoff
@app.route('/admin/playoff_aula/')
def ver_playoff_aula():
    cursor = mysql.connection.cursor()
    eliminatorias = ['cuartos','septimo','sexto','quinto','semifinales','tercero','final']
    datos_playoff = {}
    for eliminatoria in eliminatorias:
        cursor.execute("SELECT * FROM playoff_aula WHERE eliminatoria = %s", [eliminatoria])
        partidos = cursor.fetchall()
        datos_playoff[eliminatoria] = partidos
    cursor.close()
    return render_template('admin/playoff_aula.html', datos_playoff=datos_playoff)
# Modificar los partidos de los playoff
@app.route('/modificar_playoff_aula/<string:id>', methods=['GET', 'POST'])
def modificar_playoff_aula(id):
    eliminatoria = request.form['eliminatoria']
    num_partidos = int(request.form['num_partidos'])
    cur = mysql.connection.cursor()
    # Actualizar la jornada
    cur.execute('UPDATE playoff_aula SET eliminatoria = %s WHERE id = %s', (eliminatoria, id))
    # Actualizar los partidos de la jornada
    for i in range(num_partidos):
        partido_id = request.form.get(f'partido_id{i}')
        fecha = request.form.get(f'fecha{i}')
        hora = request.form.get(f'hora{i}')
        local = request.form.get(f'local{i}')
        resultadoA = request.form.get(f'resultadoA{i}')
        resultadoB = request.form.get(f'resultadoB{i}')
        visitante = request.form.get(f'visitante{i}')
        # Verificar que los campos obligatorios tienen valores válidos
        if all([partido_id, local, visitante]):
        # Asignar valores predeterminados si los campos opcionales están vacíos
            if fecha is None:
                fecha = ''
            if hora is None:
                hora = ''
            if local is None:
                local = ''
            if resultadoA is None:
                resultadoA = ''
            if resultadoB is None:
                resultadoB = ''
            if visitante is None:
                visitante = ''
        # Verificar que todos los campos están presentes
        cur.execute('UPDATE playoff_aula SET fecha = %s, hora = %s, local = %s, resultadoA = %s, resultadoB = %s, visitante = %s WHERE id = %s',
            (fecha, hora, local, resultadoA, resultadoB, visitante, partido_id))
    mysql.connection.commit()
    cur.close()       
    # Redireccionar a la página de visualización de copa
    return redirect(url_for('ver_playoff_aula'))
# Ruta para eliminar las eliminatorias
@app.route('/eliminar_playoff_aula/<string:eliminatoria>', methods=['POST'])
def eliminar_playoff_aula(eliminatoria):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM playoff_aula WHERE eliminatoria = %s', [eliminatoria])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('ver_playoff_aula'))
# Ruta para mostrar los playoffs del Aula Valladolid
@app.route('/playoffs_aula/')
def playoffs_aula():
    # Obtener datos de las eliminatorias
    cursor = mysql.connection.cursor()
    eliminatorias = ['cuartos','septimo','sexto','quinto','semifinales','tercero', 'final']
    datos_playoff = {}
    for eliminatoria in eliminatorias:
        cursor.execute("SELECT * FROM playoff_aula WHERE eliminatoria = %s", [eliminatoria])
        partidos = cursor.fetchall()
        datos_playoff[eliminatoria] = partidos
    cursor.close()
    return render_template('playoffs/aula_playoff.html', datos_playoff=datos_playoff)
# Fin Playoff Aula

# PlayOff Atlético Valladolid
# Crear formulario para los playoff
@app.route('/admin/crear_playoff_recoletas', methods=['GET', 'POST'])
def crear_playoff_recoletas():
    if request.method == 'POST':
        eliminatoria = request.form.get('eliminatoria')       
        # Determinar el máximo de partidos permitidos para la eliminatoria
        max_partidos = {
            'promocion' : 2
        }.get(eliminatoria, 0)        
        # Obtener el número de partidos del formulario
        num_partidos_str = request.form.get('num_partidos', '0').strip()
        num_partidos = int(num_partidos_str) if num_partidos_str else 0        
        # Validar el número de partidos
        if num_partidos < 0 or num_partidos > max_partidos:
            return "Número de partidos no válido"                
        # Crear un cursor para ejecutar consultas SQL
        cur = mysql.connection.cursor()
        # Iterar sobre los datos del formulario para insertar los partidos
        for i in range(num_partidos):
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            local = request.form.get(f'local{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            visitante = request.form.get(f'visitante{i}')          
            # Verificar si algún campo es None y asignar valores por defecto
            if fecha is None:
                fecha = ''
            if hora is None:
                hora = ''
            if local is None:
                local = ''
            if resultadoA is None:
                resultadoA = ''
            if resultadoB is None:
                resultadoB = ''
            if visitante is None:
                visitante = ''           
            # Insertar el partido en la tabla copa_recoletas
            cur.execute("""
                INSERT INTO playoff_recoletas (eliminatoria, fecha, hora, local, resultadoA, resultadoB, visitante)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (eliminatoria, fecha, hora, local, resultadoA, resultadoB, visitante))       
        # Confirmar los cambios en la base de datos
        mysql.connection.commit()        
        # Cerrar el cursor
        cur.close()        
        # Redireccionar a la vista de la copa_recoletas
        return redirect(url_for('ver_playoff_recoletas'))
    # Si no es una solicitud POST, renderizar el formulario
    return render_template('admin/playoff_recoletas.html')
# Crear formulario para los playoff
@app.route('/admin/playoff_recoletas/')
def ver_playoff_recoletas():
    cursor = mysql.connection.cursor()
    eliminatorias = ['promocion']
    datos_playoff = {}
    for eliminatoria in eliminatorias:
        cursor.execute("SELECT * FROM playoff_recoletas WHERE eliminatoria = %s", [eliminatoria])
        partidos = cursor.fetchall()
        datos_playoff[eliminatoria] = partidos
    cursor.close()
    return render_template('admin/playoff_recoletas.html', datos_playoff=datos_playoff)
# Modificar los partidos de los playoff
@app.route('/modificar_playoff_recoletas/<string:id>', methods=['GET', 'POST'])
def modificar_playoff_recoletas(id):
    eliminatoria = request.form['eliminatoria']
    num_partidos = int(request.form['num_partidos'])
    cur = mysql.connection.cursor()
    # Actualizar la jornada
    cur.execute('UPDATE playoff_recoletas SET eliminatoria = %s WHERE id = %s', (eliminatoria, id))
    # Actualizar los partidos de la jornada
    for i in range(num_partidos):
        partido_id = request.form.get(f'partido_id{i}')
        fecha = request.form.get(f'fecha{i}')
        hora = request.form.get(f'hora{i}')
        local = request.form.get(f'local{i}')
        resultadoA = request.form.get(f'resultadoA{i}')
        resultadoB = request.form.get(f'resultadoB{i}')
        visitante = request.form.get(f'visitante{i}')
        # Verificar que los campos obligatorios tienen valores válidos
        if all([partido_id, local, visitante]):
        # Asignar valores predeterminados si los campos opcionales están vacíos
            if fecha is None:
                fecha = ''
            if hora is None:
                hora = ''
            if local is None:
                local = ''
            if resultadoA is None:
                resultadoA = ''
            if resultadoB is None:
                resultadoB = ''
            if visitante is None:
                visitante = ''
        # Verificar que todos los campos están presentes
        cur.execute('UPDATE playoff_recoletas SET fecha = %s, hora = %s, local = %s, resultadoA = %s, resultadoB = %s, visitante = %s WHERE id = %s',
            (fecha, hora, local, resultadoA, resultadoB, visitante, partido_id))
    mysql.connection.commit()
    cur.close()       
    # Redireccionar a la página de visualización de copa
    return redirect(url_for('ver_playoff_recoletas'))
# Ruta para eliminar las eliminatorias
@app.route('/eliminar_playoff_recoletas/<string:eliminatoria>', methods=['POST'])
def eliminar_playoff_recoletas(eliminatoria):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM playoff_recoletas WHERE eliminatoria = %s', [eliminatoria])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('ver_playoff_recoletas'))
# Ruta para mostrar los playoffs del Atlético Valladolid
@app.route('/playoffs_recoletas/')
def playoffs_recoletas():
    # Obtener datos de las eliminatorias
    cursor = mysql.connection.cursor()
    eliminatorias = ['promocion']
    datos_playoff = {}
    for eliminatoria in eliminatorias:
        cursor.execute("SELECT * FROM playoff_recoletas WHERE eliminatoria = %s", [eliminatoria])
        partidos = cursor.fetchall()
        datos_playoff[eliminatoria] = partidos
    cursor.close()
    return render_template('playoffs/recoletas_playoff.html', datos_playoff=datos_playoff)
# Fin playoff promoción Recoletas

# PlayOff El Salvador
# Crear formulario para los playoff
@app.route('/admin/crear_playoff_salvador', methods=['GET', 'POST'])
def crear_playoff_salvador():
    if request.method == 'POST':
        eliminatoria = request.form.get('eliminatoria')       
        # Determinar el máximo de partidos permitidos para la eliminatoria
        max_partidos = {
            'cuartos' : 4,
            'semifinales': 2,
            'final' : 1
        }.get(eliminatoria, 0)        
        # Obtener el número de partidos del formulario
        num_partidos_str = request.form.get('num_partidos', '0').strip()
        num_partidos = int(num_partidos_str) if num_partidos_str else 0        
        # Validar el número de partidos
        if num_partidos < 0 or num_partidos > max_partidos:
            return "Número de partidos no válido"                
        # Crear un cursor para ejecutar consultas SQL
        cur = mysql.connection.cursor()
        # Iterar sobre los datos del formulario para insertar los partidos
        for i in range(num_partidos):
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            local = request.form.get(f'local{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            visitante = request.form.get(f'visitante{i}')          
            # Verificar si algún campo es None y asignar valores por defecto
            if fecha is None:
                fecha = ''
            if hora is None:
                hora = ''
            if local is None:
                local = ''
            if resultadoA is None:
                resultadoA = ''
            if resultadoB is None:
                resultadoB = ''
            if visitante is None:
                visitante = ''           
            # Insertar el partido en la tabla copa_recoletas
            cur.execute("""
                INSERT INTO playoff_salvador (eliminatoria, fecha, hora, local, resultadoA, resultadoB, visitante)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (eliminatoria, fecha, hora, local, resultadoA, resultadoB, visitante))       
        # Confirmar los cambios en la base de datos
        mysql.connection.commit()        
        # Cerrar el cursor
        cur.close()        
        # Redireccionar a la vista de la copa_recoletas
        return redirect(url_for('ver_playoff_salvador'))
    # Si no es una solicitud POST, renderizar el formulario
    return render_template('admin/playoff_salvador.html')
# Ver formulario playoff
@app.route('/admin/playoff_salvador/')
def ver_playoff_salvador():
    cursor = mysql.connection.cursor()
    eliminatorias = ['cuartos','semifinales','final']
    datos_playoff = {}
    for eliminatoria in eliminatorias:
        cursor.execute("SELECT * FROM playoff_salvador WHERE eliminatoria = %s", [eliminatoria])
        partidos = cursor.fetchall()
        datos_playoff[eliminatoria] = partidos
    cursor.close()
    return render_template('admin/playoff_salvador.html', datos_playoff=datos_playoff)
# Modificar los partidos de los playoff
@app.route('/modificar_playoff_salvador/<string:id>', methods=['GET', 'POST'])
def modificar_playoff_salvador(id):
    eliminatoria = request.form['eliminatoria']
    num_partidos = int(request.form['num_partidos'])
    cur = mysql.connection.cursor()
    # Actualizar la jornada
    cur.execute('UPDATE playoff_salvador SET eliminatoria = %s WHERE id = %s', (eliminatoria, id))
    # Actualizar los partidos de la jornada
    for i in range(num_partidos):
        partido_id = request.form.get(f'partido_id{i}')
        fecha = request.form.get(f'fecha{i}')
        hora = request.form.get(f'hora{i}')
        local = request.form.get(f'local{i}')
        resultadoA = request.form.get(f'resultadoA{i}')
        resultadoB = request.form.get(f'resultadoB{i}')
        visitante = request.form.get(f'visitante{i}')
        # Verificar que los campos obligatorios tienen valores válidos
        if all([partido_id, local, visitante]):
        # Asignar valores predeterminados si los campos opcionales están vacíos
            if fecha is None:
                fecha = ''
            if hora is None:
                hora = ''
            if local is None:
                local = ''
            if resultadoA is None:
                resultadoA = ''
            if resultadoB is None:
                resultadoB = ''
            if visitante is None:
                visitante = ''
        # Verificar que todos los campos están presentes
        cur.execute('UPDATE playoff_salvador SET fecha = %s, hora = %s, local = %s, resultadoA = %s, resultadoB = %s, visitante = %s WHERE id = %s',
            (fecha, hora, local, resultadoA, resultadoB, visitante, partido_id))
    mysql.connection.commit()
    cur.close()  
    return redirect(url_for('ver_playoff_salvador'))
# Ruta para eliminar las eliminatorias
@app.route('/eliminar_playoff_salvador/<string:eliminatoria>', methods=['POST'])
def eliminar_playoff_salvador(eliminatoria):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM playoff_salvador WHERE eliminatoria = %s', [eliminatoria])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('ver_playoff_salvador'))
# Ruta para mostrar los playoffs de El Salvador
@app.route('/playoffs_salvador/')
def playoffs_salvador():
    # Obtener datos de las eliminatorias
    cursor = mysql.connection.cursor()
    eliminatorias = ['cuartos','semifinales','final']
    datos_playoff = {}
    for eliminatoria in eliminatorias:
        cursor.execute("SELECT * FROM playoff_salvador WHERE eliminatoria = %s", [eliminatoria])
        partidos = cursor.fetchall()
        datos_playoff[eliminatoria] = partidos
    cursor.close()
    return render_template('playoffs/salvador_playoff.html', datos_playoff=datos_playoff)
# Fin playoff El Salvador

# PlayOff VRAC
# Crear formulario para los playoff
@app.route('/admin/crear_playoff_vrac', methods=['GET', 'POST'])
def crear_playoff_vrac():
    if request.method == 'POST':
        eliminatoria = request.form.get('eliminatoria')       
        # Determinar el máximo de partidos permitidos para la eliminatoria
        max_partidos = {
            'cuartos' : 4,
            'semifinales': 2,
            'final' : 1
        }.get(eliminatoria, 0)        
        # Obtener el número de partidos del formulario
        num_partidos_str = request.form.get('num_partidos', '0').strip()
        num_partidos = int(num_partidos_str) if num_partidos_str else 0        
        # Validar el número de partidos
        if num_partidos < 0 or num_partidos > max_partidos:
            return "Número de partidos no válido"                
        # Crear un cursor para ejecutar consultas SQL
        cur = mysql.connection.cursor()
        # Iterar sobre los datos del formulario para insertar los partidos
        for i in range(num_partidos):
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            local = request.form.get(f'local{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            visitante = request.form.get(f'visitante{i}')          
            # Verificar si algún campo es None y asignar valores por defecto
            if fecha is None:
                fecha = ''
            if hora is None:
                hora = ''
            if local is None:
                local = ''
            if resultadoA is None:
                resultadoA = ''
            if resultadoB is None:
                resultadoB = ''
            if visitante is None:
                visitante = ''           
            # Insertar el partido en la tabla copa_recoletas
            cur.execute("""
                INSERT INTO playoff_vrac (eliminatoria, fecha, hora, local, resultadoA, resultadoB, visitante)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (eliminatoria, fecha, hora, local, resultadoA, resultadoB, visitante))       
        # Confirmar los cambios en la base de datos
        mysql.connection.commit()        
        # Cerrar el cursor
        cur.close()        
        # Redireccionar a la vista de la copa_recoletas
        return redirect(url_for('ver_playoff_vrac'))
    # Si no es una solicitud POST, renderizar el formulario
    return render_template('admin/playoff_vrac.html')
# Ver formulario para los playoff
@app.route('/admin/playoff_vrac/')
def ver_playoff_vrac():
    cursor = mysql.connection.cursor()
    eliminatorias = ['cuartos','semifinales','final']
    datos_playoff = {}
    for eliminatoria in eliminatorias:
        cursor.execute("SELECT * FROM playoff_vrac WHERE eliminatoria = %s", [eliminatoria])
        partidos = cursor.fetchall()
        datos_playoff[eliminatoria] = partidos
    cursor.close()
    return render_template('admin/playoff_vrac.html', datos_playoff=datos_playoff)
# Modificar los partidos de los playoff
@app.route('/modificar_playoff_vrac/<string:id>', methods=['GET', 'POST'])
def modificar_playoff_vrac(id):
    eliminatoria = request.form['eliminatoria']
    num_partidos = int(request.form['num_partidos'])
    cur = mysql.connection.cursor()
    # Actualizar la jornada
    cur.execute('UPDATE playoff_vrac SET eliminatoria = %s WHERE id = %s', (eliminatoria, id))
    # Actualizar los partidos de la jornada
    for i in range(num_partidos):
        partido_id = request.form.get(f'partido_id{i}')
        fecha = request.form.get(f'fecha{i}')
        hora = request.form.get(f'hora{i}')
        local = request.form.get(f'local{i}')
        resultadoA = request.form.get(f'resultadoA{i}')
        resultadoB = request.form.get(f'resultadoB{i}')
        visitante = request.form.get(f'visitante{i}')
        # Verificar que los campos obligatorios tienen valores válidos
        if all([partido_id, local, visitante]):
        # Asignar valores predeterminados si los campos opcionales están vacíos
            if fecha is None:
                fecha = ''
            if hora is None:
                hora = ''
            if local is None:
                local = ''
            if resultadoA is None:
                resultadoA = ''
            if resultadoB is None:
                resultadoB = ''
            if visitante is None:
                visitante = ''
        # Verificar que todos los campos están presentes
        cur.execute('UPDATE playoff_vrac SET fecha = %s, hora = %s, local = %s, resultadoA = %s, resultadoB = %s, visitante = %s WHERE id = %s',
            (fecha, hora, local, resultadoA, resultadoB, visitante, partido_id))
    mysql.connection.commit()
    cur.close()  
    return redirect(url_for('ver_playoff_vrac')) 
# Ruta para eliminar las eliminatorias
@app.route('/eliminar_playoff_vrac/<string:eliminatoria>', methods=['POST'])
def eliminar_playoff_vrac(eliminatoria):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM playoff_vrac WHERE eliminatoria = %s', [eliminatoria])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('ver_playoff_vrac'))
# Ruta para mostrar los playoffs del VRAC
@app.route('/playoffs_vrac/')
def playoffs_vrac():
    # Obtener datos de las eliminatorias
    cursor = mysql.connection.cursor()
    eliminatorias = ['cuartos','semifinales','final']
    datos_playoff = {}
    for eliminatoria in eliminatorias:
        cursor.execute("SELECT * FROM playoff_vrac WHERE eliminatoria = %s", [eliminatoria])
        partidos = cursor.fetchall()
        datos_playoff[eliminatoria] = partidos
    cursor.close()
    return render_template('playoffs/vrac_playoff.html', datos_playoff=datos_playoff)   
# Fin playoff VRAC

# PlayOff El Salvador Fem.
# Crear formulario para los playoff
@app.route('/admin/crear_playoff_salvador_fem', methods=['GET', 'POST'])
def crear_playoff_salvador_fem():
    if request.method == 'POST':
        eliminatoria = request.form.get('eliminatoria')       
        # Determinar el máximo de partidos permitidos para la eliminatoria
        max_partidos = {
            'cuartos' : 4,
            'semifinales': 2,
            'final' : 1
        }.get(eliminatoria, 0)        
        # Obtener el número de partidos del formulario
        num_partidos_str = request.form.get('num_partidos', '0').strip()
        num_partidos = int(num_partidos_str) if num_partidos_str else 0        
        # Validar el número de partidos
        if num_partidos < 0 or num_partidos > max_partidos:
            return "Número de partidos no válido"                
        # Crear un cursor para ejecutar consultas SQL
        cur = mysql.connection.cursor()
        # Iterar sobre los datos del formulario para insertar los partidos
        for i in range(num_partidos):
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            local = request.form.get(f'local{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            visitante = request.form.get(f'visitante{i}')          
            # Verificar si algún campo es None y asignar valores por defecto
            if fecha is None:
                fecha = ''
            if hora is None:
                hora = ''
            if local is None:
                local = ''
            if resultadoA is None:
                resultadoA = ''
            if resultadoB is None:
                resultadoB = ''
            if visitante is None:
                visitante = ''           
            # Insertar el partido en la tabla copa_recoletas
            cur.execute("""
                INSERT INTO playoff_salvador_fem (eliminatoria, fecha, hora, local, resultadoA, resultadoB, visitante)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (eliminatoria, fecha, hora, local, resultadoA, resultadoB, visitante))       
        # Confirmar los cambios en la base de datos
        mysql.connection.commit()        
        # Cerrar el cursor
        cur.close()        
        # Redireccionar a la vista de la copa_recoletas
        return redirect(url_for('ver_playoff_salvador_fem'))
    # Si no es una solicitud POST, renderizar el formulario
    return render_template('admin/playoff_salvador_fem.html')
# Ver formulario para los playoff
@app.route('/admin/playoff_salvador_fem/')
def ver_playoff_salvador_fem():
    cursor = mysql.connection.cursor()
    eliminatorias = ['cuartos','semifinales','final']
    datos_playoff = {}
    for eliminatoria in eliminatorias:
        cursor.execute("SELECT * FROM playoff_salvador_fem WHERE eliminatoria = %s", [eliminatoria])
        partidos = cursor.fetchall()
        datos_playoff[eliminatoria] = partidos
    cursor.close()
    return render_template('admin/playoff_salvador_fem.html', datos_playoff=datos_playoff)
# Modificar los partidos de los playoff
@app.route('/modificar_playoff_salvador_fem/<string:id>', methods=['GET', 'POST'])
def modificar_playoff_salvador_fem(id):
    eliminatoria = request.form['eliminatoria']
    num_partidos = int(request.form['num_partidos'])
    cur = mysql.connection.cursor()
    # Actualizar la jornada
    cur.execute('UPDATE playoff_salvador_fem SET eliminatoria = %s WHERE id = %s', (eliminatoria, id))
    # Actualizar los partidos de la jornada
    for i in range(num_partidos):
        partido_id = request.form.get(f'partido_id{i}')
        fecha = request.form.get(f'fecha{i}')
        hora = request.form.get(f'hora{i}')
        local = request.form.get(f'local{i}')
        resultadoA = request.form.get(f'resultadoA{i}')
        resultadoB = request.form.get(f'resultadoB{i}')
        visitante = request.form.get(f'visitante{i}')
        # Verificar que los campos obligatorios tienen valores válidos
        if all([partido_id, local, visitante]):
        # Asignar valores predeterminados si los campos opcionales están vacíos
            if fecha is None:
                fecha = ''
            if hora is None:
                hora = ''
            if local is None:
                local = ''
            if resultadoA is None:
                resultadoA = ''
            if resultadoB is None:
                resultadoB = ''
            if visitante is None:
                visitante = ''
        # Verificar que todos los campos están presentes
        cur.execute('UPDATE playoff_salvador_fem SET fecha = %s, hora = %s, local = %s, resultadoA = %s, resultadoB = %s, visitante = %s WHERE id = %s',
            (fecha, hora, local, resultadoA, resultadoB, visitante, partido_id))
    mysql.connection.commit()
    cur.close()  
    return redirect(url_for('ver_playoff_salvador_fem')) 
# Ruta para eliminar las eliminatorias
@app.route('/eliminar_playoff_salvador_fem/<string:eliminatoria>', methods=['POST'])
def eliminar_playoff_salvador_fem(eliminatoria):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM playoff_salvador_fem WHERE eliminatoria = %s', [eliminatoria])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('ver_playoff_salvador_fem'))
# Ruta para mostrar los playoffs de El Salvador Fem.
@app.route('/playoffs_salvador_fem/')
def playoffs_salvador_fem():
    # Obtener datos de las eliminatorias
    cursor = mysql.connection.cursor()
    eliminatorias = ['cuartos','semifinales','final']
    datos_playoff = {}
    for eliminatoria in eliminatorias:
        cursor.execute("SELECT * FROM playoff_salvador_fem WHERE eliminatoria = %s", [eliminatoria])
        partidos = cursor.fetchall()
        datos_playoff[eliminatoria] = partidos
    cursor.close()
    return render_template('playoffs/salvador_fem_playoff.html', datos_playoff=datos_playoff) 
# Fin playoff El Salvador Fem.

# PlayOff Caja Rural CPLV
# Crear formulario para los playoff
@app.route('/admin/crear_playoff_caja', methods=['GET', 'POST'])
def crear_playoff_caja():
    if request.method == 'POST':
        eliminatoria = request.form.get('eliminatoria')       
        # Determinar el máximo de partidos permitidos para la eliminatoria
        max_partidos = {
            'semifinales': 6,
            'final' : 3,
            'play-out' : 3
        }.get(eliminatoria, 0)        
        # Obtener el número de partidos del formulario
        num_partidos_str = request.form.get('num_partidos', '0').strip()
        num_partidos = int(num_partidos_str) if num_partidos_str else 0        
        # Validar el número de partidos
        if num_partidos < 0 or num_partidos > max_partidos:
            return "Número de partidos no válido"                
        # Crear un cursor para ejecutar consultas SQL
        cur = mysql.connection.cursor()
        # Iterar sobre los datos del formulario para insertar los partidos
        for i in range(num_partidos):
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            local = request.form.get(f'local{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            visitante = request.form.get(f'visitante{i}')          
            # Verificar si algún campo es None y asignar valores por defecto
            if fecha is None:
                fecha = ''
            if hora is None:
                hora = ''
            if local is None:
                local = ''
            if resultadoA is None:
                resultadoA = ''
            if resultadoB is None:
                resultadoB = ''
            if visitante is None:
                visitante = ''           
            # Insertar el partido en la tabla copa_recoletas
            cur.execute("""
                INSERT INTO playoff_caja (eliminatoria, fecha, hora, local, resultadoA, resultadoB, visitante)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (eliminatoria, fecha, hora, local, resultadoA, resultadoB, visitante))       
        # Confirmar los cambios en la base de datos
        mysql.connection.commit()        
        # Cerrar el cursor
        cur.close()        
        # Redireccionar a la vista de la copa_recoletas
        return redirect(url_for('ver_playoff_caja'))
    # Si no es una solicitud POST, renderizar el formulario
    return render_template('admin/playoff_caja.html')
# Ver formulario para los playoff
@app.route('/admin/playoff_caja/')
def ver_playoff_caja():
    cursor = mysql.connection.cursor()
    eliminatorias = ['semifinales','final','play-out']
    datos_playoff = {}
    for eliminatoria in eliminatorias:
        cursor.execute("SELECT * FROM playoff_caja WHERE eliminatoria = %s", [eliminatoria])
        partidos = cursor.fetchall()
        datos_playoff[eliminatoria] = partidos
    cursor.close()
    return render_template('admin/playoff_caja.html', datos_playoff=datos_playoff)
# Modificar los partidos de los playoff
@app.route('/modificar_playoff_caja/<string:id>', methods=['GET', 'POST'])
def modificar_playoff_caja(id):
    eliminatoria = request.form['eliminatoria']
    num_partidos = int(request.form['num_partidos'])
    cur = mysql.connection.cursor()
    # Actualizar la jornada
    cur.execute('UPDATE playoff_caja SET eliminatoria = %s WHERE id = %s', (eliminatoria, id))
    # Actualizar los partidos de la jornada
    for i in range(num_partidos):
        partido_id = request.form.get(f'partido_id{i}')
        fecha = request.form.get(f'fecha{i}')
        hora = request.form.get(f'hora{i}')
        local = request.form.get(f'local{i}')
        resultadoA = request.form.get(f'resultadoA{i}')
        resultadoB = request.form.get(f'resultadoB{i}')
        visitante = request.form.get(f'visitante{i}')
        # Verificar que los campos obligatorios tienen valores válidos
        if all([partido_id, local, visitante]):
        # Asignar valores predeterminados si los campos opcionales están vacíos
            if fecha is None:
                fecha = ''
            if hora is None:
                hora = ''
            if local is None:
                local = ''
            if resultadoA is None:
                resultadoA = ''
            if resultadoB is None:
                resultadoB = ''
            if visitante is None:
                visitante = ''
        # Verificar que todos los campos están presentes
        cur.execute('UPDATE playoff_caja SET fecha = %s, hora = %s, local = %s, resultadoA = %s, resultadoB = %s, visitante = %s WHERE id = %s',
            (fecha, hora, local, resultadoA, resultadoB, visitante, partido_id))
    mysql.connection.commit()
    cur.close()  
    return redirect(url_for('ver_playoff_caja'))
# Ruta para eliminar las eliminatorias
@app.route('/eliminar_playoff_caja/<string:eliminatoria>', methods=['POST'])
def eliminar_playoff_caja(eliminatoria):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM playoff_caja WHERE eliminatoria = %s', [eliminatoria])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('ver_playoff_caja'))
# Ruta para mostrar los playoffs del VRAC
@app.route('/playoffs_caja/')
def playoffs_caja():
    # Obtener datos de las eliminatorias
    cursor = mysql.connection.cursor()
    eliminatorias = ['semifinales','final','play-out']
    datos_playoff = {}
    for eliminatoria in eliminatorias:
        cursor.execute("SELECT * FROM playoff_caja WHERE eliminatoria = %s", [eliminatoria])
        partidos = cursor.fetchall()
        datos_playoff[eliminatoria] = partidos
    cursor.close()
    return render_template('playoffs/caja_playoff.html', datos_playoff=datos_playoff)   
# Fin playoff CPLV Caja Rural

# PlayOff CPLV Munia Panteras  
# Crear formulario para los playoff
@app.route('/admin/crear_playoff_panteras', methods=['GET', 'POST'])
def crear_playoff_panteras():
    if request.method == 'POST':
        eliminatoria = request.form.get('eliminatoria')       
        # Determinar el máximo de partidos permitidos para la eliminatoria
        max_partidos = {
            'semifinales': 6,
            'final' : 3,
            'play-out' : 3
        }.get(eliminatoria, 0)        
        # Obtener el número de partidos del formulario
        num_partidos_str = request.form.get('num_partidos', '0').strip()
        num_partidos = int(num_partidos_str) if num_partidos_str else 0        
        # Validar el número de partidos
        if num_partidos < 0 or num_partidos > max_partidos:
            return "Número de partidos no válido"                
        # Crear un cursor para ejecutar consultas SQL
        cur = mysql.connection.cursor()
        # Iterar sobre los datos del formulario para insertar los partidos
        for i in range(num_partidos):
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            local = request.form.get(f'local{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            visitante = request.form.get(f'visitante{i}')          
            # Verificar si algún campo es None y asignar valores por defecto
            if fecha is None:
                fecha = ''
            if hora is None:
                hora = ''
            if local is None:
                local = ''
            if resultadoA is None:
                resultadoA = ''
            if resultadoB is None:
                resultadoB = ''
            if visitante is None:
                visitante = ''           
            # Insertar el partido en la tabla copa_recoletas
            cur.execute("""
                INSERT INTO playoff_panteras (eliminatoria, fecha, hora, local, resultadoA, resultadoB, visitante)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (eliminatoria, fecha, hora, local, resultadoA, resultadoB, visitante))       
        # Confirmar los cambios en la base de datos
        mysql.connection.commit()        
        # Cerrar el cursor
        cur.close()        
        # Redireccionar a la vista de la copa_recoletas
        return redirect(url_for('ver_playoff_panteras'))
    # Si no es una solicitud POST, renderizar el formulario
    return render_template('admin/playoff_panteras.html')
# Crear formulario para los playoff
@app.route('/admin/playoff_panteras/')
def ver_playoff_panteras():
    cursor = mysql.connection.cursor()
    eliminatorias = ['semifinales','final','play-out']
    datos_playoff = {}
    for eliminatoria in eliminatorias:
        cursor.execute("SELECT * FROM playoff_panteras WHERE eliminatoria = %s", [eliminatoria])
        partidos = cursor.fetchall()
        datos_playoff[eliminatoria] = partidos
    cursor.close()
    return render_template('admin/playoff_panteras.html', datos_playoff=datos_playoff)
# Modificar los partidos de los playoff
@app.route('/modificar_playoff_panteras/<string:id>', methods=['GET', 'POST'])
def modificar_playoff_panteras(id):
    eliminatoria = request.form['eliminatoria']
    num_partidos = int(request.form['num_partidos'])
    cur = mysql.connection.cursor()
    # Actualizar la jornada
    cur.execute('UPDATE playoff_panteras SET eliminatoria = %s WHERE id = %s', (eliminatoria, id))
    # Actualizar los partidos de la jornada
    for i in range(num_partidos):
        partido_id = request.form.get(f'partido_id{i}')
        fecha = request.form.get(f'fecha{i}')
        hora = request.form.get(f'hora{i}')
        local = request.form.get(f'local{i}')
        resultadoA = request.form.get(f'resultadoA{i}')
        resultadoB = request.form.get(f'resultadoB{i}')
        visitante = request.form.get(f'visitante{i}')
        # Verificar que los campos obligatorios tienen valores válidos
        if all([partido_id, local, visitante]):
        # Asignar valores predeterminados si los campos opcionales están vacíos
            if fecha is None:
                fecha = ''
            if hora is None:
                hora = ''
            if local is None:
                local = ''
            if resultadoA is None:
                resultadoA = ''
            if resultadoB is None:
                resultadoB = ''
            if visitante is None:
                visitante = ''
        # Verificar que todos los campos están presentes
        cur.execute('UPDATE playoff_panteras SET fecha = %s, hora = %s, local = %s, resultadoA = %s, resultadoB = %s, visitante = %s WHERE id = %s',
            (fecha, hora, local, resultadoA, resultadoB, visitante, partido_id))
    mysql.connection.commit()
    cur.close()  
    return redirect(url_for('ver_playoff_panteras'))  
# Ruta para eliminar las eliminatorias
@app.route('/eliminar_playoff_panteras/<string:eliminatoria>', methods=['POST'])
def eliminar_playoff_panteras(eliminatoria):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM playoff_panteras WHERE eliminatoria = %s', [eliminatoria])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('ver_playoff_panteras'))
# Ruta para mostrar los playoffs de CPLV Munia Panteras
@app.route('/playoffs_panteras/')
def playoffs_panteras():
    # Obtener datos de las eliminatorias
    cursor = mysql.connection.cursor()
    eliminatorias = ['semifinales','final','play-out']
    datos_playoff = {}
    for eliminatoria in eliminatorias:
        cursor.execute("SELECT * FROM playoff_panteras WHERE eliminatoria = %s", [eliminatoria])
        partidos = cursor.fetchall()
        datos_playoff[eliminatoria] = partidos
    cursor.close()
    return render_template('playoffs/panteras_playoff.html', datos_playoff=datos_playoff)
# Fin playoff 

# Playoff Ponce Valladolid
# Crear formulario para los grupos del playoff Ponce
@app.route('/admin/crear_playoff_ponce', methods=['GET', 'POST'])
def crear_playoff_ponce():
    if request.method == 'POST':
        encuentros = request.form.get('encuentros')
        print(f"Encuentros: {encuentros}")
        num_partidos = int(request.form.get('num_partidos', 0))
        cur = mysql.connection.cursor()
        for i in range(num_partidos):
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            local = request.form.get(f'local{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            visitante = request.form.get(f'visitante{i}')
            # Verificar si algún campo es None y asignar valores por defecto
            if fecha is None:
                fecha = ''
            if hora is None:
                hora = ''
            if local is None:
                local = ''
            if resultadoA is None:
                resultadoA = ''
            if resultadoB is None:
                resultadoB = ''
            if visitante is None:
                visitante = ''
            if encuentros is None:
                encuentros = '' 
            cur.execute("""
                INSERT INTO playoff_ponce (encuentros, fecha, hora, local, resultadoA, resultadoB, visitante)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (encuentros, fecha, hora, local, resultadoA, resultadoB, visitante))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('ver_playoff_ponce'))
    # Renderizar el formulario para crear la copa UEMC
    return render_template('admin/crear_playoff_ponce.html')
# Actualizar clasificación de los grupos
def actualizar_clasificacion_ponce(clasificacion_por_grupo_ponce, local, resultado_local, resultado_visitante, visitante):
    resultado_local = int(resultado_local) if resultado_local.isdigit() else None
    resultado_visitante = int(resultado_visitante) if resultado_visitante.isdigit() else None
    # Asegurarse de que cada grupo tenga una entrada en la clasificación
    if grupo not in clasificacion_por_grupo_ponce:
        clasificacion_por_grupo_ponce[grupo] = {}
    if local not in clasificacion_por_grupo_ponce[grupo]:
        clasificacion_por_grupo_ponce[grupo][local] = {'nombre': local, 'jugados': 0, 'ganados': 0, 'perdidos': 0,'puntos': 0}
    if visitante not in clasificacion_por_grupo_ponce[grupo]:
        clasificacion_por_grupo_ponce[grupo][visitante] = {'nombre': visitante, 'jugados': 0, 'ganados': 0, 'perdidos': 0, 'puntos': 0}
    # Actualizar los partidos jugados
    if resultado_local is not None and resultado_visitante is not None:
        clasificacion_por_grupo_ponce[grupo][local]['jugados'] += 1
        clasificacion_por_grupo_ponce[grupo][visitante]['jugados'] += 1
        # Determinar el resultado del partido
        if resultado_local > resultado_visitante:
            clasificacion_por_grupo_ponce[grupo][local]['ganados'] += 1
            clasificacion_por_grupo_ponce[grupo][local]['puntos'] += 2
            clasificacion_por_grupo_ponce[grupo][visitante]['perdidos'] += 1
            clasificacion_por_grupo_ponce[grupo][visitante]['puntos'] += 1
        elif resultado_local < resultado_visitante:
            clasificacion_por_grupo_ponce[grupo][visitante]['ganados'] += 1
            clasificacion_por_grupo_ponce[grupo][visitante]['puntos'] += 2
            clasificacion_por_grupo_ponce[grupo][local]['perdidos'] += 1
            clasificacion_por_grupo_ponce[grupo][local]['puntos'] += 1
        else:
            clasificacion_por_grupo_ponce[grupo][local]['puntos'] += 1
            clasificacion_por_grupo_ponce[grupo][visitante]['puntos'] += 1
    return clasificacion_por_grupo_ponce
# Recalcular clasificación
def recalcular_clasificaciones_ponce(partidos):
    clasificaciones_ponce = {}
    enfrentamientos_directos_ponce = {}
    for partido in partidos:
        grupo = partido.get('encuentros')
        local = partido['local']
        visitante = partido['visitante']
        resultado_local = int(partido['resultadoA']) if partido['resultadoA'].isdigit() else None
        resultado_visitante = int(partido['resultadoB']) if partido['resultadoB'].isdigit() else None
        if grupo not in clasificaciones_ponce:
            clasificaciones_ponce[grupo] = {}
        # Inicializar equipos si no existen
        if local not in clasificaciones_ponce[grupo]:
            clasificaciones_ponce[grupo][local] = {'jugados': 0, 'ganados': 0, 'perdidos': 0, 'puntos': 0}
        if visitante not in clasificaciones_ponce[grupo]:
            clasificaciones_ponce[grupo][visitante] = {'jugados': 0, 'ganados': 0, 'perdidos': 0, 'puntos': 0}
        # Actualizar estadísticas de partidos
        if resultado_local is not None and resultado_visitante is not None:
            clasificaciones_ponce[grupo][local]['jugados'] += 1
            clasificaciones_ponce[grupo][visitante]['jugados'] += 1
            if resultado_local > resultado_visitante:
                clasificaciones_ponce[grupo][local]['ganados'] += 1
                clasificaciones_ponce[grupo][local]['puntos'] += 2
                clasificaciones_ponce[grupo][visitante]['perdidos'] += 1
                clasificaciones_ponce[grupo][visitante]['puntos'] += 1
            elif resultado_local < resultado_visitante:
                clasificaciones_ponce[grupo][visitante]['ganados'] += 1
                clasificaciones_ponce[grupo][visitante]['puntos'] += 2
                clasificaciones_ponce[grupo][local]['perdidos'] += 1
                clasificaciones_ponce[grupo][local]['puntos'] += 1
            else:
                clasificaciones_ponce[grupo][local]['puntos'] += 1
                clasificaciones_ponce[grupo][visitante]['puntos'] += 1
        # Almacenar el resultado del enfrentamiento directo
        if local not in enfrentamientos_directos_ponce:
            enfrentamientos_directos_ponce[local] = {}
        if visitante not in enfrentamientos_directos_ponce:
            enfrentamientos_directos_ponce[visitante] = {}
        if resultado_local is not None and resultado_visitante is not None:
            enfrentamientos_directos_ponce[local][visitante] = resultado_local - resultado_visitante
            enfrentamientos_directos_ponce[visitante][local] = resultado_visitante - resultado_local        
    return clasificaciones_ponce, enfrentamientos_directos_ponce
# Función para obtener equipos desde la base de datos
def obtener_equipos_desde_bd_ponce():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, encuentros, fecha, hora, local, resultadoA, resultadoB, visitante FROM playoff_ponce")
    partidos = cur.fetchall()
    cur.close()
    # Definir los grupos y fases de eliminatorias
    grupos_ponce = {'grupoA', 'grupoB'}
    fases_eliminatorias_ponce = {'finalA', 'finalB'}
    equipos_por_encuentros_ponce = {}
    eliminatorias_ponce = {'finalA': {'partidos': []}, 'finalB': {'partidos': []}}
    for partido in partidos:
        grupo_o_fase = partido.get('encuentros')
        if grupo_o_fase in fases_eliminatorias_ponce:
            # Añadir partidos a la fase de eliminación correspondiente
            eliminatorias_ponce[grupo_o_fase]['partidos'].append(partido)
        elif grupo_o_fase in grupos_ponce:
            # Añadir equipos y partidos a los grupos
            if grupo_o_fase not in equipos_por_encuentros_ponce:
                equipos_por_encuentros_ponce[grupo_o_fase] = {'equipos': [], 'partidos': []}
            local = {'nombre': partido['local'], 'jugados': 0, 'ganados': 0, 'perdidos': 0, 'puntos': 0}
            visitante = {'nombre': partido['visitante'], 'jugados': 0, 'ganados': 0, 'perdidos': 0, 'puntos': 0}
            # Añadir equipos si no existen en la lista de equipos del grupo
            if not any(e['nombre'] == local['nombre'] for e in equipos_por_encuentros_ponce[grupo_o_fase]['equipos']):
                equipos_por_encuentros_ponce[grupo_o_fase]['equipos'].append(local)
            if not any(e['nombre'] == visitante['nombre'] for e in equipos_por_encuentros_ponce[grupo_o_fase]['equipos']):
                equipos_por_encuentros_ponce[grupo_o_fase]['equipos'].append(visitante)
            equipos_por_encuentros_ponce[grupo_o_fase]['partidos'].append(partido)
        else:
            print(f"Grupo o fase no reconocido: {grupo_o_fase}")
    return equipos_por_encuentros_ponce, eliminatorias_ponce
#Obtener equipos Copa Uemc
def obtener_equipos_por_encuentros_ponce(partidos):
    equipos_por_encuentros_ponce = {}
    eliminatorias_ponce = {'finalA': {'partidos': []}, 'finalB': {'partidos': []}}
    # Clasificar partidos en grupos o eliminatorias
    for partido in partidos:
        grupo_o_fase = partido.get('encuentros')
        if grupo_o_fase in eliminatorias_ponce:
            eliminatorias_ponce[grupo_o_fase]['partidos'].append(partido)
        else:
            if grupo_o_fase not in equipos_por_encuentros_ponce:
                equipos_por_encuentros_ponce[grupo_o_fase] = {'equipos': [], 'partidos': []}
            # Añadir equipos si no existen en la lista de equipos del grupo
            local = {'nombre': partido['local'], 'jugados': 0, 'ganados': 0, 'perdidos': 0, 'puntos': 0}
            visitante = {'nombre': partido['visitante'], 'jugados': 0, 'ganados': 0, 'perdidos': 0, 'puntos': 0}
            if not any(e['nombre'] == local['nombre'] for e in equipos_por_encuentros_ponce[grupo_o_fase]['equipos']):
                equipos_por_encuentros_ponce[grupo_o_fase]['equipos'].append(local)
            if not any(e['nombre'] == visitante['nombre'] for e in equipos_por_encuentros_ponce[grupo_o_fase]['equipos']):
                equipos_por_encuentros_ponce[grupo_o_fase]['equipos'].append(visitante)
            equipos_por_encuentros_ponce[grupo_o_fase]['partidos'].append(partido)
    return equipos_por_encuentros_ponce, eliminatorias_ponce
# Obtener la información de la tabla copa_vrac
def obtener_playoff_ponce():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, encuentros, fecha, hora, local, resultadoA, resultadoB, visitante FROM playoff_ponce")
    partidos = cur.fetchall()
    cur.close()
    print("Partidos desde la BD:", partidos)  # Añadir esta línea para depuración
    return partidos
# Formatear partidos por grupo
def formatear_partidos_por_encuentros_ponce(partidos):
    encuentros_ponce = {
        'grupoA': {'id': 1, 'encuentros': 'grupoA', 'partidos': []},
        'grupoB': {'id': 2, 'encuentros': 'grupoB', 'partidos': []},
        'finalA': {'id': 3, 'encuentros': 'finalA', 'partidos': []},
        'finalB': {'id': 4, 'encuentros': 'finalB', 'partidos': []}
    }
    for partido in partidos:
        grupo = partido.get('encuentros', '')
        if grupo in encuentros_ponce:
            encuentros_ponce[grupo]['partidos'].append(partido)
        else:
            print(f"Grupo no encontrado: {grupo}")            
    return encuentros_ponce
# Crear formulario para los grupos y eliminatorias Ponce
@app.route('/admin/playoff_ponce/')
def ver_playoff_ponce():
    try:
        # Obtener todos los partidos de los Playoff Ponce
        partidos = obtener_playoff_ponce()
        # Formatear los partidos por grupos y eliminatorias
        dats6 = formatear_partidos_por_encuentros_ponce(partidos)
        # Imprimir para depuración
        print(dats6)
        # Renderizar la plantilla con los datos formateados
        return render_template('admin/playoff_ponce.html', dats6=dats6)
    except Exception as e:
        print(f"Error al obtener o formatear los datos de los Playoff Ponce: {e}")
        # Renderizar una plantilla de error o manejar el error de alguna manera
        return render_template('error.html')
# Modificar los partidos de los playoff
@app.route('/modificar_playoff_ponce/<int:id>', methods=['POST'])
def modificar_playoff_ponce(id):
    if request.method == 'POST':
        encuentros = request.form.get('encuentros')
        num_partidos = int(request.form.get('num_partidos', 0))
        try:
            cur = mysql.connection.cursor()
            # Actualizar la eliminatoria de la jornada
            cur.execute('UPDATE playoff_ponce SET encuentros = %s WHERE id = %s', (encuentros, id))
            print(f"Consulta para actualizar la eliminatoria ejecutada para id {id}")
            # Actualizar los detalles de cada partido
            for i in range(num_partidos):
                partido_id = request.form.get(f'partido_id{i}')
                fecha = request.form.get(f'fecha{i}')
                hora = request.form.get(f'hora{i}')
                local = request.form.get(f'local{i}')
                resultadoA = request.form.get(f'resultadoA{i}')
                resultadoB = request.form.get(f'resultadoB{i}')
                visitante = request.form.get(f'visitante{i}')
                # Verificar que los campos obligatorios tienen valores válidos
                if all([partido_id, local, visitante]):
                    # Asignar valores predeterminados si los campos opcionales están vacíos
                    if fecha is None:
                        fecha = ''
                    if hora is None:
                        hora = ''
                    if local is None:
                        local = ''
                    if resultadoA is None:
                        resultadoA = ''
                    if resultadoB is None:
                        resultadoB = ''
                    if visitante is None:
                        visitante = ''
                    # Actualizar el partido en la base de datos
                    cur.execute('UPDATE playoff_ponce SET fecha = %s, hora = %s, local = %s, resultadoA = %s, resultadoB = %s, visitante = %s WHERE id = %s',
                                (fecha, hora, local, resultadoA, resultadoB, visitante, partido_id))
                    print(f"Consulta para actualizar el partido ejecutada para id {partido_id}")
            # Commit de la transacción
            mysql.connection.commit()
        except MySQLdb.Error as e:
            print(f"Error en la base de datos: {e}")
            mysql.connection.rollback()  # Revertir cambios en caso de error
        finally:
            if 'cur' in locals() and cur:
                cur.close()  # Cerrar cursor
        return redirect(url_for('ver_playoff_ponce'))
    return render_template('tu_template.html')
#Eliminar partidos Copa UEMC
@app.route('/eliminar_playoff_ponce/<string:identificador>', methods=['POST'])
def eliminar_playoff_ponce(identificador):
    cur = mysql.connection.cursor()
    try:
        if identificador.startswith('grupo') or identificador in ['finalA', 'finalB']:
            cur.execute('DELETE FROM playoff_ponce WHERE encuentros = %s', [identificador])
            mysql.connection.commit()
            flash('Partidos eliminados correctamente', 'success')
        else:
            flash('Identificador de encuentros no válido', 'error')
    except Exception as e:
        flash(f'Error al eliminar partidos: {str(e)}', 'error')
    finally:
        cur.close()
    return redirect(url_for('ver_playoff_ponce'))
# Ruta para mostrar la copa UEMC
@app.route('/playoffs_ponce/')
def playoff_ponce():
    partidos = obtener_playoff_ponce()
    equipos_por_encuentros, eliminatorias = obtener_equipos_por_encuentros_ponce(partidos)
    clasificaciones, enfrentamientos_directos = recalcular_clasificaciones_ponce(partidos)
    # Convertir clasificaciones a una estructura adecuada para la vista
    data_clasificaciones = {}
    for grupo, equipos in clasificaciones.items():
        # Ordenar equipos primero por puntos, luego por victorias, derrotas, y partidos jugados
        equipos_ordenados = sorted(equipos.items(), key=lambda item: (-item[1]['puntos'], item[1]['ganados'], item[1]['perdidos'], -item[1]['jugados']))      
        # Aplicar el criterio de desempate basado en enfrentamientos directos
        def criterio_enfrentamientos_directos(equipo1, equipo2):
            if equipo1 in enfrentamientos_directos and equipo2 in enfrentamientos_directos[equipo1]:
                resultado_directo = enfrentamientos_directos[equipo1][equipo2]
                return resultado_directo  # Resultado positivo indica que equipo1 ganó
            return 0
        # Crear una lista ordenada usando el criterio de desempate de enfrentamientos directos
        equipos_ordenados = sorted(equipos_ordenados, key=lambda item: (
            -item[1]['puntos'], 
            item[1]['ganados'], 
            item[1]['perdidos'], 
            -item[1]['jugados'],
            -criterio_enfrentamientos_directos(item[0], item[0])
        ))
        # Ajustar el orden para el desempate directo
        for i in range(len(equipos_ordenados)):
            for j in range(i + 1, len(equipos_ordenados)):
                equipo_a, stats_a = equipos_ordenados[i]
                equipo_b, stats_b = equipos_ordenados[j]
                if stats_a['puntos'] == stats_b['puntos'] and stats_a['ganados'] == stats_b['ganados'] and stats_a['perdidos'] == stats_b['perdidos']:
                    resultado_directo = criterio_enfrentamientos_directos(equipo_a, equipo_b)
                    if resultado_directo > 0:  # equipo_a ganó el enfrentamiento directo
                        # Intercambiar posiciones para que equipo_a quede por encima de equipo_b
                        equipos_ordenados[i], equipos_ordenados[j] = equipos_ordenados[j], equipos_ordenados[i]
                    elif resultado_directo < 0:  # equipo_b ganó el enfrentamiento directo
                        # Intercambiar posiciones para que equipo_b quede por encima de equipo_a
                        equipos_ordenados[i], equipos_ordenados[j] = equipos_ordenados[j], equipos_ordenados[i]
        data_clasificaciones[grupo] = equipos_ordenados
    return render_template('playoffs/ponce_playoff.html', equipos_por_encuentros=equipos_por_encuentros, eliminatorias=eliminatorias, clasificaciones=data_clasificaciones)
# Fin copa UEMC Valladolid

if __name__ == '__main__':
    app.secret_key = 'pinchellave'
    app.run(debug=True)