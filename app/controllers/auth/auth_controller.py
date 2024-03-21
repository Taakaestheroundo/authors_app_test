from flask import Blueprint,request,jsonify
from app.stutus_code import HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT,HTTP_500_INTERNAL_SERVER_ERROR,HTTP_201_CREATED
import validators
from app.models.users import user
from app.extentions import db,bcrypt
from flask_bcrypt import Bcrypt

auth = Blueprint('auth', __name__, Url_prefix='api/v1/auth')


# User registration

@auth.route('/reqister', methods=['POST'])

def reqister_user():
    
    data = request.json
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    contact = data.get('contact')
    image= data.get('image')
    password = data.get('password')
    biography = data.get('biography', '') if type == "author" else''
    #validation for the incoming request.
    
    
    if not first_name or last_name or not contact or not password or not email:
        return jsonify({ "error": "All field are required" }),HTTP_400_BAD_REQUEST
    
    if type == 'author' and not biography:
        return jsonify({ "error": "Enter your authors biography" }),HTTP_400_BAD_REQUEST
    
    if len(password) <8:
         return jsonify({ "error": "password is too short" }),HTTP_400_BAD_REQUEST
     
    if not validators.email(email):
         return jsonify({ "error": "email is not valid" }),HTTP_400_BAD_REQUEST
     
    if user.query.filter_by(email=email).first() is not None:
        return jsonify({ "error": "email address in use" }),HTTP_409_CONFLICT
    
    if user.query.filter_by(contact=contact).first() is not None:
        return jsonify({ "error": "email address in use" }),HTTP_409_CONFLICT
    
    try:
        hashed_password = bcrypt.generate_password_hash(password)# hashing aperson
        # creating a new user
        new_user = user(first_name=first_name,last_name=last_name,password=hashed_password,email=email,contact=contact,biography=biography)
        db.session.add(new_user)
        db.session.commit()
        
        # username
        
        username = new_user.get_full_name()
        
        
        return jsonify({
            'message': username + "has been successfully created" + new_user.user_type,
            'user':{
                "id":new_user.id,
                "first_name":new_user.first_name,
                "last_name":new_user.last_name,
                "email":new_user.email,
                "contact":new_user.contact,
                "type":new_user.type,
                "biography":new_user.biography,
                "created_at":new_user.created_at,
                
            }
            
            
            
            
        }),HTTP_201_CREATED
    except Exception as e: 
        db.session.rollback()   
        return jsonify({'error':str(e)}),HTTP_500_INTERNAL_SERVER_ERROR
    
    
        
        
        
     