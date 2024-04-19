import math

from flask import render_template,request,redirect,url_for
from saleapp import  app,login
import utils
import cloudinary.uploader
from flask_login import login_user,logout_user
@app.route('/')
def home():


    cate_id=request.args.get('category_id')
    kw=request.args.get('keyword')
    page = request.args.get('page',1)
    counter = utils.count_products()
    products = utils.load_product(cate_id=cate_id,kw=kw, page=int(page))

    return render_template('index.html',products=products,pages = math.ceil(counter/app.config['PAGE_SIZE']))

@app.route('/products')
def product_list():
    products = utils.load_product()

    cate_id = request.args.get('category_id')
    kw = request.args.get('keyword')
    from_price = request.args.get('from_price')
    to_price = request.args.get('to_price')

    products=utils.load_product(cate_id=cate_id, kw=kw , from_price=from_price, to_price=to_price)

    return render_template('products.html',products=products)


@app.route('/products/<int:product_id>')
def product_detail(product_id):
    product = utils.get_product_by_id(product_id)

    return  render_template('product_detail.html',product=product)

@app.route('/register',methods=['GET','POST'])
def user_register():

    error = ""
    if request.method == 'POST':
        name = request.form.get('name')
        print(request.form)
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        confirm = request.form.get('confirm')
        avatar_path = None
        try:
            if password.strip()==(confirm.strip()):
                avatar = request.files.get('avatar')
                if avatar:
                    res = cloudinary.uploader.upload(avatar)
                    avatar_path = res['secure_url']
                utils.add_user(name=name,username=username,password=password,email=email,avatar=avatar_path)
                return redirect(url_for('home'))
            else:
                error = "Mat khau khong khop"
        except Exception as e:
            error = 'He thong dang co loi '+str(e)


    return render_template('register.html',error=error)

@app.context_processor
def common_response():
    return{
        'categories': utils.load_categories(),
    }

@app.route('/login',methods=['GET','POST'])
def user_sigin():
    err=''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = utils.check_login(username=username,password=password)

        if user:
            login_user(user=user)
            return redirect(url_for('home'))

        else:
            err='Tai khoan hoac mat khau khong dung'

    return render_template('login.html',error=err)

@login.user_loader
def user_load(user_id):
    return utils.get_user_by_id(user_id=user_id)


@app.route('/logout')
def user_signout():
    logout_user()
    return redirect(url_for('user_sigin'))

if __name__ == '__main__':
    from saleapp.admin import *
    app.run(debug=True)
