from  sqlalchemy import Column, Integer, String,ForeignKey, Boolean, Date, DateTime,Enum
from sqlalchemy.orm import relationship
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

    def __str__(self):
        return self.name




if __name__ == '__main__':
     with app.app_context():
         db.create_all()

    # c1 = category(name='Dien thoai')
    # c2 = category(name='May tinh bang')
    # c3 = category(name='Dong ho thong minh')
    #
    # with app.app_context():
    #     db.session.add(c1)
    #     db.session.add(c2)
    #     db.session.add(c3)
    #     db.session.commit()
    # products = [{
    #     "id": 1,
    #     "name": "iPhone 7 Plus",
    #     "description": "Apple, 32GB, RAM: 3GB, iOS13",
    #     "price": 17000000,
    #     "image":"images/p1.png",
    #     "category_id": 1
    # }, {
    #     "id": 2,
    #     "name": "iPad Pro 2020",
    #     "description": "Apple, 128GB, RAM: 6GB",
    #     "price": 37000000,
    #     "image":"images/p2.png",
    #     "category_id": 2
    # }, {
    #     "id": 3,
    #     "name": "Galaxy Note 10 Plus",
    #     "description": "Samsung, 64GB, RAML: 6GB",
    #     "price": 24000000,
    #     "image":"images/p3.png",
    #     "category_id": 1
    # }]
    # with app.app_context():
    #     for p in products:
    #         pro = product(name=p['name'],price=p['price'],image=p['image'],category_id=p['category_id'],description=p['description'])
    #
    #
    #         db.session.add(pro)
    #         print(pro.price)
    #
    #
    #     db.session.commit()

