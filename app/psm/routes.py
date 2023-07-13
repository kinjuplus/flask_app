import pandas as pd
from flask import Blueprint, render_template, request, Response, jsonify, json
from app import db
from app.psm.models import Project, Employee, ConstantSetting, UserRole
from sqlalchemy import select,exc
from sqlalchemy.orm import joinedload, DeclarativeMeta



psm = Blueprint('psm', __name__)


@psm.route('/createConstant', methods=['POST'])
def createConstant():
    try:
        content = request.json
        setting = ConstantSetting(
            constant_key=content['constant_key'],
            constant_value=content['constant_value'],
        )
        db.session.add(setting)
        db.session.commit()
        return jsonify(
            errorCode='00',
            errorMsg=''
        )
    except exc.SQLAlchemyError:
        return jsonify(
            errorCode='01',
            errorMsg=''
        )
    except:
        return jsonify(
            errorCode='99',
            errorMsg=''
        )


@psm.route('/queryProjects', methods=['GET','POST'])
def queryProjects():
    if request.method == 'POST':
        content = request.json
        condition = {}
        if 'state' in content:
            condition['state'] = content['state']
        else:
            condition['state'] = None
        if 'product_id' in content:
            condition['product_id'] = content['product_id']
        else:
            condition['product_id'] = None    
        querySql = '''
        SELECT *
        FROM psm_gantt_project p
        WHERE 1 = 1 
        and (:state is null or p.project_state = :state)
        and (:product_id is null or p.product_id = :product_id)
        '''
        result = pd.read_sql(sql = querySql, con=db.get_engine('psm'), params= condition)
    else:        
        result = pd.read_sql(sql = "select * from psm_gantt_project p where p.project_state='OPEN'", con=db.get_engine('psm'))
    
    return Response(result.to_json(orient="records", force_ascii=False), mimetype='application/json')

@psm.route('/queryProjectByParams')
def queryProjectByParams():
    state = request.args.get('status')
    product_id = request.args.get('product_id')
    sqlResult = db.session.query(Project).join(Employee, Project.owner).filter(Employee.name== "沈建慶")
    #sqlResult = db.session.query(Project).filter(Project.owner.has( Employee.name== "沈建慶"))
    result = []
    for row in sqlResult:
       result.append(row.to_dict())
    json_string = json.dumps(result,ensure_ascii = False)
    return Response(json_string,content_type="application/json; charset=utf-8" )

@psm.route('/api/employees/queryEmpByEmpNo')
def queryEmpByEmpNo():
    empNo = request.args.get('empNo')
    sqlResult = db.session.query(Employee).filter(Employee.emp_no == empNo)
  
    result = []
    for row in sqlResult:
        result.append(row.to_dict())
    
    json_string = json.dumps(result,ensure_ascii = False)
    return Response(json_string,content_type="application/json; charset=utf-8" )

@psm.route('/api/employees/findEmployeeByKeyword')
def findEmployeeByKeyword():
    keyword = request.args.get('keyword')
    sqlResult = db.session.query(Employee).filter(Employee.emp_no.like('%'+keyword+'%') | Employee.name.like('%'+keyword+'%') | Employee.e_mail.like('%'+keyword+'%') | Employee.emp_no.like('%'+keyword+'%'))
  
    result = []
    for row in sqlResult:
        result.append(row.to_dict())
    
    json_string = json.dumps(result,ensure_ascii = False)
    return Response(json_string,content_type="application/json; charset=utf-8" )


@psm.route('/api/constants/<constantKey>')
def queryConstantByKey(constantKey):
    sqlResult = db.session.query(ConstantSetting).get(constantKey)
    json_string = json.dumps(sqlResult.to_dict(),ensure_ascii = False)
    return Response(json_string,content_type="application/json; charset=utf-8" )

def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d
