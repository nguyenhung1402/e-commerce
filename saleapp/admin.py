from sqlalchemy import inspect

from  saleapp import app,db,utils
from flask import redirect,request
from flask_admin import Admin,BaseView,expose,AdminIndexView
from saleapp.models import category, product,UserRole
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user,logout_user
from datetime import datetime, date


class AuthenticatedModelView(ModelView):
     def is_accessible(self):
          return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN
class ProductView(ModelView):
     can_view_details = True
     # column_labels = {
     #      'name':'Ten san pham',
     #      'price':'Gia',
     #      'image':'Anh dai dien',
     #      'category_id':'Danh phum',
     #
     # }
     column_list = [c_attr.key for c_attr in inspect(product).mapper.column_attrs]
     column_hide_backrefs = False
     def is_accessible(self):
          return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN
class CategoryView(ModelView):
     column_display_pk = True # optional, but I like to see the IDs in the list
     column_hide_backrefs = False
     def is_accessible(self):
          return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

class LogoutView(BaseView):

     @expose('/')
     def index(self):
          logout_user()
          return redirect('/admin')

     def is_accessible(self):
          return current_user.is_authenticated

class MyAdminIndexView(AdminIndexView):
     @expose('/')
     def index(self):
          return self.render('admin/index.html',
                             stats=utils.category_stats())


class StatsView(BaseView):
     @expose('/')
     def index(self):
          kw = request.args.get('kw')
          from_date = request.args.get('from_date')
          to_date = request.args.get('to_date')
          year = request.args.get('year',datetime.now().year)

          return self.render('admin/stats.html',
                             month_stats = utils.product_month_stats(year = year),
                             stats=utils.product_stats(kw=kw,from_date=from_date,to_date=to_date))
     def is_accessible(self):
          return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

admin = Admin(app=app, name='Adminstration', template_mode='bootstrap4', index_view=MyAdminIndexView())
admin.add_view(AuthenticatedModelView(category,db.session))
admin.add_view(ProductView(product,db.session))
admin.add_view(LogoutView(name='logout'))
admin.add_view(StatsView(name='Stats'))
