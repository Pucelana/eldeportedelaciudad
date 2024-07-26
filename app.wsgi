import sys
import logging

# Configurar el directorio del proyecto
import os
from pathlib import Path
project_path = Path(__file__).resolve().parent
sys.path.insert(0, str(project_path))

# Configurar la aplicación
from myapp import app as application

# Configurar logging (opcional)
logging.basicConfig(level=logging.INFO)

# Definir la variable WSGI
application = application