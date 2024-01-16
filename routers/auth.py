from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Path
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class CreateUser(BaseModel):
    email: str
    passwordRaw: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


def authenticate_user(email: str, password: str, db):
    user = db.query(Users).filter(Users.email == email).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    return True



@router.post("/auth/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUser):
    create_user_model = Users(email=create_user_request.email, password=bcrypt_context.hash(create_user_request.passwordRaw))

    db.add(create_user_model)
    db.commit()

    return create_user_model

@router.post("/token")
async def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                     db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Failed Authentication")
    return {"message": "Succeed Authentication"}


