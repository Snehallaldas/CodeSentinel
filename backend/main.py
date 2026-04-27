from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from scanner import scan_code, detect_language
from database import save_scan, get_all_scans
from auth import hash_password, verify_password, create_token, decode_token
from database import create_user, get_user_by_email
import json
from pydantic import BaseModel
import os
print("Database location:", os.getcwd())

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScanRequest(BaseModel):
    code: str
    language: str

class SignupRequest(BaseModel):
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

@app.post("/scan-file")
async def scan_file(file: UploadFile = File(...)):
    contents = await file.read()
    code = contents.decode("utf-8")
    language = detect_language(file.filename)
    result = scan_code(code, language)
    
    # add these lines to save to database
    save_scan(
        language=language,
        total_findings=len(result["vulnerabilities"]),
        results=json.dumps(result)
    )
    
    return result

@app.post("/scan")
def analyze_code(request: ScanRequest):
    result = scan_code(request.code, request.language)
    save_scan(
        language=request.language,
        total_findings=len(result["vulnerabilities"]),
        results=json.dumps(result)
    )
    return result

@app.get("/history")
def get_history():
    scans = get_all_scans()
    return [
        {
            "id": s.id,
            "language": s.language,
            "total_findings": s.total_findings,
            "created_at": str(s.created_at),
            "results": json.loads(s.result)
        }
        for s in scans
    ]

@app.post("/signup")
def signup(request: SignupRequest):
    # check if user already exists
    existing = get_user_by_email(request.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # hash password and save user
    hashed = hash_password(request.password)
    create_user(request.username, request.email, hashed)
    
    return {"message": "Account created successfully"}

@app.post("/login")
def login(request: LoginRequest):
    # find user by email
    user = get_user_by_email(request.email)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    # verify password
    if not verify_password(request.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    # create and return token
    token = create_token({"user_id": user.id, "username": user.username})
    return {"token": token, "username": user.username}