from fastapi import FastAPI
from routers import users

app = FastAPI()

#Routers
app.include_router(users.router)


@app.get("/")
async def root():
    return "Hello word!!!" 

"""
Instalar fastapi: 
Iniciar el server: uvicorn:app --reload
Detener el server: CTRL+C

Url local: http://127.0.0.1:8000

Url Swagger UI: /docs
Url Redoc UI: /redoc
"""