
from app import db
from time import time
from flask import current_app
from sqlalchemy import Integer, String, Column, ForeignKey, DateTime, BigInteger
from sqlalchemy.orm import relationship, Mapped, mapped_column, backref
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declared_attr

class ZxNpdpPlan(db.Model):
    __bind_key__ = 'plmde'
    __tablename__ = 'zx_npdp_plan'
    product_id = db.Column(db.String, primary_key=True)
    application = db.Column(db.String)
    bd = db.Column(db.String)
    model_name = db.Column(db.String)