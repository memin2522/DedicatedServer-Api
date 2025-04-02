from marshmallow import Schema, fields
from datetime import datetime
import enum

#User Schemas
class ServerSchema(Schema):
    posX = fields.Int(required=True)
    posY = fields.Int(required=True)
    posZ = fields.Int(required=True)

