from marshmallow import Schema, fields
from datetime import datetime
import enum

#User Schemas
class ServerSchema(Schema):
    posX = fields.Float(required=True)
    posY = fields.Float(required=True)
    posZ = fields.Float(required=True)

