from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date, DateTime, Enum, Float
from sqlalchemy.orm import relationship,joinedload
from saleapp import db
from datetime import datetime
from saleapp import  app
from enum import Enum as UserEnum
from flask_login import UserMixin

class BaseModel(db.Model):
    #khong tao bang nay
    __abstract__ = True
    id = Column(Integer, primary_key=True,autoincrement=True)

#ke thua thang basemodel
class category(BaseModel):
    __tablename__ = 'category'


    name = Column(String(20), nullable=False)
    products = relationship('product', backref='category')

    def __str__(self):
        return self.name



class product(BaseModel):
    __tablename__ = 'product'

    name = Column(String(50), nullable=False)
    description = Column(String(250))
    price = Column(Integer, default=0)
    image = Column(String(100))
    active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.now())
    #'' thi phai la ten cua bang du lieu tablename con khong thi ten class
    category_id = Column(Integer,ForeignKey(category.id),nullable=True,default=1 )
    receipts_details = relationship('ReceiptDetails',backref='prodcut',lazy=True)
    comments = relationship('Comment',backref='product',lazy=True)
    def __str__(self):
        return self.name


class UserRole(UserEnum):
    ADMIN = 1
    USER = 2

class User(BaseModel,UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False,unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100))
    email = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    joined_date = Column(DateTime, default=datetime.now())
    user_role = Column(Enum(UserRole),default=UserRole.USER)
    receipts = relationship('Receipt',backref='user',lazy=True)
    user_comments = relationship('Comment',backref='comment_user_backref',lazy= True)
    def __str__(self):
        return self.name


class Receipt(BaseModel):
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer,ForeignKey(User.id),nullable=False)
    datails = relationship('ReceiptDetails',backref='receipt',lazy=True)

class ReceiptDetails(db.Model):
    receipt_id = Column(Integer,ForeignKey('receipt.id'),nullable=False,primary_key=True)
    product_id = Column(Integer,ForeignKey('product.id'),nullable=False,primary_key=True)
    quantity = Column(Integer,default=0)
    unit_price = Column(Float,default=0)

class Comment(BaseModel):
    content = Column(String(250), nullable=False)
    product_id = Column(Integer,ForeignKey('product.id'),nullable=False)
    user_id = Column(Integer,ForeignKey(User.id),nullable=False)
    created_date = Column(DateTime, default=datetime.now())
    comment_user = relationship("User", backref='user_comments_backref', lazy='joined')
    def __str__(self):
        return self.content

if __name__ == '__main__':
     with app.app_context():
         db.create_all()



