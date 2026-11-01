import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "code"))

from fastapi import FastAPI, File, UploadFile, Form, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import shutil
import uuid
import asyncio

from pipeline import process_claim
from models import ClaimInput
from llm.multi_provider_client import MultiProviderClient

app = FastAPI(
    title="Multi-Modal Evidence Review API",
    description="Enterprise API for processing insurance claims via VLMs",
    version="1.0.0"
)

# Zero Trust CORS Configuration: Explicit origin allowlist (NIST SP 800-207)
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "")
if allowed_origins_env.strip():
    allowed_origins = [origin.strip() for origin in allowed_origins_env.split(",") if origin.strip()]
else:
    allowed_origins = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}

class ClaimResponse(BaseModel):
    user_id: str
    claim_status: str
    issue_type: str
    object_part: str
    severity: str
    evidence_standard_met: bool
    risk_flags: List[str]
    claim_status_justification: str

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/api/v1/claims/submit", response_model=ClaimResponse)
async def submit_claim(
    user_id: str = Form(...),
    claim_object: str = Form(...),
    user_claim: str = Form(...),
    use_mock: bool = Form(False),
    images: List[UploadFile] = File(...)
):
    upload_dir = Path(__file__).parent.parent.parent / "dataset" / "images" / "uploads"
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    image_paths = []
    for image in images:
        raw_ext = (image.filename.split('.')[-1] if image.filename else "jpg").lower()
        if raw_ext not in ALLOWED_IMAGE_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file format '{raw_ext}'. Allowed formats: {', '.join(sorted(ALLOWED_IMAGE_EXTENSIONS))}"
            )
        file_path = upload_dir / f"{uuid.uuid4()}.{raw_ext}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        image_paths.append(str(file_path))
        
    claim_input = ClaimInput(
        user_id=user_id,
        image_paths=";".join(image_paths),
        user_claim=user_claim,
        claim_object=claim_object,
    )
    
    # Run the orchestration pipeline synchronously in a thread
    llm_client = MultiProviderClient(provider_name="mock") if use_mock else None
    output = await asyncio.to_thread(process_claim, claim_input, llm_client)
    
    return ClaimResponse(
        user_id=output.user_id,
        claim_status=output.claim_status,
        issue_type=output.issue_type,
        object_part=output.object_part,
        severity=output.severity,
        evidence_standard_met=output.evidence_standard_met == "true",
        risk_flags=[flag.strip() for flag in output.risk_flags.split(";") if flag.strip()],
        claim_status_justification=output.claim_status_justification
    )
