from datetime import datetime
from . import db

class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Constructor
    def __init__(self, email, password_hash, name, role='student'):
        self.email = email
        self.password_hash = password_hash
        self.name = name
        self.role = role

    # CRUD functions can be implemented via SQLAlchemy basic methods like db.session.add(user)
    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.get(user_id)
        
    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
