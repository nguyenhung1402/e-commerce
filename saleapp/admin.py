from  saleapp import app,db

from flask_admin import Admin
from saleapp.models import category, product
from flask_admin.contrib.sqla import ModelView

admin = Admin(app=app, name='Adminstration', template_mode='bootstrap4')


class ProductView(ModelView):
     can_view_details = True
     column_labels = {
          'name':'Ten san pham',
          'price':'Gia',
          'image':'Anh dai dien',
          'category_id':'Danh phum',

     }
     column_display_pk = True # optional, but I like to see the IDs in the list
     column_hide_backrefs = False

class CategoryView(ModelView):
     column_display_pk = True # optional, but I like to see the IDs in the list
     column_hide_backrefs = False
admin.add_view(CategoryView(category,db.session))
admin.add_view(ProductView(product,db.session))