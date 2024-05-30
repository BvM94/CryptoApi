from fastapi import APIRouter, HTTPException, status
from db.models.user import User, UserReduced
from db.client import db_client
from db.schemas.user import user_schema, users_schema
from bson import ObjectId

router = APIRouter(prefix="/usersdb", tags=["usersdb"])
    
not_found_exeption = HTTPException(status.HTTP_404_NOT_FOUND, "No se ha encontrado el usuario.")

@router.get("/", 
response_model=list[User])
async def users():
    return get_all_user()

@router.get("/{id}", 
response_model=User)
async def user(id: str):
    user = get_user_by_id(id)
    if not user:
        raise not_found_exeption
    return user

@router.post("/", 
response_model=User,
status_code=201)
async def user(user: UserReduced):
    return create_user(user)
    
@router.put("/{id}", 
response_model=User)
async def user(id: str,user: UserReduced):
    return update_user(id, user)

@router.delete("/{id}", 
                status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str):
    return delete_user(id) 
    
def get_user_by_id(id: str) -> User:
    try:
        object_id = ObjectId(id)
    except:
        return None
    
    return get_user("_id",object_id)

def get_user_by_email(email: str) -> User:
    return get_user("email",email)

def get_user(key: str, value) -> User:
    try:
        print(key, value)
        user = user_schema(db_client.users.find_one({key:value}))
        print(user)
    except:
        return None
    return User(**user)

def get_all_user():
    try:
        users = users_schema(db_client.users.find())
    except:
        raise not_found_exeption
    return users

def create_user(user: UserReduced):
    if isinstance(get_user_by_email(user.email), User):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "El usuario ya existe.")
    
    id = db_client.users.insert_one(dict(user)).inserted_id
    new_user = user_schema(db_client.users.find_one({"_id":id}))
    
    return User(**new_user)
    
def update_user(id: str, user: UserReduced):
    existing_user = get_user_by_email(user.email)
    if existing_user is not None and existing_user.id != id:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "El email ya esta en uso.")   
    
    try:
        db_client.users.find_one_and_replace({"_id": ObjectId(id)},dict(user))
    except:
        raise not_found_exeption
    
    return get_user_by_id(id)    

def delete_user(id: str):
    found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})
            
    if not found:
        raise not_found_exeption