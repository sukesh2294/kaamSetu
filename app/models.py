from .extensions import db
from datetime import datetime


class OTPVerification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=True)
    password_hash = db.Column(db.String(128), nullable=True)
    email = db.Column(db.String(120), nullable=False)
    otp = db.Column(db.String(6), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_used = db.Column(db.Boolean, default=False)
    temp_face_encoding = db.Column(db.Text, nullable=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), default="user")  # user / worker
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Worker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    skill = db.Column(db.String(100))
    location = db.Column(db.String(100))
    price_per_hour = db.Column(db.Float)
    is_verified = db.Column(db.Boolean, default=False)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    worker_id = db.Column(db.Integer, db.ForeignKey("worker.id"))
    is_verified = db.Column(db.Boolean, default=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default="pending")
