from fastapi import APIRouter, HTTPException
from pydantic  import BaseModel

router = APIRouter(prefix="/users", tags=["users"])

class User(BaseModel):
    id: int
    name: str
    surname: str
    age: int 
    
users = [
    User(id=1, name = "Mauro",surname= "Bernabeu",age= 29),
    User(id=2, name = "Lautaro",surname= "Bernabeu",age= 27),
    User(id=3, name = "Viviana",surname= "Verón",age= 55)
]

@router.get("/", 
response_model=list[User])
async def get_users():
    return users

@router.get("/{id}", 
response_model=User)
async def user(id: int):
    return get_user(id)

@router.post("/", 
response_model=User,
status_code=201)
async def user(user: User):
    return create_user(user)
    
@router.put("/", 
response_model=User)
async def user(user: User):
    return update_user(user)

@router.delete("/{id}", 
response_model=int)
async def user(id: int):
    return delete_user(id)
    
    
def get_user(id: int):
    try:
      user = next(filter(lambda user: user.id == id, users))
    except:
      raise HTTPException(404, create_error("No se ha encontrado el usuario."))
    return user

def create_user(user: User):
    if isinstance(get_user(user.id), User):
        raise HTTPException(422, create_error("El usuario ya existe."))
    
    users.append(user)
    return user
    
def update_user(user: User):
    found = False
    
    for index, saved_user in enumerate(users):
        if saved_user.id == user.id:
            users[index] = user
            found = True
    
    if not found:
        raise HTTPException(404, create_error("No se ha encontrado el usuario."))
    
    return user

def delete_user(id: int):
    found = False
    
    for index, saved_user in enumerate(users):
        if saved_user.id == id:
            del users[index]
            found = True
            
    if not found:
        raise HTTPException(404, create_error("No se ha encontrado el usuario."))
    
    return id 

def create_error(message: str):
    return {"error": message}