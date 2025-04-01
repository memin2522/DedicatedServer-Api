import os
import uuid
import json
import logging

# Configurar logging (si aún no está configurado en el script)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


BASE_DIR = os.path.abspath(os.path.dirname(__file__))  
PROJECT_DIR = os.path.dirname(BASE_DIR)  
UPLOAD_FOLDER = os.path.join(PROJECT_DIR, 'uploads') 

def get_upload_folder():
    return UPLOAD_FOLDER

def get_file_path(dict_name):
    return os.path.join(get_upload_folder(), dict_name)

def save_dict_to_json(data, dict_name, save_with_id= True):
    FILE_PATH = get_file_path(dict_name)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    try:

        if os.path.exists(FILE_PATH) and os.path.getsize(FILE_PATH) > 0:
            with open(FILE_PATH, 'r', encoding='utf-8') as json_file:
                try:
                    file_info = json.load(json_file)
                    logger.info("Archivo existente cargado correctamente.")
                except json.JSONDecodeError:
                    logger.warning(f"El archivo {FILE_PATH} está corrupto o vacío. Se sobrescribirá.")
                    file_info = {} 
        else:
            file_info = {}
        
        if save_with_id:
            file_id = str(uuid.uuid4())
            file_info[file_id] = data
        else:
            file_info = data

        with open(FILE_PATH, 'w', encoding='utf-8') as json_file:
            json.dump(file_info, json_file, indent=4, ensure_ascii=False)

        return True

    except Exception as e:
        logger.error(f"Error al guardar JSON en {FILE_PATH}: {str(e)}", exc_info=True)
        return False
    
def load_dict_info(dict_name):
    FILE_PATH = os.path.join(get_upload_folder(), dict_name)
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)
    return {}