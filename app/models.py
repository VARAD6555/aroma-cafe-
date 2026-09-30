from datetime import datetime
from decimal import Decimal
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import db

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class CafeTable(db.Model):
    __tablename__ = "cafe_tables"
    id = db.Column(db.Integer, primary_key=True)
    table_number = db.Column(db.String(20), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

class MenuItem(db.Model):
    __tablename__ = "menu_items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(50), nullable=False, index=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    rating = db.Column(db.Numeric(3, 1), default=0)
    reviews = db.Column(db.Integer, default=0)
    image = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    gallery = db.relationship("MenuImage", backref="menu_item", cascade="all, delete-orphan")
    addons = db.relationship("Addon", backref="menu_item", cascade="all, delete-orphan")

class MenuImage(db.Model):
    __tablename__ = "menu_images"
    id = db.Column(db.Integer, primary_key=True)
    menu_item_id = db.Column(db.Integer, db.ForeignKey("menu_items.id"), nullable=False)
    image_url = db.Column(db.Text, nullable=False)
    sort_order = db.Column(db.Integer, default=0)

class Addon(db.Model):
    __tablename__ = "addons"
    id = db.Column(db.Integer, primary_key=True)
    menu_item_id = db.Column(db.Integer, db.ForeignKey("menu_items.id"), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)

class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(30), unique=True, nullable=False, index=True)
    table_id = db.Column(db.Integer, db.ForeignKey("cafe_tables.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    status = db.Column(db.String(30), default="pending", nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    tax = db.Column(db.Numeric(10, 2), nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    special_instructions = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    table = db.relationship("CafeTable")
    user = db.relationship("User")
    items = db.relationship("OrderItem", backref="order", cascade="all, delete-orphan")

class OrderItem(db.Model):
    __tablename__ = "order_items"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey("menu_items.id"), nullable=False)
    item_name = db.Column(db.String(150), nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    instructions = db.Column(db.Text)
    menu_item = db.relationship("MenuItem")
    addons = db.relationship("OrderItemAddon", backref="order_item", cascade="all, delete-orphan")

class OrderItemAddon(db.Model):
    __tablename__ = "order_item_addons"
    id = db.Column(db.Integer, primary_key=True)
    order_item_id = db.Column(db.Integer, db.ForeignKey("order_items.id"), nullable=False)
    addon_id = db.Column(db.Integer, db.ForeignKey("addons.id"), nullable=False)
    addon_name = db.Column(db.String(150), nullable=False)
    addon_price = db.Column(db.Numeric(10, 2), nullable=False)

class Feedback(db.Model):
    __tablename__ = "feedback"
    id = db.Column(db.Integer, primary_key=True)
    table_id = db.Column(db.Integer, db.ForeignKey("cafe_tables.id"), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    table = db.relationship("CafeTable")

class WaiterRequest(db.Model):
    __tablename__ = "waiter_requests"
    id = db.Column(db.Integer, primary_key=True)
    table_id = db.Column(db.Integer, db.ForeignKey("cafe_tables.id"), nullable=False)
    status = db.Column(db.String(30), default="pending", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    table = db.relationship("CafeTable")

class BillRequest(db.Model):
    __tablename__ = "bill_requests"
    id = db.Column(db.Integer, primary_key=True)
    table_id = db.Column(db.Integer, db.ForeignKey("cafe_tables.id"), nullable=False)
    status = db.Column(db.String(30), default="pending", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    table = db.relationship("CafeTable")
