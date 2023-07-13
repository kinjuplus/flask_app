from config import config
from flask import Flask
from flask_assets import Environment, Bundle
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelConversionError, SQLAlchemyAutoSchema
from sqlalchemy import event
from sqlalchemy.orm import mapper
from json import JSONEncoder
import datetime 

db = SQLAlchemy()


class CustomJSONEncoder(JSONEncoder):
  "Add support for serializing timedeltas"

  def default(o):
    if type(o) == datetime.timedelta:
      return str(o)
    if type(o) == datetime.datetime:
      return o.isoformat()
    return super().default(o)

def create_app(config_name='development'):
    """For to use dynamic environment"""
    global security
    app = Flask(__name__)
    assets = Environment(app)
    app.config.from_object(config[config_name])
    app.config['JSON_AS_ASCII'] = False
    db.init_app(app)

    from app.psm.routes import psm
    app.register_blueprint(psm)

    from app.plmde.routes import plmde
    app.register_blueprint(plmde)
    
    app.json_encoder = CustomJSONEncoder
    
    return app
