import json,os
from saleapp import app,db
from saleapp.models import category,product,User,Receipt,ReceiptDetails,UserRole,Comment
import hashlib
from flask_login import current_user
from sqlalchemy import func
from sqlalchemy.sql import extract
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

def check_login(username,password,role=UserRole.USER ):


    if username and password:

        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return User.query.filter(User.username.__eq__(username.strip()),User.password.__eq__(password),User.user_role.__eq__(role)).first()

def get_user_by_id(user_id):
    return User.query.get(user_id)

def count_cart(cart):
    total_quantity ,total_amount = 0,0

    if cart:
        for c in cart.values():
            total_quantity += c['quantity']
            total_amount += c['quantity']*int(c['price'])


    return {
        'total_quantity':total_quantity,
        'total_amount':total_amount
    }


def add_reipt(cart):
    with app.app_context():
        if cart:
            receipt = Receipt(user=current_user)
            print("a"+str(receipt))
            db.session.add(receipt)
            print(cart.values())

            for c in cart.values():
                d = ReceiptDetails(receipt=receipt,product_id=c['id'],quantity=c['quantity'],unit_price=c['price'])
                print(d)
                db.session.add(d)

            db.session.commit()


def category_stats():
    '''
    select c.id,c.name count(p.id)
    from category c left outer join product p on p.category_id=c.id
    group by c.id,c.name

    '''
    with app.app_context():
    #     return category.query.join(product,product.category_id.__eq__(category.id),isouter=True).add_columns(func.count(product.id)).group_by(category.id,category.name).all()

        return db.session.query(category.id,category.name,func.count(product.id))\
            .join(product,category.id.__eq__(product.category_id),isouter=True).group_by(category.id,category.name).all()

def product_stats(kw = None , from_date = None,to_date = None):
    with app.app_context():
        p = db.session.query(product.id, product.name, func.sum(ReceiptDetails.quantity * ReceiptDetails.unit_price))\
            .join(ReceiptDetails, ReceiptDetails.product_id.__eq__(product.id),isouter=True)\
            .join(Receipt,Receipt.id.__eq__(ReceiptDetails.receipt_id))\
            .group_by(product.id, product.name)

        if kw:
            p = p.filter(product.name.contains(kw))

        if from_date:
            p = p.filter(Receipt.created_date.__ge__(from_date))

        if to_date:
            p = p.filter(Receipt.created_date.__le__(to_date))

        return p.all()

def product_month_stats(year):
    with app.app_context():
        return db.session.query(extract('month',Receipt.created_date),func.sum(ReceiptDetails.quantity*ReceiptDetails.unit_price)).join(ReceiptDetails,ReceiptDetails.receipt_id.__eq__(Receipt.id)).filter(extract('year',Receipt.created_date) == year).group_by(extract('month',Receipt.created_date)).order_by(extract('month',Receipt.created_date)).all()


def add_comment(content, product_id):
    with app.app_context():
        comment = Comment(content=content,product_id=product_id,user_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        print(comment)
        return comment

def get_comments(product_id,page=1):
    with app.app_context():
        page_size = app.config.get('COMMENT_SIZE')
        start = (page - 1) * page_size

        return db.session.query(Comment).filter(Comment.product_id.__eq__(product_id)).order_by(-Comment.id).slice(start,start+page_size).all()

def count_comments(product_id):
    with app.app_context():
        return db.session.query(Comment).filter(Comment.product_id.__eq__(product_id)).count()