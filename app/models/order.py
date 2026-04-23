from datetime import datetime
from . import db

class Order(db.Model):
    __tablename__ = 'order'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    shop_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='pending')
    pickup_time = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    items = db.relationship('OrderItem', backref='order', lazy=True)

    def __init__(self, student_id, shop_id, total_price, pickup_time=None):
        self.student_id = student_id
        self.shop_id = shop_id
        self.total_price = total_price
        self.pickup_time = pickup_time

    @classmethod
    def get_by_student(cls, student_id):
        return cls.query.filter_by(student_id=student_id).all()
        
    @classmethod
    def get_by_shop(cls, shop_id):
        return cls.query.filter_by(shop_id=shop_id).all()

class OrderItem(db.Model):
    __tablename__ = 'order_item'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_item.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)

    def __init__(self, order_id, menu_item_id, quantity, unit_price):
        self.order_id = order_id
        self.menu_item_id = menu_item_id
        self.quantity = quantity
        self.unit_price = unit_price
