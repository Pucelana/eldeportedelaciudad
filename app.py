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
# Ingresar los resultados de los partidos del CD Parquesol
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
        resultados_a_modificar = next((result for result in data6 if result['id'] == id), None)
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
    equipo_aula = 'Aula Valladolid'
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








        
if __name__ == '__main__':
    app.secret_key = 'pinchellave'
    app.run(debug=True)
 
 