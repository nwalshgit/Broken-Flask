# https://scotch.io/tutorials/build-a-crud-web-app-with-python-and-flask-part-one

# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager

class Employee(UserMixin, db.Model):
    """Create an Emploee table"""
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash= db.Column(db.String(128))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """Prevent password from being accessed"""
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """Set password to a hashed password"""
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """Check if hashed password matches actual password"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Employee: {}>'.format(self.username)

# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))

class Department(db.Model):
    """Create a Department table"""
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='department', lazy='dynamic')

    def __repr__(self):
        return '<Department: {}>'.format(self.name)

class Role(db.Model):
    """Create a Role table"""
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='role', lazy='dynamic')
    
    def __repr__(self):
        return '<Role: {}>'.format(self.name)

class Unit(db.Model):
    """Create a Unit table"""
    __tablename__ = 'units'
    unit = db.Column(db.String(7), primary_key=True)
    unit_type = db.Column(db.String(1))
    def __repr__(self):
        return '<Unit: {}>'.format(self.unit)

class Area(db.Model):
    """Create an Area table"""
    __tablename__ = 'areas'
    id = db.Column(db.Integer, primary_key=True)
    area = db.Column(db.String(31), unique=True)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    listorder = db.Column(db.Integer)
    def __repr__(self):
        return '<Area: {}>'.format(self.area)

class Location(UserMixin, db.Model):
    """Create a Location table"""
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(31), index=True, unique=True)
    areas = db.relationship('Area', backref='location', lazy='dynamic')
    def __repr__(self):
        return '<Location: {}>'.format(self.location)

class Item(db.Model):
    """Create an Item table"""
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(63)) 
    manufacturer = db.Column(db.String(31)) 
    default_unit = db.Column(db.String(7), db.ForeignKey('units.unit'))
    #default_size = db.Column(db.Decimal(5,2))
    default_size = db.Column(db.Integer)
    print("models.py:Item.default_size is integer but should be decimal(5,2)")
    qty_needed = db.Column(db.Integer)
    print("models.py:Item.qty_needed is integer but should be decimal(5,2)")
    def __repr__(self):
        return '<Item: {}>'.format(self.item)

class ItemLocation(db.Model):
    """Create an ItemLocation table"""
    __tablename__ = 'item_location'
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), primary_key=True)
    area_id = db.Column(db.Integer, db.ForeignKey('areas.id'), primary_key=True)
    def __repr__(self):
        return '<Item: {}>'.format(self.item_id)+'<Location: {}>'.format(self.location_id)+'<Area: {}>'.format(self.area_id)


