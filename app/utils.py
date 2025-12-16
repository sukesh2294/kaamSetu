import random, string
from flask import current_app
from datetime import datetime, timedelta
from flask_mail import Message
from app.extensions import mail
from app.models import OTPVerification, db

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

def send_otp_email(email, otp, purpose="registration"):
    try:
        if purpose == "login":
            subject = 'User Login OTP'
            title = 'Login Verification'
        else:
            subject = 'User Registration OTP'
            title = 'Registration Verification'
            
        msg = Message(
            subject,
            sender=current_app.config['MAIL_USERNAME'],
            recipients=[email]
        )
        msg.html = f'''
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #4CAF50;">{title}</h2>
            <p>Your OTP for {purpose} is:</p>
            <h1 style="color: #2196F3; font-size: 2em; letter-spacing: 5px;">{otp}</h1>
            <p>This OTP is valid for 10 minutes.</p>
        </div>
        '''
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

def verify_otp(email, otp):
    otp_record = OTPVerification.query.filter_by(
        email=email,
        otp=otp,
        is_used=False
    ).first()
    
    if not otp_record:
        return None
        
    # Check if OTP is expired (10 minutes)
    if datetime.utcnow() - otp_record.created_at > timedelta(minutes=10):
        return None
        
    otp_record.is_used = True
    db.session.commit()
    return otp_record

