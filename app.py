from flask import Flask
from flask import render_template, request, redirect,url_for, session, render_template_string
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
from flask_caching import Cache
from collections import defaultdict
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
# Ruta sección de hockey línea
@app.route('/seccion/hockey')
def seccion_hockey():
    return render_template('secciones/hockey.html')
# Ruta sección de rugby
@app.route('/seccion/rugby')
def seccion_rugby():
    return render_template('secciones/rugby.html')
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
        equipoLocal = request.form.get(f'local{i}')
        resultadoA = request.form.get(f'resultadoA{i}')
        resultadoB = request.form.get(f'resultadoB{i}')
        equipoVisitante = request.form.get(f'visitante{i}')
        
        nuevo_partido = {
            #'id': id_nuevo,
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
                nuevo_partido = {
                    'local': equipoLocal,
                    'resultadoA': resultadoA,
                    'resultadoB': resultadoB,
                    'visitante': equipoVisitante
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
            # Actualizar los datos del partido
            partido['local'] = local
            partido['resultadoA'] = resultadoA
            partido['resultadoB'] = resultadoB
            partido['visitante'] = visitante
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
        equipoLocal = request.form.get(f'local{i}')
        resultadoA = request.form.get(f'resultadoA{i}')
        resultadoB = request.form.get(f'resultadoB{i}')
        equipoVisitante = request.form.get(f'visitante{i}')
        
        nuevo_partido = {
            #'id': id_nuevo,
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
                nuevo_partido = {
                    'local': equipoLocal,
                    'resultadoA': resultadoA,
                    'resultadoB': resultadoB,
                    'visitante': equipoVisitante
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
        equipoLocal = request.form.get(f'local{i}')
        resultadoA = request.form.get(f'resultadoA{i}')
        resultadoB = request.form.get(f'resultadoB{i}')
        equipoVisitante = request.form.get(f'visitante{i}')
        nuevo_partido = {
            #'id': id_nuevo,
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
                equipoLocal = request.form.get(f'local{i}')
                resultadoA = request.form.get(f'resultadoA{i}')
                resultadoB = request.form.get(f'resultadoB{i}')
                equipoVisitante = request.form.get(f'visitante{i}')
                nuevo_partido = {
                    'local': equipoLocal,
                    'resultadoA': resultadoA,
                    'resultadoB': resultadoB,
                    'visitante': equipoVisitante
                }
                resultados_a_modificar['partidos'].append(nuevo_partido)
            # Guardar los cambios en el archivo JSON
            guardar_partidos_en_archivo_ponce(data2)            
            return redirect(url_for('calend_ponce'))
    return redirect(url_for('calend_ponce'))
# Ruta para borrar jornadas
@app.route('/eliminar_jorn_aliados/<string:id>', methods=['POST'])
def eliminar_jorn_aliados(id):
    data2 = obtener_datos_aliados()
    jornada_a_eliminar = [j for j in data2 if j['id'] != id]  # Filtrar las jornadas diferentes de la que se va a eliminar
    guardar_partidos_en_archivo_aliados(jornada_a_eliminar)
    # Redirigir a la página de encuentros_uemc (o a donde desees después de eliminar)
    return redirect(url_for('calend_aliados'))
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
                elif 'segundo_enfrentamiento' not in tabla_partidos_ponce[equipo_contrario]:
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
        nuevo_partido = {
            #'id': id_nuevo,
            'local': equipoLocal,
            'resultadoA': resultadoA,
            'resultadoB': resultadoB,
            'visitante': equipoVisitante
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
                nuevo_partido = {
                    'local': equipoLocal,
                    'resultadoA': resultadoA,
                    'resultadoB': resultadoB,
                    'visitante': equipoVisitante
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
        nuevo_partido = {
            #'id': id_nuevo,
            'local': equipoLocal,
            'resultadoA': resultadoA,
            'resultadoB': resultadoB,
            'visitante': equipoVisitante
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
                nuevo_partido = {
                    'local': equipoLocal,
                    'resultadoA': resultadoA,
                    'resultadoB': resultadoB,
                    'visitante': equipoVisitante
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
        nuevo_partido = {
            #'id': id_nuevo,
            'local': equipoLocal,
            'resultadoA': resultadoA,
            'resultadoB': resultadoB,
            'visitante': equipoVisitante
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
                nuevo_partido = {
                    'local': equipoLocal,
                    'resultadoA': resultadoA,
                    'resultadoB': resultadoB,
                    'visitante': equipoVisitante
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
# Partidos V Simancas
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
        nuevo_partido = {
            #'id': id_nuevo,
            'local': equipoLocal,
            'resultadoA': resultadoA,
            'resultadoB': resultadoB,
            'visitante': equipoVisitante
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
                nuevo_partido = {
                    'local': equipoLocal,
                    'resultadoA': resultadoA,
                    'resultadoB': resultadoB,
                    'visitante': equipoVisitante
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
        nuevo_partido = {
            #'id': id_nuevo,
            'local': equipoLocal,
            'resultadoA': resultadoA,
            'resultadoB': resultadoB,
            'visitante': equipoVisitante
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
                nuevo_partido = {
                    'local': equipoLocal,
                    'resultadoA': resultadoA,
                    'resultadoB': resultadoB,
                    'visitante': equipoVisitante
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
        nuevo_partido = {
            #'id': id_nuevo,
            'local': equipoLocal,
            'resultadoA': resultadoA,
            'resultadoB': resultadoB,
            'visitante': equipoVisitante
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
                nuevo_partido = {
                    'local': equipoLocal,
                    'resultadoA': resultadoA,
                    'resultadoB': resultadoB,
                    'visitante': equipoVisitante
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
        nuevo_partido = {
            #'id': id_nuevo,
            'local': equipoLocal,
            'bonusA': bonusA,
            'resultadoA': resultadoA,
            'resultadoB': resultadoB,
            'bonusB': bonusB,
            'visitante': equipoVisitante
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
                nuevo_partido = {
                    'local': equipoLocal,
                    'bonusA': bonusA,
                    'resultadoA': resultadoA,
                    'resultadoB': resultadoB,
                    'bonusB': bonusB,
                    'visitante': equipoVisitante
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
            # Actualizar los datos del partido
            partido['local'] = local
            partido['resultadoA'] = resultadoA
            partido['resultadoB'] = resultadoB
            partido['visitante'] = visitante
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
# Crear la clasificación para el GrupoA y GrupoB de El Salvador
def generar_clasificacion_grupoA_grupoB(data11, total_partidos_temporada_grupos_salvador):
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
    grupoA = clasificacion_ordenada[:6]
    grupoB = clasificacion_ordenada[6:12]
    return grupoA, grupoB
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
    grupoA, grupoB = generar_clasificacion_grupoA_grupoB(data11, total_partidos_temporada_grupos_salvador)
    
    return render_template('equipos_rugby/clasi_analis_salvador.html', clasificacion_analisis_salvador=clasificacion_analisis_salvador, grupoA=grupoA, grupoB=grupoB)
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
        nuevo_partido = {
            #'id': id_nuevo,
            'local': equipoLocal,
            'bonusA': bonusA,
            'resultadoA': resultadoA,
            'resultadoB': resultadoB,
            'bonusB': bonusB,
            'visitante': equipoVisitante
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
                nuevo_partido = {
                    'local': equipoLocal,
                    'bonusA': bonusA,
                    'resultadoA': resultadoA,
                    'resultadoB': resultadoB,
                    'bonusB': bonusB,
                    'visitante': equipoVisitante
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
            # Actualizar los datos del partido
            partido['local'] = local
            partido['resultadoA'] = resultadoA
            partido['resultadoB'] = resultadoB
            partido['visitante'] = visitante
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
# Crear la clasificación para el GrupoA y GrupoB del VRAC
def generar_clasificacion_grupoA_grupoB(data12, total_partidos_temporada_grupos_vrac):
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
    grupoA = clasificacion_ordenada[:6]
    grupoB = clasificacion_ordenada[6:12]
    return grupoA, grupoB
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
    grupoA, grupoB = generar_clasificacion_grupoA_grupoB(data12, total_partidos_temporada_grupos_vrac)
    return render_template('equipos_rugby/clasi_analis_vrac.html', clasificacion_analisis_vrac=clasificacion_analisis_vrac, grupoA=grupoA, grupoB=grupoB)
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
        nuevo_partido = {
            #'id': id_nuevo,
            'local': equipoLocal,
            'bonusA': bonusA,
            'resultadoA': resultadoA,
            'resultadoB': resultadoB,
            'bonusB': bonusB,
            'visitante': equipoVisitante
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
                nuevo_partido = {
                    'local': equipoLocal,
                    'bonusA': bonusA,
                    'resultadoA': resultadoA,
                    'resultadoB': resultadoB,
                    'bonusB': bonusB,
                    'visitante': equipoVisitante
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
            # Actualizar los datos del partido
            partido['local'] = local
            partido['resultadoA'] = resultadoA
            partido['resultadoB'] = resultadoB
            partido['visitante'] = visitante
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
        nuevo_partido = {
            #'id': id_nuevo,
            'local': equipoLocal,
            'bonusA': bonusA,
            'resultadoA': resultadoA,
            'resultadoB': resultadoB,
            'bonusB': bonusB,
            'visitante': equipoVisitante
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
                nuevo_partido = {
                    'local': equipoLocal,
                    'bonusA': bonusA,
                    'resultadoA': resultadoA,
                    'resultadoB': resultadoB,
                    'bonusB': bonusB,
                    'visitante': equipoVisitante
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
            # Actualizar los datos del partido
            partido['local'] = local
            partido['resultadoA'] = resultadoA
            partido['resultadoB'] = resultadoB
            partido['visitante'] = visitante
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
        nuevo_partido = {
            #'id': id_nuevo,
            'local': equipoLocal,
            'bonusA': bonusA,
            'resultadoA': resultadoA,
            'resultadoB': resultadoB,
            'bonusB': bonusB,
            'visitante': equipoVisitante
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
                nuevo_partido = {
                    'local': equipoLocal,
                    'bonusA': bonusA,
                    'resultadoA': resultadoA,
                    'resultadoB': resultadoB,
                    'bonusB': bonusB,
                    'visitante': equipoVisitante
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
            # Actualizar los datos del partido
            partido['local'] = local
            partido['resultadoA'] = resultadoA
            partido['resultadoB'] = resultadoB
            partido['visitante'] = visitante
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














    
if __name__ == '__main__':
    app.secret_key = 'pinchellave'
    app.run(debug=True)