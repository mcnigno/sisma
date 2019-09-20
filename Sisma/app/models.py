from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from flask_appbuilder.models.mixins import AuditMixin
from sqlalchemy import Table


"""

You can use the extra Flask-AppBuilder fields and Mixin's

AuditMixin will add automatic timestamp of created and modified by who


"""
class Datasource(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    connection = Column(String(255), nullable=False)

    def __repr__(self):
        return self.name


class Template(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    template = Column(Text, nullable=False)

    def __repr__(self):
        return self.name

class Query(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    query = Column(Text, nullable=False)
    
    datasource_id = Column(Integer, ForeignKey('datasource.id'))
    datasource = relationship(Datasource)

    def __repr__(self):
        return self.name

class Mailgroup(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

    def __repr__(self):
        return self.name

assoc_mailgroup_mailuser = Table('mailgroup_mailuser', Model.metadata,
                                      Column('id', Integer, primary_key=True),
                                      Column('mailgruop_id', Integer, ForeignKey('mailgroup.id')),
                                      Column('mailuser_id', Integer, ForeignKey('mailuser.id'))
)

class Mailuser(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)

    mailgroups = relationship('Mailgroup', secondary=assoc_mailgroup_mailuser, backref='UserList')

    def __repr__(self):
        return self.name

class Report(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    schedule = Column(String(255), nullable=False)

    datasource_id = Column(Integer, ForeignKey('datasource.id'))
    datasource = relationship(Datasource)

    query_id = Column(Integer, ForeignKey('query.id'))
    query = relationship(Query)

    template_id = Column(Integer, ForeignKey('template.id'))
    template = relationship(Template)

    status = Column(Boolean, default=False)

    def __repr__(self):
        return self.name