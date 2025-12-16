from flask import Blueprint, request, jsonify, render_template, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app.models import User, OTPVerification
from app.extensions import db
from app.utils import generate_otp, verify_otp, send_otp_email

bp = Blueprint("auth", __name__)

# Render HTML login page
@bp.route("/login", methods=["GET"])
def login_page():
    return render_template("user_login.html")

# Register API
@bp.route("/register", methods=["POST"])
def register():
    if request.method == 'POST':
        data = request.get_json()
        fullname = data.get("fullname")
        email = data.get("email")
        password = data.get("password")

        if not fullname or not email or not password:
            return jsonify({'success': False, 'message': 'All fields are required'})
        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'success': False, 'message': 'This email is already registered'})

        otp = generate_otp()
        print(f"OTP for {email}: {otp}")  

        # Delete any existing OTP for this email
        OTPVerification.query.filter_by(email=email).delete()
        db.session.commit()
            
        otp_record = OTPVerification(
            email=email, 
            otp=otp,
            fullname=fullname,
            password_hash=generate_password_hash(password)
        )
        db.session.add(otp_record)
        db.session.commit()

        if send_otp_email(email, otp, "registration"):
            return jsonify({
                'success': True, 
                'message': 'OTP sent to your email',
                'email': email  # Return email to client
            })
        else:
            return jsonify({'success': False, 'message': 'Error sending email'})
    
    return render_template("login.html")

# Verify Register OTP
@bp.route("/verify-register", methods=["POST"])
def verify_register():
    data = request.get_json()
    email = data.get("email")
    otp = data.get("otp")

    if not email or not otp:
        return jsonify({"error": "Email and OTP are required"}), 400

    # Verify OTP and get the OTP record with user data
    otp_record = verify_otp(email, otp)
    if otp_record:
        # Create user using data from OTP record
        new_user = User(
            name=otp_record.fullname, 
            email=email, 
            password=otp_record.password_hash, 
            is_verified=True
        )
        db.session.add(new_user)
        
        # Clean up OTP record
        db.session.delete(otp_record)
        db.session.commit()
        
        return jsonify({"message": "Registration complete"}), 200
    
    return jsonify({"error": "Invalid or expired OTP"}), 400

# Login API
@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 401

    otp = generate_otp()
    print(f"Login OTP for {email}: {otp}")

    # Delete any existing OTP for this email
    OTPVerification.query.filter_by(email=email).delete()
    
    # Store OTP for verification
    otp_record = OTPVerification(email=email, otp=otp)
    db.session.add(otp_record)
    db.session.commit()

    if send_otp_email(email, otp, "login"):
        return jsonify({
            "message": "OTP sent to your email", 
            "email": email  
        }), 200
    else:
        return jsonify({"error": "Error sending OTP email"}), 500

# Verify Login OTP
@bp.route("/verify-login", methods=["POST"])
def verify_login():
    data = request.get_json()
    email = data.get("email")
    otp = data.get("otp")

    # Verify OTP
    otp_record = verify_otp(email, otp)
    if otp_record:
        user = User.query.filter_by(email=email).first()
        if user:
            # Clean up OTP record
            db.session.delete(otp_record)
            db.session.commit()
            
            token = create_access_token(identity=user.id)

            session["email"] = user.email 
            return jsonify({
                "message": "Login successful", 
                "token": token,
                'success': True
            }), 200
    
    return jsonify({"error": "Invalid or expired OTP"}), 400


