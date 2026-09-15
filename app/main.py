from fastapi import  FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import  engine
from app.routers import user,post,auth,vote


origins = ["https://www.google.com"]

app  = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"hello" : "root"}


app.include_router(user.Router)
app.include_router(post.Router)
app.include_router(auth.router)
app.include_router(vote.router)









# try:
#     conn = psycopg2.connect(host = 'localhost',port = 5433,database = 'FastApi', user = 'postgres',
#                             password = 'postgres', cursor_factory=RealDictCursor)
#     print("connection succesful")
#     cursor = conn.cursor()
# except Exception as error:
#     print("failed")
#     print(error)





