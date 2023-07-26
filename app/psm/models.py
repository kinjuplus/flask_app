
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
from datetime import datetime
import re

    
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
    
    serialize_only = ('product_id', 'model_name', 'bu', 'application','mapp_chat_sn','product_classification','owner','phase','work_time','project_type','product_group','project_state','template','projectOwnerDisplay','last_modified_date','memberRoleList','taskList','assignments')
    
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
    
    memberRoleList: Mapped[List["ProjectMemberRole"]] = relationship(
        'ProjectMemberRole',
        primaryjoin='Project.product_id == ProjectMemberRole.product_id',
        back_populates='project',
        foreign_keys='ProjectMemberRole.product_id'
    )

    taskList: Mapped[List["ProjectTask"]] = relationship(
        'ProjectTask',
        primaryjoin='Project.product_id == ProjectTask.product_id',
        back_populates='project',
        foreign_keys='ProjectTask.product_id'
    )

    assignments: Mapped[List["ProjectAssignment"]] = relationship(
        'ProjectAssignment',
        primaryjoin='Project.product_id == ProjectAssignment.product_id',
        back_populates='project',
        foreign_keys='ProjectAssignment.product_id'
    )

    def projectOwnerDisplay(self):
        return self.owner.name +'('+self.owner.emp_no+')'


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

class ProjectTask(AuditableMixin,db.Model,SerializerMixin):
    __bind_key__ = 'psm'
    __tablename__ = 'psm_gantt_project_task'

    serialize_only = ('id','name','description','duration','start_date','end_date','actual_start_date','actual_end_date','effort','effort_unit',
                      'duration_unit','percent_done','scheduling_mode','note','manually_scheduled','effort_driven','expanded',
                      'actual_start_confirm','actual_end_confirm','constraint_type','constraint_date','ems_doc_no','key_word','children','getDisplayColor')

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    duration = db.Column(db.Numeric)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    actual_start_date = db.Column(db.DateTime)
    actual_end_date = db.Column(db.DateTime)
    effort = db.Column(db.Numeric)
    effort_unit = db.Column(db.String, default='hour')
    duration_unit = db.Column(db.String, default='day')
    percent_done = db.Column(db.Numeric, default=0)
    scheduling_mode = db.Column(db.String)
    note = db.Column(db.String)
    manually_scheduled = db.Column(db.Boolean, default=False)
    effort_driven = db.Column(db.Boolean, default=False)
    expanded = db.Column(db.Boolean)
    actual_start_confirm = db.Column(db.Boolean, default=False)
    actual_end_confirm = db.Column(db.Boolean, default=False)
    constraint_type = db.Column(db.String)
    constraint_date = db.Column(db.DateTime)
    ems_doc_no = db.Column(db.String)
    key_word = db.Column(db.String)
    parent_id = mapped_column(BigInteger, ForeignKey("psm_gantt_project_task.id"))
    children = relationship("ProjectTask", back_populates="parent")
    parent = relationship("ProjectTask", back_populates="children", remote_side=[id])
    product_id = db.Column(db.String, db.ForeignKey('project.product_id'), nullable=False)
    project = relationship(
        'Project',
        primaryjoin='ProjectTask.product_id == Project.product_id',
        back_populates='taskList',
        foreign_keys=product_id
    )

    def getDisplayColor(self):
        if(self.project.project_state and self.project.project_state != 'OPEN'):
            return ''
        if(self.actual_end_date is not None or self.parent is None or re.search("^DR\d{1}$", self.name) or self.children is None or self.children == []):
            return ''
        current_dateTime = datetime.now()
        if(self.end_date is not None):
            difference = self.end_date - current_dateTime
            if (self.actual_end_date is None and (difference.days >= 0 and difference.days <=3) and (self.actual_end_confirm is None or  not self.actual_end_confirm) ):
                return 'yellow'
            if(difference.days < 0 and self.actual_end_date is None):
                return 'red'
            if(self.actual_end_date is not None):
                return ''

        if(self.start_date is not None):
            difference = self.start_date - current_dateTime
            if(difference.days >=0 and self.actual_start_date is None and  difference.days <=3):
                return 'yellow'
            if(difference.days < 0 and self.actual_start_date is None):
                return 'red'
            if(self.actual_start_date is not None):
                if(self.actual_start_date > self.start_date and (self.actual_start_confirm is None or not self.actual_start_confirm)):
                    return 'yellow'
                if(self.actual_start_date <= self.start_date and (self.actual_start_confirm is None or not self.actual_start_confirm)):
                    return 'blue'
            if(self.actual_start_confirm is not None and self.actual_start_confirm):
                return ''
        return ''


class ProjectMemberRole(AuditableMixin,db.Model,SerializerMixin):
    __bind_key__ = 'psm'
    __tablename__ = 'psm_gantt_project_role'
    serialize_only = ('id', 'name','product_id','memberList')
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    product_id = db.Column(db.String, db.ForeignKey('project.product_id'), nullable=False)
    project = relationship(
        'Project',
        primaryjoin='ProjectMemberRole.product_id == Project.product_id',
        back_populates='memberRoleList',
        foreign_keys=product_id
    )
    memberList: Mapped[List["ProjectMember"]] = relationship(
        'ProjectMember',
        primaryjoin='ProjectMemberRole.id == ProjectMember.role_id',
        back_populates='role',
        foreign_keys='ProjectMember.role_id'
    )


class ProjectMember(AuditableMixin,db.Model,SerializerMixin):
    __bind_key__ = 'psm'
    __tablename__ = 'psm_gantt_project_member'
    serialize_only = ('id', 'employee')
    id = db.Column(db.String, primary_key=True)
    emp_no = db.Column(db.String, db.ForeignKey('employee.emp_no'), nullable=False)
    employee = relationship(
        'Employee',
        primaryjoin='ProjectMember.emp_no == Employee.emp_no',
        foreign_keys=emp_no
    )
    role_id = db.Column(db.String, db.ForeignKey('role.id'), nullable=False)
    role = relationship(
        'ProjectMemberRole',
        primaryjoin='ProjectMemberRole.id == ProjectMember.role_id',
        back_populates='memberList',
        foreign_keys=role_id
    )

class ProjectAssignment(db.Model,SerializerMixin):
    __bind_key__ = 'psm'
    __tablename__ = 'psm_gantt_project_assignment'
    serialize_only = ('id', 'units','member','task')
    id = db.Column(db.BigInteger, primary_key=True)
    units = db.Column(db.Integer)
    product_id = db.Column(db.String, db.ForeignKey('project.product_id'), nullable=False)
    project = relationship(
        'Project',
        primaryjoin='Project.product_id == ProjectAssignment.product_id',
        back_populates='assignments',
        foreign_keys=product_id
    )
    member_id = db.Column(db.BigInteger, db.ForeignKey('member.id'), nullable=False)
    member = relationship(
        'ProjectMember',
        primaryjoin='ProjectMember.id == ProjectAssignment.member_id',
        foreign_keys=member_id
    )
    task_id = db.Column(db.BigInteger, db.ForeignKey('task.id'), nullable=False)
    task = relationship(
        'ProjectTask',
        primaryjoin='ProjectTask.id == ProjectAssignment.task_id',
        foreign_keys=task_id
    )
    


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

