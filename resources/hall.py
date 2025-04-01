import os
import json
import logging

from flask import request, send_file
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from werkzeug.utils import secure_filename
from utils.json_utils import save_dict_to_json, get_upload_folder, get_file_path

from schemas import ServerSchema

blp = Blueprint("server", __name__, description="Dedicated Server")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@blp.route("/server/<string:game_id>")
class Server(MethodView):
    @blp.response(200, )
    def get(self):
        hall_info_path = get_file_path("hall_info.json")


        if not os.path.exists(hall_info_path):
            abort(500, message="Archivo de metadatos no encontrado.")

        try:
            with open(hall_info_path, "r") as f:
                if f.readable():
                    content = f.read().strip()  # Elimina espacios vacíos
                    if not content:
                        raise ValueError("El archivo JSON está vacío")
                    metadata_dict = json.loads(content)
                else:
                    raise IOError("No se puede leer el archivo JSON")
        except (json.JSONDecodeError, ValueError) as e:
            print("Error al cargar el JSON:", e)
            metadata_dict = {}  # O un valor por defecto

        return metadata_dict
    
    @blp.arguments(HallSchema, location="json")
    def post(self, media_data):
        save_dict_to_json(media_data, "hall_info.json", False)

        return {
            "message": f"Archivo hall_info.json guardado exitosamente.",
        }, 200

        