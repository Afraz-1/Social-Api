from fastapi import  FastAPI
from app import models
from .database import  engine
from app.routers import user,post,auth


models.Base.metadata.create_all(bind = engine)


app  = FastAPI()

@app.get("/")
def root():
    return {"hello" : "root"}


app.include_router(user.Router)
app.include_router(post.Router)
app.include_router(auth.router)

# try:
#     conn = psycopg2.connect(host = 'localhost',port = 5433,database = 'FastApi', user = 'postgres',
#                             password = 'postgres', cursor_factory=RealDictCursor)
#     print("connection succesful")
#     cursor = conn.cursor()
# except Exception as error:
#     print("failed")
#     print(error)





