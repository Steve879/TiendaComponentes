import logging
import os
import requests
from fastapi import HTTPException
from firebase_admin import auth as firebase_auth
from models.user import UserCreate, UserLogin
from utils.mongo import get_collection
from utils.security import create_jwt_token

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def register_user(user: UserCreate):
    try:
        # Firebase registration
        user_record = firebase_auth.create_user(
            email=user.email,
            password=user.password
        )
        
        # MongoDB storage
        coll = get_collection("users")
        user_data = user.dict(exclude={"password"})
        user_data.update({
            "firebase_uid": user_record.uid,
            "active": True,
            "role": "user"
        })
        result = coll.insert_one(user_data)
        
        return {"id": str(result.inserted_id), "email": user.email}
        
    except firebase_auth.EmailAlreadyExistsError:
        raise HTTPException(400, "Email already registered")
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        if 'user_record' in locals():
            firebase_auth.delete_user(user_record.uid)
        raise HTTPException(500, "Registration failed")

async def login_user(credentials: UserLogin):
    try:
        # Firebase authentication
        api_key = os.getenv("FIREBASE_API_KEY")
        response = requests.post(
            f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}",
            json={
                "email": credentials.email,
                "password": credentials.password,
                "returnSecureToken": True
            }
        )
        data = response.json()
        
        if "error" in data:
            raise HTTPException(401, "Invalid credentials")
        
        # Get user from MongoDB
        coll = get_collection("users")
        user = coll.find_one({"email": credentials.email})
        if not user:
            raise HTTPException(404, "User not found")
        
        # Generate JWT
        token = create_jwt_token(
            user_id=str(user["_id"]),
            email=user["email"],
            role=user.get("role", "user")
        )
        
        return {
            "token": token,
            "user": {
                "id": str(user["_id"]),
                "email": user["email"],
                "role": user.get("role", "user")
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(500, "Login failed")