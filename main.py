from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message" : "Hello World"}

@app.get("/about")
def about():
    return {"message" : "CampusX is good platform to learn machine learning."}

@app.get("/users/{user_id}")
def users(user_id : int):
    return{
        "message" : "Hello Users",
        "User_id" : user_id
    }
