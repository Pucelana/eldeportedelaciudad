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

# Ruta sección de clasificación y ánalisis del Fundaión Aliados 
@app.route('/equipos_basket/clasif_analisis_aliados')
def clasif_analisis_aliados():
    return render_template('equipos_basket/clasif_analisis_aliados.html')

# Ruta calendario Fundación Aliados
@app.route('/equipos_basket/calendario_aliados')
def calendario_aliados():
    return render_template('equipos_basket/calendario_aliados.html')  

# Ruta calendario y resultados R.Valladolid
@app.route('/equipos_futbol/calend_resul_vallad')
def calend_resul_vallad():
    return render_template('equipos_futbol/calend_resul_vallad.html')

# Ruta clasificación y analisis R.Valladolid
@app.route('/equipos_futbol/clasi_analis_vallad')
def clasi_analis_vallad():
    return render_template('equipos_futbol/clasi_analis_vallad.html')

# Ruta calendario y resultados V Simancas
@app.route('/equipos_futbol/calend_resul_siman')
def calend_resul_siman():
    return render_template('equipos_futbol/calend_resul_siman.html')

# Ruta clasificación y analisis V Simancas
@app.route('/equipos_futbol/clasi_analis_siman')
def clasi_analis_siman():
    return render_template('equipos_futbol/clasi_analis_siman.html')

# Ruta calendario y resultados Promesas
@app.route('/equipos_futbol/calend_resul_prome')
def calend_resul_prome():
    return render_template('equipos_futbol/calend_resul_prome.html')

# Ruta clasificación y analisis Promesas
@app.route('/equipos_futbol/clasi_analis_prome')
def clasi_analis_prome():
    return render_template('equipos_futbol/clasi_analis_prome.html')

#Todo el proceso de calendario y clasificación del UEMC
# Rutas de partidos UEMC
part_uemc = 'json/partidos_uemc.json'
def guardar_datos(data):
    # Guardar los datos en el archivo JSON
    with open(part_uemc, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)
def obtener_datos():
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
    data = obtener_datos()
    print(data)
    return render_template('admin/calend_uemc.html', data=data)
# Ingresar los resultados de los partidos UEMC
@app.route('/admin/crear_calendario', methods=['POST'])
def ingresar_resultado():
    data = obtener_datos()
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
        
    guardar_datos(data)
    return redirect(url_for('calendarios_uemc'))

# Toma la lista de los resultados y los guarda
def guardar_partidos_en_archivo(data):
    arch_guardar = 'json/partidos_uemc.json'
    # Guardar en el archivo
    with open(arch_guardar, 'w', encoding='UTF-8') as archivo:
        json.dump(data, archivo)
# Modificar los partidos de cada jornada
@app.route('/modificar_jornada/<string:id>', methods=['POST'])
def modificar_jornada(id):
    data = obtener_datos()
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
            guardar_partidos_en_archivo(data)            
            return redirect(url_for('calendarios_uemc'))
    return redirect(url_for('calendarios_uemc'))

# Ruta para borrar jornadas
@app.route('/eliminar_jornada/<string:id>', methods=['POST'])
def eliminar_jornada(id):
    data = obtener_datos()
    jornada_a_eliminar = [j for j in data if j['id'] != id]  # Filtrar las jornadas diferentes de la que se va a eliminar
    guardar_partidos_en_archivo(jornada_a_eliminar)
    # Redirigir a la página de encuentros_uemc (o a donde desees después de eliminar)
    return redirect(url_for('calendarios_uemc'))

# Crear la clasificación UEMC
def generar_clasificacion_analisis_baloncesto(data, total_partidos_temporada):
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
    print(generar_clasificacion_analisis_baloncesto)
    return clasificacion_ordenada

# Ruta para mostrar la clasificación y análisis del UEMC
@app.route('/equipos_basket/clasif_analisis_uemc/')
def clasif_analisis_uemc():
    data = obtener_datos()
    total_partidos_temporada = 34
    # Llama a la función para generar la clasificación y análisis
    clasificacion_analisis = generar_clasificacion_analisis_baloncesto(data, total_partidos_temporada)
    # Ordena la clasificación por puntos y diferencia de canastas
    clasificacion_analisis = sorted(clasificacion_analisis, key=lambda x: (x['datos']['ganados'], x['datos']['diferencia_canastas']), reverse=True)
    # Calcular la proximidad
    #proximidad = calcular_proximidad(data, clasificacion_analisis, total_partidos_temporada)
    return render_template('equipos_basket/clasif_analisis_uemc.html', clasificacion_analisis=clasificacion_analisis)

# Ruta y creación del calendario individual del UEMC
@app.route('/equipos_basket/calendario_uemc')
def calendario_uemc():
    datos = obtener_datos()
    nuevos_datos = [dato for dato in datos if dato]
    equipo_uemc = 'UEMC Real Valladolid'
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
    return render_template('equipos_basket/calendario_uemc.html', tabla_partidos_uemc=tabla_partidos_uemc, nuevos_datos=nuevos_datos)  
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
    print(generar_clasificacion_analisis_baloncesto_ponce)
    return clasificacion_ordenada

# Ruta para mostrar la clasificación y análisis del Ponce
@app.route('/equipos_basket/clasif_analisis_ponce/')
def clasif_analisis_ponce():
    data1 = obtener_datos_ponce()
    total_partidos_temporada_ponce = 34
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
                    tabla_partidos_ponce[equipo_contrario]['jornadas'][jornada['nombre']]['rol_uemc'] = rol_ponce
                  else:
                    tabla_partidos_ponce[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_ponce[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_ponce[equipo_contrario]['jornadas'][jornada['nombre']]['rol_uemc'] = rol_ponce
                else:
                  if not tabla_partidos_ponce[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA']:
                    tabla_partidos_ponce[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_ponce[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_ponce[equipo_contrario]['jornadas'][jornada['nombre']]['rol_uemc'] = rol_ponce
                  else:
                    tabla_partidos_ponce[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                    tabla_partidos_ponce[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                    tabla_partidos_ponce[equipo_contrario]['jornadas'][jornada['nombre']]['rol_uemc'] = rol_ponce
    return render_template('equipos_basket/calendario_ponce.html', tabla_partidos_ponce=tabla_partidos_ponce, nuevos_datos_ponce=nuevos_datos_ponce) 
# Fin proceso Ponce Valladolid



if __name__ == '__main__':
    app.secret_key = 'pinchellave'
    app.run(debug=True)
 
 