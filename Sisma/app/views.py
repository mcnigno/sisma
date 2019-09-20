from flask import render_template, redirect
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView, ModelRestApi, BaseView
from .models import Mailgroup, Mailuser, Query, Template, Report, Datasource

from . import appbuilder, db
from flask_appbuilder import expose, has_access, action
from .helpers import query

"""
    Create your Model based REST API::

    class MyModelApi(ModelRestApi):
        datamodel = SQLAInterface(MyModel)

    appbuilder.add_api(MyModelApi)


    Create your Views::


    class MyModelView(ModelView):
        datamodel = SQLAInterface(MyModel)


    Next, register your Views::


    appbuilder.add_view(
        MyModelView,
        "My View",
        icon="fa-folder-open-o",
        category="My Category",
        category_icon='fa-envelope'
    )
"""
class DataSourceView(ModelView):
        datamodel = SQLAInterface(Datasource)
        add_columns = ['name','connection']
        list_columns = ['name']


class MailGroupView(ModelView):
        datamodel = SQLAInterface(Mailgroup)
        add_columns = ['name']
        list_columns = ['name']

class MailUserView(ModelView):
        datamodel = SQLAInterface(Mailuser)
        add_columns = ['name','email', 'mailgroups']
        list_columns = ['name','email', 'mailgroups']
        

class ReportView(ModelView):

    datamodel = SQLAInterface(Report) 
    add_columns = ['name','datasource','query','template','description','schedule']
    list_columns = ['name']

    @action("report","Do something on this record","Do you really want to?","fa-rocket")
    def report(self, item):
        con = item.datasource.connection
        sqlquery = item.query.query
        data = query(con,sqlquery)


        """
            do something with the item record
        """
        return render_template('table.html', data=data)

class TemplateView(ModelView):
    datamodel = SQLAInterface(Template)
    add_columns = ['name','template']
    list_columns = ['name','template']

class QueryView(ModelView):
    datamodel = SQLAInterface(Query)
    add_columns = ['name', 'query']
    list_columns = ['name','query']


class MyView(BaseView):

    default_view = 'method1'

    @expose('/method1/')
    @has_access
    def method1(self):
        # do something with param1
        # and return to previous page or index
        data = ['a','b','c']
        return render_template('table.html', data=data)

    @expose('/method2/<string:param1>')
    @has_access
    def method2(self, param1):
        # do something with param1
        # and render template with param
        param1 = 'Goodbye %s' % (param1)
        return param1
    

appbuilder.add_view(MyView, "Method1", category='My View')
appbuilder.add_link("Method2", href='/myview/method2/john', category='My View')

"""
    Application wide 404 error handler
"""
appbuilder.add_view(DataSourceView, "Datasource", icon="fa-folder-open-o", category="My Category", category_icon='fa-envelope')

appbuilder.add_view(MailGroupView, "Mail Group", icon="fa-folder-open-o", category="My Category", category_icon='fa-envelope')
appbuilder.add_view(MailUserView, "Mail User", icon="fa-folder-open-o", category="My Category", category_icon='fa-envelope')
appbuilder.add_view(TemplateView, "Template", icon="fa-folder-open-o", category="My Category", category_icon='fa-envelope')
appbuilder.add_view(QueryView, "Query", icon="fa-folder-open-o", category="My Category", category_icon='fa-envelope')
appbuilder.add_view(ReportView, "Report", icon="fa-folder-open-o", category="My Category", category_icon='fa-envelope')


@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "404.html", base_template=appbuilder.base_template, appbuilder=appbuilder
        ),
        404,
    )


db.create_all()
