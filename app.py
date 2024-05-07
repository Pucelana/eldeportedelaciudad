from flask import Flask
from flask import render_template, request, redirect,url_for, session, render_template_string, jsonify
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
from flask_caching import Cache
from collections import defaultdict
from werkzeug.security import generate_password_hash, check_password_hash
import os
import uuid
import json

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
"""app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'app_suculentas'
mysql = MySQL(app)"""

# Función para cargar las credenciales desde el archivo JSON
# Función para verificar si el usuario está autenticado
credenciales = {}
json_path = 'json/acceso.json'
def esta_autenticado():
    return 'usuario' in session
def cargar_credenciales():
    global credenciales
    try:
        with open('json/acceso.json', 'r') as file:
            credenciales = json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        # Manejar el caso en el que el archivo JSON esté vacío o no exista
        pass
    return credenciales
# Función para guardar las credenciales en el archivo JSON
def guardar_credenciales(credenciales):
    with open('json/acceso.json', 'w') as file:
        json.dump(credenciales, file)
# Función para verificar las credenciales de inicio de sesión
def verificar_credenciales(email, password):
    credenciales = cargar_credenciales()
    if email in credenciales:
        stored_password = credenciales[email]['password']
        if check_password_hash(stored_password, password):
            return True
    return False
# Variable global para verificar si hay un administrador registrado
administrador_registrado = False
@app.route('/registro', methods=['GET', 'POST'])
def registro_admin():
    global administrador_registrado, credenciales
    if administrador_registrado:
        return redirect(url_for('news'))  
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']       
        # Verificar si el email ya está registrado
        if email in credenciales:
            return redirect(url_for('news'))
        # Encriptar la contraseña antes de guardarla
        hashed_password = generate_password_hash(password)
        # Guardar las credenciales en el archivo JSON
        credenciales[email] = {'password': hashed_password}
        with open(json_path, 'w') as file:
            json.dump(credenciales, file)       
        administrador_registrado = True
        session['usuario'] = email  # Autenticar al administrador
        return redirect(url_for('news'))   
    return render_template('admin/registro.html')
@app.route('/news', methods=['GET', 'POST'])
def news():
    # Verificar si el usuario está autenticado
    if not esta_autenticado():
        return redirect(url_for('registro_admin'))

    # Si la solicitud es POST, verificar las credenciales antes de mostrar el formulario de creación de noticias
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if not verificar_credenciales(email, password):
            return redirect(url_for('news'))

        return render_template('admin/crear_noticia.html')

    # Si la solicitud es GET, renderizar la plantilla normalmente
    return render_template('admin/home.html')

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
"""@app.route('/publicar_noticia/<string:id>', methods=['POST'])
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
# Página inicio y resultados
@app.route('/')
def sitio_home():
    nuevos_resultados = [dato for dato in resultados if dato]
    return render_template('sitio/home.html', nuevos_resultados=nuevos_resultados)
# Creación de partidos y resultados
horarios_partidos = 'json/horarios.json'
def guardar_horarios(data):
    with open(horarios_partidos, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)     
def cargar_resultados_desde_archivo():
    try:
        with open(horarios_partidos, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except json.decoder.JSONDecodeError:
        return []
resultados = cargar_resultados_desde_archivo()   
# Ruta de los resultados creados
@app.route('/admin/pub_marcadores')
def pub_marcadores():
    resultados_publicados = cargar_resultados_desde_archivo()    
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
    guardar_horarios_en_archivo(resultados)
    return redirect(url_for('pub_marcadores'))
# Toma la lista de los resultados y los guarda
def guardar_horarios_en_archivo(data):
    # Ruta del archivo donde guardar los resultados
    archivo_horarios = 'json/horarios.json'
    # Guardar en el archivo
    with open(archivo_horarios, 'w', encoding='utf-8') as archivo:
        json.dump(data, archivo)        
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
    global resultados
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
            # Guardar los cambios en el archivo JSON
            guardar_horarios_en_archivo(resultados)
    return redirect(url_for('pub_marcadores'))
# Ruta para eliminar los resultados
@app.route('/eliminar_resultado/<string:id>', methods=['POST'])
def eliminar_resultado(id):
    global resultados
    resultados = [r for r in resultados if r['id'] != id]
    guardar_resultados_en_archivo(resultados)
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
"""# Ruta playoff de baloncesto
@app.route('/playoff/baloncesto')
def playoff_baloncesto():
    return render_template('playoffs/baloncesto.html')
# Ruta playoff de fútbol
@app.route('/playoff/futbol')
def playoff_futbol():
    return render_template('playoffs/futbol.html')
# Ruta playoff de balonmano
@app.route('/playoff/balonmano')
def playoff_balonmano():
    return render_template('playoffs/balonmano.html')
# Ruta playoff de hockey
@app.route('/playoff/hockey')
def playoff_hockey():
    return render_template('playoffs/hockey.html')
