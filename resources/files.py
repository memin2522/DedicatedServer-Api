import os
import json

from flask import request, send_file
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from werkzeug.utils import secure_filename
from utils.json_utils import save_dict_to_json, get_upload_folder, get_file_path

from no_relational_schemas import MediaStorageSchema

blp = Blueprint("files", __name__, description="Operations on Files")

@blp.route("/files")
class FileUpload(MethodView):
    @blp.arguments(MediaStorageSchema, location="form")
    def post(self, media_data):
        if 'file' not in request.files:
            abort(400, message="No se encontró ningún archivo en la solicitud.")

        file = request.files['file']
        if file.filename == '':
            abort(400, message="No se seleccionó ningún archivo.")
        try:
            filename = secure_filename(media_data["fileName"])
            file_path = os.path.join(get_upload_folder(), filename)

            save_dict_to_json(media_data, "file_info.json")
            file.save(file_path)

            return {
                "message": f"Archivo {filename} guardado exitosamente.",
                "fileName": filename,
                "hallId": media_data["hallId"],
                "markId": media_data["markId"],
                "mediaExtension": media_data["mediaExtension"],
                "entryType": media_data["entryType"],
                "mediaType": media_data["mediaType"],
                "filePath": file_path
            }, 200

        except Exception as e:
            abort(500, message=f"Error al guardar el archivo: {str(e)}")

@blp.route("/files/<string:file_id>")
class FileDownload(MethodView):
    def get(self, file_id):
        file_info_path = get_file_path("file_info.json")

        if not os.path.exists(file_info_path):
            abort(500, message="Archivo de metadatos no encontrado.")

        with open(file_info_path, "r", encoding="utf-8") as f:
            metadata_dict = json.load(f)

        if file_id not in metadata_dict:
            abort(404, message=f"Metadatos no encontrados para el archivo.")

        metadata = metadata_dict[file_id]
        file_name = metadata.get("fileName")

        if not file_name:
            abort(404, message="Nombre de archivo no encontrado en metadatos.")

        file_path = os.path.join(get_upload_folder(), secure_filename(file_name))

        if not os.path.exists(file_path):
            abort(404, message="Archivo no encontrado.")

        response = send_file(file_path, as_attachment=True, download_name=file_name)

        for key, value in metadata.items():
            response.headers[key] = str(value)

        return response

@blp.route("/files/<string:hall_id>/<string:mark_id>")
class FileInfo(MethodView):
    @blp.response(200, MediaStorageSchema(many=True))
    def get(self, hall_id, mark_id):
        file_info_path = get_file_path("file_info.json")

        if not os.path.exists(file_info_path):
            abort(500, message="Archivo de metadatos no encontrado.")

        with open(file_info_path, "r", encoding="utf-8") as f:
            metadata_dict = json.load(f)

        matching_metadata = []
        for file_name, metadata in metadata_dict.items():
            if metadata.get("hallId") == hall_id and metadata.get("markId") == mark_id:
                metadata["file_name"] = file_name
                matching_metadata.append(metadata)

        if not matching_metadata:
            abort(404, message="No se encontraron archivos con el hallID y markID proporcionados.")

        return matching_metadata

