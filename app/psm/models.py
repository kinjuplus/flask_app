
from app import db
from time import time
from flask import current_app
from sqlalchemy import Integer, String, Column, ForeignKey, DateTime, BigInteger
from sqlalchemy.orm import relationship, Mapped, mapped_column, backref
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declared_attr
from dataclasses import dataclass
from marshmallow_sqlalchemy import ModelConversionError, SQLAlchemyAutoSchema
from sqlalchemy import event
from sqlalchemy.orm import mapper
from typing import List
from sqlalchemy_serializer import SerializerMixin


    
class AuditableMixin(object):
    creation_date = Column(DateTime, default=func.now())
    last_modified_date = Column(DateTime, default=func.now())
    @declared_attr
    def created_by(cls):
        return Column(String, ForeignKey('Employee.emp_no'))
    @declared_attr
    def last_modified_by(cls):
        return Column(String, ForeignKey('Employee.emp_no'))


class Project(AuditableMixin,db.Model,SerializerMixin):
    __bind_key__ = 'psm'
    __tablename__ = 'psm_gantt_project'
    
    serialize_only = ('product_id', 'model_name', 'bu', 'application','mapp_chat_sn','product_classification','owner','phase','work_time','project_type','product_group','project_state','template','projectOwnerDisplay','last_modified_date')
    
    product_id = db.Column(db.String, primary_key=True)
    model_name = db.Column(db.String, nullable=False)
    bu = db.Column(db.String, nullable=False)
    application = db.Column(db.String, nullable=False)
    mapp_chat_sn = db.Column(db.String)
    product_classification = db.Column(db.String)
    project_owner = Column(String, ForeignKey('Employee.emp_no'))
    owner: Mapped["Employee"] = relationship("Employee", uselist=False, foreign_keys=[project_owner], primaryjoin="and_(Employee.emp_no==Project.project_owner)")
    
    phase = db.Column(db.String)
    work_time = db.Column(db.String)
    project_type = db.Column(db.String)
    product_group = db.Column(db.String)
    project_state = db.Column(db.String)
    template_id = Column(BigInteger, ForeignKey('ProjectTemplate.id'))
    template: Mapped["ProjectTemplate"] = relationship("ProjectTemplate", uselist=False, foreign_keys=[template_id], primaryjoin="and_(ProjectTemplate.id==Project.template_id)" )
    
    def projectOwnerDisplay(self):
        return self.owner.name +'('+self.owner.emp_no+')'

@dataclass
class Employee(db.Model,SerializerMixin):
    __bind_key__ = 'psm'
    __tablename__ = 'hr_emp_reorg'

    serialize_only = ('emp_no', 'name', 'sex', 'e_mail','dept_no','manager_id','location','ext_no','per_state','real_dept_name','ad_account','mail_to','roles')
    emp_no = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    sex = db.Column(db.String)
    e_mail = db.Column(db.String)
    dept_no = db.Column(db.String)
    manager_id = db.Column(db.String)
    location = db.Column(db.String)
    ext_no = db.Column(db.String)
    per_state = db.Column(db.String)
    real_dept_name = db.Column(db.String)
    ad_account = db.Column(db.String)
    mail_to = db.Column(db.String)
    roles: Mapped[List["UserRole"]] = relationship(
        'UserRole',
        primaryjoin='Employee.emp_no == UserRole.user_id',
        back_populates='user',
        foreign_keys='UserRole.user_id'
    )
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

@dataclass
class UserRole(db.Model,SerializerMixin):
    __bind_key__ = 'psm'
    __tablename__ = 'psm_user_role'

    serialize_only = ('id', 'role_id','user_id')
    id = db.Column(db.String, primary_key=True)
    role_id = db.Column(db.String)
    user_id = db.Column(db.String, db.ForeignKey('user.emp_no'), nullable=False)
    user = relationship(
        'Employee',
        primaryjoin='UserRole.user_id == Employee.emp_no',
        back_populates='roles',
        foreign_keys=user_id
    )
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class ProjectTemplate(AuditableMixin,db.Model,SerializerMixin):
    __bind_key__ = 'psm'
    __tablename__ = 'psm_gantt_template'
    serialize_only = ('id', 'name','description','application')
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    application = db.Column(db.String)

class ConstantSetting(db.Model,SerializerMixin):
    __bind_key__ = 'psm'
    __tablename__ = 'psm_constant_setting'
    constant_key = db.Column(db.String, primary_key=True)
    constant_value = db.Column(db.String)