# Ruta playoff de rugby
@app.route('/playoff/rugby')
def playoff_rugby():
    return render_template('playoffs/rugby.html')"""
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

# EQUIPOS BALONCESTO
#Todo el proceso de calendario y clasificación del UEMC
# Rutas de partidos UEMC
part_uemc = 'json/partidos_uemc.json'
def guardar_datos_uemc(data):
    # Guardar los datos en el archivo JSON
    with open(part_uemc, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)
def obtener_datos_uemc():
    try:
    # Leer los datos desde el archivo JSON
      with open(part_uemc, 'r', encoding='utf-8') as file:
        data = json.load(file)
      return data
    except json.decoder.JSONDecodeError:
        # Manejar archivo vacío, inicializar con una estructura JSON válida
        return []
# Partidos UEMC
@app.route('/admin/calendario_uemc')
def calendarios_uemc():
    data = obtener_datos_uemc()
    print(data)
    return render_template('admin/calend_uemc.html', data=data)
# Ingresar los resultados de los partidos UEMC
@app.route('/admin/crear_calendario_uemc', methods=['POST'])
def ingresar_resultado_uemc():
    data = obtener_datos_uemc()
    num_partidos = int(request.form.get('num_partidos', 0))
    jornada_nombre = request.form.get('nombre')
    jornada_existente = next((j for j in data if j["nombre"] == jornada_nombre), None)
    if jornada_existente:
        # Si la jornada ya existe, utiliza su identificador existente
        jornada_id = jornada_existente["id"]
        jornada = jornada_existente
    else:
        # Si la jornada no existe, crea un nuevo identificador
        jornada_id = str(uuid.uuid4())
        jornada = {"id": jornada_id, "nombre": jornada_nombre, "partidos": []}
        data.append(jornada)
    for i in range(num_partidos):
        #id_nuevo = str(uuid.uuid4())
        fecha = request.form.get(f'fecha{i}')
        hora = request.form.get(f'hora{i}')
        equipoLocal = request.form.get(f'local{i}')
        resultadoA = request.form.get(f'resultadoA{i}')
        resultadoB = request.form.get(f'resultadoB{i}')
        equipoVisitante = request.form.get(f'visitante{i}')
        nuevo_partido = {
            #'id': id_nuevo,
            'fecha' : fecha,
            'hora' :hora,
            'local': equipoLocal,
            'resultadoA': resultadoA,
            'resultadoB': resultadoB,
            'visitante': equipoVisitante
        }
        jornada["partidos"].append(nuevo_partido)
        
    guardar_datos_uemc(data)
    return redirect(url_for('calendarios_uemc'))
# Toma la lista de los resultados y los guarda
def guardar_partidos_en_archivo_uemc(data):
    arch_guardar_uemc = 'json/partidos_uemc.json'
    # Guardar en el archivo
    with open(arch_guardar_uemc, 'w', encoding='UTF-8') as archivo:
        json.dump(data, archivo)
# Modificar los partidos de cada jornada
@app.route('/modificar_jornada_uemc/<string:id>', methods=['POST'])
def modificar_jornada_uemc(id):
    data = obtener_datos_uemc()
    if request.method == 'POST':
        jornada_nombre = request.form.get('nombre')
        resultados_a_modificar = next((result for result in data if result['id'] == id), None)
        if resultados_a_modificar:
            resultados_a_modificar['nombre'] = jornada_nombre
            resultados_a_modificar['partidos'] = []  # Reiniciar la lista de partidos
            for i in range(9):  # Ajusta según la cantidad máxima de partidos
                equipoLocal = request.form.get(f'local{i}')
                resultadoA = request.form.get(f'resultadoA{i}')
                resultadoB = request.form.get(f'resultadoB{i}')
                equipoVisitante = request.form.get(f'visitante{i}')
                fecha = request.form.get(f'fecha{i}')
                hora = request.form.get(f'hora{i}')
                nuevo_partido = {
                    'local': equipoLocal,
                    'resultadoA': resultadoA,
                    'resultadoB': resultadoB,
                    'visitante': equipoVisitante,
                    'fecha' : fecha,
                    'hora' : hora
                }
                resultados_a_modificar['partidos'].append(nuevo_partido)
            # Guardar los cambios en el archivo JSON
            guardar_partidos_en_archivo_uemc(data)            
            return redirect(url_for('calendarios_uemc'))
    return redirect(url_for('calendarios_uemc'))
# Ruta para borrar jornadas
@app.route('/eliminar_jornada_uemc/<string:id>', methods=['POST'])
def eliminar_jornada_uemc(id):
    data = obtener_datos_uemc()
    jornada_a_eliminar = [j for j in data if j['id'] != id]  # Filtrar las jornadas diferentes de la que se va a eliminar
    guardar_partidos_en_archivo_uemc(jornada_a_eliminar)
    # Redirigir a la página de encuentros_uemc (o a donde desees después de eliminar)
    return redirect(url_for('calendarios_uemc'))
# PlayOff UEMC Valladolid
playoff_uemc = 'json_playoff/playoff_uemc.json'
def guardar_playoff_uemc(datas4):
    with open(playoff_uemc, 'w', encoding='utf-8') as file:
        json.dump(datas4, file, indent=4)
def obtener_playoff_uemc():
    try:
        with open(playoff_uemc, 'r', encoding='utf-8') as file:
            datas4 = json.load(file)
        return datas4
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return {'cuartos': [], 'semifinales': [], 'final': []}
nuevos_enfrentamientos_uemc = []
partido_uemc = None
# Crear formulario para los playoff
@app.route('/admin/playoff_uemc/')
def ver_playoff_uemc():
    datas4 = obtener_playoff_uemc()
    return render_template('admin/playoff_uemc.html', datas4=datas4)
# Crear formulario para los playoff
@app.route('/admin/crear_playoff_uemc', methods=['GET', 'POST'])
def crear_playoff_uemc():
    # Obtener los enfrentamientos actuales del archivo JSON
    datas4 = obtener_playoff_uemc()
    if request.method == 'POST':
        # Obtener la etapa del torneo seleccionada por el usuario
        eliminatoria = request.form.get('eliminatoria')
        # Verificar el número máximo de partidos permitidos según la etapa del torneo
        if eliminatoria == 'cuartos':
            max_partidos = 12
        elif eliminatoria == 'semifinales':
            max_partidos = 2
        elif eliminatoria == 'final':
            max_partidos = 1
        else:
            # Manejar caso no válido
            return "Etapa de torneo no válida"
        # Recuperar los datos del formulario y procesarlos
        num_partidos_str = request.form.get('num_partidos', '0')  # Valor predeterminado '0' si num_partidos está vacío
        num_partidos_str = num_partidos_str.strip()  # Eliminar espacios en blanco
        if num_partidos_str:
            num_partidos = int(num_partidos_str)
        else:
            num_partidos = 0  # Valor predeterminado si num_partidos está vacío
        # Si num_partidos es cero, se ignora la validación
        if num_partidos < 0:
            return "Número de partidos no válido"
        # Crear un identificador único para la eliminatoria
        eliminatoria_id = str(uuid.uuid4())  # Generar un UUID único
        # Crear un nuevo diccionario con los datos de la eliminatoria
        eliminatoria_data = {
            'id': eliminatoria_id,
            'partidos': []
        }
        # Recuperar los datos de cada partido del formulario
        for i in range(num_partidos):
            local = request.form.get(f'local{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            visitante = request.form.get(f'visitante{i}')
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            # Crear un nuevo diccionario con los datos del partido
            partido = {
                'local': local,
                'resultadoA': resultadoA,
                'resultadoB': resultadoB,
                'visitante': visitante,
                'fecha' : fecha,
                'hora' : hora  
            }
            # Agregar el partido a la lista de partidos de la eliminatoria
            eliminatoria_data['partidos'].append(partido)
            # Agregar los nuevos enfrentamientos a la lista correspondiente
        datas4[eliminatoria] = eliminatoria_data
         # Agregar los nuevos enfrentamientos a la lista correspondiente
        nuevos_enfrentamientos.clear()  
        # Guardar la lista de partidos en el archivo JSON
        guardar_playoff_uemc(datas4)
        # Redireccionar a la página de visualización del playoff
        return redirect(url_for('ver_playoff_uemc'))
    # Si no es una solicitud POST, renderizar el formulario
    return render_template('admin/playoff_uemc.html', datas4=datas4)
# Toma la lista de los playoff y los guarda
def guardar_playoff_en_archivo_uemc(datas4):
    arch_guardar_playoff_uemc = 'json_playoff/playoff_uemc.json'
    # Guardar en el archivo
    with open(arch_guardar_playoff_uemc, 'w', encoding='UTF-8') as archivo:
        json.dump(datas4, archivo)
# Modificar los partidos de los playoff
@app.route('/modificar_eliminatoria_uemc/<string:id>', methods=['GET', 'POST'])
def modificar_playoff_uemc(id):
    datas4 = obtener_playoff_uemc()
    # Buscar la eliminatoria correspondiente al ID proporcionado
    eliminatoria_encontrada = None
    for eliminatoria, datos_eliminatoria in datas4.items():
        if datos_eliminatoria['id'] == id:
            eliminatoria_encontrada = datos_eliminatoria
            break
    if not eliminatoria_encontrada:
        return "Eliminatoria no encontrada"
    if request.method == 'POST':
        nuevos_partidos = []
        for index, partido in enumerate(eliminatoria_encontrada['partidos']):
            local = request.form.get(f'local{index}')
            resultadoA = request.form.get(f'resultadoA{index}')
            resultadoB = request.form.get(f'resultadoB{index}')
            visitante = request.form.get(f'visitante{index}')
            fecha = request.form.get(f'fecha{index}')
            hora = request.form.get(f'hora{index}')
            # Actualizar los datos del partido
            partido['local'] = local
            partido['resultadoA'] = resultadoA
            partido['resultadoB'] = resultadoB
            partido['visitante'] = visitante
            partido['fecha'] = fecha
            partido['hora'] = hora
            nuevos_partidos.append(partido)   
        eliminatoria_encontrada['partidos'] = nuevos_partidos       
        # Guardar los cambios en el archivo JSON
        guardar_playoff_uemc(datas4)       
        # Redireccionar a la página de visualización del playoff
        return redirect(url_for('ver_playoff_uemc')) 
# Crear la clasificación UEMC
def generar_clasificacion_analisis_baloncesto_uemc(data, total_partidos_temporada_uemc):
    default_dict = defaultdict(lambda: {})
    clasificacion = defaultdict(lambda: {'jugados': 0, 'ganados': 0, 'perdidos': 0, 'favor': 0, 'contra': 0, 'diferencia_canastas': 0, 'puntos': 0})
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
    # Ordena la clasificación por puntos y diferencia de canastas
    clasificacion_ordenada = [{'equipo': equipo, 'datos': datos} for equipo, datos in sorted(clasificacion.items(), key=lambda x: (x[1]['puntos'], x[1]['diferencia_canastas']), reverse=True)]
    print(generar_clasificacion_analisis_baloncesto_uemc)
    return clasificacion_ordenada
# Ruta para mostrar la clasificación y análisis del UEMC
@app.route('/equipos_basket/clasif_analisis_uemc/')
def clasif_analisis_uemc():
    data = obtener_datos_uemc()
    total_partidos_temporada_uemc = 34
    # Llama a la función para generar la clasificación y análisis
    clasificacion_analisis_uemc = generar_clasificacion_analisis_baloncesto_uemc(data, total_partidos_temporada_uemc)
    # Ordena la clasificación por puntos y diferencia de canastas
    clasificacion_analisis_uemc = sorted(clasificacion_analisis_uemc, key=lambda x: (x['datos']['ganados'], x['datos']['diferencia_canastas']), reverse=True)
    # Calcular la proximidad
    #proximidad = calcular_proximidad(data, clasificacion_analisis, total_partidos_temporada)
    return render_template('equipos_basket/clasif_analisis_uemc.html', clasificacion_analisis_uemc=clasificacion_analisis_uemc)
# Ruta para mostrar los playoffs del UEMC Valladolid
@app.route('/playoffs_uemc/')
def playoffs_uemc():
    # Obtener datos de las eliminatorias
    datas4 = obtener_playoff_uemc()
    return render_template('playoffs/uemc_playoff.html', datas4=datas4)
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
# Fin proceso del UEMC

#Todo el proceso de calendario y clasificación del Ponce
# Ruta de partidos Ponce Valladolid
part_ponce = 'json/partidos_ponce.json'
def guardar_datos_ponce(data1):
    # Guardar los datos en el archivo JSON
    with open(part_ponce, 'w', encoding='utf-8') as file:
        json.dump(data1, file, indent=4)
def obtener_datos_ponce():
    try:
    # Leer los datos desde el archivo JSON
      with open(part_ponce, 'r', encoding='utf-8') as file:
        data1 = json.load(file)
      return data1
    except json.decoder.JSONDecodeError:
        # Manejar archivo vacío, inicializar con una estructura JSON válida
        return []
# Partidos UEMC
@app.route('/admin/calendario_ponce')
def calend_ponce():
    data1 = obtener_datos_ponce()
    print(data1)
    return render_template('admin/calend_ponce.html', data1=data1)
# Ingresar los resultados de los partidos Ponce
@app.route('/admin/crear_calendario_ponce', methods=['POST'])
def ingresar_resul_ponce():
    data1 = obtener_datos_ponce()
    nums_partidos = int(request.form.get('num_partidos', 0))
    jornada_nombre = request.form.get('nombre')
    jornada_existente = next((j for j in data1 if j["nombre"] == jornada_nombre), None)
    if jornada_existente:
        # Si la jornada ya existe, utiliza su identificador existente
        jornada_id = jornada_existente["id"]
        jornada = jornada_existente
    else:
        # Si la jornada no existe, crea un nuevo identificador
        jornada_id = str(uuid.uuid4())
        jornada = {"id": jornada_id, "nombre": jornada_nombre, "partidos": []}
        data1.append(jornada)
    for i in range(nums_partidos):
        #id_nuevo = str(uuid.uuid4())
        fecha = request.form.get(f'fecha{i}')
        hora = request.form.get(f'hora{i}')
        equipoLocal = request.form.get(f'local{i}')
        resultadoA = request.form.get(f'resultadoA{i}')
        resultadoB = request.form.get(f'resultadoB{i}')
        equipoVisitante = request.form.get(f'visitante{i}')
        nuevo_partido = {
            #'id': id_nuevo,
            'fecha' : fecha,
            'hora' : hora,
            'local': equipoLocal,
            'resultadoA': resultadoA,
            'resultadoB': resultadoB,
            'visitante': equipoVisitante            
        }
        jornada["partidos"].append(nuevo_partido)
    guardar_datos_ponce(data1)
    return redirect(url_for('calend_ponce'))
# Toma la lista de los resultados y los guarda
def guardar_partidos_en_archivo_ponce(data1):
    arch_guardar_ponce = 'json/partidos_ponce.json'
    # Guardar en el archivo
    with open(arch_guardar_ponce, 'w', encoding='UTF-8') as archivo:
        json.dump(data1, archivo)
# Modificar los partidos de cada jornada
@app.route('/modificar_jornada_ponce/<string:id>', methods=['POST'])
def modificar_jorn_ponce(id):
    data1 = obtener_datos_ponce()
    if request.method == 'POST':
        jornada_nombre = request.form.get('nombre')
        resultados_a_modificar = next((result for result in data1 if result['id'] == id), None)
        if resultados_a_modificar:
            resultados_a_modificar['nombre'] = jornada_nombre
            resultados_a_modificar['partidos'] = []  # Reiniciar la lista de partidos
            for i in range(7):  # Ajusta según la cantidad máxima de partidos
                equipoLocal = request.form.get(f'local{i}')
                resultadoA = request.form.get(f'resultadoA{i}')
                resultadoB = request.form.get(f'resultadoB{i}')
                equipoVisitante = request.form.get(f'visitante{i}')
                fecha = request.form.get(f'fecha{i}')
                hora = request.form.get(f'hora{i}')
                nuevo_partido = {
                    'local': equipoLocal,
                    'resultadoA': resultadoA,
                    'resultadoB': resultadoB,
                    'visitante': equipoVisitante,
                    'fecha' : fecha,
                    'hora' : hora
                }
                resultados_a_modificar['partidos'].append(nuevo_partido)
            # Guardar los cambios en el archivo JSON
            guardar_partidos_en_archivo_ponce(data1)            
            return redirect(url_for('calend_ponce'))
    return redirect(url_for('calend_ponce'))
# Ruta para borrar jornadas
@app.route('/eliminar_jorn_ponce/<string:id>', methods=['POST'])
def eliminar_jorn_ponce(id):
    data1 = obtener_datos_ponce()
    jornada_a_eliminar = [j for j in data1 if j['id'] != id]  # Filtrar las jornadas diferentes de la que se va a eliminar
    guardar_partidos_en_archivo_ponce(jornada_a_eliminar)
    # Redirigir a la página de encuentros_uemc (o a donde desees después de eliminar)
    return redirect(url_for('calend_ponce'))
# PlayOff Ponce Valladolid
playoff_ponce = 'json_playoff/playoff_ponce.json'
def guardar_playoff_ponce(datas8):
    with open(playoff_ponce, 'w', encoding='utf-8') as file:
        json.dump(datas8, file, indent=4)
def obtener_playoff_ponce():
    try:
        with open(playoff_ponce, 'r', encoding='utf-8') as file:
            datas8 = json.load(file)
        return datas8
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return {'cuartos': [], 'semifinales': [], 'final': []}
nuevos_enfrentamientos_ponce = []
partido_ponce = None
# Crear formulario para los playoff
@app.route('/admin/playoff_ponce/')
def ver_playoff_ponce():
    datas8 = obtener_playoff_ponce()
    return render_template('admin/playoff_ponce.html', datas8=datas8)
# Crear formulario para los playoff
@app.route('/admin/crear_playoff_ponce', methods=['GET', 'POST'])
def crear_playoff_ponce():
    # Obtener los enfrentamientos actuales del archivo JSON
    datas8 = obtener_playoff_ponce()
    if request.method == 'POST':
        # Obtener la etapa del torneo seleccionada por el usuario
        eliminatoria = request.form.get('eliminatoria')
        # Verificar el número máximo de partidos permitidos según la etapa del torneo
        if eliminatoria == 'cuartos':
            max_partidos = 12
        elif eliminatoria == 'semifinales':
            max_partidos = 2
        elif eliminatoria == 'final':
            max_partidos = 1
        else:
            # Manejar caso no válido
            return "Etapa de torneo no válida"
        # Recuperar los datos del formulario y procesarlos
        num_partidos_str = request.form.get('num_partidos', '0')  # Valor predeterminado '0' si num_partidos está vacío
        num_partidos_str = num_partidos_str.strip()  # Eliminar espacios en blanco
        if num_partidos_str:
            num_partidos = int(num_partidos_str)
        else:
            num_partidos = 0  # Valor predeterminado si num_partidos está vacío
        # Si num_partidos es cero, se ignora la validación
        if num_partidos < 0:
            return "Número de partidos no válido"
        # Crear un identificador único para la eliminatoria
        eliminatoria_id = str(uuid.uuid4())  # Generar un UUID único
        # Crear un nuevo diccionario con los datos de la eliminatoria
        eliminatoria_data = {
            'id': eliminatoria_id,
            'partidos': []
        }
        # Recuperar los datos de cada partido del formulario
        for i in range(num_partidos):
            local = request.form.get(f'local{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            visitante = request.form.get(f'visitante{i}')
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            # Crear un nuevo diccionario con los datos del partido
            partido = {
                'local': local,
                'resultadoA': resultadoA,
                'resultadoB': resultadoB,
                'visitante': visitante,
                'fecha' : fecha,
                'hora' : hora
            }
            # Agregar el partido a la lista de partidos de la eliminatoria
            eliminatoria_data['partidos'].append(partido)
            # Agregar los nuevos enfrentamientos a la lista correspondiente
        datas8[eliminatoria] = eliminatoria_data
         # Agregar los nuevos enfrentamientos a la lista correspondiente
        nuevos_enfrentamientos.clear()  
        # Guardar la lista de partidos en el archivo JSON
        guardar_playoff_ponce(datas8)
        # Redireccionar a la página de visualización del playoff
        return redirect(url_for('ver_playoff_ponce'))
    # Si no es una solicitud POST, renderizar el formulario
    return render_template('admin/playoff_ponce.html', datas8=datas8)
# Toma la lista de los playoff y los guarda
def guardar_playoff_en_archivo_ponce(datas8):
    arch_guardar_playoff_ponce = 'json_playoff/playoff_ponce.json'
    # Guardar en el archivo
    with open(arch_guardar_playoff_ponce, 'w', encoding='UTF-8') as archivo:
        json.dump(datas8, archivo)
# Modificar los partidos de los playoff
@app.route('/modificar_eliminatoria_ponce/<string:id>', methods=['GET', 'POST'])
def modificar_playoff_ponce(id):
    datas8 = obtener_playoff_ponce()
    # Buscar la eliminatoria correspondiente al ID proporcionado
    eliminatoria_encontrada = None
    for eliminatoria, datos_eliminatoria in datas8.items():
        if datos_eliminatoria['id'] == id:
            eliminatoria_encontrada = datos_eliminatoria
            break
    if not eliminatoria_encontrada:
        return "Eliminatoria no encontrada"
    if request.method == 'POST':
        nuevos_partidos = []
        for index, partido in enumerate(eliminatoria_encontrada['partidos']):
            local = request.form.get(f'local{index}')
            resultadoA = request.form.get(f'resultadoA{index}')
            resultadoB = request.form.get(f'resultadoB{index}')
            visitante = request.form.get(f'visitante{index}')
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            # Actualizar los datos del partido
            partido['local'] = local
            partido['resultadoA'] = resultadoA
            partido['resultadoB'] = resultadoB
            partido['visitante'] = visitante
            partido['fecha'] = fecha
            partido['hora'] = hora
            nuevos_partidos.append(partido)   
        eliminatoria_encontrada['partidos'] = nuevos_partidos       
        # Guardar los cambios en el archivo JSON
        guardar_playoff_ponce(datas8)       
        # Redireccionar a la página de visualización del playoff
        return redirect(url_for('ver_playoff_ponce')) 
# Crear la clasificación Ponce
def generar_clasificacion_analisis_baloncesto_ponce(data1, total_partidos_temporada_ponce):
    default_dict = defaultdict(lambda: {})
    clasificacion = defaultdict(lambda: {'jugados': 0, 'ganados': 0, 'perdidos': 0, 'favor': 0, 'contra': 0, 'diferencia_canastas': 0, 'puntos': 0})
    print(clasificacion)
    for jornada in data1:
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
    # Ordena la clasificación por puntos y diferencia de canastas
    clasificacion_ordenada = [{'equipo': equipo, 'datos': datos} for equipo, datos in sorted(clasificacion.items(), key=lambda x: (x[1]['puntos'], x[1]['diferencia_canastas']), reverse=True)]
    print(generar_clasificacion_analisis_baloncesto_ponce)
    return clasificacion_ordenada
# Ruta para mostrar la clasificación y análisis del Ponce
@app.route('/equipos_basket/clasif_analisis_ponce/')
def clasif_analisis_ponce():
    data1 = obtener_datos_ponce()
    total_partidos_temporada_ponce = 26
    # Llama a la función para generar la clasificación y análisis
    clasificacion_analisis_ponce = generar_clasificacion_analisis_baloncesto_ponce(data1, total_partidos_temporada_ponce)
    # Ordena la clasificación por puntos y diferencia de canastas
    clasificacion_analisis_ponce = sorted(clasificacion_analisis_ponce, key=lambda x: (x['datos']['ganados'], x['datos']['diferencia_canastas']), reverse=True)
    # Calcular la proximidad
    #proximidad = calcular_proximidad(data, clasificacion_analisis, total_partidos_temporada)
    return render_template('equipos_basket/clasif_analisis_ponce.html', clasificacion_analisis_ponce=clasificacion_analisis_ponce)
# Ruta para mostrar los playoffs del Ponce Valladolid
@app.route('/playoffs_ponce/')
def playoffs_ponce():
    # Obtener datos de las eliminatorias
    datas8 = obtener_playoff_ponce()
    return render_template('playoffs/ponce_playoff.html', datas8=datas8)
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
# Fin proceso Ponce Valladolid

#Todo el proceso de calendario y clasificación de Fundación Aliados
# Ruta de partidos Fundación Aliados
part_aliados = 'json/partidos_aliados.json'
def guardar_datos_aliados(data2):
    # Guardar los datos en el archivo JSON
    with open(part_aliados, 'w', encoding='utf-8') as file:
        json.dump(data2, file, indent=4)
def obtener_datos_aliados():
    try:
    # Leer los datos desde el archivo JSON
      with open(part_aliados, 'r', encoding='utf-8') as file:
        data2 = json.load(file)
      return data2
    except json.decoder.JSONDecodeError:
        # Manejar archivo vacío, inicializar con una estructura JSON válida
        return []
# Partidos Fundación Aliados
@app.route('/admin/calendario_aliados')
def calend_aliados():
    data2 = obtener_datos_aliados()
    print(data2)
    return render_template('admin/calend_aliados.html', data2=data2)
# Ingresar los resultados de los partidos Ponce
@app.route('/admin/crear_calendario_aliados', methods=['POST'])
def ingresar_resul_aliados():
    data2 = obtener_datos_aliados()
    nums_partidos = int(request.form.get('num_partidos', 0))
    jornada_nombre = request.form.get('nombre')
    jornada_existente = next((j for j in data2 if j["nombre"] == jornada_nombre), None)
    if jornada_existente:
        # Si la jornada ya existe, utiliza su identificador existente
        jornada_id = jornada_existente["id"]
        jornada = jornada_existente
    else:
        # Si la jornada no existe, crea un nuevo identificador
        jornada_id = str(uuid.uuid4())
        jornada = {"id": jornada_id, "nombre": jornada_nombre, "partidos": []}
        data2.append(jornada)
    for i in range(nums_partidos):
        #id_nuevo = str(uuid.uuid4())
        fecha = request.form.get(f'fecha{i}')
        hora = request.form.get(f'hora{i}')
        equipoLocal = request.form.get(f'local{i}')
        resultadoA = request.form.get(f'resultadoA{i}')
        resultadoB = request.form.get(f'resultadoB{i}')
        equipoVisitante = request.form.get(f'visitante{i}')       
        nuevo_partido = {
            #'id': id_nuevo,
            'fecha': fecha,
            'hora': hora,
            'local': equipoLocal,
            'resultadoA': resultadoA,
            'resultadoB': resultadoB,
            'visitante': equipoVisitante           
        }
        jornada["partidos"].append(nuevo_partido)
    guardar_datos_aliados(data2)
    return redirect(url_for('calend_aliados'))    
# Toma la lista de los resultados y los guarda
def guardar_partidos_en_archivo_aliados(data2):
    arch_guardar_aliados = 'json/partidos_aliados.json'
    # Guardar en el archivo
    with open(arch_guardar_aliados, 'w', encoding='UTF-8') as archivo:
        json.dump(data2, archivo)
# Modificar los partidos de cada jornada
@app.route('/modificar_jornada_aliados/<string:id>', methods=['POST'])
def modificar_jorn_aliados(id):
    data2 = obtener_datos_aliados()
    if request.method == 'POST':
        jornada_nombre = request.form.get('nombre')
        resultados_a_modificar = next((result for result in data2 if result['id'] == id), None)
        if resultados_a_modificar:
            resultados_a_modificar['nombre'] = jornada_nombre
            resultados_a_modificar['partidos'] = []  # Reiniciar la lista de partidos
            for i in range(6):  # Ajusta según la cantidad máxima de partidos
                fecha = request.form.get(f'fecha{i}')
                hora = request.form.get(f'hora{i}')   
                equipoLocal = request.form.get(f'local{i}')
                resultadoA = request.form.get(f'resultadoA{i}')
                resultadoB = request.form.get(f'resultadoB{i}')
                equipoVisitante = request.form.get(f'visitante{i}')                          
                nuevo_partido = {
                    'fecha': fecha,
                    'hora': hora,
                    'local': equipoLocal,
                    'resultadoA': resultadoA,
                    'resultadoB': resultadoB,
                    'visitante': equipoVisitante
                }
                resultados_a_modificar['partidos'].append(nuevo_partido)
            # Guardar los cambios en el archivo JSON
            guardar_partidos_en_archivo_aliados(data2)            
            return redirect(url_for('calend_aliados'))
    return redirect(url_for('calend_aliados'))
# Ruta para borrar jornadas
@app.route('/eliminar_jorn_aliados/<string:id>', methods=['POST'])
def eliminar_jorn_aliados(id):
    data2 = obtener_datos_aliados()
    jornada_a_eliminar = [j for j in data2 if j['id'] != id]  # Filtrar las jornadas diferentes de la que se va a eliminar
    guardar_partidos_en_archivo_aliados(jornada_a_eliminar)
    # Redirigir a la página de encuentros_uemc (o a donde desees después de eliminar)
    return redirect(url_for('calend_aliados'))
# PlayOff Fundación Aliados
playoff_aliados = 'json_playoff/playoff_aliados.json'
def guardar_playoff_aliados(datas9):
    with open(playoff_aliados, 'w', encoding='utf-8') as file:
        json.dump(datas9, file, indent=4)
def obtener_playoff_aliados():
    try:
        with open(playoff_aliados, 'r', encoding='utf-8') as file:
            datas9 = json.load(file)
        return datas9
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return {'cuartos': [], 'semifinales': [], 'final': []}
nuevos_enfrentamientos_aliados = []
partido_aliados = None
# Crear formulario para los playoff
@app.route('/admin/playoff_aliados/')
def ver_playoff_aliados():
    datas9 = obtener_playoff_aliados()
    return render_template('admin/playoff_aliados.html', datas9=datas9)
# Crear formulario para los playoff
@app.route('/admin/crear_playoff_aliados', methods=['GET', 'POST'])
def crear_playoff_aliados():
    # Obtener los enfrentamientos actuales del archivo JSON
    datas9 = obtener_playoff_aliados()
    if request.method == 'POST':
        # Obtener la etapa del torneo seleccionada por el usuario
        eliminatoria = request.form.get('eliminatoria')
        # Verificar el número máximo de partidos permitidos según la etapa del torneo
        if eliminatoria == 'cuartos':
            max_partidos = 12
        elif eliminatoria == 'semifinales':
            max_partidos = 2
        elif eliminatoria == 'final':
            max_partidos = 1
        else:
            # Manejar caso no válido
            return "Etapa de torneo no válida"
        # Recuperar los datos del formulario y procesarlos
        num_partidos_str = request.form.get('num_partidos', '0')  # Valor predeterminado '0' si num_partidos está vacío
        num_partidos_str = num_partidos_str.strip()  # Eliminar espacios en blanco
        if num_partidos_str:
            num_partidos = int(num_partidos_str)
        else:
            num_partidos = 0  # Valor predeterminado si num_partidos está vacío
        # Si num_partidos es cero, se ignora la validación
        if num_partidos < 0:
            return "Número de partidos no válido"
        # Crear un identificador único para la eliminatoria
        eliminatoria_id = str(uuid.uuid4())  # Generar un UUID único
        # Crear un nuevo diccionario con los datos de la eliminatoria
        eliminatoria_data = {
            'id': eliminatoria_id,
            'partidos': []
        }
        # Recuperar los datos de cada partido del formulario
        for i in range(num_partidos):
            local = request.form.get(f'local{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            visitante = request.form.get(f'visitante{i}')
            # Crear un nuevo diccionario con los datos del partido
            partido = {
                'local': local,
                'resultadoA': resultadoA,
                'resultadoB': resultadoB,
                'visitante': visitante
            }
            # Agregar el partido a la lista de partidos de la eliminatoria
            eliminatoria_data['partidos'].append(partido)
            # Agregar los nuevos enfrentamientos a la lista correspondiente
        datas9[eliminatoria] = eliminatoria_data
         # Agregar los nuevos enfrentamientos a la lista correspondiente
        nuevos_enfrentamientos.clear()  
        # Guardar la lista de partidos en el archivo JSON
        guardar_playoff_aliados(datas9)
        # Redireccionar a la página de visualización del playoff
        return redirect(url_for('ver_playoff_aliados'))
    # Si no es una solicitud POST, renderizar el formulario
    return render_template('admin/playoff_aliados.html', datas9=datas9)
# Toma la lista de los playoff y los guarda
def guardar_playoff_en_archivo_aliados(datas9):
    arch_guardar_playoff_aliados = 'json_playoff/playoff_aliados.json'
    # Guardar en el archivo
    with open(arch_guardar_playoff_aliados, 'w', encoding='UTF-8') as archivo:
        json.dump(datas9, archivo)
# Modificar los partidos de los playoff
@app.route('/modificar_eliminatoria_aliados/<string:id>', methods=['GET', 'POST'])
def modificar_playoff_aliados(id):
    datas9 = obtener_playoff_aliados()
    # Buscar la eliminatoria correspondiente al ID proporcionado
    eliminatoria_encontrada = None
    for eliminatoria, datos_eliminatoria in datas9.items():
        if datos_eliminatoria['id'] == id:
            eliminatoria_encontrada = datos_eliminatoria
            break
    if not eliminatoria_encontrada:
        return "Eliminatoria no encontrada"
    if request.method == 'POST':
        nuevos_partidos = []
        for index, partido in enumerate(eliminatoria_encontrada['partidos']):
            local = request.form.get(f'local{index}')
            resultadoA = request.form.get(f'resultadoA{index}')
            resultadoB = request.form.get(f'resultadoB{index}')
            visitante = request.form.get(f'visitante{index}')
            # Actualizar los datos del partido
            partido['local'] = local
            partido['resultadoA'] = resultadoA
            partido['resultadoB'] = resultadoB
            partido['visitante'] = visitante
            nuevos_partidos.append(partido)   
        eliminatoria_encontrada['partidos'] = nuevos_partidos       
        # Guardar los cambios en el archivo JSON
        guardar_playoff_aliados(datas9)       
        # Redireccionar a la página de visualización del playoff
        return redirect(url_for('ver_playoff_aliados'))
# Crear la clasificación Ponce
def generar_clasificacion_analisis_baloncesto_aliados(data2, total_partidos_temporada_aliados):
    default_dict = defaultdict(lambda: {})
    clasificacion = defaultdict(lambda: {'jugados': 0, 'ganados': 0, 'perdidos': 0, 'favor': 0, 'contra': 0, 'diferencia_canastas': 0, 'puntos': 0})
    print(clasificacion)
    for jornada in data2:
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
    total_partidos_temporada_aliados = 34
    # Llama a la función para generar la clasificación y análisis
    clasificacion_analisis_aliados = generar_clasificacion_analisis_baloncesto_aliados(data2, total_partidos_temporada_aliados)
    # Ordena la clasificación por puntos y diferencia de canastas
    clasificacion_analisis_aliados = sorted(clasificacion_analisis_aliados, key=lambda x: (x['datos']['ganados'], x['datos']['diferencia_canastas']), reverse=True)
    # Calcular la proximidad
    #proximidad = calcular_proximidad(data, clasificacion_analisis, total_partidos_temporada)
    return render_template('equipos_basket/clasif_analisis_aliados.html', clasificacion_analisis_aliados=clasificacion_analisis_aliados)
# Ruta para mostrar los playoffs de Fundación Aliados
@app.route('/playoffs_aliados/')
def playoffs_aliados():
    # Obtener datos de las eliminatorias
    datas9 = obtener_playoff_aliados()
    return render_template('playoffs/aliados_playoff.html', datas9=datas9)
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
# Fin proceso Fundación Aliados

# EQUIPOS FÚTBOL
#Todo el proceso de calendario y clasificación del Real Valladolid
# Ruta de partidos Real Valladolid
part_valladolid = 'json/partidos_valladolid.json'
def guardar_datos_valladolid(data3):
    # Guardar los datos en el archivo JSON
    with open(part_valladolid, 'w', encoding='utf-8') as file:
        json.dump(data3, file, indent=4)
def obtener_datos_valladolid():
    try:
    # Leer los datos desde el archivo JSON
      with open(part_valladolid, 'r', encoding='utf-8') as file:
        data3 = json.load(file)
      return data3
    except json.decoder.JSONDecodeError:
        # Manejar archivo vacío, inicializar con una estructura JSON válida
        return []
# Partidos Real Valladolid
@app.route('/admin/calend_valladolid')
def calend_valladolid():
    data3 = obtener_datos_valladolid()
    print(data3)
    return render_template('admin/calend_valladolid.html', data3=data3)
# Ingresar los resultados de los partidos del Real Valladolid
@app.route('/admin/crear_calendario_valladolid', methods=['POST'])
def ingresar_resul_valladolid():
    data3 = obtener_datos_valladolid()
    nums_partidos = int(request.form.get('num_partidos', 0))
    jornada_nombre = request.form.get('nombre')
    jornada_existente = next((j for j in data3 if j["nombre"] == jornada_nombre), None)
    if jornada_existente:
        # Si la jornada ya existe, utiliza su identificador existente
        jornada_id = jornada_existente["id"]
        jornada = jornada_existente
    else:
        # Si la jornada no existe, crea un nuevo identificador
        jornada_id = str(uuid.uuid4())
        jornada = {"id": jornada_id, "nombre": jornada_nombre, "partidos": []}
        data3.append(jornada)
    for i in range(nums_partidos):
        #id_nuevo = str(uuid.uuid4())
        equipoLocal = request.form.get(f'local{i}')
        resultadoA = request.form.get(f'resultadoA{i}')
        resultadoB = request.form.get(f'resultadoB{i}')
        equipoVisitante = request.form.get(f'visitante{i}')
        fecha = request.form.get(f'fecha{i}')
        hora = request.form.get(f'hora{i}')
        nuevo_partido = {
            #'id': id_nuevo,
            'local': equipoLocal,
            'resultadoA': resultadoA,
            'resultadoB': resultadoB,
            'visitante': equipoVisitante,
            'fecha' : fecha,
            'hora' : hora
        }
        jornada["partidos"].append(nuevo_partido)
    guardar_datos_valladolid(data3)
    return redirect(url_for('calend_valladolid')) 
# Toma la lista de los resultados y los guarda
def guardar_partidos_en_archivo_valladolid(data3):
    arch_guardar_valladolid = 'json/partidos_valladolid.json'
    # Guardar en el archivo
    with open(arch_guardar_valladolid, 'w', encoding='UTF-8') as archivo:
        json.dump(data3, archivo)
# Modificar los partidos de cada jornada
@app.route('/modificar_jornada_valladolid/<string:id>', methods=['POST'])
def modificar_jorn_valladolid(id):
    data3 = obtener_datos_valladolid()
    if request.method == 'POST':
        jornada_nombre = request.form.get('nombre')
        resultados_a_modificar = next((result for result in data3 if result['id'] == id), None)
        if resultados_a_modificar:
            resultados_a_modificar['nombre'] = jornada_nombre
            resultados_a_modificar['partidos'] = []  # Reiniciar la lista de partidos
            for i in range(11):  # Ajusta según la cantidad máxima de partidos
                equipoLocal = request.form.get(f'local{i}')
                resultadoA = request.form.get(f'resultadoA{i}')
                resultadoB = request.form.get(f'resultadoB{i}')
                equipoVisitante = request.form.get(f'visitante{i}')
                fecha = request.form.get(f'fecha{i}')
                hora = request.form.get(f'hora{i}')
                nuevo_partido = {
                    'local': equipoLocal,
                    'resultadoA': resultadoA,
                    'resultadoB': resultadoB,
                    'visitante': equipoVisitante,
                    'fecha' : fecha,
                    'hora' : hora
                }
                resultados_a_modificar['partidos'].append(nuevo_partido)
            # Guardar los cambios en el archivo JSON
            guardar_partidos_en_archivo_valladolid(data3)            
            return redirect(url_for('calend_valladolid'))
    return redirect(url_for('calend_valladolid'))
# Ruta para borrar jornadas
@app.route('/eliminar_jorn_valladolid/<string:id>', methods=['POST'])
def eliminar_jorn_valladolid(id):
    data3 = obtener_datos_valladolid()
    jornada_a_eliminar = [j for j in data3 if j['id'] != id]  # Filtrar las jornadas diferentes de la que se va a eliminar
    guardar_partidos_en_archivo_valladolid(jornada_a_eliminar)
    # Redirigir a la página de encuentros_uemc (o a donde desees después de eliminar)
    return redirect(url_for('calend_valladolid'))
# PlayOff Valladolid
playoff_valladolid = 'json_playoff/playoff_valladolid.json'
def guardar_playoff_valladolid(datas10):
    with open(playoff_valladolid, 'w', encoding='utf-8') as file:
        json.dump(datas10, file, indent=4)
def obtener_playoff_valladolid():
    try:
        with open(playoff_valladolid, 'r', encoding='utf-8') as file:
            datas10 = json.load(file)
        return datas10
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return {'semifinales': [], 'final': []}
nuevos_enfrentamientos_valladolid = []
partido_valladolid = None
# Crear formulario para los playoff
@app.route('/admin/playoff_valladolid/')
def ver_playoff_valladolid():
    datas10 = obtener_playoff_valladolid()
    return render_template('admin/playoff_valladolid.html', datas10=datas10)
# Crear formulario para los playoff
@app.route('/admin/crear_playoff_valladolid', methods=['GET', 'POST'])
def crear_playoff_valladolid():
    # Obtener los enfrentamientos actuales del archivo JSON
    datas10 = obtener_playoff_valladolid()
    if request.method == 'POST':
        # Obtener la etapa del torneo seleccionada por el usuario
        eliminatoria = request.form.get('eliminatoria')
        # Verificar el número máximo de partidos permitidos según la etapa del torneo
        if eliminatoria == 'semifinales':
            max_partidos = 4
        elif eliminatoria == 'final':
            max_partidos = 2
        else:
            # Manejar caso no válido
            return "Etapa de torneo no válida"
        # Recuperar los datos del formulario y procesarlos
        num_partidos_str = request.form.get('num_partidos', '0')  # Valor predeterminado '0' si num_partidos está vacío
        num_partidos_str = num_partidos_str.strip()  # Eliminar espacios en blanco
        if num_partidos_str:
            num_partidos = int(num_partidos_str)
        else:
            num_partidos = 0  # Valor predeterminado si num_partidos está vacío
        # Si num_partidos es cero, se ignora la validación
        if num_partidos < 0:
            return "Número de partidos no válido"
        # Crear un identificador único para la eliminatoria
        eliminatoria_id = str(uuid.uuid4())  # Generar un UUID único
        # Crear un nuevo diccionario con los datos de la eliminatoria
        eliminatoria_data = {
            'id': eliminatoria_id,
            'partidos': []
        }
        # Recuperar los datos de cada partido del formulario
        for i in range(num_partidos):
            local = request.form.get(f'local{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            visitante = request.form.get(f'visitante{i}')
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            # Crear un nuevo diccionario con los datos del partido
            partido = {
                'local': local,
                'resultadoA': resultadoA,
                'resultadoB': resultadoB,
                'visitante': visitante,
                'fecha' : fecha,
                'hora' : hora
            }
            # Agregar el partido a la lista de partidos de la eliminatoria
            eliminatoria_data['partidos'].append(partido)
            # Agregar los nuevos enfrentamientos a la lista correspondiente
        datas10[eliminatoria] = eliminatoria_data
         # Agregar los nuevos enfrentamientos a la lista correspondiente
        nuevos_enfrentamientos.clear()  
        # Guardar la lista de partidos en el archivo JSON
        guardar_playoff_valladolid(datas10)
        # Redireccionar a la página de visualización del playoff
        return redirect(url_for('ver_playoff_valladolid'))
    # Si no es una solicitud POST, renderizar el formulario
    return render_template('admin/playoff_valladolid.html', datas10=datas10)
# Toma la lista de los playoff y los guarda
def guardar_playoff_en_archivo_valladolid(datas10):
    arch_guardar_playoff_valladolid = 'json_playoff/partidos_valladolid.json'
    # Guardar en el archivo
    with open(arch_guardar_playoff_valladolid, 'w', encoding='UTF-8') as archivo:
        json.dump(datas10, archivo)
# Modificar los partidos de los playoff
@app.route('/modificar_eliminatoria_valladolid/<string:id>', methods=['GET', 'POST'])
def modificar_playoff_valladolid(id):
    datas10 = obtener_playoff_valladolid()
    # Buscar la eliminatoria correspondiente al ID proporcionado
    eliminatoria_encontrada = None
    for eliminatoria, datos_eliminatoria in datas10.items():
        if datos_eliminatoria['id'] == id:
            eliminatoria_encontrada = datos_eliminatoria
            break
    if not eliminatoria_encontrada:
        return "Eliminatoria no encontrada"
    if request.method == 'POST':
        nuevos_partidos = []
        for index, partido in enumerate(eliminatoria_encontrada['partidos']):
            local = request.form.get(f'local{index}')
            resultadoA = request.form.get(f'resultadoA{index}')
            resultadoB = request.form.get(f'resultadoB{index}')
            visitante = request.form.get(f'visitante{index}')
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            # Actualizar los datos del partido
            partido['local'] = local
            partido['resultadoA'] = resultadoA
            partido['resultadoB'] = resultadoB
            partido['visitante'] = visitante
            partido['fecha'] = fecha
            partido['hora'] = hora
            nuevos_partidos.append(partido)   
        eliminatoria_encontrada['partidos'] = nuevos_partidos       
        # Guardar los cambios en el archivo JSON
        guardar_playoff_valladolid(datas10)       
        # Redireccionar a la página de visualización del playoff
        return redirect(url_for('ver_playoff_valladolid'))
# Crear la clasificación del Real Valladolid
def generar_clasificacion_analisis_futbol_valladolid(data3, total_partidos_temporada_valladolid):
    default_dict = defaultdict(lambda: {})
    clasificacion = defaultdict(lambda: {'puntos': 0,'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'favor': 0, 'contra': 0, 'diferencia_goles': 0})
    print(clasificacion)
    for jornada in data3:
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
    total_partidos_temporada_valladolid = 42
    # Llama a la función para generar la clasificación y análisis
    clasificacion_analisis_valladolid = generar_clasificacion_analisis_futbol_valladolid(data3, total_partidos_temporada_valladolid)
    # Ordena la clasificación por puntos y diferencia de goles
    clasificacion_analisis_valladolid = sorted(clasificacion_analisis_valladolid, key=lambda x: (x['datos']['puntos'], x['datos']['diferencia_goles']), reverse=True)
    # Calcular la proximidad
    #proximidad = calcular_proximidad(data, clasificacion_analisis, total_partidos_temporada)
    return render_template('equipos_futbol/clasi_analis_vallad.html', clasificacion_analisis_valladolid=clasificacion_analisis_valladolid)
# Ruta para mostrar los playoffs del Real Valladolid
@app.route('/playoffs_valladolid/')
def playoffs_valladolid():
    # Obtener datos de las eliminatorias
    datas10 = obtener_playoff_valladolid()
    return render_template('playoffs/valladolid_playoff.html', datas10=datas10)
# Ruta y creación del calendario individual del Real Valladolid
@app.route('/equipos_futbol/calendario_vallad')
def calendarios_valladolid():
    print("Se llamo a la ruta/'equipo_futbol/calendario_vallad")
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
# Fin proceso Real Valladolid

#Todo el proceso de calendario y clasificación del Promesas
# Ruta de partidos Promesas
part_promesas = 'json/partidos_promesas.json'
def guardar_datos_promesas(data4):
    # Guardar los datos en el archivo JSON
    with open(part_promesas, 'w', encoding='utf-8') as file:
        json.dump(data4, file, indent=4)
def obtener_datos_promesas():
    try:
    # Leer los datos desde el archivo JSON
      with open(part_promesas, 'r', encoding='utf-8') as file:
        data4 = json.load(file)
      return data4
    except json.decoder.JSONDecodeError:
        # Manejar archivo vacío, inicializar con una estructura JSON válida
        return []
# Partidos Promesas
@app.route('/admin/calend_promesas')
def calend_promesas():
    data4 = obtener_datos_promesas()
    print(data4)
    return render_template('admin/calend_promesas.html', data4=data4)
# Ingresar los resultados de los partidos del Promesas
@app.route('/admin/crear_calendario_promesas', methods=['POST'])
def ingresar_resul_promesas():
    data4 = obtener_datos_promesas()
    nums_partidos = int(request.form.get('num_partidos', 0))
    jornada_nombre = request.form.get('nombre')
    jornada_existente = next((j for j in data4 if j["nombre"] == jornada_nombre), None)
    if jornada_existente:
        # Si la jornada ya existe, utiliza su identificador existente
        jornada_id = jornada_existente["id"]
        jornada = jornada_existente
    else:
        # Si la jornada no existe, crea un nuevo identificador
        jornada_id = str(uuid.uuid4())
        jornada = {"id": jornada_id, "nombre": jornada_nombre, "partidos": []}
        data4.append(jornada)
    for i in range(nums_partidos):
        #id_nuevo = str(uuid.uuid4())
        equipoLocal = request.form.get(f'local{i}')
        resultadoA = request.form.get(f'resultadoA{i}')
        resultadoB = request.form.get(f'resultadoB{i}')
        equipoVisitante = request.form.get(f'visitante{i}')
        fecha = request.form.get(f'fecha{i}')
        hora = request.form.get(f'hora{i}')
        nuevo_partido = {
            #'id': id_nuevo,
            'local': equipoLocal,
            'resultadoA': resultadoA,
            'resultadoB': resultadoB,
            'visitante': equipoVisitante,
            'fecha' : fecha,
            'hora' : hora
        }
        jornada["partidos"].append(nuevo_partido)
    guardar_datos_promesas(data4)
    return redirect(url_for('calend_promesas')) 
# Toma la lista de los resultados y los guarda
def guardar_partidos_en_archivo_promesas(data4):
    arch_guardar_promesas = 'json/partidos_promesas.json'
    # Guardar en el archivo
    with open(arch_guardar_promesas, 'w', encoding='UTF-8') as archivo:
        json.dump(data4, archivo)
# Modificar los partidos de cada jornada
@app.route('/modificar_jornada_promesas/<string:id>', methods=['POST'])
def modificar_jorn_promesas(id):
    data4 = obtener_datos_promesas()
    if request.method == 'POST':
        jornada_nombre = request.form.get('nombre')
        resultados_a_modificar = next((result for result in data4 if result['id'] == id), None)
        if resultados_a_modificar:
            resultados_a_modificar['nombre'] = jornada_nombre
            resultados_a_modificar['partidos'] = []  # Reiniciar la lista de partidos
            for i in range(9):  # Ajusta según la cantidad máxima de partidos
                equipoLocal = request.form.get(f'local{i}')
                resultadoA = request.form.get(f'resultadoA{i}')
                resultadoB = request.form.get(f'resultadoB{i}')
                equipoVisitante = request.form.get(f'visitante{i}')
                fecha = request.form.get(f'fecha{i}')
                hora = request.form.get(f'hora{i}')
                nuevo_partido = {
                    'local': equipoLocal,
                    'resultadoA': resultadoA,
                    'resultadoB': resultadoB,
                    'visitante': equipoVisitante,
                    'fecha' : fecha,
                    'hora' : hora
                }
                resultados_a_modificar['partidos'].append(nuevo_partido)
            # Guardar los cambios en el archivo JSON
            guardar_partidos_en_archivo_promesas(data4)            
            return redirect(url_for('calend_promesas'))
    return redirect(url_for('calend_promesas'))        
# Ruta para borrar jornadas
@app.route('/eliminar_jorn_promesas/<string:id>', methods=['POST'])
def eliminar_jorn_promesas(id):
    data4 = obtener_datos_promesas()
    jornada_a_eliminar = [j for j in data4 if j['id'] != id]  # Filtrar las jornadas diferentes de la que se va a eliminar
    guardar_partidos_en_archivo_promesas(jornada_a_eliminar)
    # Redirigir a la página de encuentros_uemc (o a donde desees después de eliminar)
    return redirect(url_for('calend_promesas'))        
# PlayOff Real Valladolid Promesas
playoff_promesas = 'json_playoff/playoff_promesas.json'
def guardar_playoff_promesas(datas11):
    with open(playoff_promesas, 'w', encoding='utf-8') as file:
        json.dump(datas11, file, indent=4)
def obtener_playoff_promesas():
    try:
        with open(playoff_promesas, 'r', encoding='utf-8') as file:
            datas11 = json.load(file)
        return datas11
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return {'semifinales': [], 'final': [], 'promocion': []}
nuevos_enfrentamientos_promesas = []
partido_promesas = None
# Crear formulario para los playoff
@app.route('/admin/playoff_promesas/')
def ver_playoff_promesas():
    datas11 = obtener_playoff_promesas()
    return render_template('admin/playoff_promesas.html', datas11=datas11)
# Crear formulario para los playoff
@app.route('/admin/crear_playoff_promesas', methods=['GET', 'POST'])
def crear_playoff_promesas():
    # Obtener los enfrentamientos actuales del archivo JSON
    datas11 = obtener_playoff_promesas()
    if request.method == 'POST':
        # Obtener la etapa del torneo seleccionada por el usuario
        eliminatoria = request.form.get('eliminatoria')
        # Verificar el número máximo de partidos permitidos según la etapa del torneo
        if eliminatoria == 'semifinales':
            max_partidos = 10
        elif eliminatoria == 'final':
            max_partidos = 5
        elif eliminatoria == 'promocion':
            max_partidos = 2
        else:
            # Manejar caso no válido
            return "Etapa de torneo no válida"
        # Recuperar los datos del formulario y procesarlos
        num_partidos_str = request.form.get('num_partidos', '0')  # Valor predeterminado '0' si num_partidos está vacío
        num_partidos_str = num_partidos_str.strip()  # Eliminar espacios en blanco
        if num_partidos_str:
            num_partidos = int(num_partidos_str)
        else:
            num_partidos = 0  # Valor predeterminado si num_partidos está vacío
        # Si num_partidos es cero, se ignora la validación
        if num_partidos < 0:
            return "Número de partidos no válido"
        # Crear un identificador único para la eliminatoria
        eliminatoria_id = str(uuid.uuid4())  # Generar un UUID único
        # Crear un nuevo diccionario con los datos de la eliminatoria
        eliminatoria_data = {
            'id': eliminatoria_id,
            'partidos': []
        }
        # Recuperar los datos de cada partido del formulario
        for i in range(num_partidos):
            local = request.form.get(f'local{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            visitante = request.form.get(f'visitante{i}')
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            # Crear un nuevo diccionario con los datos del partido
            partido = {
                'local': local,
                'resultadoA': resultadoA,
                'resultadoB': resultadoB,
                'visitante': visitante,
                'fecha' : fecha,
                'hora' : hora
            }
            # Agregar el partido a la lista de partidos de la eliminatoria
            eliminatoria_data['partidos'].append(partido)
            # Agregar los nuevos enfrentamientos a la lista correspondiente
        datas11[eliminatoria] = eliminatoria_data
         # Agregar los nuevos enfrentamientos a la lista correspondiente
        nuevos_enfrentamientos.clear()  
        # Guardar la lista de partidos en el archivo JSON
        guardar_playoff_promesas(datas11)
        # Redireccionar a la página de visualización del playoff
        return redirect(url_for('ver_playoff_promesas'))
    # Si no es una solicitud POST, renderizar el formulario
    return render_template('admin/playoff_promesas.html', datas11=datas11)
# Toma la lista de los playoff y los guarda
def guardar_playoff_en_archivo_promesas(datas11):
    arch_guardar_playoff_promesas = 'json_playoff/partidos_promesas.json'
    # Guardar en el archivo
    with open(arch_guardar_playoff_promesas, 'w', encoding='UTF-8') as archivo:
        json.dump(datas11, archivo)
# Modificar los partidos de los playoff
@app.route('/modificar_eliminatoria_promesas/<string:id>', methods=['GET', 'POST'])
def modificar_playoff_promesas(id):
    datas11 = obtener_playoff_promesas()
    # Buscar la eliminatoria correspondiente al ID proporcionado
    eliminatoria_encontrada = None
    for eliminatoria, datos_eliminatoria in datas11.items():
        if datos_eliminatoria['id'] == id:
            eliminatoria_encontrada = datos_eliminatoria
            break
    if not eliminatoria_encontrada:
        return "Eliminatoria no encontrada"
    if request.method == 'POST':
        nuevos_partidos = []
        for index, partido in enumerate(eliminatoria_encontrada['partidos']):
            local = request.form.get(f'local{index}')
            resultadoA = request.form.get(f'resultadoA{index}')
            resultadoB = request.form.get(f'resultadoB{index}')
            visitante = request.form.get(f'visitante{index}')
            fecha = request.form.get(f'fecha{index}')
            hora = request.form.get(f'hora{index}')
            # Actualizar los datos del partido
            partido['local'] = local
            partido['resultadoA'] = resultadoA
            partido['resultadoB'] = resultadoB
            partido['visitante'] = visitante
            partido['fecha'] = fecha
            partido['hora'] = hora
            nuevos_partidos.append(partido)   
        eliminatoria_encontrada['partidos'] = nuevos_partidos       
        # Guardar los cambios en el archivo JSON
        guardar_playoff_promesas(datas11)       
        # Redireccionar a la página de visualización del playoff
        return redirect(url_for('ver_playoff_promesas'))
# Crear la clasificación del Promesas
def generar_clasificacion_analisis_futbol_promesas(data4, total_partidos_temporada_promesas):
    default_dict = defaultdict(lambda: {})
    clasificacion = defaultdict(lambda: {'puntos': 0,'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'favor': 0, 'contra': 0, 'diferencia_goles': 0})
    print(clasificacion)
    for jornada in data4:
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
    total_partidos_temporada_promesas = 34
    # Llama a la función para generar la clasificación y análisis
    clasificacion_analisis_promesas = generar_clasificacion_analisis_futbol_promesas(data4, total_partidos_temporada_promesas)
    # Ordena la clasificación por puntos y diferencia de goles
    clasificacion_analisis_promesas = sorted(clasificacion_analisis_promesas, key=lambda x: (x['datos']['puntos'], x['datos']['diferencia_goles']), reverse=True)
    # Calcular la proximidad
    #proximidad = calcular_proximidad(data, clasificacion_analisis, total_partidos_temporada)
    return render_template('equipos_futbol/clasi_analis_prome.html', clasificacion_analisis_promesas=clasificacion_analisis_promesas)        
# Ruta para mostrar los playoffs del Real Valladolid Promesas
@app.route('/playoffs_promesas/')
def playoffs_promesas():
    # Obtener datos de las eliminatorias
    datas11 = obtener_playoff_promesas()
    return render_template('playoffs/promesas_playoff.html', datas11=datas11)
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
# Fin proceso Promesas

#Todo el proceso de calendario y clasificación del V Simancas
# Ruta de partidos V Simancas       
part_simancas = 'json/partidos_simancas.json'
def guardar_datos_simancas(data5):
    # Guardar los datos en el archivo JSON
    with open(part_simancas, 'w', encoding='utf-8') as file:
        json.dump(data5, file, indent=4)
def obtener_datos_simancas():
    try:
    # Leer los datos desde el archivo JSON
      with open(part_simancas, 'r', encoding='utf-8') as file:
        data5 = json.load(file)
      return data5
    except json.decoder.JSONDecodeError:
        # Manejar archivo vacío, inicializar con una estructura JSON válida
        return []       
# Partidos V Simancas
@app.route('/admin/calend_simancas')
def calend_simancas():
    data5 = obtener_datos_simancas()
    print(data5)
    return render_template('admin/calend_simancas.html', data5=data5)       
# Ingresar los resultados de los partidos del V Simancas
@app.route('/admin/crear_calendario_simancas', methods=['POST'])
def ingresar_resul_simancas():
    data5 = obtener_datos_simancas()
    nums_partidos = int(request.form.get('num_partidos', 0))
    jornada_nombre = request.form.get('nombre')
    jornada_existente = next((j for j in data5 if j["nombre"] == jornada_nombre), None)
    if jornada_existente:
        # Si la jornada ya existe, utiliza su identificador existente
        jornada_id = jornada_existente["id"]
        jornada = jornada_existente
    else:
        # Si la jornada no existe, crea un nuevo identificador
        jornada_id = str(uuid.uuid4())
        jornada = {"id": jornada_id, "nombre": jornada_nombre, "partidos": []}
        data5.append(jornada)
    for i in range(nums_partidos):
        #id_nuevo = str(uuid.uuid4())
        equipoLocal = request.form.get(f'local{i}')
        resultadoA = request.form.get(f'resultadoA{i}')
        resultadoB = request.form.get(f'resultadoB{i}')
        equipoVisitante = request.form.get(f'visitante{i}')
        fecha = request.form.get(f'fecha{i}')
        hora = request.form.get(f'hora{i}')
        nuevo_partido = {
            #'id': id_nuevo,
            'local': equipoLocal,
            'resultadoA': resultadoA,
            'resultadoB': resultadoB,
            'visitante': equipoVisitante,
            'fecha' : fecha,
            'hora' : hora
        }
        jornada["partidos"].append(nuevo_partido)
    guardar_datos_simancas(data5)
    return redirect(url_for('calend_simancas'))         
# Toma la lista de los resultados y los guarda
def guardar_partidos_en_archivo_simancas(data5):
    arch_guardar_simancas = 'json/partidos_simancas.json'
    # Guardar en el archivo
    with open(arch_guardar_simancas, 'w', encoding='UTF-8') as archivo:
        json.dump(data5, archivo)        
# Modificar los partidos de cada jornada
@app.route('/modificar_jornada_simancas/<string:id>', methods=['POST'])
def modificar_jorn_simancas(id):
    data5 = obtener_datos_simancas()
    if request.method == 'POST':
        jornada_nombre = request.form.get('nombre')
        resultados_a_modificar = next((result for result in data5 if result['id'] == id), None)
        if resultados_a_modificar:
            resultados_a_modificar['nombre'] = jornada_nombre
            resultados_a_modificar['partidos'] = []  # Reiniciar la lista de partidos
            for i in range(8):  # Ajusta según la cantidad máxima de partidos
                equipoLocal = request.form.get(f'local{i}')
                resultadoA = request.form.get(f'resultadoA{i}')
                resultadoB = request.form.get(f'resultadoB{i}')
                equipoVisitante = request.form.get(f'visitante{i}')
                fecha = request.form.get(f'fecha{i}')
                hora = request.form.get(f'hora{i}')
                nuevo_partido = {
                    'local': equipoLocal,
                    'resultadoA': resultadoA,
                    'resultadoB': resultadoB,
                    'visitante': equipoVisitante,
                    'fecha' : fecha,
                    'hora' : hora
                }
                resultados_a_modificar['partidos'].append(nuevo_partido)
            # Guardar los cambios en el archivo JSON
            guardar_partidos_en_archivo_simancas(data5)            
            return redirect(url_for('calend_simancas'))
    return redirect(url_for('calend_simancas'))        
# Ruta para borrar jornadas
@app.route('/eliminar_jorn_simancas/<string:id>', methods=['POST'])
def eliminar_jorn_simancas(id):
    data5 = obtener_datos_simancas()
    jornada_a_eliminar = [j for j in data5 if j['id'] != id]  # Filtrar las jornadas diferentes de la que se va a eliminar
    guardar_partidos_en_archivo_simancas(jornada_a_eliminar)
    # Redirigir a la página de encuentros_simancas (o a donde desees después de eliminar)
    return redirect(url_for('calend_simancas'))         
# Crear la clasificación del V Simancas
def generar_clasificacion_analisis_futbol_simancas(data5, total_partidos_temporada_simancas):
    default_dict = defaultdict(lambda: {})
    clasificacion = defaultdict(lambda: {'puntos': 0,'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'favor': 0, 'contra': 0, 'diferencia_goles': 0})
    print(clasificacion)
    for jornada in data5:
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
# Ruta para mostrar la clasificación y análisis del V Simancas
@app.route('/equipos_futbol/clasi_analis_siman/')
def clasif_analisis_simancas():
    data5 = obtener_datos_simancas()
    total_partidos_temporada_simancas = 30
    # Llama a la función para generar la clasificación y análisis
    clasificacion_analisis_simancas = generar_clasificacion_analisis_futbol_simancas(data5, total_partidos_temporada_simancas)
    # Ordena la clasificación por puntos y diferencia de goles
    clasificacion_analisis_simancas = sorted(clasificacion_analisis_simancas, key=lambda x: (x['datos']['puntos'], x['datos']['diferencia_goles']), reverse=True)
    # Calcular la proximidad
    #proximidad = calcular_proximidad(data, clasificacion_analisis, total_partidos_temporada)
    return render_template('equipos_futbol/clasi_analis_siman.html', clasificacion_analisis_simancas=clasificacion_analisis_simancas)         
# Ruta y creación del calendario individual del V Simancas
@app.route('/equipos_futbol/calendario_simancas')
def calendarios_simancas():
    datos5 = obtener_datos_simancas()
    nuevos_datos_simancas = [dato for dato in datos5 if dato]
    equipo_simancas = 'V Simancas'
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
# Fin proceso V Simancas

#Todo el proceso de calendario y clasificación del CD Parquesol
# Ruta de partidos CD Parquesol        
part_parquesol = 'json/partidos_parquesol.json'
def guardar_datos_parquesol(data6):
    # Guardar los datos en el archivo JSON
    with open(part_parquesol, 'w', encoding='utf-8') as file:
        json.dump(data6, file, indent=4)
def obtener_datos_parquesol():
    try:
    # Leer los datos desde el archivo JSON
      with open(part_parquesol, 'r', encoding='utf-8') as file:
        data6 = json.load(file)
      return data6
    except json.decoder.JSONDecodeError:
        # Manejar archivo vacío, inicializar con una estructura JSON válida
        return []        
# Partidos CD Parquesol
@app.route('/admin/calend_parquesol')
def calend_parquesol():
    data6 = obtener_datos_parquesol()
    print(data6)
    return render_template('admin/calend_parquesol.html', data6=data6)
# Ingresar los resultados de los partidos del CD Parquesol
@app.route('/admin/crear_calendario_parquesol', methods=['POST'])
def ingresar_resul_parquesol():
    data6 = obtener_datos_parquesol()
    nums_partidos = int(request.form.get('num_partidos', 0))
    jornada_nombre = request.form.get('nombre')
    jornada_existente = next((j for j in data6 if j["nombre"] == jornada_nombre), None)
    if jornada_existente:
        # Si la jornada ya existe, utiliza su identificador existente
        jornada_id = jornada_existente["id"]
        jornada = jornada_existente
    else:
        # Si la jornada no existe, crea un nuevo identificador
        jornada_id = str(uuid.uuid4())
        jornada = {"id": jornada_id, "nombre": jornada_nombre, "partidos": []}
        data6.append(jornada)
    for i in range(nums_partidos):
        #id_nuevo = str(uuid.uuid4())
        equipoLocal = request.form.get(f'local{i}')
        resultadoA = request.form.get(f'resultadoA{i}')
        resultadoB = request.form.get(f'resultadoB{i}')
        equipoVisitante = request.form.get(f'visitante{i}')
        fecha = request.form.get(f'fecha{i}')
        hora = request.form.get(f'hora{i}')
        nuevo_partido = {
            #'id': id_nuevo,
            'local': equipoLocal,
            'resultadoA': resultadoA,
            'resultadoB': resultadoB,
            'visitante': equipoVisitante,
            'fecha' : fecha,
            'hora' : hora
        }
        jornada["partidos"].append(nuevo_partido)
    guardar_datos_parquesol(data6)
    return redirect(url_for('calend_parquesol')) 
# Toma la lista de los resultados y los guarda
def guardar_partidos_en_archivo_parquesol(data6):
    arch_guardar_parquesol = 'json/partidos_parquesol.json'
    # Guardar en el archivo
    with open(arch_guardar_parquesol, 'w', encoding='UTF-8') as archivo:
        json.dump(data6, archivo)
# Modificar los partidos de cada jornada
@app.route('/modificar_jornada_parquesol/<string:id>', methods=['POST'])
def modificar_jorn_parquesol(id):
    data6 = obtener_datos_parquesol()
    if request.method == 'POST':
        jornada_nombre = request.form.get('nombre')
        resultados_a_modificar = next((result for result in data6 if result['id'] == id), None)
        if resultados_a_modificar:
            resultados_a_modificar['nombre'] = jornada_nombre
            resultados_a_modificar['partidos'] = []  # Reiniciar la lista de partidos
            for i in range(8):  # Ajusta según la cantidad máxima de partidos
                equipoLocal = request.form.get(f'local{i}')
                resultadoA = request.form.get(f'resultadoA{i}')
                resultadoB = request.form.get(f'resultadoB{i}')
                equipoVisitante = request.form.get(f'visitante{i}')
                fecha = request.form.get(f'fecha{i}')
                hora = request.form.get(f'hora{i}')
                nuevo_partido = {
                    'local': equipoLocal,
                    'resultadoA': resultadoA,
                    'resultadoB': resultadoB,
                    'visitante': equipoVisitante,
                    'fecha' : fecha,
                    'hora' : hora
                }
                resultados_a_modificar['partidos'].append(nuevo_partido)
            # Guardar los cambios en el archivo JSON
            guardar_partidos_en_archivo_parquesol(data6)            
            return redirect(url_for('calend_parquesol'))
    return redirect(url_for('calend_parquesol'))
# Ruta para borrar jornadas
@app.route('/eliminar_jorn_parquesol/<string:id>', methods=['POST'])
def eliminar_jorn_parquesol(id):
    data6 = obtener_datos_parquesol()
    jornada_a_eliminar = [j for j in data6 if j['id'] != id]  # Filtrar las jornadas diferentes de la que se va a eliminar
    guardar_partidos_en_archivo_parquesol(jornada_a_eliminar)
    # Redirigir a la página de encuentros_simancas (o a donde desees después de eliminar)
    return redirect(url_for('calend_parquesol')) 
# Crear la clasificación del CD Parquesol
def generar_clasificacion_analisis_futbol_parquesol(data6, total_partidos_temporada_parquesol):
    default_dict = defaultdict(lambda: {})
    clasificacion = defaultdict(lambda: {'puntos': 0,'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'favor': 0, 'contra': 0, 'diferencia_goles': 0})
    for jornada in data6:
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
    total_partidos_temporada_parquesol = 30
    # Llama a la función para generar la clasificación y análisis
    clasificacion_analisis_parquesol = generar_clasificacion_analisis_futbol_parquesol(data6, total_partidos_temporada_parquesol)
    # Ordena la clasificación por puntos y diferencia de goles
    clasificacion_analisis_parquesol = sorted(clasificacion_analisis_parquesol, key=lambda x: (x['datos']['puntos'], x['datos']['diferencia_goles']), reverse=True)
    # Calcular la proximidad
    #proximidad = calcular_proximidad(data, clasificacion_analisis, total_partidos_temporada)
    return render_template('equipos_futbol/clasi_analis_parque.html', clasificacion_analisis_parquesol=clasificacion_analisis_parquesol) 
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
# Fin proceso CD Parquesol

# EQUIPOS FÚTBOL SALA
#Todo el proceso de calendario y clasificación del Valladolid FS
# Ruta de partidos Valladolid FS
part_valladolid_fs = 'json/partidos_valladolid_fs.json'
def guardar_datos_valladolid_fs(data16):
    # Guardar los datos en el archivo JSON
    with open(part_valladolid_fs, 'w', encoding='utf-8') as file:
        json.dump(data16, file, indent=4)
def obtener_datos_valladolid_fs():
    try:
    # Leer los datos desde el archivo JSON
      with open(part_valladolid_fs, 'r', encoding='utf-8') as file:
        data16 = json.load(file)
      return data16
    except json.decoder.JSONDecodeError:
        # Manejar archivo vacío, inicializar con una estructura JSON válida
        return [] 
# Partidos Valladolid FS
@app.route('/admin/calend_valladolid_fs')
def calend_valladolid_fs():
    data16 = obtener_datos_valladolid_fs()
    print(data16)
    return render_template('admin/calend_vallad_fs.html', data16=data16)
# Ingresar los resultados de los partidos del Valladolid FS
@app.route('/admin/crear_calendario_valladolid_fs', methods=['POST'])
def ingresar_resul_valladolid_fs():
    data16 = obtener_datos_valladolid_fs()
    nums_partidos = int(request.form.get('num_partidos', 0))
    jornada_nombre = request.form.get('nombre')
    jornada_existente = next((j for j in data16 if j["nombre"] == jornada_nombre), None)
    if jornada_existente:
        # Si la jornada ya existe, utiliza su identificador existente
        jornada_id = jornada_existente["id"]
        jornada = jornada_existente
    else:
        # Si la jornada no existe, crea un nuevo identificador
        jornada_id = str(uuid.uuid4())
        jornada = {"id": jornada_id, "nombre": jornada_nombre, "partidos": []}
        data16.append(jornada)
    for i in range(nums_partidos):
        #id_nuevo = str(uuid.uuid4())
        equipoLocal = request.form.get(f'local{i}')
        resultadoA = request.form.get(f'resultadoA{i}')
        resultadoB = request.form.get(f'resultadoB{i}')
        equipoVisitante = request.form.get(f'visitante{i}')
        fecha = request.form.get(f'fecha{i}')
        hora = request.form.get(f'hora{i}')
        nuevo_partido = {
            #'id': id_nuevo,
            'local': equipoLocal,
            'resultadoA': resultadoA,
            'resultadoB': resultadoB,
            'visitante': equipoVisitante,
            'fecha' : fecha,
            'hora' : hora
        }
        jornada["partidos"].append(nuevo_partido)
    guardar_datos_valladolid_fs(data16)
    return redirect(url_for('calend_valladolid_fs')) 
# Toma la lista de los resultados y los guarda
def guardar_partidos_en_archivo_valladolid_fs(data16):
    arch_guardar_valladolid_fs = 'json/partidos_valladolid_fs.json'
    # Guardar en el archivo
    with open(arch_guardar_valladolid_fs, 'w', encoding='UTF-8') as archivo:
        json.dump(data16, archivo)
# Modificar los partidos de cada jornada
@app.route('/modificar_jornada_valladolid_fs/<string:id>', methods=['POST'])
def modificar_jorn_valladolid_fs(id):
    data16 = obtener_datos_valladolid_fs()
    if request.method == 'POST':
        jornada_nombre = request.form.get('nombre')
        resultados_a_modificar = next((result for result in data16 if result['id'] == id), None)
        if resultados_a_modificar:
            resultados_a_modificar['nombre'] = jornada_nombre
            resultados_a_modificar['partidos'] = []  # Reiniciar la lista de partidos
            for i in range(8):  # Ajusta según la cantidad máxima de partidos
                equipoLocal = request.form.get(f'local{i}')
                resultadoA = request.form.get(f'resultadoA{i}')
                resultadoB = request.form.get(f'resultadoB{i}')
                equipoVisitante = request.form.get(f'visitante{i}')
                fecha = request.form.get(f'fecha{i}')
                hora = request.form.get(f'hora{i}')
                nuevo_partido = {
                    'local': equipoLocal,
                    'resultadoA': resultadoA,
                    'resultadoB': resultadoB,
                    'visitante': equipoVisitante,
                    'fecha' : fecha,
                    'hora' : hora
                }
                resultados_a_modificar['partidos'].append(nuevo_partido)
            # Guardar los cambios en el archivo JSON
            guardar_partidos_en_archivo_valladolid_fs(data16)            
            return redirect(url_for('calend_valladolid_fs'))
    return redirect(url_for('calend_valladolid_fs'))
# Ruta para borrar jornadas
@app.route('/eliminar_jorn_valladolid_fs/<string:id>', methods=['POST'])
def eliminar_jorn_valladolid_fs(id):
    data16 = obtener_datos_valladolid_fs()
    jornada_a_eliminar = [j for j in data16 if j['id'] != id]  # Filtrar las jornadas diferentes de la que se va a eliminar
    guardar_partidos_en_archivo_valladolid_fs(jornada_a_eliminar)
    # Redirigir a la página de encuentros_simancas (o a donde desees después de eliminar)
    return redirect(url_for('calend_valladolid_fs')) 
# Crear la clasificación del Valladolid FS
def generar_clasificacion_analisis_futsal_valladolid_fs(data16, total_partidos_temporada_valladolid_fs):
    default_dict = defaultdict(lambda: {})
    clasificacion = defaultdict(lambda: {'puntos': 0,'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'favor': 0, 'contra': 0, 'diferencia_goles': 0})
    for jornada in data16:
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
    data16 = obtener_datos_valladolid_fs()
    total_partidos_temporada_valladolid_fs = 30
    # Llama a la función para generar la clasificación y análisis
    clasificacion_analisis_valladolid_fs = generar_clasificacion_analisis_futsal_valladolid_fs(data16, total_partidos_temporada_valladolid_fs)
    # Ordena la clasificación por puntos y diferencia de goles
    clasificacion_analisis_valladolid_fs = sorted(clasificacion_analisis_valladolid_fs, key=lambda x: (x['datos']['puntos'], x['datos']['diferencia_goles']), reverse=True)
    # Calcular la proximidad
    #proximidad = calcular_proximidad(data, clasificacion_analisis, total_partidos_temporada)
    return render_template('equipos_futbol_sala/clasi_analis_vallad_fs.html', clasificacion_analisis_valladolid_fs=clasificacion_analisis_valladolid_fs) 
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
            if equipo_local == equipo_parquesol or equipo_visitante == equipo_parquesol:
                # Determinamos el equipo contrario y los resultados
                if equipo_local == equipo_parquesol:
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
# Fin proceso Valladolid FS

#Todo el proceso de calendario y clasificación del Universidad Valladolid
# Ruta de partidos Universidad Valladolid
part_universidad = 'json/partidos_universidad.json'
def guardar_datos_universidad(data17):
    # Guardar los datos en el archivo JSON
    with open(part_universidad, 'w', encoding='utf-8') as file:
        json.dump(data17, file, indent=4)
def obtener_datos_universidad():
    try:
    # Leer los datos desde el archivo JSON
      with open(part_universidad, 'r', encoding='utf-8') as file:
        data17 = json.load(file)
      return data17
    except json.decoder.JSONDecodeError:
        # Manejar archivo vacío, inicializar con una estructura JSON válida
        return [] 
# Partidos Universidad Valladolid
@app.route('/admin/calend_universidad')
def calend_universidad():
    data17 = obtener_datos_universidad()
    print(data17)
    return render_template('admin/calend_universidad.html', data17=data17)
# Ingresar los resultados de los partidos del Universidad Valladolid
@app.route('/admin/crear_calendario_universidad', methods=['POST'])
def ingresar_resul_universidad():
    data17 = obtener_datos_universidad()
    nums_partidos = int(request.form.get('num_partidos', 0))
    jornada_nombre = request.form.get('nombre')
    jornada_existente = next((j for j in data17 if j["nombre"] == jornada_nombre), None)
    if jornada_existente:
        # Si la jornada ya existe, utiliza su identificador existente
        jornada_id = jornada_existente["id"]
        jornada = jornada_existente
    else:
        # Si la jornada no existe, crea un nuevo identificador
        jornada_id = str(uuid.uuid4())
        jornada = {"id": jornada_id, "nombre": jornada_nombre, "partidos": []}
        data17.append(jornada)
    for i in range(nums_partidos):
        #id_nuevo = str(uuid.uuid4())
        equipoLocal = request.form.get(f'local{i}')
        resultadoA = request.form.get(f'resultadoA{i}')
        resultadoB = request.form.get(f'resultadoB{i}')
        equipoVisitante = request.form.get(f'visitante{i}')
        fecha = request.form.get(f'fecha{i}')
        hora = request.form.get(f'hora{i}')
        nuevo_partido = {
            #'id': id_nuevo,
            'local': equipoLocal,
            'resultadoA': resultadoA,
            'resultadoB': resultadoB,
            'visitante': equipoVisitante,
            'fecha' : fecha,
            'hora' : hora
        }
        jornada["partidos"].append(nuevo_partido)
    guardar_datos_universidad(data17)
    return redirect(url_for('calend_universidad')) 
# Toma la lista de los resultados y los guarda
def guardar_partidos_en_archivo_universidad(data17):
    arch_guardar_universidad = 'json/partidos_universidad.json'
    # Guardar en el archivo
    with open(arch_guardar_universidad, 'w', encoding='UTF-8') as archivo:
        json.dump(data17, archivo)
# Modificar los partidos de cada jornada
@app.route('/modificar_jornada_universidad/<string:id>', methods=['POST'])
def modificar_jorn_universidad(id):
    data17 = obtener_datos_universidad()
    if request.method == 'POST':
        jornada_nombre = request.form.get('nombre')
        resultados_a_modificar = next((result for result in data17 if result['id'] == id), None)
        if resultados_a_modificar:
            resultados_a_modificar['nombre'] = jornada_nombre
            resultados_a_modificar['partidos'] = []  # Reiniciar la lista de partidos
            for i in range(8):  # Ajusta según la cantidad máxima de partidos
                equipoLocal = request.form.get(f'local{i}')
                resultadoA = request.form.get(f'resultadoA{i}')
                resultadoB = request.form.get(f'resultadoB{i}')
                equipoVisitante = request.form.get(f'visitante{i}')
                fecha = request.form.get(f'fecha{i}')
                hora = request.form.get(f'hora{i}')
                nuevo_partido = {
                    'local': equipoLocal,
                    'resultadoA': resultadoA,
                    'resultadoB': resultadoB,
                    'visitante': equipoVisitante,
                    'fecha' : fecha,
                    'hora' : hora
                }
                resultados_a_modificar['partidos'].append(nuevo_partido)
            # Guardar los cambios en el archivo JSON
            guardar_partidos_en_archivo_universidad(data17)            
            return redirect(url_for('calend_universidad'))
    return redirect(url_for('calend_universidad'))
# Ruta para borrar jornadas
@app.route('/eliminar_jorn_universidad/<string:id>', methods=['POST'])
def eliminar_jorn_universidad(id):
    data17 = obtener_datos_universidad()
    jornada_a_eliminar = [j for j in data17 if j['id'] != id]  # Filtrar las jornadas diferentes de la que se va a eliminar
    guardar_partidos_en_archivo_universidad(jornada_a_eliminar)
    # Redirigir a la página de encuentros_universidad (o a donde desees después de eliminar)
    return redirect(url_for('calend_universidad')) 
# Crear la clasificación del Universidad Valladolid
def generar_clasificacion_analisis_futsal_universidad(data17, total_partidos_temporada_universidad):
    default_dict = defaultdict(lambda: {})
    clasificacion = defaultdict(lambda: {'puntos': 0,'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'favor': 0, 'contra': 0, 'diferencia_goles': 0})
    for jornada in data17:
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
    data17 = obtener_datos_universidad()
    total_partidos_temporada_universidad = 30
    # Llama a la función para generar la clasificación y análisis
    clasificacion_analisis_universidad = generar_clasificacion_analisis_futsal_universidad(data17, total_partidos_temporada_universidad)
    # Ordena la clasificación por puntos y diferencia de goles
    clasificacion_analisis_universidad = sorted(clasificacion_analisis_universidad, key=lambda x: (x['datos']['puntos'], x['datos']['diferencia_goles']), reverse=True)
    # Calcular la proximidad
    #proximidad = calcular_proximidad(data, clasificacion_analisis, total_partidos_temporada)
    return render_template('equipos_futbol_sala/clasi_analis_universidad.html', clasificacion_analisis_universidad=clasificacion_analisis_universidad) 
# Ruta y creación del calendario individual del Universidad Valladolid
@app.route('/equipos_futbol_sala/calendario_universidad')
def calendarios_universidad():
    datos17 = obtener_datos_universidad()
    nuevos_datos_universidad = [dato for dato in datos17 if dato]
    equipo_universidad = 'Univ. Valladolid'
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
                if equipo_local == equipo_parquesol:
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
# Fin proceso Universidad Valladolid

# EQUIPOS BALONMANO
#Todo el proceso de calendario y clasificación del Aula Valladolid
# Ruta de partidos Aula Valladolid
part_aula = 'json/partidos_aula.json'
def guardar_datos_aula(data7):
    # Guardar los datos en el archivo JSON
    with open(part_aula, 'w', encoding='utf-8') as file:
        json.dump(data7, file, indent=4)
def obtener_datos_aula():
    try:
    # Leer los datos desde el archivo JSON
      with open(part_aula, 'r', encoding='utf-8') as file:
        data7 = json.load(file)
      return data7
    except json.decoder.JSONDecodeError:
        # Manejar archivo vacío, inicializar con una estructura JSON válida
        return []
# Partidos Aula
@app.route('/admin/calend_aula')
def calend_aula():
    data7 = obtener_datos_aula()
    return render_template('admin/calend_aula.html', data7=data7)
# Ingresar los resultados de los partidos del Aula Valladolid
@app.route('/admin/crear_calendario_aula', methods=['POST'])
def ingresar_resul_aula():
    data7 = obtener_datos_aula()
    nums_partidos = int(request.form.get('num_partidos', 0))
    jornada_nombre = request.form.get('nombre')
    jornada_existente = next((j for j in data7 if j["nombre"] == jornada_nombre), None)
    if jornada_existente:
        # Si la jornada ya existe, utiliza su identificador existente
        jornada_id = jornada_existente["id"]
        jornada = jornada_existente
    else:
        # Si la jornada no existe, crea un nuevo identificador
        jornada_id = str(uuid.uuid4())
        jornada = {"id": jornada_id, "nombre": jornada_nombre, "partidos": []}
        data7.append(jornada)
    for i in range(nums_partidos):
        #id_nuevo = str(uuid.uuid4())
        equipoLocal = request.form.get(f'local{i}')
        resultadoA = request.form.get(f'resultadoA{i}')
        resultadoB = request.form.get(f'resultadoB{i}')
        equipoVisitante = request.form.get(f'visitante{i}')
        fecha = request.form.get(f'fecha{i}')
        hora = request.form.get(f'hora{i}')
        
        nuevo_partido = {
            #'id': id_nuevo,
            'local': equipoLocal,
            'resultadoA': resultadoA,
            'resultadoB': resultadoB,
            'visitante': equipoVisitante,
            'fecha': fecha,
            'hora': hora
        }
        jornada["partidos"].append(nuevo_partido)
    guardar_datos_aula(data7)
    return redirect(url_for('calend_aula')) 
# Toma la lista de los resultados y los guarda
def guardar_partidos_en_archivo_aula(data7):
    arch_guardar_aula = 'json/partidos_aula.json'
    # Guardar en el archivo
    with open(arch_guardar_aula, 'w', encoding='UTF-8') as archivo:
        json.dump(data7, archivo)
# Modificar los partidos de cada jornada
@app.route('/modificar_jornada_aula/<string:id>', methods=['POST'])
def modificar_jorn_aula(id):
    data7 = obtener_datos_aula()
    if request.method == 'POST':
        jornada_nombre = request.form.get('nombre')
        resultados_a_modificar = next((result for result in data7 if result['id'] == id), None)
        if resultados_a_modificar:
            resultados_a_modificar['nombre'] = jornada_nombre
            resultados_a_modificar['partidos'] = []  # Reiniciar la lista de partidos
            for i in range(6):  # Ajusta según la cantidad máxima de partidos
                equipoLocal = request.form.get(f'local{i}')
                resultadoA = request.form.get(f'resultadoA{i}')
                resultadoB = request.form.get(f'resultadoB{i}')
                equipoVisitante = request.form.get(f'visitante{i}')
                fecha = request.form.get(f'fecha{i}')
                hora = request.form.get(f'hora{i}')
                nuevo_partido = {
                    'local': equipoLocal,
                    'resultadoA': resultadoA,
                    'resultadoB': resultadoB,
                    'visitante': equipoVisitante,
                    'fecha': fecha,
                    'hora': hora
                }
                resultados_a_modificar['partidos'].append(nuevo_partido)
            # Guardar los cambios en el archivo JSON
            guardar_partidos_en_archivo_aula(data7)            
            return redirect(url_for('calend_aula'))
    return redirect(url_for('calend_aula'))
# Ruta para borrar jornadas
@app.route('/eliminar_jorn_aula/<string:id>', methods=['POST'])
def eliminar_jorn_aula(id):
    data7 = obtener_datos_aula()
    jornada_a_eliminar = [j for j in data7 if j['id'] != id]  # Filtrar las jornadas diferentes de la que se va a eliminar
    guardar_partidos_en_archivo_aula(jornada_a_eliminar)
    return redirect(url_for('calend_aula')) 
# PlayOff Aula Valladolid
playoff_aula = 'json_playoff/playoff_aula.json'
def guardar_playoff_aula(datas7):
    with open(playoff_aula, 'w', encoding='utf-8') as file:
        json.dump(datas7, file, indent=4)
def obtener_playoff_aula():
    try:
        with open(playoff_aula, 'r', encoding='utf-8') as file:
            datas7 = json.load(file)
        return datas7
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return {'cuartos': [], 'semifinales': [], 'final': []}
nuevos_enfrentamientos_aula = []
partido_aula = None
# Crear formulario para los playoff
@app.route('/admin/playoff_aula/')
def ver_playoff_aula():
    datas7 = obtener_playoff_aula()
    return render_template('admin/playoff_aula.html', datas7=datas7)
# Crear formulario para los playoff
@app.route('/admin/crear_playoff_aula', methods=['GET', 'POST'])
def crear_playoff_aula():
    # Obtener los enfrentamientos actuales del archivo JSON
    datas7 = obtener_playoff_aula()
    if request.method == 'POST':
        # Obtener la etapa del torneo seleccionada por el usuario
        eliminatoria = request.form.get('eliminatoria')
        # Verificar el número máximo de partidos permitidos según la etapa del torneo
        if eliminatoria == 'cuartos':
            max_partidos = 6
        elif eliminatoria == 'semifinales':
            max_partidos = 4
        elif eliminatoria == 'final':
            max_partidos = 2
        else:
            # Manejar caso no válido
            return "Etapa de torneo no válida"
        # Recuperar los datos del formulario y procesarlos
        num_partidos_str = request.form.get('num_partidos', '0')  # Valor predeterminado '0' si num_partidos está vacío
        num_partidos_str = num_partidos_str.strip()  # Eliminar espacios en blanco
        if num_partidos_str:
            num_partidos = int(num_partidos_str)
        else:
            num_partidos = 0  # Valor predeterminado si num_partidos está vacío
        # Si num_partidos es cero, se ignora la validación
        if num_partidos < 0:
            return "Número de partidos no válido"
        # Crear un identificador único para la eliminatoria
        eliminatoria_id = str(uuid.uuid4())  # Generar un UUID único
        # Crear un nuevo diccionario con los datos de la eliminatoria
        eliminatoria_data = {
            'id': eliminatoria_id,
            'partidos': []
        }
        # Recuperar los datos de cada partido del formulario
        for i in range(num_partidos):
            local = request.form.get(f'local{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            visitante = request.form.get(f'visitante{i}')
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            # Crear un nuevo diccionario con los datos del partido
            partido = {
                'local': local,
                'resultadoA': resultadoA,
                'resultadoB': resultadoB,
                'visitante': visitante,
                'fecha': fecha,
                'hora': hora
            }
            # Agregar el partido a la lista de partidos de la eliminatoria
            eliminatoria_data['partidos'].append(partido)
            # Agregar los nuevos enfrentamientos a la lista correspondiente
        datas7[eliminatoria] = eliminatoria_data
         # Agregar los nuevos enfrentamientos a la lista correspondiente
        nuevos_enfrentamientos.clear()  
        # Guardar la lista de partidos en el archivo JSON
        guardar_playoff_aula(datas7)
        # Redireccionar a la página de visualización del playoff
        return redirect(url_for('ver_playoff_aula'))
    # Si no es una solicitud POST, renderizar el formulario
    return render_template('admin/playoff_aula.html', datas7=datas7)
# Toma la lista de los playoff y los guarda
def guardar_playoff_en_archivo_aula(datas7):
    arch_guardar_playoff_aula = 'json_playoff/partidos_aula.json'
    # Guardar en el archivo
    with open(arch_guardar_playoff_aula, 'w', encoding='UTF-8') as archivo:
        json.dump(datas7, archivo)
# Modificar los partidos de los playoff
@app.route('/modificar_eliminatoria_aula/<string:id>', methods=['GET', 'POST'])
def modificar_playoff_aula(id):
    datas7 = obtener_playoff_aula()
    # Buscar la eliminatoria correspondiente al ID proporcionado
    eliminatoria_encontrada = None
    for eliminatoria, datos_eliminatoria in datas7.items():
        if datos_eliminatoria['id'] == id:
            eliminatoria_encontrada = datos_eliminatoria
            break
    if not eliminatoria_encontrada:
        return "Eliminatoria no encontrada"
    if request.method == 'POST':
        nuevos_partidos = []
        for index, partido in enumerate(eliminatoria_encontrada['partidos']):
            local = request.form.get(f'local{index}')
            resultadoA = request.form.get(f'resultadoA{index}')
            resultadoB = request.form.get(f'resultadoB{index}')
            visitante = request.form.get(f'visitante{index}')
            fecha = request.form.get(f'fecha{index}')
            hora = request.form.get(f'hora{index}')
            # Actualizar los datos del partido
            partido['local'] = local
            partido['resultadoA'] = resultadoA
            partido['resultadoB'] = resultadoB
            partido['visitante'] = visitante
            partido['fecha'] = fecha
            partido['hora'] = hora
            nuevos_partidos.append(partido)   
        eliminatoria_encontrada['partidos'] = nuevos_partidos       
        # Guardar los cambios en el archivo JSON
        guardar_playoff_aula(datas7)       
        # Redireccionar a la página de visualización del playoff
        return redirect(url_for('ver_playoff_aula'))
# Crear la clasificación del Aula Valladolid
def generar_clasificacion_analisis_balonmano_aula(data7, total_partidos_temporada_aula):
    default_dict = defaultdict(lambda: {})
    clasificacion = defaultdict(lambda: {'puntos': 0,'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'favor': 0, 'contra': 0, 'diferencia_goles': 0})
    for jornada in data7:
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
"""# Crear la clasificación para el GrupoA y GrupoB de Aula Valladolid
def generar_clasificacion_grupoA_grupoB(data7, total_partidos_temporada_grupos_aula):
    clasificacion = defaultdict(lambda: {'puntos': 0, 'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'favor': 0, 'contra': 0, 'diferencia_goles': 0, 'bonus': 0})
    for jornada in data7[:total_partidos_temporada_grupos_aula]:
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
                clasificacion[equipo_local]['puntos'] += 3 + bonus_local
                clasificacion[equipo_local]['ganados'] += 1
                clasificacion[equipo_visitante]['puntos'] += 0 + bonus_visitante
                clasificacion[equipo_visitante]['perdidos'] += 1
            elif resultado_local < resultado_visitante:
                clasificacion[equipo_local]['puntos'] += 0 + bonus_local
                clasificacion[equipo_local]['perdidos'] += 1
                clasificacion[equipo_visitante]['puntos'] += 3 + bonus_visitante
                clasificacion[equipo_visitante]['ganados'] += 1
            else:
                clasificacion[equipo_local]['puntos'] += 1 + bonus_local
                clasificacion[equipo_visitante]['puntos'] += 1 + bonus_visitante
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
    grupoA = clasificacion_ordenada[:4]
    grupoB = clasificacion_ordenada[4:8]
    return grupoA, grupoB"""
# Ruta para mostrar la clasificación y análisis del Aula Valladolid
@app.route('/equipos_balonmano/clasi_analis_aula/')
def clasif_analisis_aula():
    data7 = obtener_datos_aula()
    total_partidos_temporada_aula = 22
    # Llama a la función para generar la clasificación y análisis
    clasificacion_analisis_aula = generar_clasificacion_analisis_balonmano_aula(data7, total_partidos_temporada_aula)
    # Ordena la clasificación por puntos y diferencia de goles
    clasificacion_analisis_aula = sorted(clasificacion_analisis_aula, key=lambda x: (x['datos']['puntos'], x['datos']['diferencia_goles']), reverse=True)
    return render_template('equipos_balonmano/clasi_analis_aula.html', clasificacion_analisis_aula=clasificacion_analisis_aula)
# Ruta para mostrar los playoffs del Aula Valladolid
@app.route('/playoffs_aula/')
def playoffs_aula():
    # Obtener datos de las eliminatorias
    datas7 = obtener_playoff_aula()
    return render_template('playoffs/aula_playoff.html', datas7=datas7)
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
#Fin proceso Aula Valladolid

#Todo el proceso de calendario y clasificación del Atlético Valladolid
# Ruta de partidos Atlético Valladolid
part_recoletas = 'json/partidos_recoletas.json'
def guardar_datos_recoletas(data8):
    # Guardar los datos en el archivo JSON
    with open(part_recoletas, 'w', encoding='utf-8') as file:
        json.dump(data8, file, indent=4)
def obtener_datos_recoletas():
    try:
    # Leer los datos desde el archivo JSON
      with open(part_recoletas, 'r', encoding='utf-8') as file:
        data8 = json.load(file)
      return data8
    except json.decoder.JSONDecodeError:
        # Manejar archivo vacío, inicializar con una estructura JSON válida
        return []
# Partidos Atlético Valladolid
@app.route('/admin/calend_recoletas')
def calend_recoletas():
    data8 = obtener_datos_recoletas()
    return render_template('admin/calend_recoletas.html', data8=data8)
# Ingresar los resultados de los partidos del Atlético Valladolid
@app.route('/admin/crear_calendario_recoletas', methods=['POST'])
def ingresar_resul_recoletas():
    data8 = obtener_datos_recoletas()
    nums_partidos = int(request.form.get('num_partidos', 0))
    jornada_nombre = request.form.get('nombre')
    jornada_existente = next((j for j in data8 if j["nombre"] == jornada_nombre), None)
    if jornada_existente:
        # Si la jornada ya existe, utiliza su identificador existente
        jornada_id = jornada_existente["id"]
        jornada = jornada_existente
    else:
        # Si la jornada no existe, crea un nuevo identificador
        jornada_id = str(uuid.uuid4())
        jornada = {"id": jornada_id, "nombre": jornada_nombre, "partidos": []}
        data8.append(jornada)
    for i in range(nums_partidos):
        #id_nuevo = str(uuid.uuid4())
        equipoLocal = request.form.get(f'local{i}')
        resultadoA = request.form.get(f'resultadoA{i}')
        resultadoB = request.form.get(f'resultadoB{i}')
        equipoVisitante = request.form.get(f'visitante{i}')
        fecha = request.form.get(f'fecha{i}')
        hora = request.form.get(f'hora{i}')
        nuevo_partido = {
            #'id': id_nuevo,
            'local': equipoLocal,
            'resultadoA': resultadoA,
            'resultadoB': resultadoB,
            'visitante': equipoVisitante,
            'fecha' : fecha,
            'hora' : hora
        }
        jornada["partidos"].append(nuevo_partido)
    guardar_datos_recoletas(data8)
    return redirect(url_for('calend_recoletas')) 
# Toma la lista de los resultados y los guarda
def guardar_partidos_en_archivo_recoletas(data8):
    arch_guardar_recoletas = 'json/partidos_recoletas.json'
    # Guardar en el archivo
    with open(arch_guardar_recoletas, 'w', encoding='UTF-8') as archivo:
        json.dump(data8, archivo)
# Modificar los partidos de cada jornada
@app.route('/modificar_jornada_recoletas/<string:id>', methods=['POST'])
def modificar_jorn_recoletas(id):
    data8 = obtener_datos_recoletas()
    if request.method == 'POST':
        jornada_nombre = request.form.get('nombre')
        resultados_a_modificar = next((result for result in data8 if result['id'] == id), None)
        if resultados_a_modificar:
            resultados_a_modificar['nombre'] = jornada_nombre
            resultados_a_modificar['partidos'] = []  # Reiniciar la lista de partidos
            for i in range(8):  # Ajusta según la cantidad máxima de partidos
                equipoLocal = request.form.get(f'local{i}')
                resultadoA = request.form.get(f'resultadoA{i}')
                resultadoB = request.form.get(f'resultadoB{i}')
                equipoVisitante = request.form.get(f'visitante{i}')
                fecha = request.form.get(f'fecha{i}')
                hora = request.form.get(f'hora{i}')
                nuevo_partido = {
                    'local': equipoLocal,
                    'resultadoA': resultadoA,
                    'resultadoB': resultadoB,
                    'visitante': equipoVisitante,
                    'fecha' : fecha,
                    'hora' : hora
                }
                resultados_a_modificar['partidos'].append(nuevo_partido)
            # Guardar los cambios en el archivo JSON
            guardar_partidos_en_archivo_recoletas(data8)            
            return redirect(url_for('calend_recoletas'))
    return redirect(url_for('calend_recoletas'))
# Ruta para borrar jornadas
@app.route('/eliminar_jorn_recoletas/<string:id>', methods=['POST'])
def eliminar_jorn_recoletas(id):
    data8 = obtener_datos_recoletas()
    jornada_a_eliminar = [j for j in data8 if j['id'] != id]  # Filtrar las jornadas diferentes de la que se va a eliminar
    guardar_partidos_en_archivo_recoletas(jornada_a_eliminar)
    return redirect(url_for('calend_recoletas'))
# PlayOff Atlético Valladolid
playoff_recoletas = 'json_playoff/playoff_recoletas.json'
def guardar_playoff_recoletas(datas12):
    with open(playoff_recoletas, 'w', encoding='utf-8') as file:
        json.dump(datas12, file, indent=4)
def obtener_playoff_recoletas():
    try:
        with open(playoff_recoletas, 'r', encoding='utf-8') as file:
            datas12 = json.load(file)
        return datas12
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return {'promocion': []}
nuevos_enfrentamientos_recoletas = []
partido_recoletas = None
# Crear formulario para los playoff
@app.route('/admin/playoff_recoletas/')
def ver_playoff_recoletas():
    datas12 = obtener_playoff_recoletas()
    return render_template('admin/playoff_recoletas.html', datas12=datas12)
# Crear formulario para los playoff
@app.route('/admin/crear_playoff_recoletas', methods=['GET', 'POST'])
def crear_playoff_recoletas():
    # Obtener los enfrentamientos actuales del archivo JSON
    datas12 = obtener_playoff_recoletas()
    if request.method == 'POST':
        # Obtener la etapa del torneo seleccionada por el usuario
        eliminatoria = request.form.get('eliminatoria')
        # Verificar el número máximo de partidos permitidos según la etapa del torneo
        if eliminatoria == 'promocion':
            max_partidos = 1
        else:
            # Manejar caso no válido
            return "Etapa de torneo no válida"
        # Recuperar los datos del formulario y procesarlos
        num_partidos_str = request.form.get('num_partidos', '0')  # Valor predeterminado '0' si num_partidos está vacío
        num_partidos_str = num_partidos_str.strip()  # Eliminar espacios en blanco
        if num_partidos_str:
            num_partidos = int(num_partidos_str)
        else:
            num_partidos = 0  # Valor predeterminado si num_partidos está vacío
        # Si num_partidos es cero, se ignora la validación
        if num_partidos < 0:
            return "Número de partidos no válido"
        # Crear un identificador único para la eliminatoria
        eliminatoria_id = str(uuid.uuid4())  # Generar un UUID único
        # Crear un nuevo diccionario con los datos de la eliminatoria
        eliminatoria_data = {
            'id': eliminatoria_id,
            'partidos': []
        }
        # Recuperar los datos de cada partido del formulario
        for i in range(num_partidos):
            local = request.form.get(f'local{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            visitante = request.form.get(f'visitante{i}')
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            # Crear un nuevo diccionario con los datos del partido
            partido = {
                'local': local,
                'resultadoA': resultadoA,
                'resultadoB': resultadoB,
                'visitante': visitante,
                'fecha' : fecha,
                'hora' : hora
            }
            # Agregar el partido a la lista de partidos de la eliminatoria
            eliminatoria_data['partidos'].append(partido)
            # Agregar los nuevos enfrentamientos a la lista correspondiente
        datas12[eliminatoria] = eliminatoria_data
         # Agregar los nuevos enfrentamientos a la lista correspondiente
        nuevos_enfrentamientos.clear()  
        # Guardar la lista de partidos en el archivo JSON
        guardar_playoff_recoletas(datas12)
        # Redireccionar a la página de visualización del playoff
        return redirect(url_for('ver_playoff_recoletas'))
    # Si no es una solicitud POST, renderizar el formulario
    return render_template('admin/playoff_recoletas.html', datas12=datas12)
# Toma la lista de los playoff y los guarda
def guardar_playoff_en_archivo_recoletas(datas12):
    arch_guardar_playoff_recoletas = 'json_playoff/partidos_recoletas.json'
    # Guardar en el archivo
    with open(arch_guardar_playoff_recoletas, 'w', encoding='UTF-8') as archivo:
        json.dump(datas12, archivo)
# Modificar los partidos de los playoff
@app.route('/modificar_eliminatoria_recoletas/<string:id>', methods=['GET', 'POST'])
def modificar_playoff_recoletas(id):
    datas12 = obtener_playoff_recoletas()
    # Buscar la eliminatoria correspondiente al ID proporcionado
    eliminatoria_encontrada = None
    for eliminatoria, datos_eliminatoria in datas12.items():
        if datos_eliminatoria['id'] == id:
            eliminatoria_encontrada = datos_eliminatoria
            break
    if not eliminatoria_encontrada:
        return "Eliminatoria no encontrada"
    if request.method == 'POST':
        nuevos_partidos = []
        for index, partido in enumerate(eliminatoria_encontrada['partidos']):
            local = request.form.get(f'local{index}')
            resultadoA = request.form.get(f'resultadoA{index}')
            resultadoB = request.form.get(f'resultadoB{index}')
            visitante = request.form.get(f'visitante{index}')
            fecha = request.form.get(f'fecha{index}')
            hora = request.form.get(f'hora{index}')
            # Actualizar los datos del partido
            partido['local'] = local
            partido['resultadoA'] = resultadoA
            partido['resultadoB'] = resultadoB
            partido['visitante'] = visitante
            partido['fecha'] = fecha
            partido['hora'] = hora
            nuevos_partidos.append(partido)   
        eliminatoria_encontrada['partidos'] = nuevos_partidos       
        # Guardar los cambios en el archivo JSON
        guardar_playoff_recoletas(datas12)       
        # Redireccionar a la página de visualización del playoff
        return redirect(url_for('ver_playoff_recoletas'))
# Crear la clasificación del Atlético Valladolid
def generar_clasificacion_analisis_balonmano_recoletas(data8, total_partidos_temporada_recoletas):
    default_dict = defaultdict(lambda: {})
    clasificacion = defaultdict(lambda: {'puntos': 0,'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'favor': 0, 'contra': 0, 'diferencia_goles': 0})
    for jornada in data8:
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
    data8 = obtener_datos_recoletas()
    total_partidos_temporada_recoletas = 30
    # Llama a la función para generar la clasificación y análisis
    clasificacion_analisis_recoletas = generar_clasificacion_analisis_balonmano_recoletas(data8, total_partidos_temporada_recoletas)
    # Ordena la clasificación por puntos y diferencia de goles
    clasificacion_analisis_recoletas = sorted(clasificacion_analisis_recoletas, key=lambda x: (x['datos']['puntos'], x['datos']['diferencia_goles']), reverse=True)
    return render_template('equipos_balonmano/clasi_analis_recoletas.html', clasificacion_analisis_recoletas=clasificacion_analisis_recoletas)
# Ruta para mostrar los playoffs del Atlético Valladolid
@app.route('/playoffs_recoletas/')
def playoffs_recoletas():
    # Obtener datos de las eliminatorias
    datas12 = obtener_playoff_recoletas()
    return render_template('playoffs/recoletas_playoff.html', datas12=datas12)
# Ruta y creación del calendario individual del Aula Valladolid
@app.route('/equipos_balonmano/calendario_recoletas')
def calendarios_recoletas():
    datos8 = obtener_datos_recoletas()
    nuevos_datos_recoletas = [dato for dato in datos8 if dato]
    equipo_recoletas = 'Atl. Valladolid'
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
#Fin proceso Atlético Valladolid

#EQUIPOS RUGBY
#Todo el proceso de calendario y clasificación del El Salvador
# Ruta de partidos El Salvador
part_salvador = 'json/partidos_salvador.json'
def guardar_datos_salvador(data11):
    # Guardar los datos en el archivo JSON
    with open(part_salvador, 'w', encoding='utf-8') as file:
        json.dump(data11, file, indent=4)
def obtener_datos_salvador():
    try:
    # Leer los datos desde el archivo JSON
      with open(part_salvador, 'r', encoding='utf-8') as file:
        data11 = json.load(file)
      return data11
    except json.decoder.JSONDecodeError:
        # Manejar archivo vacío, inicializar con una estructura JSON válida
        return []
# Partidos El Salvador
@app.route('/admin/calend_salvador')
def calend_salvador():
    data11 = obtener_datos_salvador()
    return render_template('admin/calend_salvador.html', data11=data11)
# Ingresar los resultados de los partidos de El Salvador
@app.route('/admin/crear_calendario_salvador', methods=['POST'])
def ingresar_resul_salvador():
    data11 = obtener_datos_salvador()
    nums_partidos = int(request.form.get('num_partidos', 0))
    jornada_nombre = request.form.get('nombre')
    jornada_existente = next((j for j in data11 if j["nombre"] == jornada_nombre), None)
    if jornada_existente:
        # Si la jornada ya existe, utiliza su identificador existente
        jornada_id = jornada_existente["id"]
        jornada = jornada_existente
    else:
        # Si la jornada no existe, crea un nuevo identificador
        jornada_id = str(uuid.uuid4())
        jornada = {"id": jornada_id, "nombre": jornada_nombre, "partidos": []}
        data11.append(jornada)
    for i in range(nums_partidos):
        #id_nuevo = str(uuid.uuid4())
        equipoLocal = request.form.get(f'local{i}')
        bonusA = request.form.get(f'bonusA{i}')
        resultadoA = request.form.get(f'resultadoA{i}')
        resultadoB = request.form.get(f'resultadoB{i}')
        bonusB = request.form.get(f'bonusB{i}')
        equipoVisitante = request.form.get(f'visitante{i}')
        fecha = request.form.get(f'fecha{i}')
        hora = request.form.get(f'hora{i}')
        nuevo_partido = {
            #'id': id_nuevo,
            'local': equipoLocal,
            'bonusA': bonusA,
            'resultadoA': resultadoA,
            'resultadoB': resultadoB,
            'bonusB': bonusB,
            'visitante': equipoVisitante,
            'fecha' : fecha,
            'hora' : hora
        }
        jornada["partidos"].append(nuevo_partido)
    guardar_datos_salvador(data11)
    return redirect(url_for('calend_salvador'))
# Toma la lista de los resultados y los guarda
def guardar_partidos_en_archivo_salvador(data11):
    arch_guardar_salvador = 'json/partidos_salvador.json'
    # Guardar en el archivo
    with open(arch_guardar_salvador, 'w', encoding='UTF-8') as archivo:
        json.dump(data11, archivo)
# Modificar los partidos de cada jornada
@app.route('/modificar_jornada_salvador/<string:id>', methods=['POST'])
def modificar_jorn_salvador(id):
    data11 = obtener_datos_salvador()
    if request.method == 'POST':
        jornada_nombre = request.form.get('nombre')
        resultados_a_modificar = next((result for result in data11 if result['id'] == id), None)
        if resultados_a_modificar:
            resultados_a_modificar['nombre'] = jornada_nombre
            resultados_a_modificar['partidos'] = []  # Reiniciar la lista de partidos
            for i in range(6):  # Ajusta según la cantidad máxima de partidos
                equipoLocal = request.form.get(f'local{i}')
                bonusA = request.form.get(f'bonusA{i}')
                resultadoA = request.form.get(f'resultadoA{i}')
                resultadoB = request.form.get(f'resultadoB{i}')
                bonusB = request.form.get(f'bonusB{i}')
                equipoVisitante = request.form.get(f'visitante{i}')
                fecha = request.form.get(f'fecha{i}')
                hora = request.form.get(f'hora{i}')
                nuevo_partido = {
                    'local': equipoLocal,
                    'bonusA': bonusA,
                    'resultadoA': resultadoA,
                    'resultadoB': resultadoB,
                    'bonusB': bonusB,
                    'visitante': equipoVisitante,
                    'fecha' : fecha,
                    'hora' : hora
                }
                resultados_a_modificar['partidos'].append(nuevo_partido)
            # Guardar los cambios en el archivo JSON
            guardar_partidos_en_archivo_salvador(data11)            
            return redirect(url_for('calend_salvador'))
    return redirect(url_for('calend_salvador'))
# Ruta para borrar jornadas
@app.route('/eliminar_jorn_salvador/<string:id>', methods=['POST'])
def eliminar_jorn_salvador(id):
    data11 = obtener_datos_salvador()
    jornada_a_eliminar = [j for j in data11 if j['id'] != id]  # Filtrar las jornadas diferentes de la que se va a eliminar
    guardar_partidos_en_archivo_salvador(jornada_a_eliminar)
    return redirect(url_for('calend_salvador'))
# PlayOff El Salvador
playoff_salvador = 'json_playoff/playoff_salvador.json'
def guardar_playoff_salvador(datas1):
    with open(playoff_salvador, 'w', encoding='utf-8') as file:
        json.dump(datas1, file, indent=4)
def obtener_playoff_salvador():
    try:
        with open(playoff_salvador, 'r', encoding='utf-8') as file:
            datas1 = json.load(file)
        return datas1
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return {'cuartos': [], 'semifinales': [], 'final': []}
nuevos_enfrentamientos = []
partido = None
# Crear formulario para los playoff
@app.route('/admin/playoff_salvador/')
def ver_playoff_salvador():
    datas1 = obtener_playoff_salvador()
    return render_template('admin/playoff_salvador.html', datas1=datas1)
# Crear formulario para los playoff
@app.route('/admin/crear_playoff_salvador', methods=['GET', 'POST'])
def crear_playoff_salvador():
    # Obtener los enfrentamientos actuales del archivo JSON
    datas1 = obtener_playoff_salvador()
    if request.method == 'POST':
        # Obtener la etapa del torneo seleccionada por el usuario
        eliminatoria = request.form.get('eliminatoria')
        # Verificar el número máximo de partidos permitidos según la etapa del torneo
        if eliminatoria == 'cuartos':
            max_partidos = 4
        elif eliminatoria == 'semifinales':
            max_partidos = 2
        elif eliminatoria == 'final':
            max_partidos = 1
        else:
            # Manejar caso no válido
            return "Etapa de torneo no válida"
        # Recuperar los datos del formulario y procesarlos
        num_partidos_str = request.form.get('num_partidos', '0')  # Valor predeterminado '0' si num_partidos está vacío
        num_partidos_str = num_partidos_str.strip()  # Eliminar espacios en blanco
        if num_partidos_str:
            num_partidos = int(num_partidos_str)
        else:
            num_partidos = 0  # Valor predeterminado si num_partidos está vacío
        # Si num_partidos es cero, se ignora la validación
        if num_partidos < 0:
            return "Número de partidos no válido"
        # Crear un identificador único para la eliminatoria
        eliminatoria_id = str(uuid.uuid4())  # Generar un UUID único
        # Crear un nuevo diccionario con los datos de la eliminatoria
        eliminatoria_data = {
            'id': eliminatoria_id,
            'partidos': []
        }
        # Recuperar los datos de cada partido del formulario
        for i in range(num_partidos):
            local = request.form.get(f'local{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            visitante = request.form.get(f'visitante{i}')
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            # Crear un nuevo diccionario con los datos del partido
            partido = {
                'local': local,
                'resultadoA': resultadoA,
                'resultadoB': resultadoB,
                'visitante': visitante,
                'fecha' : fecha,
                'hora' : hora
            }
            # Agregar el partido a la lista de partidos de la eliminatoria
            eliminatoria_data['partidos'].append(partido)
            # Agregar los nuevos enfrentamientos a la lista correspondiente
        datas1[eliminatoria] = eliminatoria_data
         # Agregar los nuevos enfrentamientos a la lista correspondiente
        nuevos_enfrentamientos.clear()  
        # Guardar la lista de partidos en el archivo JSON
        guardar_playoff_salvador(datas1)
        # Redireccionar a la página de visualización del playoff
        return redirect(url_for('ver_playoff_salvador'))
    # Si no es una solicitud POST, renderizar el formulario
    return render_template('admin/playoff_salvador.html', datas1=datas1)
# Toma la lista de los playoff y los guarda
def guardar_playoff_en_archivo_salvador(datas1):
    arch_guardar_playoff_salvador = 'json_playoff/partidos_salvador.json'
    # Guardar en el archivo
    with open(arch_guardar_playoff_salvador, 'w', encoding='UTF-8') as archivo:
        json.dump(datas1, archivo)
# Modificar los partidos de los playoff
@app.route('/modificar_eliminatoria_salvador/<string:id>', methods=['GET', 'POST'])
def modificar_playoff_salvador(id):
    datas1 = obtener_playoff_salvador()
    # Buscar la eliminatoria correspondiente al ID proporcionado
    eliminatoria_encontrada = None
    for eliminatoria, datos_eliminatoria in datas1.items():
        if datos_eliminatoria['id'] == id:
            eliminatoria_encontrada = datos_eliminatoria
            break
    if not eliminatoria_encontrada:
        return "Eliminatoria no encontrada"
    if request.method == 'POST':
        nuevos_partidos = []
        for index, partido in enumerate(eliminatoria_encontrada['partidos']):
            local = request.form.get(f'local{index}')
            resultadoA = request.form.get(f'resultadoA{index}')
            resultadoB = request.form.get(f'resultadoB{index}')
            visitante = request.form.get(f'visitante{index}')
            fecha = request.form.get(f'fecha{index}')
            hora = request.form.get(f'hora{index}')
            # Actualizar los datos del partido
            partido['local'] = local
            partido['resultadoA'] = resultadoA
            partido['resultadoB'] = resultadoB
            partido['visitante'] = visitante
            partido['fecha'] = fecha
            partido['hora'] = hora
            nuevos_partidos.append(partido)   
        eliminatoria_encontrada['partidos'] = nuevos_partidos       
        # Guardar los cambios en el archivo JSON
        guardar_playoff_salvador(datas1)       
        # Redireccionar a la página de visualización del playoff
        return redirect(url_for('ver_playoff_salvador'))   
# Crear la clasificación de El Salvador
def generar_clasificacion_analisis_rugby_salvador(data11, total_partidos_temporada_salvador):
    default_dict = defaultdict(lambda: {})
    clasificacion = defaultdict(lambda: {'puntos': 0,'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'favor': 0, 'contra': 0, 'diferencia_goles': 0, 'bonus': 0})
    for jornada in data11[:total_partidos_temporada_salvador]:
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
    print(generar_clasificacion_analisis_rugby_salvador)
    return clasificacion_ordenada
# Crear la clasificación para el GrupoA1 y GrupoB1 de El Salvador
def generar_clasificacion_grupoA1_grupoB1(data11, total_partidos_temporada_grupos_salvador):
    clasificacion = defaultdict(lambda: {'puntos': 0, 'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'favor': 0, 'contra': 0, 'diferencia_goles': 0, 'bonus': 0})
    for jornada in data11[:total_partidos_temporada_grupos_salvador]:
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
    data11 = obtener_datos_salvador()
    total_partidos_temporada_salvador = 11
    total_partidos_temporada_grupos_salvador = 16
    # Llama a la función para generar la clasificación y análisis
    clasificacion_analisis_salvador = generar_clasificacion_analisis_rugby_salvador(data11, total_partidos_temporada_salvador)
    # Ordena la clasificación por puntos y diferencia de goles
    clasificacion_analisis_salvador = sorted(clasificacion_analisis_salvador, key=lambda x: (x['datos']['puntos'], x['datos']['diferencia_goles']), reverse=True)
    # Genera los grupos A y B
    grupoA1, grupoB1 = generar_clasificacion_grupoA1_grupoB1(data11, total_partidos_temporada_grupos_salvador)
    
    return render_template('equipos_rugby/clasi_analis_salvador.html', clasificacion_analisis_salvador=clasificacion_analisis_salvador, grupoA1=grupoA1, grupoB1=grupoB1)
# Ruta para mostrar los playoffs de El Salvador
@app.route('/playoffs_salvador/')
def playoffs_salvador():
    # Obtener datos de las eliminatorias
    datas1 = obtener_playoff_salvador()
    return render_template('playoffs/salvador_playoff.html', datas1=datas1)
# Ruta y creación del calendario individual de El Salvador
@app.route('/equipos_rugby/calendario_salvador')
def calendarios_salvador():
    datos11 = obtener_datos_salvador()
    nuevos_datos_salvador = [dato for dato in datos11 if dato]
    equipo_salvador = 'El Salvador'
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
#Fin proceso El Salvador

#Todo el proceso de calendario y clasificación del VRAC
# Ruta de partidos VRAC
part_vrac = 'json/partidos_vrac.json'
def guardar_datos_vrac(data12):
    # Guardar los datos en el archivo JSON
    with open(part_vrac, 'w', encoding='utf-8') as file:
        json.dump(data12, file, indent=4)
def obtener_datos_vrac():
    try:
    # Leer los datos desde el archivo JSON
      with open(part_vrac, 'r', encoding='utf-8') as file:
        data12 = json.load(file)
      return data12
    except json.decoder.JSONDecodeError:
        # Manejar archivo vacío, inicializar con una estructura JSON válida
        return []
# Partidos El Salvador
@app.route('/admin/calend_vrac')
def calend_vrac():
    data12 = obtener_datos_vrac()
    return render_template('admin/calend_vrac.html', data12=data12)
# Ingresar los resultados de los partidos del VRAC
@app.route('/admin/crear_calendario_vrac', methods=['POST'])
def ingresar_resul_vrac():
    data12 = obtener_datos_vrac()
    nums_partidos = int(request.form.get('num_partidos', 0))
    jornada_nombre = request.form.get('nombre')
    jornada_existente = next((j for j in data12 if j["nombre"] == jornada_nombre), None)
    if jornada_existente:
        # Si la jornada ya existe, utiliza su identificador existente
        jornada_id = jornada_existente["id"]
        jornada = jornada_existente
    else:
        # Si la jornada no existe, crea un nuevo identificador
        jornada_id = str(uuid.uuid4())
        jornada = {"id": jornada_id, "nombre": jornada_nombre, "partidos": []}
        data12.append(jornada)
    for i in range(nums_partidos):
        #id_nuevo = str(uuid.uuid4())
        equipoLocal = request.form.get(f'local{i}')
        bonusA = request.form.get(f'bonusA{i}')
        resultadoA = request.form.get(f'resultadoA{i}')
        resultadoB = request.form.get(f'resultadoB{i}')
        bonusB = request.form.get(f'bonusB{i}')
        equipoVisitante = request.form.get(f'visitante{i}')
        fecha = request.form.get(f'fecha{i}')
        hora = request.form.get(f'hora{i}')
        nuevo_partido = {
            #'id': id_nuevo,
            'local': equipoLocal,
            'bonusA': bonusA,
            'resultadoA': resultadoA,
            'resultadoB': resultadoB,
            'bonusB': bonusB,
            'visitante': equipoVisitante,
            'fecha' : fecha,
            'hora' : hora
        }
        jornada["partidos"].append(nuevo_partido)
    guardar_datos_vrac(data12)
    return redirect(url_for('calend_vrac'))
# Toma la lista de los resultados y los guarda
def guardar_partidos_en_archivo_vrac(data12):
    arch_guardar_vrac = 'json/partidos_vrac.json'
    # Guardar en el archivo
    with open(arch_guardar_vrac, 'w', encoding='UTF-8') as archivo:
        json.dump(data12, archivo)
# Modificar los partidos de cada jornada
@app.route('/modificar_jornada_vrac/<string:id>', methods=['POST'])
def modificar_jorn_vrac(id):
    data12 = obtener_datos_vrac()
    if request.method == 'POST':
        jornada_nombre = request.form.get('nombre')
        resultados_a_modificar = next((result for result in data12 if result['id'] == id), None)
        if resultados_a_modificar:
            resultados_a_modificar['nombre'] = jornada_nombre
            resultados_a_modificar['partidos'] = []  # Reiniciar la lista de partidos
            for i in range(6):  # Ajusta según la cantidad máxima de partidos
                equipoLocal = request.form.get(f'local{i}')
                bonusA = request.form.get(f'bonusA{i}')
                resultadoA = request.form.get(f'resultadoA{i}')
                resultadoB = request.form.get(f'resultadoB{i}')
                bonusB = request.form.get(f'bonusB{i}')
                equipoVisitante = request.form.get(f'visitante{i}')
                fecha = request.form.get(f'fecha{i}')
                hora = request.form.get(f'hora{i}')
                nuevo_partido = {
                    'local': equipoLocal,
                    'bonusA': bonusA,
                    'resultadoA': resultadoA,
                    'resultadoB': resultadoB,
                    'bonusB': bonusB,
                    'visitante': equipoVisitante,
                    'fecha' : fecha,
                    'hora' : hora
                }
                resultados_a_modificar['partidos'].append(nuevo_partido)
            # Guardar los cambios en el archivo JSON
            guardar_partidos_en_archivo_vrac(data12)            
            return redirect(url_for('calend_vrac'))
    return redirect(url_for('calend_vrac'))
# Ruta para borrar jornadas
@app.route('/eliminar_jorn_vrac/<string:id>', methods=['POST'])
def eliminar_jorn_vrac(id):
    data12 = obtener_datos_vrac()
    jornada_a_eliminar = [j for j in data12 if j['id'] != id]  # Filtrar las jornadas diferentes de la que se va a eliminar
    guardar_partidos_en_archivo_vrac(jornada_a_eliminar)
    return redirect(url_for('calend_vrac'))
# PlayOff El Salvador
playoff_vrac = 'json_playoff/playoff_vrac.json'
def guardar_playoff_vrac(datas2):
    with open(playoff_vrac, 'w', encoding='utf-8') as file:
        json.dump(datas2, file, indent=4)
def obtener_playoff_vrac():
    try:
        with open(playoff_vrac, 'r', encoding='utf-8') as file:
            datas2 = json.load(file)
        return datas2
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return {'cuartos': [], 'semifinales': [], 'final': []}
nuevos_enfrentamientos_vrac = []
partido_vrac = None
# Crear formulario para los playoff
@app.route('/admin/playoff_vrac/')
def ver_playoff_vrac():
    datas2 = obtener_playoff_vrac()
    return render_template('admin/playoff_vrac.html', datas2=datas2)
# Crear formulario para los playoff
@app.route('/admin/crear_playoff_vrac', methods=['GET', 'POST'])
def crear_playoff_vrac():
    # Obtener los enfrentamientos actuales del archivo JSON
    datas2 = obtener_playoff_vrac()
    if request.method == 'POST':
        # Obtener la etapa del torneo seleccionada por el usuario
        eliminatoria = request.form.get('eliminatoria')
        # Verificar el número máximo de partidos permitidos según la etapa del torneo
        if eliminatoria == 'cuartos':
            max_partidos = 4
        elif eliminatoria == 'semifinales':
            max_partidos = 2
        elif eliminatoria == 'final':
            max_partidos = 1
        else:
            # Manejar caso no válido
            return "Etapa de torneo no válida"
        # Recuperar los datos del formulario y procesarlos
        num_partidos_str = request.form.get('num_partidos', '0')  # Valor predeterminado '0' si num_partidos está vacío
        num_partidos_str = num_partidos_str.strip()  # Eliminar espacios en blanco
        if num_partidos_str:
            num_partidos = int(num_partidos_str)
        else:
            num_partidos = 0  # Valor predeterminado si num_partidos está vacío
        # Si num_partidos es cero, se ignora la validación
        if num_partidos < 0:
            return "Número de partidos no válido"
        # Crear un identificador único para la eliminatoria
        eliminatoria_id = str(uuid.uuid4())  # Generar un UUID único
        # Crear un nuevo diccionario con los datos de la eliminatoria
        eliminatoria_data = {
            'id': eliminatoria_id,
            'partidos': []
        }
        # Recuperar los datos de cada partido del formulario
        for i in range(num_partidos):
            local = request.form.get(f'local{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            visitante = request.form.get(f'visitante{i}')
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            # Crear un nuevo diccionario con los datos del partido
            partido = {
                'local': local,
                'resultadoA': resultadoA,
                'resultadoB': resultadoB,
                'visitante': visitante,
                'fecha' : fecha,
                'hora' : hora
            }
            # Agregar el partido a la lista de partidos de la eliminatoria
            eliminatoria_data['partidos'].append(partido)
            # Agregar los nuevos enfrentamientos a la lista correspondiente
        datas2[eliminatoria] = eliminatoria_data
         # Agregar los nuevos enfrentamientos a la lista correspondiente
        nuevos_enfrentamientos.clear()  
        # Guardar la lista de partidos en el archivo JSON
        guardar_playoff_vrac(datas2)
        # Redireccionar a la página de visualización del playoff
        return redirect(url_for('ver_playoff_vrac'))
    # Si no es una solicitud POST, renderizar el formulario
    return render_template('admin/playoff_vrac.html', datas2=datas2)
# Toma la lista de los playoff y los guarda
def guardar_playoff_en_archivo_vrac(datas2):
    arch_guardar_playoff_vrac = 'json_playoff/playoff_vrac.json'
    # Guardar en el archivo
    with open(arch_guardar_playoff_vrac, 'w', encoding='UTF-8') as archivo:
        json.dump(datas2, archivo)
# Modificar los partidos de los playoff
@app.route('/modificar_eliminatoria_vrac/<string:id>', methods=['GET', 'POST'])
def modificar_playoff_vrac(id):
    datas2 = obtener_playoff_vrac()
    # Buscar la eliminatoria correspondiente al ID proporcionado
    eliminatoria_encontrada = None
    for eliminatoria, datos_eliminatoria in datas2.items():
        if datos_eliminatoria['id'] == id:
            eliminatoria_encontrada = datos_eliminatoria
            break
    if not eliminatoria_encontrada:
        return "Eliminatoria no encontrada"
    if request.method == 'POST':
        nuevos_partidos = []
        for index, partido in enumerate(eliminatoria_encontrada['partidos']):
            local = request.form.get(f'local{index}')
            resultadoA = request.form.get(f'resultadoA{index}')
            resultadoB = request.form.get(f'resultadoB{index}')
            visitante = request.form.get(f'visitante{index}')
            fecha = request.form.get(f'fecha{index}')
            hora = request.form.get(f'hora{index}')
            # Actualizar los datos del partido
            partido['local'] = local
            partido['resultadoA'] = resultadoA
            partido['resultadoB'] = resultadoB
            partido['visitante'] = visitante
            partido['fecha'] = fecha
            partido['hora'] = hora
            nuevos_partidos.append(partido)   
        eliminatoria_encontrada['partidos'] = nuevos_partidos       
        # Guardar los cambios en el archivo JSON
        guardar_playoff_vrac(datas2)       
        # Redireccionar a la página de visualización del playoff
        return redirect(url_for('ver_playoff_vrac')) 
# Crear la clasificación del VRAC
def generar_clasificacion_analisis_rugby_vrac(data12, total_partidos_temporada_vrac):
    default_dict = defaultdict(lambda: {})
    clasificacion = defaultdict(lambda: {'puntos': 0,'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'favor': 0, 'contra': 0, 'diferencia_goles': 0, 'bonus': 0})
    for jornada in data12[:total_partidos_temporada_vrac]:
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
    print(generar_clasificacion_analisis_rugby_vrac)
    return clasificacion_ordenada
# Crear la clasificación para el GrupoA2 y GrupoB2 del VRAC
def generar_clasificacion_grupoA2_grupoB2(data12, total_partidos_temporada_grupos_vrac):
    clasificacion = defaultdict(lambda: {'puntos': 0, 'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'favor': 0, 'contra': 0, 'diferencia_goles': 0, 'bonus': 0})
    for jornada in data12[:total_partidos_temporada_grupos_vrac]:
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
    total_partidos_temporada_vrac = 11
    total_partidos_temporada_grupos_vrac = 16
    # Llama a la función para generar la clasificación y análisis
    clasificacion_analisis_vrac = generar_clasificacion_analisis_rugby_vrac(data12, total_partidos_temporada_vrac)
    # Ordena la clasificación por puntos y diferencia de goles
    clasificacion_analisis_vrac = sorted(clasificacion_analisis_vrac, key=lambda x: (x['datos']['puntos'], x['datos']['diferencia_goles']), reverse=True)
    # Genera los grupos A y B
    grupoA2, grupoB2 = generar_clasificacion_grupoA2_grupoB2(data12, total_partidos_temporada_grupos_vrac)
    return render_template('equipos_rugby/clasi_analis_vrac.html', clasificacion_analisis_vrac=clasificacion_analisis_vrac, grupoA2=grupoA2, grupoB2=grupoB2)
# Ruta para mostrar los playoffs del VRAC
@app.route('/playoffs_vrac/')
def playoffs_vrac():
    # Obtener datos de las eliminatorias
    datas2 = obtener_playoff_vrac()
    return render_template('playoffs/vrac_playoff.html', datas2=datas2)
# Ruta y creación del calendario individual de El Salvador
@app.route('/equipos_rugby/calendario_vrac')
def calendarios_vrac():
    datos12 = obtener_datos_vrac()
    nuevos_datos_vrac = [dato for dato in datos12 if dato]
    equipo_vrac = 'VRAC'
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
#Fin proceso del VRAC

#Todo el proceso de calendario y clasificación del El Salvador Fem.
# Ruta de partidos El Salvador Fem.
part_salvador_fem = 'json/partidos_salvador_fem.json'
def guardar_datos_salvador_fem(data13):
    # Guardar los datos en el archivo JSON
    with open(part_salvador_fem, 'w', encoding='utf-8') as file:
        json.dump(data13, file, indent=4)
def obtener_datos_salvador_fem():
    try:
    # Leer los datos desde el archivo JSON
      with open(part_salvador_fem, 'r', encoding='utf-8') as file:
        data13 = json.load(file)
      return data13
    except json.decoder.JSONDecodeError:
        # Manejar archivo vacío, inicializar con una estructura JSON válida
        return []
# Partidos El Salvador
@app.route('/admin/calend_salvador_fem')
def calend_salvador_fem():
    data13 = obtener_datos_salvador_fem()
    return render_template('admin/calend_salvador_fem.html', data13=data13)
# Ingresar los resultados de los partidos de El Salvador Fem.
@app.route('/admin/crear_calendario_salvador_fem', methods=['POST'])
def ingresar_resul_salvador_fem():
    data13 = obtener_datos_salvador_fem()
    nums_partidos = int(request.form.get('num_partidos', 0))
    jornada_nombre = request.form.get('nombre')
    jornada_existente = next((j for j in data13 if j["nombre"] == jornada_nombre), None)
    if jornada_existente:
        # Si la jornada ya existe, utiliza su identificador existente
        jornada_id = jornada_existente["id"]
        jornada = jornada_existente
    else:
        # Si la jornada no existe, crea un nuevo identificador
        jornada_id = str(uuid.uuid4())
        jornada = {"id": jornada_id, "nombre": jornada_nombre, "partidos": []}
        data13.append(jornada)
    for i in range(nums_partidos):
        #id_nuevo = str(uuid.uuid4())
        equipoLocal = request.form.get(f'local{i}')
        bonusA = request.form.get(f'bonusA{i}')
        resultadoA = request.form.get(f'resultadoA{i}')
        resultadoB = request.form.get(f'resultadoB{i}')
        bonusB = request.form.get(f'bonusB{i}')
        equipoVisitante = request.form.get(f'visitante{i}')
        fecha = request.form.get(f'fecha{i}')
        hora = request.form.get(f'hora{i}')
        nuevo_partido = {
            #'id': id_nuevo,
            'local': equipoLocal,
            'bonusA': bonusA,
            'resultadoA': resultadoA,
            'resultadoB': resultadoB,
            'bonusB': bonusB,
            'visitante': equipoVisitante,
            'fecha' : fecha,
            'hora' : hora
        }
        jornada["partidos"].append(nuevo_partido)
    guardar_datos_salvador_fem(data13)
    return redirect(url_for('calend_salvador_fem'))
# Toma la lista de los resultados y los guarda
def guardar_partidos_en_archivo_salvador_fem(data13):
    arch_guardar_salvador_fem = 'json/partidos_salvador_fem.json'
    # Guardar en el archivo
    with open(arch_guardar_salvador_fem, 'w', encoding='UTF-8') as archivo:
        json.dump(data13, archivo)
# Modificar los partidos de cada jornada
@app.route('/modificar_jornada_salvador_fem/<string:id>', methods=['POST'])
def modificar_jorn_salvador_fem(id):
    data13 = obtener_datos_salvador_fem()
    if request.method == 'POST':
        jornada_nombre = request.form.get('nombre')
        resultados_a_modificar = next((result for result in data13 if result['id'] == id), None)
        if resultados_a_modificar:
            resultados_a_modificar['nombre'] = jornada_nombre
            resultados_a_modificar['partidos'] = []  # Reiniciar la lista de partidos
            for i in range(4):  # Ajusta según la cantidad máxima de partidos
                equipoLocal = request.form.get(f'local{i}')
                bonusA = request.form.get(f'bonusA{i}')
                resultadoA = request.form.get(f'resultadoA{i}')
                resultadoB = request.form.get(f'resultadoB{i}')
                bonusB = request.form.get(f'bonusB{i}')
                equipoVisitante = request.form.get(f'visitante{i}')
                fecha = request.form.get(f'fecha{i}')
                hora = request.form.get(f'hora{i}')
                nuevo_partido = {
                    'local': equipoLocal,
                    'bonusA': bonusA,
                    'resultadoA': resultadoA,
                    'resultadoB': resultadoB,
                    'bonusB': bonusB,
                    'visitante': equipoVisitante,
                    'fecha' : fecha,
                    'hora' : hora
                }
                resultados_a_modificar['partidos'].append(nuevo_partido)
            # Guardar los cambios en el archivo JSON
            guardar_partidos_en_archivo_salvador_fem(data13)            
            return redirect(url_for('calend_salvador_fem'))
    return redirect(url_for('calend_salvador_fem'))
# Ruta para borrar jornadas
@app.route('/eliminar_jorn_salvador_fem/<string:id>', methods=['POST'])
def eliminar_jorn_salvador_fem(id):
    data13 = obtener_datos_salvador_fem()
    jornada_a_eliminar = [j for j in data13 if j['id'] != id]  # Filtrar las jornadas diferentes de la que se va a eliminar
    guardar_partidos_en_archivo_salvador_fem(jornada_a_eliminar)
    return redirect(url_for('calend_salvador_fem'))
# PlayOff El Salvador Fem.
playoff_salvador_fem = 'json_playoff/playoff_salvador_fem.json'
def guardar_playoff_salvador_fem(datas3):
    with open(playoff_salvador_fem, 'w', encoding='utf-8') as file:
        json.dump(datas3, file, indent=4)
def obtener_playoff_salvador_fem():
    try:
        with open(playoff_salvador_fem, 'r', encoding='utf-8') as file:
            datas3 = json.load(file)
        return datas3
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return {'cuartos': [], 'semifinales': [], 'final': []}
nuevos_enfrentamientos = []
partido = None
# Crear formulario para los playoff
@app.route('/admin/playoff_salvador_fem/')
def ver_playoff_salvador_fem():
    datas3 = obtener_playoff_salvador_fem()
    return render_template('admin/playoff_salvador_fem.html', datas3=datas3)
# Crear formulario para los playoff
@app.route('/admin/crear_playoff_salvador_fem', methods=['GET', 'POST'])
def crear_playoff_salvador_fem():
    # Obtener los enfrentamientos actuales del archivo JSON
    datas3 = obtener_playoff_salvador_fem()
    if request.method == 'POST':
        # Obtener la etapa del torneo seleccionada por el usuario
        eliminatoria = request.form.get('eliminatoria')
        # Verificar el número máximo de partidos permitidos según la etapa del torneo
        if eliminatoria == 'cuartos':
            max_partidos = 4
        elif eliminatoria == 'semifinales':
            max_partidos = 2
        elif eliminatoria == 'final':
            max_partidos = 1
        else:
            # Manejar caso no válido
            return "Etapa de torneo no válida"
        # Recuperar los datos del formulario y procesarlos
        num_partidos_str = request.form.get('num_partidos', '0')  # Valor predeterminado '0' si num_partidos está vacío
        num_partidos_str = num_partidos_str.strip()  # Eliminar espacios en blanco
        if num_partidos_str:
            num_partidos = int(num_partidos_str)
        else:
            num_partidos = 0  # Valor predeterminado si num_partidos está vacío
        # Si num_partidos es cero, se ignora la validación
        if num_partidos < 0:
            return "Número de partidos no válido"
        # Crear un identificador único para la eliminatoria
        eliminatoria_id = str(uuid.uuid4())  # Generar un UUID único
        # Crear un nuevo diccionario con los datos de la eliminatoria
        eliminatoria_data = {
            'id': eliminatoria_id,
            'partidos': []
        }
        # Recuperar los datos de cada partido del formulario
        for i in range(num_partidos):
            local = request.form.get(f'local{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            visitante = request.form.get(f'visitante{i}')
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            # Crear un nuevo diccionario con los datos del partido
            partido = {
                'local': local,
                'resultadoA': resultadoA,
                'resultadoB': resultadoB,
                'visitante': visitante,
                'fecha' : fecha,
                'hora' : hora
            }
            # Agregar el partido a la lista de partidos de la eliminatoria
            eliminatoria_data['partidos'].append(partido)
            # Agregar los nuevos enfrentamientos a la lista correspondiente
        datas3[eliminatoria] = eliminatoria_data
         # Agregar los nuevos enfrentamientos a la lista correspondiente
        nuevos_enfrentamientos.clear()  
        # Guardar la lista de partidos en el archivo JSON
        guardar_playoff_salvador_fem(datas3)
        # Redireccionar a la página de visualización del playoff
        return redirect(url_for('ver_playoff_salvador_fem'))
    # Si no es una solicitud POST, renderizar el formulario
    return render_template('admin/playoff_salvador_fem.html', datas3=datas3)
# Toma la lista de los playoff y los guarda
def guardar_playoff_en_archivo_salvador_fem(datas3):
    arch_guardar_playoff_salvador_fem = 'json_playoff/partidos_salvador_fem.json'
    # Guardar en el archivo
    with open(arch_guardar_playoff_salvador_fem, 'w', encoding='UTF-8') as archivo:
        json.dump(datas3, archivo)
# Modificar los partidos de los playoff
@app.route('/modificar_eliminatoria_salvador_fem/<string:id>', methods=['GET', 'POST'])
def modificar_playoff_salvador_fem(id):
    datas3 = obtener_playoff_salvador_fem()
    # Buscar la eliminatoria correspondiente al ID proporcionado
    eliminatoria_encontrada = None
    for eliminatoria, datos_eliminatoria in datas1.items():
        if datos_eliminatoria['id'] == id:
            eliminatoria_encontrada = datos_eliminatoria
            break
    if not eliminatoria_encontrada:
        return "Eliminatoria no encontrada"
    if request.method == 'POST':
        nuevos_partidos = []
        for index, partido in enumerate(eliminatoria_encontrada['partidos']):
            local = request.form.get(f'local{index}')
            resultadoA = request.form.get(f'resultadoA{index}')
            resultadoB = request.form.get(f'resultadoB{index}')
            visitante = request.form.get(f'visitante{index}')
            fecha = request.form.get(f'fecha{index}')
            hora = request.form.get(f'hora{index}')
            # Actualizar los datos del partido
            partido['local'] = local
            partido['resultadoA'] = resultadoA
            partido['resultadoB'] = resultadoB
            partido['visitante'] = visitante
            partido['fecha'] = fecha
            partido['hora'] = hora
            nuevos_partidos.append(partido)   
        eliminatoria_encontrada['partidos'] = nuevos_partidos       
        # Guardar los cambios en el archivo JSON
        guardar_playoff_salvador_fem(datas3)       
        # Redireccionar a la página de visualización del playoff
        return redirect(url_for('ver_playoff_salvador_fem'))   
# Crear la clasificación de El Salvador
def generar_clasificacion_analisis_rugby_salvador_fem(data13, total_partidos_temporada_salvador_fem):
    default_dict = defaultdict(lambda: {})
    clasificacion = defaultdict(lambda: {'puntos': 0,'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'favor': 0, 'contra': 0, 'diferencia_goles': 0, 'bonus': 0})
    for jornada in data13[:total_partidos_temporada_salvador_fem]:
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
    print(generar_clasificacion_analisis_rugby_salvador_fem)
    return clasificacion_ordenada
# Crear la clasificación para el GrupoA y GrupoB de El Salvador Fem.
def generar_clasificacion_grupoA_grupoB(data13, total_partidos_temporada_grupos_salvador_fem):
    clasificacion = defaultdict(lambda: {'puntos': 0, 'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'favor': 0, 'contra': 0, 'diferencia_goles': 0, 'bonus': 0})
    for jornada in data13[:total_partidos_temporada_grupos_salvador_fem]:
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
    grupoA = clasificacion_ordenada[:4]
    grupoB = clasificacion_ordenada[4:8]
    return grupoA, grupoB
# Ruta para mostrar la clasificación de El Salvador Fem.
@app.route('/equipos_rugby/clasi_analis_salvador_fem/')
def clasif_analisis_salvador_fem():
    data13 = obtener_datos_salvador_fem()
    total_partidos_temporada_salvador_fem = 7
    total_partidos_temporada_grupos_salvador_fem = 10
    # Llama a la función para generar la clasificación y análisis
    clasificacion_analisis_salvador_fem = generar_clasificacion_analisis_rugby_salvador_fem(data13, total_partidos_temporada_salvador_fem)
    # Ordena la clasificación por puntos y diferencia de goles
    clasificacion_analisis_salvador_fem = sorted(clasificacion_analisis_salvador_fem, key=lambda x: (x['datos']['puntos'], x['datos']['diferencia_goles']), reverse=True)
    # Genera los grupos A y B
    grupoA, grupoB = generar_clasificacion_grupoA_grupoB(data13, total_partidos_temporada_grupos_salvador_fem)
    return render_template('equipos_rugby/clasi_analis_salvador_fem.html', clasificacion_analisis_salvador_fem=clasificacion_analisis_salvador_fem, grupoA=grupoA, grupoB=grupoB)
# Ruta para mostrar los playoffs de El Salvador Fem.
@app.route('/playoffs_salvador_fem/')
def playoffs_salvador_fem():
    # Obtener datos de las eliminatorias
    datas3 = obtener_playoff_salvador_fem()
    return render_template('playoffs/salvador_fem_playoff.html', datas3=datas3)
# Ruta y creación del calendario individual de El Salvador Fem.
@app.route('/equipos_rugby/calendario_salvador_fem')
def calendarios_salvador_fem():
    datos13 = obtener_datos_salvador_fem()
    nuevos_datos_salvador_fem = [dato for dato in datos13 if dato]
    equipo_salvador_fem = 'El Salvador Fem.'
    tabla_partidos_salvador_fem = {}
    # Iteramos sobre cada jornada y partido
    for jornada in datos13:
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
                    rol_salvador = 'C'
                else:
                    equipo_contrario = equipo_local
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_salvador = 'F'
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
                # Asignamos los resultados según el rol del Real Valladolid
                if equipo_local == equipo_contrario or equipo_visitante == equipo_contrario:
                  if not tabla_partidos_salvador_fem[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA']:
                    tabla_partidos_salvador_fem[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA'] = resultado_a
                    tabla_partidos_salvador_fem[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoB'] = resultado_b
                    tabla_partidos_salvador_fem[equipo_contrario]['jornadas'][jornada['nombre']]['rol_salvador_fem'] = rol_salvador_fem
                  else:
                    tabla_partidos_salvador_fem[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_salvador_fem[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_salvador_fem[equipo_contrario]['jornadas'][jornada['nombre']]['rol_salvador_fem'] = rol_salvador_fem
                else:
                  if not tabla_partidos_salvador_fem[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA']:
                    tabla_partidos_salvador_fem[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_salvador_fem[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_salvador_fem[equipo_contrario]['jornadas'][jornada['nombre']]['rol_salvador_fem'] = rol_salvador_fem
                  else:
                    tabla_partidos_salvador_fem[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_salvador_fem[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_salvador_fem[equipo_contrario]['jornadas'][jornada['nombre']]['rol_salvador_fem'] = rol_salvador_fem
    return render_template('equipos_rugby/calendario_salvador_fem.html', tabla_partidos_salvador_fem=tabla_partidos_salvador_fem, nuevos_datos_salvador_fem=nuevos_datos_salvador_fem)
#Fin proceso El Salvador

#EQUIPOS HOCKEY
#Todo el proceso de calendario y clasificación del CPLV Caja Rural
# Ruta de partidos CPLV Caja Rural
part_caja = 'json/partidos_caja.json'
def guardar_datos_caja(data14):
    # Guardar los datos en el archivo JSON
    with open(part_caja, 'w', encoding='utf-8') as file:
        json.dump(data14, file, indent=4)
def obtener_datos_caja():
    try:
    # Leer los datos desde el archivo JSON
      with open(part_caja, 'r', encoding='utf-8') as file:
        data14 = json.load(file)
      return data14
    except json.decoder.JSONDecodeError:
        # Manejar archivo vacío, inicializar con una estructura JSON válida
        return []
# Partidos Caja Rural CPLV
@app.route('/admin/calend_caja')
def calend_caja():
    data14 = obtener_datos_caja()
    return render_template('admin/calend_caja.html', data14=data14)
# Ingresar los resultados de los partidos de CPLV Caja Rural
@app.route('/admin/crear_calendario_caja', methods=['POST'])
def ingresar_resul_caja():
    data14 = obtener_datos_caja()
    nums_partidos = int(request.form.get('num_partidos', 0))
    jornada_nombre = request.form.get('nombre')
    jornada_existente = next((j for j in data14 if j["nombre"] == jornada_nombre), None)
    if jornada_existente:
        # Si la jornada ya existe, utiliza su identificador existente
        jornada_id = jornada_existente["id"]
        jornada = jornada_existente
    else:
        # Si la jornada no existe, crea un nuevo identificador
        jornada_id = str(uuid.uuid4())
        jornada = {"id": jornada_id, "nombre": jornada_nombre, "partidos": []}
        data14.append(jornada)
    for i in range(nums_partidos):
        #id_nuevo = str(uuid.uuid4())
        equipoLocal = request.form.get(f'local{i}')
        bonusA = request.form.get(f'bonusA{i}')
        resultadoA = request.form.get(f'resultadoA{i}')
        resultadoB = request.form.get(f'resultadoB{i}')
        bonusB = request.form.get(f'bonusB{i}')
        equipoVisitante = request.form.get(f'visitante{i}')
        fecha = request.form.get(f'fecha{i}')
        hora = request.form.get(f'hora{i}')
        nuevo_partido = {
            #'id': id_nuevo,
            'local': equipoLocal,
            'bonusA': bonusA,
            'resultadoA': resultadoA,
            'resultadoB': resultadoB,
            'bonusB': bonusB,
            'visitante': equipoVisitante,
            'fecha' : fecha,
            'hora' : hora
        }
        jornada["partidos"].append(nuevo_partido)
    guardar_datos_caja(data14)
    return redirect(url_for('calend_caja'))
# Toma la lista de los resultados y los guarda
def guardar_partidos_en_archivo_caja(data14):
    arch_guardar_caja = 'json/partidos_caja.json'
    # Guardar en el archivo
    with open(arch_guardar_caja, 'w', encoding='UTF-8') as archivo:
        json.dump(data14, archivo)
# Modificar los partidos de cada jornada
@app.route('/modificar_jornada_caja/<string:id>', methods=['POST'])
def modificar_jorn_caja(id):
    data14 = obtener_datos_caja()
    if request.method == 'POST':
        jornada_nombre = request.form.get('nombre')
        resultados_a_modificar = next((result for result in data14 if result['id'] == id), None)
        if resultados_a_modificar:
            resultados_a_modificar['nombre'] = jornada_nombre
            resultados_a_modificar['partidos'] = []  # Reiniciar la lista de partidos
            for i in range(5):  # Ajusta según la cantidad máxima de partidos
                equipoLocal = request.form.get(f'local{i}')
                bonusA = request.form.get(f'bonusA{i}')
                resultadoA = request.form.get(f'resultadoA{i}')
                resultadoB = request.form.get(f'resultadoB{i}')
                bonusB = request.form.get(f'bonusB{i}')
                equipoVisitante = request.form.get(f'visitante{i}')
                fecha = request.form.get(f'fecha{i}')
                hora = request.form.get(f'hora{i}')
                nuevo_partido = {
                    'local': equipoLocal,
                    'bonusA': bonusA,
                    'resultadoA': resultadoA,
                    'resultadoB': resultadoB,
                    'bonusB': bonusB,
                    'visitante': equipoVisitante,
                    'fecha' : fecha,
                    'hora' : hora
                }
                resultados_a_modificar['partidos'].append(nuevo_partido)
            # Guardar los cambios en el archivo JSON
            guardar_partidos_en_archivo_caja(data14)            
            return redirect(url_for('calend_caja'))
    return redirect(url_for('calend_caja'))
# Ruta para borrar jornadas
@app.route('/eliminar_jorn_caja/<string:id>', methods=['POST'])
def eliminar_jorn_caja(id):
    data14 = obtener_datos_caja()
    jornada_a_eliminar = [j for j in data14 if j['id'] != id]  # Filtrar las jornadas diferentes de la que se va a eliminar
    guardar_partidos_en_archivo_caja(jornada_a_eliminar)
    return redirect(url_for('calend_caja'))
# PlayOff Caja Rural CPLV
playoff_caja = 'json_playoff/playoff_caja.json'
def guardar_playoff_caja(datas5):
    with open(playoff_caja, 'w', encoding='utf-8') as file:
        json.dump(datas5, file, indent=4)
def obtener_playoff_caja():
    try:
        with open(playoff_caja, 'r', encoding='utf-8') as file:
            datas5 = json.load(file)
        return datas5
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return {'cuartos': [], 'semifinales': [], 'final': []}
nuevos_enfrentamientos_caja = []
partido_caja = None
# Crear formulario para los playoff
@app.route('/admin/playoff_caja/')
def ver_playoff_caja():
    datas5 = obtener_playoff_caja()
    return render_template('admin/playoff_caja.html', datas5=datas5)
# Crear formulario para los playoff
@app.route('/admin/crear_playoff_caja', methods=['GET', 'POST'])
def crear_playoff_caja():
    # Obtener los enfrentamientos actuales del archivo JSON
    datas5 = obtener_playoff_caja()
    if request.method == 'POST':
        # Obtener la etapa del torneo seleccionada por el usuario
        eliminatoria = request.form.get('eliminatoria')
        # Verificar el número máximo de partidos permitidos según la etapa del torneo
        if eliminatoria == 'cuartos':
            max_partidos = 4
        elif eliminatoria == 'semifinales':
            max_partidos = 2
        elif eliminatoria == 'final':
            max_partidos = 1
        else:
            # Manejar caso no válido
            return "Etapa de torneo no válida"
        # Recuperar los datos del formulario y procesarlos
        num_partidos_str = request.form.get('num_partidos', '0')  # Valor predeterminado '0' si num_partidos está vacío
        num_partidos_str = num_partidos_str.strip()  # Eliminar espacios en blanco
        if num_partidos_str:
            num_partidos = int(num_partidos_str)
        else:
            num_partidos = 0  # Valor predeterminado si num_partidos está vacío
        # Si num_partidos es cero, se ignora la validación
        if num_partidos < 0:
            return "Número de partidos no válido"
        # Crear un identificador único para la eliminatoria
        eliminatoria_id = str(uuid.uuid4())  # Generar un UUID único
        # Crear un nuevo diccionario con los datos de la eliminatoria
        eliminatoria_data = {
            'id': eliminatoria_id,
            'partidos': []
        }
        # Recuperar los datos de cada partido del formulario
        for i in range(num_partidos):
            local = request.form.get(f'local{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            visitante = request.form.get(f'visitante{i}')
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            # Crear un nuevo diccionario con los datos del partido
            partido = {
                'local': local,
                'resultadoA': resultadoA,
                'resultadoB': resultadoB,
                'visitante': visitante,
                'fecha' : fecha,
                'hora' : hora
            }
            # Agregar el partido a la lista de partidos de la eliminatoria
            eliminatoria_data['partidos'].append(partido)
            # Agregar los nuevos enfrentamientos a la lista correspondiente
        datas5[eliminatoria] = eliminatoria_data
         # Agregar los nuevos enfrentamientos a la lista correspondiente
        nuevos_enfrentamientos.clear()  
        # Guardar la lista de partidos en el archivo JSON
        guardar_playoff_caja(datas5)
        # Redireccionar a la página de visualización del playoff
        return redirect(url_for('ver_playoff_caja'))
    # Si no es una solicitud POST, renderizar el formulario
    return render_template('admin/playoff_caja.html', datas5=datas5)
# Toma la lista de los playoff y los guarda
def guardar_playoff_en_archivo_caja(datas5):
    arch_guardar_playoff_caja = 'json_playoff/partidos_caja.json'
    # Guardar en el archivo
    with open(arch_guardar_playoff_caja, 'w', encoding='UTF-8') as archivo:
        json.dump(datas5, archivo)
# Modificar los partidos de los playoff
@app.route('/modificar_eliminatoria_caja/<string:id>', methods=['GET', 'POST'])
def modificar_playoff_caja(id):
    datas5 = obtener_playoff_caja()
    # Buscar la eliminatoria correspondiente al ID proporcionado
    eliminatoria_encontrada = None
    for eliminatoria, datos_eliminatoria in datas5.items():
        if datos_eliminatoria['id'] == id:
            eliminatoria_encontrada = datos_eliminatoria
            break
    if not eliminatoria_encontrada:
        return "Eliminatoria no encontrada"
    if request.method == 'POST':
        nuevos_partidos = []
        for index, partido in enumerate(eliminatoria_encontrada['partidos']):
            local = request.form.get(f'local{index}')
            resultadoA = request.form.get(f'resultadoA{index}')
            resultadoB = request.form.get(f'resultadoB{index}')
            visitante = request.form.get(f'visitante{index}')
            fecha = request.form.get(f'fecha{index}')
            hora = request.form.get(f'hora{index}')
            # Actualizar los datos del partido
            partido['local'] = local
            partido['resultadoA'] = resultadoA
            partido['resultadoB'] = resultadoB
            partido['visitante'] = visitante
            partido['fecha']= fecha
            partido['hora'] = hora
            nuevos_partidos.append(partido)   
        eliminatoria_encontrada['partidos'] = nuevos_partidos       
        # Guardar los cambios en el archivo JSON
        guardar_playoff_caja(datas5)       
        # Redireccionar a la página de visualización del playoff
        return redirect(url_for('ver_playoff_caja'))   
# Crear la clasificación de El Salvador
def generar_clasificacion_analisis_hockey_caja(data14, total_partidos_temporada_caja):
    default_dict = defaultdict(lambda: {})
    clasificacion = defaultdict(lambda: {'puntos': 0,'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'favor': 0, 'contra': 0, 'diferencia_goles': 0, 'bonus': 0})
    for jornada in data14[:total_partidos_temporada_caja]:
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
                clasificacion[equipo_local]['puntos'] += 3 + bonus_local
                clasificacion[equipo_local]['ganados'] += 1
                clasificacion[equipo_visitante]['puntos'] += 0 + bonus_visitante
                clasificacion[equipo_visitante]['perdidos'] += 1
            elif resultado_local < resultado_visitante:
                clasificacion[equipo_local]['puntos'] += 0 + bonus_local
                clasificacion[equipo_local]['perdidos'] += 1
                clasificacion[equipo_visitante]['puntos'] += 3 + bonus_visitante
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
"""# Crear la clasificación para el GrupoA y GrupoB de Caja Rural CPLV
def generar_clasificacion_grupoA_grupoB(data14, total_partidos_temporada_grupos_caja):
    clasificacion = defaultdict(lambda: {'puntos': 0, 'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'favor': 0, 'contra': 0, 'diferencia_goles': 0, 'bonus': 0})
    for jornada in data14[:total_partidos_temporada_grupos_caja]:
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
                clasificacion[equipo_local]['puntos'] += 3 + bonus_local
                clasificacion[equipo_local]['ganados'] += 1
                clasificacion[equipo_visitante]['puntos'] += 0 + bonus_visitante
                clasificacion[equipo_visitante]['perdidos'] += 1
            elif resultado_local < resultado_visitante:
                clasificacion[equipo_local]['puntos'] += 0 + bonus_local
                clasificacion[equipo_local]['perdidos'] += 1
                clasificacion[equipo_visitante]['puntos'] += 3 + bonus_visitante
                clasificacion[equipo_visitante]['ganados'] += 1
            else:
                clasificacion[equipo_local]['puntos'] += 1 + bonus_local
                clasificacion[equipo_visitante]['puntos'] += 1 + bonus_visitante
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
    grupoA = clasificacion_ordenada[:4]
    grupoB = clasificacion_ordenada[4:8]
    return grupoA, grupoB"""
# Ruta para mostrar la clasificación del CPLV Caja Rural
@app.route('/equipos_hockey/clasi_analis_caja/')
def clasif_analisis_caja():
    data14 = obtener_datos_caja()
    total_partidos_temporada_caja = 18
    # Llama a la función para generar la clasificación y análisis
    clasificacion_analisis_caja = generar_clasificacion_analisis_hockey_caja(data14, total_partidos_temporada_caja)
    # Ordena la clasificación por puntos y diferencia de goles
    clasificacion_analisis_caja = sorted(clasificacion_analisis_caja, key=lambda x: (x['datos']['puntos'], x['datos']['diferencia_goles']), reverse=True)
    return render_template('equipos_hockey/clasi_analis_caja.html', clasificacion_analisis_caja=clasificacion_analisis_caja)
# Ruta para mostrar los playoffs de CPLV Caja Rural
@app.route('/playoffs_caja/')
def playoffs_caja():
    # Obtener datos de las eliminatorias
    datas5 = obtener_playoff_caja()
    return render_template('playoffs/caja_playoff.html', datas5=datas5)
# Ruta y creación del calendario individual del CPLV Caja Rural
@app.route('/equipos_hockey/calendario_caja')
def calendarios_caja():
    datos14 = obtener_datos_caja()
    nuevos_datos_caja = [dato for dato in datos14 if dato]
    equipo_caja = 'CPLV Caja Rural'
    tabla_partidos_caja = {}
    # Iteramos sobre cada jornada y partido
    for jornada in datos14:
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
#Fin proceso CPLV Caja Rural

#Todo el proceso de calendario y clasificación del CPLV Munia Panteras
# Ruta de partidos CPLV Munia Panteras
part_panteras = 'json/partidos_panteras.json'
def guardar_datos_panteras(data15):
    # Guardar los datos en el archivo JSON
    with open(part_panteras, 'w', encoding='utf-8') as file:
        json.dump(data15, file, indent=4)
def obtener_datos_panteras():
    try:
    # Leer los datos desde el archivo JSON
      with open(part_panteras, 'r', encoding='utf-8') as file:
        data14 = json.load(file)
      return data15
    except json.decoder.JSONDecodeError:
        # Manejar archivo vacío, inicializar con una estructura JSON válida
        return []
# Partidos CPLV Munia Panteras
@app.route('/admin/calend_panteras')
def calend_panteras():
    data15 = obtener_datos_panteras()
    return render_template('admin/calend_panteras.html', data15=data15)
# Ingresar los resultados de los partidos de CPLV Munia Panteras
@app.route('/admin/crear_calendario_panteras', methods=['POST'])
def ingresar_resul_panteras():
    data15 = obtener_datos_panteras()
    nums_partidos = int(request.form.get('num_partidos', 0))
    jornada_nombre = request.form.get('nombre')
    jornada_existente = next((j for j in data14 if j["nombre"] == jornada_nombre), None)
    if jornada_existente:
        # Si la jornada ya existe, utiliza su identificador existente
        jornada_id = jornada_existente["id"]
        jornada = jornada_existente
    else:
        # Si la jornada no existe, crea un nuevo identificador
        jornada_id = str(uuid.uuid4())
        jornada = {"id": jornada_id, "nombre": jornada_nombre, "partidos": []}
        data15.append(jornada)
    for i in range(nums_partidos):
        #id_nuevo = str(uuid.uuid4())
        equipoLocal = request.form.get(f'local{i}')
        bonusA = request.form.get(f'bonusA{i}')
        resultadoA = request.form.get(f'resultadoA{i}')
        resultadoB = request.form.get(f'resultadoB{i}')
        bonusB = request.form.get(f'bonusB{i}')
        equipoVisitante = request.form.get(f'visitante{i}')
        fecha = request.form.get(f'fecha{i}')
        hora = request.form.get(f'hora{i}')
        nuevo_partido = {
            #'id': id_nuevo,
            'local': equipoLocal,
            'bonusA': bonusA,
            'resultadoA': resultadoA,
            'resultadoB': resultadoB,
            'bonusB': bonusB,
            'visitante': equipoVisitante,
            'fecha' : fecha,
            'hora' : hora
        }
        jornada["partidos"].append(nuevo_partido)
    guardar_datos_panteras(data15)
    return redirect(url_for('calend_panteras'))
# Toma la lista de los resultados y los guarda
def guardar_partidos_en_archivo_paneras(data15):
    arch_guardar_panteras = 'json/partidos_panteras.json'
    # Guardar en el archivo
    with open(arch_guardar_panteras, 'w', encoding='UTF-8') as archivo:
        json.dump(data15, archivo)
# Modificar los partidos de cada jornada
@app.route('/modificar_jornada_panteras/<string:id>', methods=['POST'])
def modificar_jorn_panteras(id):
    data15 = obtener_datos_panteras()
    if request.method == 'POST':
        jornada_nombre = request.form.get('nombre')
        resultados_a_modificar = next((result for result in data15 if result['id'] == id), None)
        if resultados_a_modificar:
            resultados_a_modificar['nombre'] = jornada_nombre
            resultados_a_modificar['partidos'] = []  # Reiniciar la lista de partidos
            for i in range(4):  # Ajusta según la cantidad máxima de partidos
                equipoLocal = request.form.get(f'local{i}')
                bonusA = request.form.get(f'bonusA{i}')
                resultadoA = request.form.get(f'resultadoA{i}')
                resultadoB = request.form.get(f'resultadoB{i}')
                bonusB = request.form.get(f'bonusB{i}')
                equipoVisitante = request.form.get(f'visitante{i}')
                fecha = request.form.get(f'fecha{i}')
                hora = request.form.get(f'hora{i}')
                nuevo_partido = {
                    'local': equipoLocal,
                    'bonusA': bonusA,
                    'resultadoA': resultadoA,
                    'resultadoB': resultadoB,
                    'bonusB': bonusB,
                    'visitante': equipoVisitante,
                    'fecha' : fecha,
                    'hora' : hora
                }
                resultados_a_modificar['partidos'].append(nuevo_partido)
            # Guardar los cambios en el archivo JSON
            guardar_partidos_en_archivo_panteras(data15)            
            return redirect(url_for('calend_panteras'))
    return redirect(url_for('calend_panteras'))
# Ruta para borrar jornadas
@app.route('/eliminar_jorn_panteras/<string:id>', methods=['POST'])
def eliminar_jorn_panteras(id):
    data15 = obtener_datos_panteras()
    jornada_a_eliminar = [j for j in data15 if j['id'] != id]  # Filtrar las jornadas diferentes de la que se va a eliminar
    guardar_partidos_en_archivo_panteras(jornada_a_eliminar)
    return redirect(url_for('calend_panteras'))
# PlayOff CPLV Munia Panteras
playoff_panteras = 'json_playoff/playoff_panteras.json'
def guardar_playoff_panteras(datas6):
    with open(playoff_panteras, 'w', encoding='utf-8') as file:
        json.dump(datas6, file, indent=4)
def obtener_playoff_panteras():
    try:
        with open(playoff_panteras, 'r', encoding='utf-8') as file:
            datas6 = json.load(file)
        return datas4
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return {'cuartos': [], 'semifinales': [], 'final': []}
nuevos_enfrentamientos_panteras = []
partido_panteras = None
# Crear formulario para los playoff
@app.route('/admin/playoff_panteras/')
def ver_playoff_panteras():
    datas6 = obtener_playoff_panteras()
    return render_template('admin/playoff_panteras.html', datas6=datas6)
# Crear formulario para los playoff
@app.route('/admin/crear_playoff_panteras', methods=['GET', 'POST'])
def crear_playoff_panteras():
    # Obtener los enfrentamientos actuales del archivo JSON
    datas6 = obtener_playoff_panteras()
    if request.method == 'POST':
        # Obtener la etapa del torneo seleccionada por el usuario
        eliminatoria = request.form.get('eliminatoria')
        # Verificar el número máximo de partidos permitidos según la etapa del torneo
        if eliminatoria == 'cuartos':
            max_partidos = 4
        elif eliminatoria == 'semifinales':
            max_partidos = 2
        elif eliminatoria == 'final':
            max_partidos = 1
        else:
            # Manejar caso no válido
            return "Etapa de torneo no válida"
        # Recuperar los datos del formulario y procesarlos
        num_partidos_str = request.form.get('num_partidos', '0')  # Valor predeterminado '0' si num_partidos está vacío
        num_partidos_str = num_partidos_str.strip()  # Eliminar espacios en blanco
        if num_partidos_str:
            num_partidos = int(num_partidos_str)
        else:
            num_partidos = 0  # Valor predeterminado si num_partidos está vacío
        # Si num_partidos es cero, se ignora la validación
        if num_partidos < 0:
            return "Número de partidos no válido"
        # Crear un identificador único para la eliminatoria
        eliminatoria_id = str(uuid.uuid4())  # Generar un UUID único
        # Crear un nuevo diccionario con los datos de la eliminatoria
        eliminatoria_data = {
            'id': eliminatoria_id,
            'partidos': []
        }
        # Recuperar los datos de cada partido del formulario
        for i in range(num_partidos):
            local = request.form.get(f'local{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            visitante = request.form.get(f'visitante{i}')
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            # Crear un nuevo diccionario con los datos del partido
            partido = {
                'local': local,
                'resultadoA': resultadoA,
                'resultadoB': resultadoB,
                'visitante': visitante,
                'fecha' : fecha,
                'hora' : hora
            }
            # Agregar el partido a la lista de partidos de la eliminatoria
            eliminatoria_data['partidos'].append(partido)
            # Agregar los nuevos enfrentamientos a la lista correspondiente
        datas6[eliminatoria] = eliminatoria_data
         # Agregar los nuevos enfrentamientos a la lista correspondiente
        nuevos_enfrentamientos.clear()  
        # Guardar la lista de partidos en el archivo JSON
        guardar_playoff_panteras(datas6)
        # Redireccionar a la página de visualización del playoff
        return redirect(url_for('ver_playoff_panteras'))
    # Si no es una solicitud POST, renderizar el formulario
    return render_template('admin/playoff_panteras.html', datas6=datas6)
# Toma la lista de los playoff y los guarda
def guardar_playoff_en_archivo_panteras(datas6):
    arch_guardar_playoff_panteras = 'json_playoff/partidos_panteras.json'
    # Guardar en el archivo
    with open(arch_guardar_playoff_panteras, 'w', encoding='UTF-8') as archivo:
        json.dump(datas6, archivo)
# Modificar los partidos de los playoff
@app.route('/modificar_eliminatoria_panteras/<string:id>', methods=['GET', 'POST'])
def modificar_playoff_panteras(id):
    datas6 = obtener_playoff_panteras()
    # Buscar la eliminatoria correspondiente al ID proporcionado
    eliminatoria_encontrada = None
    for eliminatoria, datos_eliminatoria in datas6.items():
        if datos_eliminatoria['id'] == id:
            eliminatoria_encontrada = datos_eliminatoria
            break
    if not eliminatoria_encontrada:
        return "Eliminatoria no encontrada"
    if request.method == 'POST':
        nuevos_partidos = []
        for index, partido in enumerate(eliminatoria_encontrada['partidos']):
            local = request.form.get(f'local{index}')
            resultadoA = request.form.get(f'resultadoA{index}')
            resultadoB = request.form.get(f'resultadoB{index}')
            visitante = request.form.get(f'visitante{index}')
            fecha = request.form.get(f'fecha{index}')
            hora = request.form.get(f'hora{index}')
            # Actualizar los datos del partido
            partido['local'] = local
            partido['resultadoA'] = resultadoA
            partido['resultadoB'] = resultadoB
            partido['visitante'] = visitante
            partido['fecha'] = fecha
            partido['hora'] = hora
            nuevos_partidos.append(partido)   
        eliminatoria_encontrada['partidos'] = nuevos_partidos       
        # Guardar los cambios en el archivo JSON
        guardar_playoff_panteras(datas6)       
        # Redireccionar a la página de visualización del playoff
        return redirect(url_for('ver_playoff_panteras'))   
# Crear la clasificación de CPLV Munia Panteras
def generar_clasificacion_analisis_hockey_panteras(data15, total_partidos_temporada_panteras):
    default_dict = defaultdict(lambda: {})
    clasificacion = defaultdict(lambda: {'puntos': 0,'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'favor': 0, 'contra': 0, 'diferencia_goles': 0, 'bonus': 0})
    for jornada in data15[:total_partidos_temporada_panteras]:
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
                clasificacion[equipo_local]['puntos'] += 3 + bonus_local
                clasificacion[equipo_local]['ganados'] += 1
                clasificacion[equipo_visitante]['puntos'] += 0 + bonus_visitante
                clasificacion[equipo_visitante]['perdidos'] += 1
            elif resultado_local < resultado_visitante:
                clasificacion[equipo_local]['puntos'] += 0 + bonus_local
                clasificacion[equipo_local]['perdidos'] += 1
                clasificacion[equipo_visitante]['puntos'] += 3 + bonus_visitante
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
"""# Crear la clasificación para el GrupoA y GrupoB de CPLV Munia Panteras
def generar_clasificacion_grupoA_grupoB(data15, total_partidos_temporada_grupos_panteras):
    clasificacion = defaultdict(lambda: {'puntos': 0, 'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'favor': 0, 'contra': 0, 'diferencia_goles': 0, 'bonus': 0})
    for jornada in data15[:total_partidos_temporada_grupos_panteras]:
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
                clasificacion[equipo_local]['puntos'] += 3 + bonus_local
                clasificacion[equipo_local]['ganados'] += 1
                clasificacion[equipo_visitante]['puntos'] += 0 + bonus_visitante
                clasificacion[equipo_visitante]['perdidos'] += 1
            elif resultado_local < resultado_visitante:
                clasificacion[equipo_local]['puntos'] += 0 + bonus_local
                clasificacion[equipo_local]['perdidos'] += 1
                clasificacion[equipo_visitante]['puntos'] += 3 + bonus_visitante
                clasificacion[equipo_visitante]['ganados'] += 1
            else:
                clasificacion[equipo_local]['puntos'] += 1 + bonus_local
                clasificacion[equipo_visitante]['puntos'] += 1 + bonus_visitante
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
    grupoA = clasificacion_ordenada[:4]
    grupoB = clasificacion_ordenada[4:8]
    return grupoA, grupoB"""
# Ruta para mostrar la clasificación del CPLV Munia Panteras
@app.route('/equipos_hockey/clasi_analis_panteras/')
def clasif_analisis_panteras():
    data15 = obtener_datos_panteras()
    total_partidos_temporada_panteras = 18
    # Llama a la función para generar la clasificación y análisis
    clasificacion_analisis_panteras = generar_clasificacion_analisis_hockey_panteras(data15, total_partidos_temporada_panteras)
    # Ordena la clasificación por puntos y diferencia de goles
    clasificacion_analisis_panteras = sorted(clasificacion_analisis_panteras, key=lambda x: (x['datos']['puntos'], x['datos']['diferencia_goles']), reverse=True)
    return render_template('equipos_hockey/clasi_analis_pante.html', clasificacion_analisis_panteras=clasificacion_analisis_panteras)
# Ruta para mostrar los playoffs de CPLV Munia Panteras
@app.route('/playoffs_panteras/')
def playoffs_panteras():
    # Obtener datos de las eliminatorias
    datas6 = obtener_playoff_panteras()
    return render_template('playoffs/panteras_playoff.html', datas6=datas6)
# Ruta y creación del calendario individual del CPLV Munia Panteras
@app.route('/equipos_hockey/calendario_panteras')
def calendarios_panteras():
    datos15 = obtener_datos_panteras()
    nuevos_datos_panteras = [dato for dato in datos15 if dato]
    equipo_panteras = 'CPLV Munia Panteras'
    tabla_partidos_panteras = {}
    # Iteramos sobre cada jornada y partido
    for jornada in datos15:
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
#Fin proceso CPLV Munia Panteras

#EQUIPOS VOLEIBOL
#Todo el proceso de calendario y clasificación del Univ. Valladolid VCV
# Ruta de partidos Univ. Valladolid VCV
part_vcv = 'json/partidos_vcv.json'
def guardar_datos_vcv(data18):
    # Guardar los datos en el archivo JSON
    with open(part_vcv, 'w', encoding='utf-8') as file:
        json.dump(data18, file, indent=4)
def obtener_datos_vcv():
    try:
    # Leer los datos desde el archivo JSON
      with open(part_vcv, 'r', encoding='utf-8') as file:
        data18 = json.load(file)
      return data18
    except json.decoder.JSONDecodeError:
        # Manejar archivo vacío, inicializar con una estructura JSON válida
        return []
# Partidos Univ. Valladolid VCV
@app.route('/admin/calend_vcv')
def calend_vcv():
    data18 = obtener_datos_vcv()
    return render_template('admin/calend_vcv.html', data18=data18)
# Ingresar los resultados de los partidos de Univ. Valladolid VCV
@app.route('/admin/crear_calendario_vcv', methods=['POST'])
def ingresar_resul_vcv():
    data18 = obtener_datos_vcv()
    nums_partidos = int(request.form.get('num_partidos', 0))
    jornada_nombre = request.form.get('nombre')
    jornada_existente = next((j for j in data18 if j["nombre"] == jornada_nombre), None)
    if jornada_existente:
        # Si la jornada ya existe, utiliza su identificador existente
        jornada_id = jornada_existente["id"]
        jornada = jornada_existente
    else:
        # Si la jornada no existe, crea un nuevo identificador
        jornada_id = str(uuid.uuid4())
        jornada = {"id": jornada_id, "nombre": jornada_nombre, "partidos": []}
        data18.append(jornada)
    for i in range(nums_partidos):
        #id_nuevo = str(uuid.uuid4())
        equipoLocal = request.form.get(f'local{i}')
        resultadoA = request.form.get(f'resultadoA{i}')
        resultadoB = request.form.get(f'resultadoB{i}')
        equipoVisitante = request.form.get(f'visitante{i}')
        fecha = request.form.get(f'fecha{i}')
        hora = request.form.get(f'hora{i}')
        nuevo_partido = {
            #'id': id_nuevo,
            'local': equipoLocal,
            'resultadoA': resultadoA,
            'resultadoB': resultadoB,
            'visitante': equipoVisitante,
            'fecha' : fecha,
            'hora' : hora
        }
        jornada["partidos"].append(nuevo_partido)
    guardar_datos_vcv(data18)
    return redirect(url_for('calend_vcv'))
# Toma la lista de los resultados y los guarda
def guardar_partidos_en_archivo_vcv(data18):
    arch_guardar_vcv = 'json/partidos_vcv.json'
    # Guardar en el archivo
    with open(arch_guardar_vcv, 'w', encoding='UTF-8') as archivo:
        json.dump(data18, archivo)
# Modificar los partidos de cada jornada
@app.route('/modificar_jornada_vcv/<string:id>', methods=['POST'])
def modificar_jorn_vcv(id):
    data18 = obtener_datos_vcv()
    if request.method == 'POST':
        jornada_nombre = request.form.get('nombre')
        resultados_a_modificar = next((result for result in data18 if result['id'] == id), None)
        if resultados_a_modificar:
            resultados_a_modificar['nombre'] = jornada_nombre
            resultados_a_modificar['partidos'] = []  # Reiniciar la lista de partidos
            for i in range(6):  # Ajusta según la cantidad máxima de partidos
                equipoLocal = request.form.get(f'local{i}')
                resultadoA = request.form.get(f'resultadoA{i}')
                resultadoB = request.form.get(f'resultadoB{i}')
                equipoVisitante = request.form.get(f'visitante{i}')
                fecha = request.form.get(f'fecha{i}')
                hora = request.form.get(f'hora{i}')
                nuevo_partido = {
                    'local': equipoLocal,
                    'resultadoA': resultadoA,
                    'resultadoB': resultadoB,
                    'visitante': equipoVisitante,
                    'fecha' : fecha,
                    'hora' : hora
                }
                resultados_a_modificar['partidos'].append(nuevo_partido)
            # Guardar los cambios en el archivo JSON
            guardar_partidos_en_archivo_vcv(data18)            
            return redirect(url_for('calend_vcv'))
    return redirect(url_for('calend_vcv'))
from collections import defaultdict
# Ruta para borrar jornadas
@app.route('/eliminar_jorn_vcv/<string:id>', methods=['POST'])
def eliminar_jorn_vcv(id):
    data18 = obtener_datos_vcv()
    jornada_a_eliminar = [j for j in data18 if j['id'] != id]  # Filtrar las jornadas diferentes de la que se va a eliminar
    guardar_partidos_en_archivo_vcv(jornada_a_eliminar)
    return redirect(url_for('calend_vcv'))
# Crear la clasificación de Univ. Valladolid VCV
def generar_clasificacion_analisis_voley_vcv(data18, total_partidos_temporada_vcv):
    clasificacion = defaultdict(lambda: {'puntos': 0, 'jugados': 0, 'ganados3': 0, 'ganados2': 0, 'perdidos1': 0, 'perdidos0': 0, 'favor': 0, 'contra': 0, 'diferencia_sets': 0})
    for jornada in data18[:total_partidos_temporada_vcv]:
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
# Ruta para mostrar la clasificación del Univ. Valladolid VCV
@app.route('/equipos_voleibol/clasi_analis_vcv/')
def clasif_analisis_vcv():
    data18 = obtener_datos_vcv()
    total_partidos_temporada_vcv = 22
    # Llama a la función para generar la clasificación y análisis
    clasificacion_analisis_vcv = generar_clasificacion_analisis_voley_vcv(data18, total_partidos_temporada_vcv)
    # Ordena la clasificación por puntos y diferencia de goles
    clasificacion_analisis_vcv = sorted(clasificacion_analisis_vcv, key=lambda x: (x['datos']['puntos'], x['datos']['diferencia_sets']), reverse=True)
    return render_template('equipos_voleibol/clasi_analis_vcv.html', clasificacion_analisis_vcv=clasificacion_analisis_vcv)
# Ruta y creación del calendario individual del Univ. Valladolid VCV
@app.route('/equipos_voleibol/calendario_vcv')
def calendarios_vcv():
    datos18 = obtener_datos_vcv()
    nuevos_datos_vcv = [dato for dato in datos18 if dato]
    equipo_vcv = 'Univ.Valladolid VCV'
    tabla_partidos_vcv = {}
    # Iteramos sobre cada jornada y partido
    for jornada in datos18:
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
#Fin proceso Univ. Valladolid VCV





# COPA DEL REY Y COPA DE LA REINA
# Copa  Real Valladolid
copa_valladolid = 'json_copa/copa_valladolid.json'
def guardar_copa_valladolid(dats1):
    with open(copa_valladolid, 'w', encoding='utf-8') as file:
        json.dump(dats1, file, indent=4)
def obtener_copa_valladolid():
    try:
        with open(copa_valladolid, 'r', encoding='utf-8') as file:
            dats1 = json.load(file)
        return dats1
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return {'ronda1': [], 'ronda2': [],'ronda3': [], 'octavos': [],'cuartos': [], 'semis': [], 'final': []}
nuevas_eliminatorias_valladolid = []
duelos_valladolid = None
# Crear formulario para los playoff
@app.route('/admin/copa_valladolid/')
def ver_copa_valladolid():
    dats1 = obtener_copa_valladolid()
    return render_template('admin/copa_valladolid.html', dats1=dats1)
# Crear formulario para los playoff
@app.route('/admin/crear_copa_valladolid', methods=['GET', 'POST'])
def crear_copa_valladolid():
    # Obtener los enfrentamientos actuales del archivo JSON
    dats1 = obtener_copa_valladolid()
    if request.method == 'POST':
        # Obtener la etapa del torneo seleccionada por el usuario
        eliminatoria = request.form.get('eliminatoria')
        # Verificar el número máximo de partidos permitidos según la etapa del torneo
        if eliminatoria == 'ronda1':
            max_partidos = 55
        elif eliminatoria == 'ronda2':
            max_partidos = 28
        elif eliminatoria == 'ronda3':
            max_partidos = 16
        elif eliminatoria == 'octavos':
            max_partidos = 8
        elif eliminatoria == 'cuartos':
            max_partidos = 4
        elif eliminatoria == 'semis':
            max_partidos = 4
        elif eliminatoria == 'final':
            max_partidos = 1                
        else:
            # Manejar caso no válido
            return "Etapa de torneo no válida"
        # Recuperar los datos del formulario y procesarlos
        num_partidos_str = request.form.get('num_partidos', '0')  # Valor predeterminado '0' si num_partidos está vacío
        num_partidos_str = num_partidos_str.strip()  # Eliminar espacios en blanco
        if num_partidos_str:
            num_partidos = int(num_partidos_str)
        else:
            num_partidos = 0  # Valor predeterminado si num_partidos está vacío
        # Si num_partidos es cero, se ignora la validación
        if num_partidos < 0:
            return "Número de partidos no válido"
        # Crear un identificador único para la eliminatoria
        eliminatoria_id = str(uuid.uuid4())  # Generar un UUID único
        # Crear un nuevo diccionario con los datos de la eliminatoria
        eliminatoria_data = {
            'id': eliminatoria_id,
            'partidos': []
        }
        # Recuperar los datos de cada partido del formulario
        for i in range(num_partidos):
            local = request.form.get(f'local{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            visitante = request.form.get(f'visitante{i}')
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            # Crear un nuevo diccionario con los datos del partido
            partido = {
                'local': local,
                'resultadoA': resultadoA,
                'resultadoB': resultadoB,
                'visitante': visitante,
                'fecha' : fecha,
                'hora' : hora
            }
            # Agregar el partido a la lista de partidos de la eliminatoria
            eliminatoria_data['partidos'].append(partido)
            # Agregar los nuevos enfrentamientos a la lista correspondiente
        dats1[eliminatoria] = eliminatoria_data
         # Agregar los nuevos enfrentamientos a la lista correspondiente
        nuevos_enfrentamientos.clear()  
        # Guardar la lista de partidos en el archivo JSON
        guardar_copa_valladolid(dats1)
        # Redireccionar a la página de visualización del playoff
        return redirect(url_for('ver_copa_valladolid'))
    # Si no es una solicitud POST, renderizar el formulario
    return render_template('admin/copa_valladolid.html', dats1=dats1)
# Toma la lista de los playoff y los guarda
def guardar_copa_en_archivo_valladolid(dats1):
    arch_guardar_copa_valladolid = 'json_playoff/copa_valladolid.json'
    # Guardar en el archivo
    with open(arch_guardar_copa_valladolid, 'w', encoding='UTF-8') as archivo:
        json.dump(dats1, archivo)
# Modificar los partidos de los playoff
@app.route('/modificar_eliminatoria_copa_valladolid/<string:id>', methods=['GET', 'POST'])
def modificar_copa_valladolid(id):
    dats1 = obtener_copa_valladolid()
    # Buscar la eliminatoria correspondiente al ID proporcionado
    eliminatoria_encontrada = None
    for eliminatoria, datos_eliminatoria in dats1.items():
        if datos_eliminatoria['id'] == id:
            eliminatoria_encontrada = datos_eliminatoria
            break
    if not eliminatoria_encontrada:
        return "Eliminatoria no encontrada"
    if request.method == 'POST':
        nuevos_partidos = []
        for index, partido in enumerate(eliminatoria_encontrada['partidos']):
            local = request.form.get(f'local{index}')
            resultadoA = request.form.get(f'resultadoA{index}')
            resultadoB = request.form.get(f'resultadoB{index}')
            visitante = request.form.get(f'visitante{index}')
            fecha = request.form.get(f'fecha{index}')
            hora = request.form.get(f'hora{index}')
            # Actualizar los datos del partido
            partido['local'] = local
            partido['resultadoA'] = resultadoA
            partido['resultadoB'] = resultadoB
            partido['visitante'] = visitante
            partido['fecha'] = fecha
            partido['hora'] = hora
            nuevos_partidos.append(partido)   
        eliminatoria_encontrada['partidos'] = nuevos_partidos       
        # Guardar los cambios en el archivo JSON
        guardar_copa_valladolid(dats1)       
        # Redireccionar a la página de visualización del playoff
        return redirect(url_for('ver_copa_valladolid')) 
# Ruta para mostrar la copa Real Valladolid
@app.route('/copa_valladolid/')
def copas_valladolid():
    # Obtener datos de las eliminatorias
    dats1 = obtener_copa_valladolid()
    return render_template('copas/valladolid_copa.html', dats1=dats1)
# Fin copa Real Valladolid

# Copa Aula Valladolid
copa_aula = 'json_copa/copa_aula.json'
def guardar_copa_aula(dats2):
    with open(copa_aula, 'w', encoding='utf-8') as file:
        json.dump(dats2, file, indent=4)
def obtener_copa_aula():
    try:
        with open(copa_aula, 'r', encoding='utf-8') as file:
            dats2 = json.load(file)
        return dats2
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return {'fase1': [], 'fase2': [],'octavos': [],'cuartos': [], 'semifinales': [], 'final': []}
nuevas_eliminatorias_aula = []
duelos_aula = None
# Crear formulario para los playoff
@app.route('/admin/copa_aula/')
def ver_copa_aula():
    dats2 = obtener_copa_aula()
    return render_template('admin/copa_aula.html', dats2=dats2)
# Crear formulario para los playoff
@app.route('/admin/crear_copa_aula', methods=['GET', 'POST'])
def crear_copa_aula():
    # Obtener los enfrentamientos actuales del archivo JSON
    dats2 = obtener_copa_aula()
    if request.method == 'POST':
        # Obtener la etapa del torneo seleccionada por el usuario
        eliminatoria = request.form.get('eliminatoria')
        # Verificar el número máximo de partidos permitidos según la etapa del torneo
        if eliminatoria == 'fase1':
            max_partidos = 6
        elif eliminatoria == 'fase2':
            max_partidos = 6
        elif eliminatoria == 'cuartos':
            max_partidos = 4
        elif eliminatoria == 'semifinales':
            max_partidos = 2
        elif eliminatoria == 'final':
            max_partidos = 1                
        else:
            # Manejar caso no válido
            return "Etapa de torneo no válida"
        # Recuperar los datos del formulario y procesarlos
        num_partidos_str = request.form.get('num_partidos', '0')  # Valor predeterminado '0' si num_partidos está vacío
        num_partidos_str = num_partidos_str.strip()  # Eliminar espacios en blanco
        if num_partidos_str:
            num_partidos = int(num_partidos_str)
        else:
            num_partidos = 0  # Valor predeterminado si num_partidos está vacío
        # Si num_partidos es cero, se ignora la validación
        if num_partidos < 0:
            return "Número de partidos no válido"
        # Crear un identificador único para la eliminatoria
        eliminatoria_id = str(uuid.uuid4())  # Generar un UUID único
        # Crear un nuevo diccionario con los datos de la eliminatoria
        eliminatoria_data = {
            'id': eliminatoria_id,
            'partidos': []
        }
        # Recuperar los datos de cada partido del formulario
        for i in range(num_partidos):
            local = request.form.get(f'local{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            visitante = request.form.get(f'visitante{i}')
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            # Crear un nuevo diccionario con los datos del partido
            partido = {
                'local': local,
                'resultadoA': resultadoA,
                'resultadoB': resultadoB,
                'visitante': visitante,
                'fecha': fecha,
                'hora': hora
            }
            # Agregar el partido a la lista de partidos de la eliminatoria
            eliminatoria_data['partidos'].append(partido)
            # Agregar los nuevos enfrentamientos a la lista correspondiente
        dats2[eliminatoria] = eliminatoria_data
         # Agregar los nuevos enfrentamientos a la lista correspondiente
        nuevos_enfrentamientos.clear()  
        # Guardar la lista de partidos en el archivo JSON
        guardar_copa_aula(dats2)
        # Redireccionar a la página de visualización del playoff
        return redirect(url_for('ver_copa_aula'))
    # Si no es una solicitud POST, renderizar el formulario
    return render_template('admin/copa_aula.html', dats2=dats2)
# Toma la lista de los playoff y los guarda
def guardar_copa_en_archivo_aula(dats2):
    arch_guardar_copa_aula = 'json_playoff/copa_aula.json'
    # Guardar en el archivo
    with open(arch_guardar_copa_aula, 'w', encoding='UTF-8') as archivo:
        json.dump(dats2, archivo)
# Modificar los partidos de los playoff
@app.route('/modificar_eliminatoria_copa_aula/<string:id>', methods=['GET', 'POST'])
def modificar_copa_aula(id):
    dats2 = obtener_copa_aula()
    # Buscar la eliminatoria correspondiente al ID proporcionado
    eliminatoria_encontrada = None
    for eliminatoria, datos_eliminatoria in dats2.items():
        if datos_eliminatoria['id'] == id:
            eliminatoria_encontrada = datos_eliminatoria
            break
    if not eliminatoria_encontrada:
        return "Eliminatoria no encontrada"
    if request.method == 'POST':
        nuevos_partidos = []
        for index, partido in enumerate(eliminatoria_encontrada['partidos']):
            local = request.form.get(f'local{index}')
            resultadoA = request.form.get(f'resultadoA{index}')
            resultadoB = request.form.get(f'resultadoB{index}')
            visitante = request.form.get(f'visitante{index}')
            fecha = request.form.get(f'fecha{index}')
            hora = request.form.get(f'hora{index}')
            # Actualizar los datos del partido
            partido['local'] = local
            partido['resultadoA'] = resultadoA
            partido['resultadoB'] = resultadoB
            partido['visitante'] = visitante
            partido['fecha'] = fecha
            partido['hora'] = hora
            nuevos_partidos.append(partido)   
        eliminatoria_encontrada['partidos'] = nuevos_partidos       
        # Guardar los cambios en el archivo JSON
        guardar_copa_aula(dats2)       
        # Redireccionar a la página de visualización del playoff
        return redirect(url_for('ver_copa_aula')) 
# Ruta para mostrar la copa Aula Valladolid
@app.route('/copa_aula/')
def copas_aula():
    # Obtener datos de las eliminatorias
    dats2 = obtener_copa_aula()
    return render_template('copas/aula_copa.html', dats2=dats2)
# Fin copa Aula Valladolid

# Copa Recoletas Atl. Valladolid
copa_recoletas = 'json_copa/copa_recoletas.json'
def guardar_copa_recoletas(dats3):
    with open(copa_recoletas, 'w', encoding='utf-8') as file:
        json.dump(dats3, file, indent=4)
def obtener_copa_recoletas():
    try:
        with open(copa_recoletas, 'r', encoding='utf-8') as file:
            dats3 = json.load(file)
        return dats3
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return {'ronda1': [], 'ronda2': [],'octavos': [],'cuartos': [], 'semifinales': [], 'final': []}
nuevas_eliminatorias_recoletas = []
duelos_recoletas = None
# Crear formulario para los playoff
@app.route('/admin/copa_recoletas/')
def ver_copa_recoletas():
    dats3 = obtener_copa_recoletas()
    return render_template('admin/copa_recoletas.html', dats3=dats3)
# Crear formulario para los playoff
@app.route('/admin/crear_copa_recoletas', methods=['GET', 'POST'])
def crear_copa_recoletas():
    # Obtener los enfrentamientos actuales del archivo JSON
    dats3 = obtener_copa_recoletas()
    if request.method == 'POST':
        # Obtener la etapa del torneo seleccionada por el usuario
        eliminatoria = request.form.get('eliminatoria')
        # Verificar el número máximo de partidos permitidos según la etapa del torneo
        if eliminatoria == 'ronda1':
            max_partidos = 12
        elif eliminatoria == 'ronda2':
            max_partidos = 6
        elif eliminatoria == 'octavos':
            max_partidos = 8
        elif eliminatoria == 'cuartos':
            max_partidos = 4
        elif eliminatoria == 'semifinal':
            max_partidos = 2
        elif eliminatoria == 'final':
            max_partidos = 1                
        else:
            # Manejar caso no válido
            return "Etapa de torneo no válida"
        # Recuperar los datos del formulario y procesarlos
        num_partidos_str = request.form.get('num_partidos', '0')  # Valor predeterminado '0' si num_partidos está vacío
        num_partidos_str = num_partidos_str.strip()  # Eliminar espacios en blanco
        if num_partidos_str:
            num_partidos = int(num_partidos_str)
        else:
            num_partidos = 0  # Valor predeterminado si num_partidos está vacío
        # Si num_partidos es cero, se ignora la validación
        if num_partidos < 0:
            return "Número de partidos no válido"
        # Crear un identificador único para la eliminatoria
        eliminatoria_id = str(uuid.uuid4())  # Generar un UUID único
        # Crear un nuevo diccionario con los datos de la eliminatoria
        eliminatoria_data = {
            'id': eliminatoria_id,
            'partidos': []
        }
        # Recuperar los datos de cada partido del formulario
        for i in range(num_partidos):
            local = request.form.get(f'local{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            visitante = request.form.get(f'visitante{i}')
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            # Crear un nuevo diccionario con los datos del partido
            partido = {
                'local': local,
                'resultadoA': resultadoA,
                'resultadoB': resultadoB,
                'visitante': visitante,
                'fecha' : fecha,
                'hora' : hora
            }
            # Agregar el partido a la lista de partidos de la eliminatoria
            eliminatoria_data['partidos'].append(partido)
            # Agregar los nuevos enfrentamientos a la lista correspondiente
        dats3[eliminatoria] = eliminatoria_data
         # Agregar los nuevos enfrentamientos a la lista correspondiente
        nuevos_enfrentamientos.clear()  
        # Guardar la lista de partidos en el archivo JSON
        guardar_copa_recoletas(dats3)
        # Redireccionar a la página de visualización del playoff
        return redirect(url_for('ver_copa_recoletas'))
    # Si no es una solicitud POST, renderizar el formulario
    return render_template('admin/copa_recoletas.html', dats3=dats3)
# Toma la lista de los playoff y los guarda
def guardar_copa_en_archivo_recoletas(dats3):
    arch_guardar_copa_recoletas = 'json_playoff/copa_recoletas.json'
    # Guardar en el archivo
    with open(arch_guardar_copa_recoletas, 'w', encoding='UTF-8') as archivo:
        json.dump(dats3, archivo)
# Modificar los partidos de los playoff
@app.route('/modificar_eliminatoria_copa_recoletas/<string:id>', methods=['GET', 'POST'])
def modificar_copa_recoletas(id):
    dats3 = obtener_copa_recoletas()
    # Buscar la eliminatoria correspondiente al ID proporcionado
    eliminatoria_encontrada = None
    for eliminatoria, datos_eliminatoria in dats3.items():
        if datos_eliminatoria['id'] == id:
            eliminatoria_encontrada = datos_eliminatoria
            break
    if not eliminatoria_encontrada:
        return "Eliminatoria no encontrada"
    if request.method == 'POST':
        nuevos_partidos = []
        for index, partido in enumerate(eliminatoria_encontrada['partidos']):
            local = request.form.get(f'local{index}')
            resultadoA = request.form.get(f'resultadoA{index}')
            resultadoB = request.form.get(f'resultadoB{index}')
            visitante = request.form.get(f'visitante{index}')
            fecha = request.form.get(f'fecha{index}')
            hora = request.form.get(f'hora{index}')
            # Actualizar los datos del partido
            partido['local'] = local
            partido['resultadoA'] = resultadoA
            partido['resultadoB'] = resultadoB
            partido['visitante'] = visitante
            partido['fecha'] = fecha
            partido['hora'] = hora
            nuevos_partidos.append(partido)   
        eliminatoria_encontrada['partidos'] = nuevos_partidos       
        # Guardar los cambios en el archivo JSON
        guardar_copa_recoletas(dats3)       
        # Redireccionar a la página de visualización del playoff
        return redirect(url_for('ver_copa_recoletas')) 
# Ruta para mostrar la copa Recoletas Atl. Valladolid
@app.route('/copa_recoletas/')
def copas_recoletas():
    # Obtener datos de las eliminatorias
    dats3 = obtener_copa_recoletas()
    return render_template('copas/recoletas_copa.html', dats3=dats3)
# Fin copa Recoletas Atl. Valladolid

# Copa Fundación Aliados
copa_aliados = 'json_copa/copa_aliados.json'
def guardar_copa_aliados(dats4):
    with open(copa_aliados, 'w', encoding='utf-8') as file:
        json.dump(dats4, file, indent=4)
def obtener_copa_aliados():
    try:
        with open(copa_aliados, 'r', encoding='utf-8') as file:
            dats4 = json.load(file)
        return dats4
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return {'cuartos': [], 'semifinales': [],'final': []}
nuevas_eliminatorias_aliados = []
duelos_aliados = None
# Crear formulario para los playoff
@app.route('/admin/copa_aliados/')
def ver_copa_aliados():
    dats4 = obtener_copa_aliados()
    return render_template('admin/copa_aliados.html', dats4=dats4)
# Crear formulario para los playoff
@app.route('/admin/crear_copa_aliados', methods=['GET', 'POST'])
def crear_copa_aliados():
    # Obtener los enfrentamientos actuales del archivo JSON
    dats4 = obtener_copa_aliados()
    if request.method == 'POST':
        # Obtener la etapa del torneo seleccionada por el usuario
        eliminatoria = request.form.get('eliminatoria')
        # Verificar el número máximo de partidos permitidos según la etapa del torneo
        if eliminatoria == 'cuartos':
            max_partidos = 4
        elif eliminatoria == 'semifinales':
            max_partidos = 2
        elif eliminatoria == 'final':
            max_partidos = 1               
        else:
            # Manejar caso no válido
            return "Etapa de torneo no válida"
        # Recuperar los datos del formulario y procesarlos
        num_partidos_str = request.form.get('num_partidos', '0')  # Valor predeterminado '0' si num_partidos está vacío
        num_partidos_str = num_partidos_str.strip()  # Eliminar espacios en blanco
        if num_partidos_str:
            num_partidos = int(num_partidos_str)
        else:
            num_partidos = 0  # Valor predeterminado si num_partidos está vacío
        # Si num_partidos es cero, se ignora la validación
        if num_partidos < 0:
            return "Número de partidos no válido"
        # Crear un identificador único para la eliminatoria
        eliminatoria_id = str(uuid.uuid4())  # Generar un UUID único
        # Crear un nuevo diccionario con los datos de la eliminatoria
        eliminatoria_data = {
            'id': eliminatoria_id,
            'partidos': []
        }
        # Recuperar los datos de cada partido del formulario
        for i in range(num_partidos):
            local = request.form.get(f'local{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            visitante = request.form.get(f'visitante{i}')
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            # Crear un nuevo diccionario con los datos del partido
            partido = {
                'local': local,
                'resultadoA': resultadoA,
                'resultadoB': resultadoB,
                'visitante': visitante,
                'fecha' : fecha,
                'hora' : hora
            }
            # Agregar el partido a la lista de partidos de la eliminatoria
            eliminatoria_data['partidos'].append(partido)
            # Agregar los nuevos enfrentamientos a la lista correspondiente
        dats4[eliminatoria] = eliminatoria_data
         # Agregar los nuevos enfrentamientos a la lista correspondiente
        nuevos_enfrentamientos.clear()  
        # Guardar la lista de partidos en el archivo JSON
        guardar_copa_aliados(dats4)
        # Redireccionar a la página de visualización del playoff
        return redirect(url_for('ver_copa_aliados'))
    # Si no es una solicitud POST, renderizar el formulario
    return render_template('admin/copa_aliados.html', dats4=dats4)
# Toma la lista de los playoff y los guarda
def guardar_copa_en_archivo_aliados(dats4):
    arch_guardar_copa_aliados = 'json_playoff/copa_aliados.json'
    # Guardar en el archivo
    with open(arch_guardar_copa_aliados, 'w', encoding='UTF-8') as archivo:
        json.dump(dats4, archivo)
# Modificar los partidos de los playoff
@app.route('/modificar_eliminatoria_copa_aliados/<string:id>', methods=['GET', 'POST'])
def modificar_copa_aliados(id):
    dats4 = obtener_copa_aliados()
    # Buscar la eliminatoria correspondiente al ID proporcionado
    eliminatoria_encontrada = None
    for eliminatoria, datos_eliminatoria in dats4.items():
        if datos_eliminatoria['id'] == id:
            eliminatoria_encontrada = datos_eliminatoria
            break
    if not eliminatoria_encontrada:
        return "Eliminatoria no encontrada"
    if request.method == 'POST':
        nuevos_partidos = []
        for index, partido in enumerate(eliminatoria_encontrada['partidos']):
            local = request.form.get(f'local{index}')
            resultadoA = request.form.get(f'resultadoA{index}')
            resultadoB = request.form.get(f'resultadoB{index}')
            visitante = request.form.get(f'visitante{index}')
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            # Actualizar los datos del partido
            partido['local'] = local
            partido['resultadoA'] = resultadoA
            partido['resultadoB'] = resultadoB
            partido['visitante'] = visitante
            partido['fecha'] = fecha
            partido['hora'] = hora
            nuevos_partidos.append(partido)   
        eliminatoria_encontrada['partidos'] = nuevos_partidos       
        # Guardar los cambios en el archivo JSON
        guardar_copa_aliados(dats4)       
        # Redireccionar a la página de visualización del playoff
        return redirect(url_for('ver_copa_aliados')) 
# Ruta para mostrar la copa Fundación Aliados
@app.route('/copa_aliados/')
def copas_aliados():
    # Obtener datos de las eliminatorias
    dats4 = obtener_copa_aliados()
    return render_template('copas/aliados_copa.html', dats4=dats4)
# Fin copa Fundación Aliados

# Copa UEMC Valladolid
copa_uemc = 'json_copa/copa_uemc.json'
def guardar_copa_uemc(dats5):
    with open(copa_uemc, 'w', encoding='utf-8') as file:
        json.dump(dats5, file, indent=4)
def obtener_copa_uemc():
    try:
        with open(copa_uemc, 'r', encoding='utf-8') as file:
            dats5 = json.load(file)
        return dats5
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return {'final': []}
nuevas_eliminatorias_uemc = []
duelos_uemc = None
# Crear formulario para los playoff
@app.route('/admin/copa_uemc/')
def ver_copa_uemc():
    dats5 = obtener_copa_uemc()
    return render_template('admin/copa_uemc.html', dats5=dats5)
# Crear formulario para los playoff
@app.route('/admin/crear_copa_uemc', methods=['GET', 'POST'])
def crear_copa_uemc():
    # Obtener los enfrentamientos actuales del archivo JSON
    dats5 = obtener_copa_uemc()
    if request.method == 'POST':
        # Obtener la etapa del torneo seleccionada por el usuario
        eliminatoria = request.form.get('eliminatoria')
        # Verificar el número máximo de partidos permitidos según la etapa del torneo
        if eliminatoria == 'final':
            max_partidos = 1              
        else:
            # Manejar caso no válido
            return "Etapa de torneo no válida"
        # Recuperar los datos del formulario y procesarlos
        num_partidos_str = request.form.get('num_partidos', '0')  # Valor predeterminado '0' si num_partidos está vacío
        num_partidos_str = num_partidos_str.strip()  # Eliminar espacios en blanco
        if num_partidos_str:
            num_partidos = int(num_partidos_str)
        else:
            num_partidos = 0  # Valor predeterminado si num_partidos está vacío
        # Si num_partidos es cero, se ignora la validación
        if num_partidos < 0:
            return "Número de partidos no válido"
        # Crear un identificador único para la eliminatoria
        eliminatoria_id = str(uuid.uuid4())  # Generar un UUID único
        # Crear un nuevo diccionario con los datos de la eliminatoria
        eliminatoria_data = {
            'id': eliminatoria_id,
            'partidos': []
        }
        # Recuperar los datos de cada partido del formulario
        for i in range(num_partidos):
            local = request.form.get(f'local{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            visitante = request.form.get(f'visitante{i}')
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            # Crear un nuevo diccionario con los datos del partido
            partido = {
                'local': local,
                'resultadoA': resultadoA,
                'resultadoB': resultadoB,
                'visitante': visitante,
                'fecha' : fecha,
                'hora' : hora
            }
            # Agregar el partido a la lista de partidos de la eliminatoria
            eliminatoria_data['partidos'].append(partido)
            # Agregar los nuevos enfrentamientos a la lista correspondiente
        dats5[eliminatoria] = eliminatoria_data
         # Agregar los nuevos enfrentamientos a la lista correspondiente
        nuevos_enfrentamientos.clear()  
        # Guardar la lista de partidos en el archivo JSON
        guardar_copa_uemc(dats5)
        # Redireccionar a la página de visualización del playoff
        return redirect(url_for('ver_copa_uemc'))
    # Si no es una solicitud POST, renderizar el formulario
    return render_template('admin/copa_uemc.html', dats5=dats5)
# Toma la lista de los playoff y los guarda
def guardar_copa_en_archivo_uemc(dats5):
    arch_guardar_copa_uemc = 'json_playoff/copa_uemc.json'
    # Guardar en el archivo
    with open(arch_guardar_copa_uemc, 'w', encoding='UTF-8') as archivo:
        json.dump(dats5, archivo)
# Modificar los partidos de los playoff
@app.route('/modificar_eliminatoria_copa_uemc/<string:id>', methods=['GET', 'POST'])
def modificar_copa_uemc(id):
    dats5 = obtener_copa_uemc()
    # Buscar la eliminatoria correspondiente al ID proporcionado
    eliminatoria_encontrada = None
    for eliminatoria, datos_eliminatoria in dats5.items():
        if datos_eliminatoria['id'] == id:
            eliminatoria_encontrada = datos_eliminatoria
            break
    if not eliminatoria_encontrada:
        return "Eliminatoria no encontrada"
    if request.method == 'POST':
        nuevos_partidos = []
        for index, partido in enumerate(eliminatoria_encontrada['partidos']):
            local = request.form.get(f'local{index}')
            resultadoA = request.form.get(f'resultadoA{index}')
            resultadoB = request.form.get(f'resultadoB{index}')
            visitante = request.form.get(f'visitante{index}')
            fecha = request.form.get(f'fecha{index}')
            hora = request.form.get(f'hora{index}')
            # Actualizar los datos del partido
            partido['local'] = local
            partido['resultadoA'] = resultadoA
            partido['resultadoB'] = resultadoB
            partido['visitante'] = visitante
            partido['fecha'] = fecha
            partido['hora'] = hora
            nuevos_partidos.append(partido)   
        eliminatoria_encontrada['partidos'] = nuevos_partidos       
        # Guardar los cambios en el archivo JSON
        guardar_copa_uemc(dats5)       
        # Redireccionar a la página de visualización del playoff
        return redirect(url_for('ver_copa_uemc')) 
# Ruta para mostrar la copa UEMC Valladolid
@app.route('/copa_uemc/')
def copas_uemc():
    # Obtener datos de las eliminatorias
    dats5 = obtener_copa_uemc()
    return render_template('copas/uemc_copa.html', dats5=dats5)
# Fin copa UEMC Valladolid

# Copa CD Parquesol
copa_parquesol = 'json_copa/copa_parquesol.json'
def guardar_copa_parquesol(dats6):
    with open(copa_parquesol, 'w', encoding='utf-8') as file:
        json.dump(dats6, file, indent=4)
def obtener_copa_parquesol():
    try:
        with open(copa_parquesol, 'r', encoding='utf-8') as file:
            dats6 = json.load(file)
        return dats6
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return {'ronda1': [],'ronda2': [],'ronda3': [],'octavos': [],'cuartos': [],'semifinales': [],'final': []}
nuevas_eliminatorias_parquesol = []
duelos_parquesol = None
# Crear formulario para la copa
@app.route('/admin/copa_parquesol/')
def ver_copa_parquesol():
    dats6 = obtener_copa_parquesol()
    return render_template('admin/copa_parquesol.html', dats6=dats6)
# Crear formulario para la copa
@app.route('/admin/crear_copa_parquesol', methods=['GET', 'POST'])
def crear_copa_parquesol():
    # Obtener los enfrentamientos actuales del archivo JSON
    dats6 = obtener_copa_parquesol()
    if request.method == 'POST':
        # Obtener la etapa del torneo seleccionada por el usuario
        eliminatoria = request.form.get('eliminatoria')
        # Verificar el número máximo de partidos permitidos según la etapa del torneo
        if eliminatoria == 'ronda1':
            max_partidos = 16
        elif eliminatoria == 'ronda2':
            max_partidos = 8
        elif eliminatoria == 'ronda3':
            max_partidos = 8 
        elif eliminatoria == 'octavos':
            max_partidos = 8 
        elif eliminatoria == 'cuartos':
            max_partidos = 4 
        elif eliminatoria == 'semifinales':
            max_partidos = 4
        elif eliminatoria == 'final':
            max_partidos = 1                                        
        else:
            # Manejar caso no válido
            return "Etapa de torneo no válida"
        # Recuperar los datos del formulario y procesarlos
        num_partidos_str = request.form.get('num_partidos', '0')  # Valor predeterminado '0' si num_partidos está vacío
        num_partidos_str = num_partidos_str.strip()  # Eliminar espacios en blanco
        if num_partidos_str:
            num_partidos = int(num_partidos_str)
        else:
            num_partidos = 0  # Valor predeterminado si num_partidos está vacío
        # Si num_partidos es cero, se ignora la validación
        if num_partidos < 0:
            return "Número de partidos no válido"
        # Crear un identificador único para la eliminatoria
        eliminatoria_id = str(uuid.uuid4())  # Generar un UUID único
        # Crear un nuevo diccionario con los datos de la eliminatoria
        eliminatoria_data = {
            'id': eliminatoria_id,
            'partidos': []
        }
        # Recuperar los datos de cada partido del formulario
        for i in range(num_partidos):
            local = request.form.get(f'local{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            visitante = request.form.get(f'visitante{i}')
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            # Crear un nuevo diccionario con los datos del partido
            partido = {
                'local': local,
                'resultadoA': resultadoA,
                'resultadoB': resultadoB,
                'visitante': visitante,
                'fecha' : fecha,
                'hora' : hora
            }
            # Agregar el partido a la lista de partidos de la eliminatoria
            eliminatoria_data['partidos'].append(partido)
            # Agregar los nuevos enfrentamientos a la lista correspondiente
        dats6[eliminatoria] = eliminatoria_data
         # Agregar los nuevos enfrentamientos a la lista correspondiente
        nuevos_enfrentamientos.clear()  
        # Guardar la lista de partidos en el archivo JSON
        guardar_copa_parquesol(dats6)
        # Redireccionar a la página de visualización del playoff
        return redirect(url_for('ver_copa_parquesol'))
    # Si no es una solicitud POST, renderizar el formulario
    return render_template('admin/copa_parquesol.html', dats6=dats6)
# Toma la lista de la copa y los guarda
def guardar_copa_en_archivo_parquesol(dats6):
    arch_guardar_copa_parquesol = 'json_playoff/copa_parquesol.json'
    # Guardar en el archivo
    with open(arch_guardar_copa_parquesol, 'w', encoding='UTF-8') as archivo:
        json.dump(dats6, archivo)
# Modificar los partidos de los playoff
@app.route('/modificar_eliminatoria_copa_parquesol/<string:id>', methods=['GET', 'POST'])
def modificar_copa_parquesol(id):
    dats6 = obtener_copa_parquesol()
    # Buscar la eliminatoria correspondiente al ID proporcionado
    eliminatoria_encontrada = None
    for eliminatoria, datos_eliminatoria in dats6.items():
        if datos_eliminatoria['id'] == id:
            eliminatoria_encontrada = datos_eliminatoria
            break
    if not eliminatoria_encontrada:
        return "Eliminatoria no encontrada"
    if request.method == 'POST':
        nuevos_partidos = []
        for index, partido in enumerate(eliminatoria_encontrada['partidos']):
            local = request.form.get(f'local{index}')
            resultadoA = request.form.get(f'resultadoA{index}')
            resultadoB = request.form.get(f'resultadoB{index}')
            visitante = request.form.get(f'visitante{index}')
            fecha = request.form.get(f'fecha{index}')
            hora = request.form.get(f'hora{index}')
            # Actualizar los datos del partido
            partido['local'] = local
            partido['resultadoA'] = resultadoA
            partido['resultadoB'] = resultadoB
            partido['visitante'] = visitante
            partido['fecha'] = fecha
            partido['hora'] = hora
            nuevos_partidos.append(partido)   
        eliminatoria_encontrada['partidos'] = nuevos_partidos       
        # Guardar los cambios en el archivo JSON
        guardar_copa_parquesol(dats6)       
        # Redireccionar a la página de visualización de copa
        return redirect(url_for('ver_copa_parquesol')) 
# Ruta para mostrar la copa CD Parquesol
@app.route('/copa_parquesol/')
def copas_parquesol():
    # Obtener datos de las eliminatorias
    dats6 = obtener_copa_parquesol()
    return render_template('copas/parquesol_copa.html', dats6=dats6)
# Fin copa CD Parquesol

# Copa CPLV Munia Panteras
copa_panteras = 'json_copa/copa_panteras.json'
def guardar_copa_panteras(dats7):
    with open(copa_panteras, 'w', encoding='utf-8') as file:
        json.dump(dats7, file, indent=4)
def obtener_copa_panteras():
    try:
        with open(copa_panteras, 'r', encoding='utf-8') as file:
            dats7 = json.load(file)
        return dats7
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return {'cuartos': [], 'semifinales': [],'final': []}
nuevas_eliminatorias_panteras = []
duelos_panteras = None
# Crear formulario para los playoff
@app.route('/admin/copa_panteras/')
def ver_copa_panteras():
    dats7 = obtener_copa_panteras()
    return render_template('admin/copa_panteras.html', dats7=dats7)
# Crear formulario para los playoff
@app.route('/admin/crear_copa_panteras', methods=['GET', 'POST'])
def crear_copa_panteras():
    # Obtener los enfrentamientos actuales del archivo JSON
    dats7 = obtener_copa_panteras()
    if request.method == 'POST':
        # Obtener la etapa del torneo seleccionada por el usuario
        eliminatoria = request.form.get('eliminatoria')
        # Verificar el número máximo de partidos permitidos según la etapa del torneo
        if eliminatoria == 'cuartos':
            max_partidos = 3
        elif eliminatoria == 'semifinales':
            max_partidos = 2
        elif eliminatoria == 'final':
            max_partidos = 1               
        else:
            # Manejar caso no válido
            return "Etapa de torneo no válida"
        # Recuperar los datos del formulario y procesarlos
        num_partidos_str = request.form.get('num_partidos', '0')  # Valor predeterminado '0' si num_partidos está vacío
        num_partidos_str = num_partidos_str.strip()  # Eliminar espacios en blanco
        if num_partidos_str:
            num_partidos = int(num_partidos_str)
        else:
            num_partidos = 0  # Valor predeterminado si num_partidos está vacío
        # Si num_partidos es cero, se ignora la validación
        if num_partidos < 0:
            return "Número de partidos no válido"
        # Crear un identificador único para la eliminatoria
        eliminatoria_id = str(uuid.uuid4())  # Generar un UUID único
        # Crear un nuevo diccionario con los datos de la eliminatoria
        eliminatoria_data = {
            'id': eliminatoria_id,
            'partidos': []
        }
        # Recuperar los datos de cada partido del formulario
        for i in range(num_partidos):
            local = request.form.get(f'local{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            visitante = request.form.get(f'visitante{i}')
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            # Crear un nuevo diccionario con los datos del partido
            partido = {
                'local': local,
                'resultadoA': resultadoA,
                'resultadoB': resultadoB,
                'visitante': visitante,
                'fecha' : fecha,
                'hora' : hora
            }
            # Agregar el partido a la lista de partidos de la eliminatoria
            eliminatoria_data['partidos'].append(partido)
            # Agregar los nuevos enfrentamientos a la lista correspondiente
        dats7[eliminatoria] = eliminatoria_data
         # Agregar los nuevos enfrentamientos a la lista correspondiente
        nuevos_enfrentamientos.clear()  
        # Guardar la lista de partidos en el archivo JSON
        guardar_copa_panteras(dats7)
        # Redireccionar a la página de visualización del playoff
        return redirect(url_for('ver_copa_panteras'))
    # Si no es una solicitud POST, renderizar el formulario
    return render_template('admin/copa_panteras.html', dats7=dats7)
# Toma la lista de los playoff y los guarda
def guardar_copa_en_archivo_panteras(dats7):
    arch_guardar_copa_panteras = 'json_playoff/copa_panteras.json'
    # Guardar en el archivo
    with open(arch_guardar_copa_panteras, 'w', encoding='UTF-8') as archivo:
        json.dump(dats7, archivo)
# Modificar los partidos de los playoff
@app.route('/modificar_eliminatoria_copa_panteras/<string:id>', methods=['GET', 'POST'])
def modificar_copa_panteras(id):
    dats7 = obtener_copa_panteras()
    # Buscar la eliminatoria correspondiente al ID proporcionado
    eliminatoria_encontrada = None
    for eliminatoria, datos_eliminatoria in dats7.items():
        if datos_eliminatoria['id'] == id:
            eliminatoria_encontrada = datos_eliminatoria
            break
    if not eliminatoria_encontrada:
        return "Eliminatoria no encontrada"
    if request.method == 'POST':
        nuevos_partidos = []
        for index, partido in enumerate(eliminatoria_encontrada['partidos']):
            local = request.form.get(f'local{index}')
            resultadoA = request.form.get(f'resultadoA{index}')
            resultadoB = request.form.get(f'resultadoB{index}')
            visitante = request.form.get(f'visitante{index}')
            fecha = request.form.get(f'fecha{index}')
            hora = request.form.get(f'hora{index}')
            # Actualizar los datos del partido
            partido['local'] = local
            partido['resultadoA'] = resultadoA
            partido['resultadoB'] = resultadoB
            partido['visitante'] = visitante
            partido['fecha'] = fecha
            partido['hora'] = hora
            nuevos_partidos.append(partido)   
        eliminatoria_encontrada['partidos'] = nuevos_partidos       
        # Guardar los cambios en el archivo JSON
        guardar_copa_panteras(dats7)       
        # Redireccionar a la página de visualización del playoff
        return redirect(url_for('ver_copa_panteras')) 
# Ruta para mostrar la copa CPLV Munia Panteras
@app.route('/copa_panteras/')
def copas_panteras():
    # Obtener datos de las eliminatorias
    dats7 = obtener_copa_panteras()
    return render_template('copas/panteras_copa.html', dats7=dats7)
# Fin copa CPLV Munia Panteras

# Copa CPLV Caja Rural
copa_caja = 'json_copa/copa_caja.json'
def guardar_copa_caja(dats8):
    with open(copa_caja, 'w', encoding='utf-8') as file:
        json.dump(dats8, file, indent=4)
def obtener_copa_caja():
    try:
        with open(copa_caja, 'r', encoding='utf-8') as file:
            dats8 = json.load(file)
        return dats8
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return {'cuartos': [], 'semifinales': [],'final': []}
nuevas_eliminatorias_caja = []
duelos_caja = None
# Crear formulario para los playoff
@app.route('/admin/copa_caja/')
def ver_copa_caja():
    dats8 = obtener_copa_caja()
    return render_template('admin/copa_caja.html', dats8=dats8)
# Crear formulario para los playoff
@app.route('/admin/crear_copa_caja', methods=['GET', 'POST'])
def crear_copa_caja():
    # Obtener los enfrentamientos actuales del archivo JSON
    dats8 = obtener_copa_caja()
    if request.method == 'POST':
        # Obtener la etapa del torneo seleccionada por el usuario
        eliminatoria = request.form.get('eliminatoria')
        # Verificar el número máximo de partidos permitidos según la etapa del torneo
        if eliminatoria == 'cuartos':
            max_partidos = 3
        elif eliminatoria == 'semifinales':
            max_partidos = 2
        elif eliminatoria == 'final':
            max_partidos = 1               
        else:
            # Manejar caso no válido
            return "Etapa de torneo no válida"
        # Recuperar los datos del formulario y procesarlos
        num_partidos_str = request.form.get('num_partidos', '0')  # Valor predeterminado '0' si num_partidos está vacío
        num_partidos_str = num_partidos_str.strip()  # Eliminar espacios en blanco
        if num_partidos_str:
            num_partidos = int(num_partidos_str)
        else:
            num_partidos = 0  # Valor predeterminado si num_partidos está vacío
        # Si num_partidos es cero, se ignora la validación
        if num_partidos < 0:
            return "Número de partidos no válido"
        # Crear un identificador único para la eliminatoria
        eliminatoria_id = str(uuid.uuid4())  # Generar un UUID único
        # Crear un nuevo diccionario con los datos de la eliminatoria
        eliminatoria_data = {
            'id': eliminatoria_id,
            'partidos': []
        }
        # Recuperar los datos de cada partido del formulario
        for i in range(num_partidos):
            local = request.form.get(f'local{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            visitante = request.form.get(f'visitante{i}')
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            # Crear un nuevo diccionario con los datos del partido
            partido = {
                'local': local,
                'resultadoA': resultadoA,
                'resultadoB': resultadoB,
                'visitante': visitante,
                'fecha' : fecha,
                'hora' : hora
            }
            # Agregar el partido a la lista de partidos de la eliminatoria
            eliminatoria_data['partidos'].append(partido)
            # Agregar los nuevos enfrentamientos a la lista correspondiente
        dats8[eliminatoria] = eliminatoria_data
         # Agregar los nuevos enfrentamientos a la lista correspondiente
        nuevos_enfrentamientos.clear()  
        # Guardar la lista de partidos en el archivo JSON
        guardar_copa_caja(dats8)
        # Redireccionar a la página de visualización del playoff
        return redirect(url_for('ver_copa_caja'))
    # Si no es una solicitud POST, renderizar el formulario
    return render_template('admin/copa_caja.html', dats8=dats8)
# Toma la lista de los playoff y los guarda
def guardar_copa_en_archivo_caja(dats8):
    arch_guardar_copa_caja = 'json_playoff/copa_caja.json'
    # Guardar en el archivo
    with open(arch_guardar_copa_caja, 'w', encoding='UTF-8') as archivo:
        json.dump(dats8, archivo)
# Modificar los partidos de los playoff
@app.route('/modificar_eliminatoria_copa_caja/<string:id>', methods=['GET', 'POST'])
def modificar_copa_caja(id):
    dats8 = obtener_copa_caja()
    # Buscar la eliminatoria correspondiente al ID proporcionado
    eliminatoria_encontrada = None
    for eliminatoria, datos_eliminatoria in dats8.items():
        if datos_eliminatoria['id'] == id:
            eliminatoria_encontrada = datos_eliminatoria
            break
    if not eliminatoria_encontrada:
        return "Eliminatoria no encontrada"
    if request.method == 'POST':
        nuevos_partidos = []
        for index, partido in enumerate(eliminatoria_encontrada['partidos']):
            local = request.form.get(f'local{index}')
            resultadoA = request.form.get(f'resultadoA{index}')
            resultadoB = request.form.get(f'resultadoB{index}')
            visitante = request.form.get(f'visitante{index}')
            fecha = request.form.get(f'fecha{index}')
            hora = request.form.get(f'hora{index}')
            # Actualizar los datos del partido
            partido['local'] = local
            partido['resultadoA'] = resultadoA
            partido['resultadoB'] = resultadoB
            partido['visitante'] = visitante
            partido['fecha'] = fecha
            partido['hora'] = hora
            nuevos_partidos.append(partido)   
        eliminatoria_encontrada['partidos'] = nuevos_partidos       
        # Guardar los cambios en el archivo JSON
        guardar_copa_caja(dats8)       
        # Redireccionar a la página de visualización del playoff
        return redirect(url_for('ver_copa_caja')) 
# Ruta para mostrar la copa CPLV Caja Rural
@app.route('/copa_caja/')
def copas_caja():
    # Obtener datos de las eliminatorias
    dats8 = obtener_copa_caja()
    return render_template('copas/caja_copa.html', dats8=dats8)
# Fin copa CPLV Caja Rural

# Copa CR El Salvador Fem
copa_salvador_fem = 'json_copa/copa_salvador_fem.json'
def guardar_copa_salvador_fem(dats9):
    with open(copa_salvador_fem, 'w', encoding='utf-8') as file:
        json.dump(dats9, file, indent=4)
def obtener_copa_salvador_fem():
    try:
        with open(copa_salvador_fem, 'r', encoding='utf-8') as file:
            dats9 = json.load(file)
        return dats9
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return {'grupo1': [],'grupo2': [],'grupo3': [],'grupo4': [], 'semifinales': [],'final': []}
nuevas_eliminatorias_salvador_fem = []
duelos_salvador_fem = None
# Crear formulario para los playoff
@app.route('/admin/copa_salvador_fem/')
def ver_copa_salvador_fem():
    dats9 = obtener_copa_salvador_fem()
    return render_template('admin/copa_salvador_fem.html', dats9=dats9)
# Crear formulario para los playoff
@app.route('/admin/crear_copa_salvador_fem', methods=['GET', 'POST'])
def crear_copa_salvador_fem():
    # Obtener los enfrentamientos actuales del archivo JSON
    dats9 = obtener_copa_salvador_fem()
    if request.method == 'POST':
        # Obtener la etapa del torneo seleccionada por el usuario
        eliminatoria = request.form.get('eliminatoria')
        # Verificar el número máximo de partidos permitidos según la etapa del torneo
        if eliminatoria == 'grupo1':
            max_partidos = 12
        elif eliminatoria == 'grupo2':
            max_partidos = 12
        elif eliminatoria == 'grupo3':
            max_partidos = 12
        elif eliminatoria == 'grupo4':
            max_partidos = 12            
        elif eliminatoria == 'semifinales':
            max_partidos = 2
        elif eliminatoria == 'final':
            max_partidos = 1               
        else:
            # Manejar caso no válido
            return "Etapa de torneo no válida"
        # Recuperar los datos del formulario y procesarlos
        num_partidos_str = request.form.get('num_partidos', '0')  # Valor predeterminado '0' si num_partidos está vacío
        num_partidos_str = num_partidos_str.strip()  # Eliminar espacios en blanco
        if num_partidos_str:
            num_partidos = int(num_partidos_str)
        else:
            num_partidos = 0  # Valor predeterminado si num_partidos está vacío
        # Si num_partidos es cero, se ignora la validación
        if num_partidos < 0:
            return "Número de partidos no válido"
        # Crear un identificador único para la eliminatoria
        eliminatoria_id = str(uuid.uuid4())  # Generar un UUID único
        # Crear un nuevo diccionario con los datos de la eliminatoria
        eliminatoria_data = {
            'id': eliminatoria_id,
            'partidos': []
        }
        # Recuperar los datos de cada partido del formulario
        for i in range(num_partidos):
            local = request.form.get(f'local{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            visitante = request.form.get(f'visitante{i}')
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            # Crear un nuevo diccionario con los datos del partido
            partido = {
                'local': local,
                'resultadoA': resultadoA,
                'resultadoB': resultadoB,
                'visitante': visitante,
                'fecha' : fecha,
                'hora' : hora
            }
            # Agregar el partido a la lista de partidos de la eliminatoria
            eliminatoria_data['partidos'].append(partido)
            # Agregar los nuevos enfrentamientos a la lista correspondiente
        dats9[eliminatoria] = eliminatoria_data
         # Agregar los nuevos enfrentamientos a la lista correspondiente
        nuevos_enfrentamientos.clear()  
        # Guardar la lista de partidos en el archivo JSON
        guardar_copa_salvador_fem(dats9)
        # Redireccionar a la página de visualización del playoff
        return redirect(url_for('ver_copa_salvador_fem'))
    # Si no es una solicitud POST, renderizar el formulario
    return render_template('admin/copa_salvador_fem.html', dats9=dats9)
# Toma la lista de los playoff y los guarda
def guardar_copa_en_archivo_salvador_fem(dats9):
    arch_guardar_copa_salvador_fem = 'json_playoff/copa_salvador_fem.json'
    # Guardar en el archivo
    with open(arch_guardar_copa_salvador_fem, 'w', encoding='UTF-8') as archivo:
        json.dump(dats9, archivo)
# Modificar los partidos de los playoff
@app.route('/modificar_eliminatoria_copa_salvador_fem/<string:id>', methods=['GET', 'POST'])
def modificar_copa_salvador_fem(id):
    dats9 = obtener_copa_salvador_fem()
    # Buscar la eliminatoria correspondiente al ID proporcionado
    eliminatoria_encontrada = None
    for eliminatoria, datos_eliminatoria in dats9.items():
        if datos_eliminatoria['id'] == id:
            eliminatoria_encontrada = datos_eliminatoria
            break
    if not eliminatoria_encontrada:
        return "Eliminatoria no encontrada"
    if request.method == 'POST':
        nuevos_partidos = []
        for index, partido in enumerate(eliminatoria_encontrada['partidos']):
            local = request.form.get(f'local{index}')
            resultadoA = request.form.get(f'resultadoA{index}')
            resultadoB = request.form.get(f'resultadoB{index}')
            visitante = request.form.get(f'visitante{index}')
            fecha = request.form.get(f'fecha{index}')
            hora = request.form.get(f'hora{index}')
            # Actualizar los datos del partido
            partido['local'] = local
            partido['resultadoA'] = resultadoA
            partido['resultadoB'] = resultadoB
            partido['visitante'] = visitante
            partido['fecha'] = fecha
            partido['hora'] = hora
            nuevos_partidos.append(partido)   
        eliminatoria_encontrada['partidos'] = nuevos_partidos       
        # Guardar los cambios en el archivo JSON
        guardar_copa_salvador_fem(dats9)       
        # Redireccionar a la página de visualización del playoff
        return redirect(url_for('ver_copa_salvador_fem')) 
# Ruta para mostrar la copa CPLV Caja Rural
@app.route('/copa_salvador_fem/')
def copas_salvador_fem():
    # Obtener datos de las eliminatorias
    dats9 = obtener_copa_salvador_fem()
    return render_template('copas/salvador_fem_copa.html', dats9=dats9)
# Fin copa CR El Salvador Fem

# Copa CR El Salvador
copa_salvador = 'json_copa/copa_salvador.json'
def guardar_copa_salvador(dats10):
    with open(copa_salvador, 'w', encoding='utf-8') as file:
        json.dump(dats10, file, indent=4)
def obtener_copa_salvador():
    try:
        with open(copa_salvador, 'r', encoding='utf-8') as file:
            dats10 = json.load(file)
        return dats10
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return {'grupo1': [],'grupo2': [],'grupo3': [],'grupo4': [], 'semifinales': [],'final': []}
nuevas_eliminatorias_salvador = []
duelos_salvador = None
# Crear formulario para los playoff
@app.route('/admin/copa_salvador/')
def ver_copa_salvador():
    dats10 = obtener_copa_salvador()
    return render_template('admin/copa_salvador.html', dats10=dats10)
# Crear formulario para los playoff
@app.route('/admin/crear_copa_salvador', methods=['GET', 'POST'])
def crear_copa_salvador():
    # Obtener los enfrentamientos actuales del archivo JSON
    dats10 = obtener_copa_salvador()
    if request.method == 'POST':
        # Obtener la etapa del torneo seleccionada por el usuario
        eliminatoria = request.form.get('eliminatoria')
        # Verificar el número máximo de partidos permitidos según la etapa del torneo
        if eliminatoria == 'grupo1':
            max_partidos = 9
        elif eliminatoria == 'grupo2':
            max_partidos = 9
        elif eliminatoria == 'grupo3':
            max_partidos = 9
        elif eliminatoria == 'grupo4':
            max_partidos = 9            
        elif eliminatoria == 'semifinales':
            max_partidos = 2
        elif eliminatoria == 'final':
            max_partidos = 1               
        else:
            # Manejar caso no válido
            return "Etapa de torneo no válida"
        # Recuperar los datos del formulario y procesarlos
        num_partidos_str = request.form.get('num_partidos', '0')  # Valor predeterminado '0' si num_partidos está vacío
        num_partidos_str = num_partidos_str.strip()  # Eliminar espacios en blanco
        if num_partidos_str:
            num_partidos = int(num_partidos_str)
        else:
            num_partidos = 0  # Valor predeterminado si num_partidos está vacío
        # Si num_partidos es cero, se ignora la validación
        if num_partidos < 0:
            return "Número de partidos no válido"
        # Crear un identificador único para la eliminatoria
        eliminatoria_id = str(uuid.uuid4())  # Generar un UUID único
        # Crear un nuevo diccionario con los datos de la eliminatoria
        eliminatoria_data = {
            'id': eliminatoria_id,
            'partidos': []
        }
        # Recuperar los datos de cada partido del formulario
        for i in range(num_partidos):
            local = request.form.get(f'local{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            visitante = request.form.get(f'visitante{i}')
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            # Crear un nuevo diccionario con los datos del partido
            partido = {
                'local': local,
                'resultadoA': resultadoA,
                'resultadoB': resultadoB,
                'visitante': visitante,
                'fecha' : fecha,
                'hora' : hora
            }
            # Agregar el partido a la lista de partidos de la eliminatoria
            eliminatoria_data['partidos'].append(partido)
            # Agregar los nuevos enfrentamientos a la lista correspondiente
        dats10[eliminatoria] = eliminatoria_data
         # Agregar los nuevos enfrentamientos a la lista correspondiente
        nuevos_enfrentamientos.clear()  
        # Guardar la lista de partidos en el archivo JSON
        guardar_copa_salvador(dats10)
        # Redireccionar a la página de visualización del playoff
        return redirect(url_for('ver_copa_salvador'))
    # Si no es una solicitud POST, renderizar el formulario
    return render_template('admin/copa_salvador.html', dats10=dats10)
# Toma la lista de los playoff y los guarda
def guardar_copa_en_archivo_salvador(dats10):
    arch_guardar_copa_salvador = 'json_playoff/copa_salvador.json'
    # Guardar en el archivo
    with open(arch_guardar_copa_salvador, 'w', encoding='UTF-8') as archivo:
        json.dump(dats10, archivo)
# Modificar los partidos de los playoff
@app.route('/modificar_eliminatoria_copa_salvador/<string:id>', methods=['GET', 'POST'])
def modificar_copa_salvador(id):
    dats10 = obtener_copa_salvador()
    # Buscar la eliminatoria correspondiente al ID proporcionado
    eliminatoria_encontrada = None
    for eliminatoria, datos_eliminatoria in dats9.items():
        if datos_eliminatoria['id'] == id:
            eliminatoria_encontrada = datos_eliminatoria
            break
    if not eliminatoria_encontrada:
        return "Eliminatoria no encontrada"
    if request.method == 'POST':
        nuevos_partidos = []
        for index, partido in enumerate(eliminatoria_encontrada['partidos']):
            local = request.form.get(f'local{index}')
            resultadoA = request.form.get(f'resultadoA{index}')
            resultadoB = request.form.get(f'resultadoB{index}')
            visitante = request.form.get(f'visitante{index}')
            fecha = request.form.get(f'fecha{index}')
            hora = request.form.get(f'hora{index}')
            # Actualizar los datos del partido
            partido['local'] = local
            partido['resultadoA'] = resultadoA
            partido['resultadoB'] = resultadoB
            partido['visitante'] = visitante
            partido['fecha'] = fecha
            partido['hora'] = hora
            nuevos_partidos.append(partido)   
        eliminatoria_encontrada['partidos'] = nuevos_partidos       
        # Guardar los cambios en el archivo JSON
        guardar_copa_salvador(dats10)       
        # Redireccionar a la página de visualización del playoff
        return redirect(url_for('ver_copa_salvador')) 
# Ruta para mostrar la copa CPLV Caja Rural
@app.route('/copa_salvador/')
def copas_salvador():
    # Obtener datos de las eliminatorias
    dats10 = obtener_copa_salvador()
    return render_template('copas/salvador_copa.html', dats10=dats10)
# Fin copa CR El Salvador

# Copa VRAC
copa_vrac = 'json_copa/copa_vrac.json'
def guardar_copa_vrac(dats11):
    with open(copa_vrac, 'w', encoding='utf-8') as file:
        json.dump(dats11, file, indent=4)
def obtener_copa_vrac():
    try:
        with open(copa_vrac, 'r', encoding='utf-8') as file:
            dats11 = json.load(file)
        return dats11
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return {'grupo1': [],'grupo2': [],'grupo3': [],'grupo4': [], 'semifinales': [],'final': []}
nuevas_eliminatorias_vrac = []
duelos_vrac = None
# Crear formulario para los playoff
@app.route('/admin/copa_vrac/')
def ver_copa_vrac():
    dats11 = obtener_copa_vrac()
    return render_template('admin/copa_vrac.html', dats11=dats11)
# Crear formulario para los playoff
@app.route('/admin/crear_copa_vrac', methods=['GET', 'POST'])
def crear_copa_vrac():
    # Obtener los enfrentamientos actuales del archivo JSON
    dats11 = obtener_copa_vrac()
    if request.method == 'POST':
        # Obtener la etapa del torneo seleccionada por el usuario
        eliminatoria = request.form.get('eliminatoria')
        # Verificar el número máximo de partidos permitidos según la etapa del torneo
        if eliminatoria == 'grupo1':
            max_partidos = 9
        elif eliminatoria == 'grupo2':
            max_partidos = 9
        elif eliminatoria == 'grupo3':
            max_partidos = 9
        elif eliminatoria == 'grupo4':
            max_partidos = 9            
        elif eliminatoria == 'semifinales':
            max_partidos = 2
        elif eliminatoria == 'final':
            max_partidos = 1               
        else:
            # Manejar caso no válido
            return "Etapa de torneo no válida"
        # Recuperar los datos del formulario y procesarlos
        num_partidos_str = request.form.get('num_partidos', '0')  # Valor predeterminado '0' si num_partidos está vacío
        num_partidos_str = num_partidos_str.strip()  # Eliminar espacios en blanco
        if num_partidos_str:
            num_partidos = int(num_partidos_str)
        else:
            num_partidos = 0  # Valor predeterminado si num_partidos está vacío
        # Si num_partidos es cero, se ignora la validación
        if num_partidos < 0:
            return "Número de partidos no válido"
        # Crear un identificador único para la eliminatoria
        eliminatoria_id = str(uuid.uuid4())  # Generar un UUID único
        # Crear un nuevo diccionario con los datos de la eliminatoria
        eliminatoria_data = {
            'id': eliminatoria_id,
            'partidos': []
        }
        # Recuperar los datos de cada partido del formulario
        for i in range(num_partidos):
            local = request.form.get(f'local{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            visitante = request.form.get(f'visitante{i}')
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            # Crear un nuevo diccionario con los datos del partido
            partido = {
                'local': local,
                'resultadoA': resultadoA,
                'resultadoB': resultadoB,
                'visitante': visitante,
                'fecha' : fecha,
                'hora' : hora
            }
            # Agregar el partido a la lista de partidos de la eliminatoria
            eliminatoria_data['partidos'].append(partido)
            # Agregar los nuevos enfrentamientos a la lista correspondiente
        dats11[eliminatoria] = eliminatoria_data
         # Agregar los nuevos enfrentamientos a la lista correspondiente
        nuevos_enfrentamientos.clear()  
        # Guardar la lista de partidos en el archivo JSON
        guardar_copa_vrac(dats11)
        # Redireccionar a la página de visualización del playoff
        return redirect(url_for('ver_copa_vrac'))
    # Si no es una solicitud POST, renderizar el formulario
    return render_template('admin/copa_vrac.html', dats11=dats11)
# Toma la lista de los playoff y los guarda
def guardar_copa_en_archivo_vrac(dats11):
    arch_guardar_copa_vrac = 'json_playoff/copa_vrac.json'
    # Guardar en el archivo
    with open(arch_guardar_copa_vrac, 'w', encoding='UTF-8') as archivo:
        json.dump(dats11, archivo)
# Modificar los partidos de los playoff
@app.route('/modificar_eliminatoria_copa_vrac/<string:id>', methods=['GET', 'POST'])
def modificar_copa_vrac(id):
    dats11 = obtener_copa_vrac()
    # Buscar la eliminatoria correspondiente al ID proporcionado
    eliminatoria_encontrada = None
    for eliminatoria, datos_eliminatoria in dats11.items():
        if datos_eliminatoria['id'] == id:
            eliminatoria_encontrada = datos_eliminatoria
            break
    if not eliminatoria_encontrada:
        return "Eliminatoria no encontrada"
    if request.method == 'POST':
        nuevos_partidos = []
        for index, partido in enumerate(eliminatoria_encontrada['partidos']):
            local = request.form.get(f'local{index}')
            resultadoA = request.form.get(f'resultadoA{index}')
            resultadoB = request.form.get(f'resultadoB{index}')
            visitante = request.form.get(f'visitante{index}')
            fecha = request.form.get(f'fecha{index}')
            hora = request.form.get(f'hora{index}')
            # Actualizar los datos del partido
            partido['local'] = local
            partido['resultadoA'] = resultadoA
            partido['resultadoB'] = resultadoB
            partido['visitante'] = visitante
            partido['fecha'] = fecha
            partido['hora'] = hora
            nuevos_partidos.append(partido)   
        eliminatoria_encontrada['partidos'] = nuevos_partidos       
        # Guardar los cambios en el archivo JSON
        guardar_copa_vrac(dats11)       
        # Redireccionar a la página de visualización del playoff
        return redirect(url_for('ver_copa_vrac')) 
# Ruta para mostrar la copa CPLV Caja Rural
@app.route('/copa_vrac/')
def copas_vrac():
    # Obtener datos de las eliminatorias
    dats11 = obtener_copa_vrac()
    return render_template('copas/vrac_copa.html', dats11=dats11)
# Fin copa VRAC
















    
if __name__ == '__main__':
    app.secret_key = 'pinchellave'
    app.run(debug=True)