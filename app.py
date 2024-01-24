from flask import Flask
from flask import render_template, request, redirect,url_for, session
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
def cargar_resultados_desde_archivo():
    archivo_resultados = 'json/horarios.json'

    if os.path.exists(archivo_resultados):
        with open(archivo_resultados, 'r') as archivo:
            return json.load(archivo)
    else:
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
    
    guardar_resultados_en_archivo(resultados)
    
    return redirect(url_for('pub_marcadores'))

# Toma la lista de los resultados y los guarda
def guardar_resultados_en_archivo(resultados):
    # Ruta del archivo donde guardar los resultados
    archivo_resultados = 'json/horarios.json'
    # Guardar en el archivo
    with open(archivo_resultados, 'w') as archivo:
        json.dump(resultados, archivo)        

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
            guardar_resultados_en_archivo(resultados)
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

# Ruta sección de clasificación y ánalisis del Ponce Valladolid 
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

# Rutas de partidos UEMC
part_uemc = 'json/partidos_uemc.json'
def guardar_datos(data):
    # Guardar los datos en el archivo JSON
    with open(part_uemc, 'w') as file:
        json.dump(data, file, indent=4)
def obtener_datos():
    try:
    # Leer los datos desde el archivo JSON
      with open(part_uemc, 'r') as file:
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
    return render_template('admin/calendario_uemc.html', data=data)
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
    with open(arch_guardar, 'w') as archivo:
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

# Generar Clasificación y Análisis para Baloncesto
def generar_clasificacion_analisis_baloncesto(data, total_partidos_temporada):
    clasificacion = defaultdict(lambda: {'jugados': 0, 'ganados': 0, 'perdidos': 0, 'favor': 0, 'contra': 0, 'diferencia_canastas': 0, 'puntos': 0})
    print(clasificacion)
    for jornada in data:
        for partido in jornada['partidos']:
            equipo_local = partido['local']
            resultado_local = int(partido['resultadoA'])
            resultado_visitante = int(partido['resultadoB'])
            equipo_visitante = partido['visitante']

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

    return clasificacion_ordenada

# Ruta para mostrar la clasificación y análisis del UEMC
@app.route('/equipos_basket/clasif_analisis_uemc/')
def clasif_analisis_uemc():
    data = obtener_datos()
    total_partidos_temporada = 34
    # Llama a la función para generar la clasificación y análisis
    clasificacion_analisis = generar_clasificacion_analisis_baloncesto(data, total_partidos_temporada)
    # Ordena la clasificación por puntos y diferencia de canastas
    clasificacion_analisis = sorted(clasificacion_analisis, key=lambda x: (x['datos']['puntos'], x['datos']['diferencia_canastas']), reverse=True)
    return render_template('equipos_basket/clasif_analisis_uemc.html', clasificacion_analisis=clasificacion_analisis)

# Calcular proximidad al ascenso
def calcular_proximidad(partidos_jugados, victorias_actuales, total_partidos_temporada,data):
    proximidad_porcentaje = (victorias_actuales / partidos_jugados) * 100
    partidos_restantes = total_partidos_temporada - partidos_jugados
    victorias_posibles = victorias_actuales + partidos_restantes
    victorias_optimistas = victorias_posibles + partidos_restantes
    victorias_pesimistas = victorias_actuales
    return {
        'proximidad_porcentaje': proximidad_porcentaje,
        'partidos_restantes': partidos_restantes,
        'victorias_posibles': victorias_posibles,
        'victorias_optimistas': victorias_optimistas,
        'victorias_pesimistas': victorias_pesimistas
    }

# Ruta para la proximidad al ascenso
@app.route('/equipos_basket/analisis_uemc/')
def proximidad_ascenso():
    total_partidos_temporada = 34
    data = obtener_datos() 
    # Llama a la función para generar la clasificación y análisis
    clasificacion_analisis = generar_clasificacion_analisis_baloncesto(data, total_partidos_temporada)
    proximidad_info = []

    for equipo_info in clasificacion_analisis:
        equipo_local = equipo_info['equipo']
        datos_equipo = equipo_info['datos']

        # Descomenta esta línea
        proximidad_info.append({
            'equipo': equipo_local,
            'proximidad': calcular_proximidad(datos_equipo['jugados'], datos_equipo['ganados'], total_partidos_temporada)
        })
        print(proximidad_info)

    return render_template('equipos_basket/clasif_analisis_uemc.html', proximidad_info=proximidad_info, clasificacion_analisis=clasificacion_analisis)









    

    
    


    
            

    


          

            






if __name__ == '__main__':
    app.secret_key = 'pinchellave'
    app.run(debug=True)
 
 