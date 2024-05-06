import math

from flask import render_template, request, redirect, url_for, session,jsonify
from saleapp import  app,login
import utils
import cloudinary.uploader
from flask_login import login_user,logout_user, login_required
from  saleapp.models import UserRole
@app.route('/')
def home():


    cate_id=request.args.get('category_id')
    kw=request.args.get('keyword')
    page = request.args.get('page',1)
    counter = utils.count_products()
    products = utils.load_product(cate_id=cate_id,kw=kw, page=int(page))

    return render_template('index.html',
                           products=products,
                           pages = math.ceil(counter/app.config['PAGE_SIZE']))

@app.route('/products')
def product_list():
    products = utils.load_product()
    print(products)
    cate_id = request.args.get('category_id')
    kw = request.args.get('keyword')
    from_price = request.args.get('from_price')
    to_price = request.args.get('to_price')

    products=utils.load_product(cate_id=cate_id, kw=kw , from_price=from_price, to_price=to_price)

    return render_template('products.html',products=products)


@app.route('/products/<int:product_id>')
def product_detail(product_id):
    product = utils.get_product_by_id(product_id)
    comments = utils.get_comments(product_id=product_id,page= int(request.args.get('page',1)))

    return  render_template('product_detail.html',
                            comments=comments,
                            product=product,
                            pages = math.ceil(utils.count_comments(product_id=product_id)/app.config['COMMENT_SIZE']))

@app.route('/register',methods=['GET','POST'])
def user_register():

    error = ""
    if request.method == 'POST':
        name = request.form.get('name')
        # print(request.form)
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        confirm = request.form.get('confirm')
        avatar_path = None
        try:
            if password.strip().__eq__(confirm.strip()):
                avatar = request.files.get('avatar')
                # print(avatar)
                if avatar:
                    res = cloudinary.uploader.upload(avatar)
                    # print(res)
                    avatar_path = res['secure_url']
                    # print(avatar_path)

                utils.add_user(name=name,username=username,password=password,email=email,avatar=avatar_path)
                return redirect(url_for('home'))
            else:
                error = "Mat khau khong khop"
        except Exception as e:
            error = 'He thong dang co loi '+str(e)


    return render_template('register.html',error=error)


#cho moi trang deu duoc co thong tin de cho thang header
@app.context_processor
def common_response():
    return{
        'categories': utils.load_categories(),
        'cart_start': utils.count_cart(session.get('cart'))
    }

@app.route('/login',methods=['GET','POST'])
def user_sigin():
    err=''
    try:
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            user = utils.check_login(username=username,password=password)

            if user:
                login_user(user=user)
                next = request.args.get('next','home')

                return redirect(url_for(next))

            else:
                err='Tai khoan hoac mat khau khong dung'
    except Exception as e:
        err='He thong dang co loi '+str(e)

    return render_template('login.html',error=err)

@app.route('/admin-login',methods=['POST'])
def admin_sigin():
    err=''
    try:
        username = request.form.get('username')
        password = request.form.get('password')

        user = utils.check_login(username=username,password=password, role=UserRole.ADMIN)

        if user:
            login_user(user=user)
    except Exception as e:
        err = 'He thong dang co loi '+str(e)
    print(err)
    return redirect('/admin')



@login.user_loader
def user_load(user_id):
    return utils.get_user_by_id(user_id=user_id)


@app.route('/logout')
def user_signout():
    logout_user()
    return redirect(url_for('user_sigin'))
@app.route('/api/add-cart',methods=['POST'])
def add_to_cart():
    data = request.json
    id = str(data.get('id'))
    name = str(data.get('name'))
    price = str(data.get('price'))

    cart = session.get('cart')
    print(session)
    if not cart:
        cart = {}

    if id in cart:
        cart[id]['quantity'] += 1
    else:
        cart[id] = {
            'id' : id,
            'name' : name,
            'price' : price,
            'quantity' : 1,
        }

    session['cart'] = cart

    return jsonify(utils.count_cart(cart))


@app.route('/api/update-cart',methods=['PUT'])
def update_cart():
    data = request.json

    id = str(data.get('id'))
    quantity = int(data.get('quantity'))
    cart = session.get('cart')

    if cart and id in cart:
        cart[id]['quantity'] = quantity
        session['cart'] = cart

    return jsonify(utils.count_cart(cart))

@app.route('/api/delete-cart/<product_id>',methods=['DELETE'])
def delete_cart(product_id):
    cart = session.get('cart')
    if cart and product_id in cart:
        del cart[product_id]
        session['cart'] = cart

    return jsonify(utils.count_cart(cart))

@app.route('/cart')
def cart():
    return render_template('cart.html',starts = utils.count_cart(session.get('cart')))

@app.route('/api/pay',methods=['POST'])
@login_required
def pay():
    try:
        utils.add_reipt(session.get('cart'))
        del session['cart']
    except:
        return jsonify({'code': 400})

    return jsonify({'code': 200})

@app.route('/api/comments',methods=['POST'])
@login_required
def add_comment():
    data = request.json
    content = data.get('content')
    product_id = str(data.get('product_id'))

    try:
        c = utils.add_comment(content=content, product_id=product_id)
        # print('a')
    except:
        # print('b')
        return {'status': 404, 'err_msg': 'Bi loi!!'}

    # print('c')
    # print(c)
    return {'status': 201, 'comment': {
        'content': c.content,
        'id': c.id,
        'created_date': c.created_date,
        'user': {
            'username': current_user.username,
            'avatar': current_user.avatar

        }
    }}


if __name__ == '__main__':
    from saleapp.admin import *
    app.run(debug=True)
