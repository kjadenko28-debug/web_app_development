from datetime import datetime
from . import db

class MenuItem(db.Model):
    __tablename__ = 'menu_item'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    shop_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    is_available = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, shop_id, name, price, description=None, is_available=True):
        self.shop_id = shop_id
        self.name = name
        self.price = price
        self.description = description
        self.is_available = is_available

    @classmethod
    def get_by_shop_id(cls, shop_id):
        return cls.query.filter_by(shop_id=shop_id).all()
