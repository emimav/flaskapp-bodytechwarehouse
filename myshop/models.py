from datetime import datetime
from myshop import app, db, login_manager

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from sqlalchemy.orm import backref


# All user information in one User model
class User(db.Model, UserMixin):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)

    # User authentification details
    username = db.Column(db.String(15), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    # User Email information
    email = db.Column(db.String(120), unique=True, nullable=False)

    # User information
    is_active = db.Column(db.Boolean(), nullable=False, default=True)
    is_admin = db.Column(db.Boolean(), nullable=False, default=False)
    first_name = db.Column(db.String(50), nullable=False, default='')
    last_name = db.Column(db.String(50), nullable=False, default='')

    # review = db.relationship('Review', backref=backref('user', lazy='dynamic'))
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Enquiry(db.Model):
    __tablename__ = 'Enquiry'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), nullable=False)
    content = db.Column(db.String(300), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Enquiry('{self.content}')"


class Item(db.Model):
    __tablename__ = "Item"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000), nullable=False)
    description = db.Column(db.String(5000), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock_level = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
                            nullable=False)
    category = db.relationship('Category',
                               backref=db.backref('item', lazy=True))
    images = db.relationship('Image', backref='item', lazy='dynamic')
    colors = db.relationship('Color', backref='item', lazy='dynamic')
    sizes = db.relationship('Size', backref='item', lazy='dynamic')
    cartitem = db.relationship('CartItem', backref='item_id', lazy='dynamic')

"""
    def __repr__(self):
        return f"Item('{self.title}', '{self.description}', '{self.price}', '{self.stock_level}')"
"""

class Image(db.Model):
    __tablename__ = "Image"
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(200), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('Item.id'),
                        nullable=False)

    def __repr__(self):
        return self.url


class Color(db.Model):
        __tablename__ = "Color"
        id = db.Column(db.Integer, primary_key=True)
        color = db.Column(db.String(50), nullable=False)
        item_id = db.Column(db.Integer, db.ForeignKey('Item.id'),
                            nullable=False)

        def __repr__(self):
            return self.color


class Size(db.Model):
    __tablename__ = "Size"
    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.String(50), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('Item.id'),
                        nullable=False)

    def __repr__(self):
        return '{}'.format(self.size)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '{}'.format(self.name)


class ReviewItem(db.Model):
    __tablename__ = "Review"
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    item = db.Column(db.Integer, db.ForeignKey("Item.id"), nullable=False)
    content = db.Column(db.String(300), nullable=False)
    rating = db.String(db.String(10))
    timestamp = db.Column(db.String(50))

    def __repr__(self):
        return '<Review {}>'.format(self.content)

class CartItem(db.Model):
    __tablename__ = "CartItem"
    id = db.Column(db.Integer, primary_key=True)
    cart = db.Column(db.Integer, db.ForeignKey("Cart.id"), nullable=False)
    item = db.Column(db.Integer, db.ForeignKey("Item.id"), nullable=False)
    quantity = db.Column(db.Integer, default=0)


class Cart(db.Model):
    __tablename__ = "Cart"
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
     # items = db.relationship('item', secondary="Cart Item", backref='cart', lazy='dynamic')
    cartItems = db.relationship('CartItem', backref='Cart', primaryjoin=id == CartItem.cart)
    last_update = db.Column(db.DateTime)


    def __repr__(self):
        return f"User('{self.name}', '{self.last_update}')"


class Order(db.Model):
    __tablename__ = "Order"
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    total = db.Column(db.Float, nullable=False)
    order_date = db.Column(db.DateTime)

    def __repr__(self):
        return f"Order('{self.name}', '{self.total}', '{self.order_date}')"


class OrderItem(db.Model):
    __tablename = "OrderItem"
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.Integer, db.ForeignKey("Item.id"))
    quantity = db.Column(db.Integer)
    item_price = db.Column(db.Float)

    def __repr__(self):
        return f"Item('{self.item}', '{self.item_price}', '{self.quantity}')"


class BillingInformation(db.Model):
    __tablename__ = "BillingInformation"
    id = db.Column(db.Integer, primary_key=True)
    credit_card_num = db.Column('credit_card_num', db.Integer(), nullable=False)
    bill_date = db.Column('bill_date', db.Date, nullable=False)
    billing_addr = db.Column('billing_addr', db.String(120), nullable=False)
    credit_card_expiry = db.Column("credit_card_expiry", db.Date, nullable=False)
    first_name = db.Column(db.String(50), nullable=False, default='')
    last_name = db.Column(db.String(50), nullable=False, default='')
    user = db.Column('user', db.Integer, db.ForeignKey('User.id'))

    def __repr__(self):
        return f"Item('{self.first_name}', '{self.last_name}', '{self.user}', {self.billing_addr })"
