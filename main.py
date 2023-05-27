from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, BaseSettings

app = FastAPI(docs_url="/docs")

class LoginRequest(BaseModel):
    uname: str
    pwd: str

class ValidCreds(BaseSettings):
    login_uname: str
    login_pass: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

creds = ValidCreds()

@app.get("/")
async def root():
    return {"message": "Hello"}

@app.post("/login")
async def login(user: LoginRequest):
    if user.uname != creds.login_uname or user.pwd != creds.login_pass:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"token": "validtoken"}
    
    