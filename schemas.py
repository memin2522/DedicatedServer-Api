from marshmallow import Schema, fields
from datetime import datetime
import enum

#User Schemas
class ServerSchema(Schema):
    id_game = fields.Int(dump_only=True)
    posX = fields.Int(required=True)
    posY = fields.Int(required=True)
    posZ = fields.Int(required=True)

