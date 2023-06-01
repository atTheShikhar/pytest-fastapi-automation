from fastapi.testclient import TestClient
from pydantic import BaseSettings

from main import app

client = TestClient(app)

class LoginCreds(BaseSettings):
    valid_uname: str
    valid_pass: str
    invalid_uname: str
    invalid_pass: str

    class Config:
        env_file = "test.env"
        env_file_encoding = "utf-8"

test_creds = LoginCreds()

def test_root():
    resp = client.get("/")
    assert resp.status_code == 201
    assert resp.json() == {"message": "Hello"}

def test_valid_login():
    resp = client.post("/login", json={"uname": test_creds.valid_uname, "pwd": test_creds.valid_pass})
    assert resp.status_code == 200
    assert resp.json() == {"token": "validtoken"}

def test_invalid_login():
    resp = client.post("/login", json={"uname": test_creds.invalid_uname, "pwd": test_creds.invalid_pass})
    assert resp.status_code == 401
    assert resp.json() == {"detail": "Invalid credentials"}
    
