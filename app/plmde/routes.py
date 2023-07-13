import pandas as pd
from flask import Blueprint, render_template, request, Response
from app import db
from app.plmde.models import ZxNpdpPlan
from sqlalchemy import select

plmde = Blueprint('plmde', __name__)



@plmde.route('/plmde/queryProjectByParams')
def queryProjectByParams():
    
    product_id = request.args.get('product_id')
    sqlResult = db.session.query(ZxNpdpPlan).filter(ZxNpdpPlan.product_id== "GDD101IA0160S")
    #sqlResult = db.session.query(Project).filter(Project.owner.has( Employee.name== "沈建慶"))
    result = []
    for row in sqlResult:
       result.append(row2dict(row))
    return result


def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d