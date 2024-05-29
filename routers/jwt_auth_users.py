import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic  import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
# Ejecutar en git bash
# openssl rand -hex 32
SECRET = "9f78d542d7b1e1786c8ad6e54290ff24822f636b0f05e721b4b71dd67d46818e"


router = APIRouter()
oauth2 = OAuth2PasswordBearer(tokenUrl="login")
crypt = CryptContext(schemes="bcrypt")
authenticate_exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Credenciales de autenticación inválidas",
                headers= {"www-Authenticate" : "Bearer"})

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

users_db = {
    "mauro":{
        "username": "mauro",
        "full_name": "Mauro Bernabeu Veron",
        "email": "mauro@gmail.com",
        "disabled": False,
        "password": "$2a$12$p.eut8YsY74NQhnEIBcJW.Fr8i7Dtn77aa9HcnH3FW6u3PXlU6kf2" #123456
    },
    "mauro2":{
        "username": "mauro2",
        "full_name": "Mauro Bernabeu",
        "email": "mauro2@gmail.com",
        "disabled": True,
        "password": "$2a$12$vb9BtVle688gMHlZb4pCSeLz3z6tmhpPbH1DPiaPXtnIQ8lhdVp7i" #654321
    }
}

async def auth_user(token: str = Depends(oauth2)):
    try:
        username = jwt.decode(token, key= SECRET, algorithms=ALGORITHM).get("sub")
        if username is None:
            raise authenticate_exception     

    except InvalidTokenError:
        raise authenticate_exception
    
    user = search_user(username)
    
    return user

async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuario inactivo")
    
    return user

@router.get("/")
async def root():
    return "Hello word!!!" 

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    error_message : str =  "El usuario o contraseña no es correcto." 
    
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status.HTTP_404_NOT_FOUND, error_message)
    
    user = search_user_db(form.username)
    
    if not crypt.verify(form.password, user.password):
        raise HTTPException(status.HTTP_404_NOT_FOUND, error_message)

    access_token = {
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    }
    
    
    return {
        "access_token" : jwt.encode(access_token, key = SECRET, algorithm=ALGORITHM),
        "token_type": "bearer"
    }
    
@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])