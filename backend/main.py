from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from scanner import scan_code, detect_language
from database import save_scan, get_all_scans
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