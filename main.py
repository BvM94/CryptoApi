from fastapi import FastAPI
from routers import users, jwt_auth_users, basic_auth_users
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

#Routers
#Forma de exponer recursos estaticos.
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(users.router)
app.include_router(jwt_auth_users.router)
app.include_router(basic_auth_users.router)


@app.get("/")
async def root():
    return "Hello word!!!" 

# Ruta específica para servir el favicon.ico
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")

"""
Instalar fastapi: 
Iniciar el server: uvicorn:app --reload
Detener el server: CTRL+C

Url local: http://127.0.0.1:8000

Url Swagger UI: /docs
Url Redoc UI: /redoc
"""