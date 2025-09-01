from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from models.users import User, TokenResponse
from auth.hash_password import HashPassword
from auth.jwt_handler import create_access_token
from database.connection import Database


user_router = APIRouter(
    tags=["User"]
)

user_database = Database(User)
hash_password = HashPassword()


@user_router.post("/signup")
async def sign_new_user(data: User) -> dict:
    user_exist = await User.find_one(User.email == data.email)
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )
    hashed_password = hash_password.create_hash(data.password)
    data.password = hashed_password
    await user_database.save(data)
    return {
        "message": "User created successfully"
    }


@user_router.post("/signin", response_model=TokenResponse)
async def sign_in_user(user: OAuth2PasswordRequestForm=Depends()) -> dict:
    user_exist = await User.find_one(User.email == user.username)
    if not user_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if hash_password.verify_hash(user.password, user_exist.password):
        access_token = create_access_token(user_exist.email)
        return {
            "access_token": access_token,
            "token_type": "Bearer"
        }
    
    
