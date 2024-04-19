import json,os
from saleapp import app,db
from saleapp.models import category,product,User
import hashlib

def read_json(path):
   with open(path,'r') as f:
       return json.load(f)

def load_categories():
    return category.query.all()

def load_product(cate_id=None,kw=None,from_price=None,to_price=None,page=1):
    # products = read_json(os.path.join(app.root_path,'data/products.json'))
    #
    # if cate_id:
    #     products = [p for p in products if p['category_id'] == int(cate_id)]
    #
    # if kw:
    #     products = [p for p in products if p['name'].lower().find(kw.lower()) >= 0]
    #
    # if from_price:
    #     products = [p for p in products if p['price'] >= float(from_price)]
    #
    # if to_price:
    #     products = [p for p in products if p['price'] <= float(to_price)]
    products = product.query.filter(product.active.__eq__(True))

    if cate_id :
        products = products.filter(product.category_id.__eq__(cate_id))

    if kw:
        products = products.filter(product.name.contains(kw))

    if from_price:
        products = products.filter(product.price.__ge__(from_price))

    if to_price:
        products = products.filter(product.price.__le__(to_price))

    page_size = int(app.config['PAGE_SIZE'])
    start = (page-1)*page_size
    end = start + page_size

    return products.slice(start,end).all()


def get_product_by_id(product_id):
    return product.query.get(product_id)

    # products = read_json(os.path.join(app.root_path,'data/products.json'))
    #
    # for p in products:
    #     if p['id'] == product_id:
    #         return p

def count_products():
    return product.query.filter(product.active.__eq__(True)).count()


def add_user(name,username,password,email,**kwargs):

    with app.app_context():
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        user = User(name=name.strip(),username=username.strip(),password=password,email=email,avatar=kwargs.get('avatar'))

        db.session.add(user)
        db.session.commit()

def check_login(username,password):

    if username and password:

        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return User.query.filter(User.username == username and User.password == password).first()

def get_user_by_id(user_id):
    return User.query.get(user_id)