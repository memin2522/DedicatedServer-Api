import os
import json
import logging

from flask import request, send_file
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from werkzeug.utils import secure_filename
from utils.json_utils import save_dict_to_json, get_upload_folder, get_file_path

from collections import defaultdict
from schemas import ServerSchema

blp = Blueprint("server", __name__, description="Dedicated Server")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


info_dict = defaultdict(dict) 

@blp.route("/server/<string:game_id>/<string:player_id>")
class Server(MethodView):
    @blp.response(200, ServerSchema)
    def get(self, game_id, player_id):
        try:
            if game_id not in info_dict:
                return {"message": "Game not found"}, 404
            if player_id not in info_dict[game_id]:
                return {"message": "Player not found in this game"}, 404
                
            requested_info = info_dict[game_id][player_id]
            return requested_info
        except Exception as e:
            return {"error": str(e)}, 500

    
    @blp.arguments(ServerSchema, location="json")
    def post(self, media_data, game_id, player_id):
        """Store media data for a specific game and player"""
        # Initialize nested dictionaries if they don't exist
        if game_id not in info_dict:
            info_dict[game_id] = {}
        
        info_dict[game_id][player_id] = media_data
        
        return {
            "message": "Data stored successfully",
            "game_id": game_id,
            "player_id": player_id,
            "data": media_data
        }, 201
        