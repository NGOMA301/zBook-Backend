# app/auth/auth_routes.py

from fastapi import APIRouter, Request, Response, HTTPException, Depends
from passlib.hash import bcrypt
from app.db.mongo import db
from app.models.user_model import UserCreate, UserLogin
from app.auth.auth_handler import create_token, verify_token
from app.auth.auth_handler import get_current_user  # ✅ add this import if not already


router = APIRouter()

@router.post("/register")
async def register(user: UserCreate):
    existing = await db.users.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = bcrypt.hash(user.password)
    await db.users.insert_one({"email": user.email, "password": hashed_pw})
    return {"message": "User registered successfully"}

@router.post("/login")
async def login(user: UserLogin, response: Response):
    db_user = await db.users.find_one({"email": user.email})
    if not db_user or not bcrypt.verify(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({"user_id": str(db_user["_id"]), "email": db_user["email"]})

    response.set_cookie(
        key="session",
        value=token,
        httponly=True,
        max_age=30 * 24 * 60 * 60,  # 30 days
        secure=False,  # set to True in production with HTTPS
        samesite="lax"
    )
    return {"message": "Logged in successfully"}

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("session")
    return {"message": "Logged out successfully"}

@router.get("/me")
async def check_auth(user=Depends(get_current_user)):
    return {
        "user_id": str(user["user_id"]),
        "email": user["email"],
        "status": "authenticated"
    }