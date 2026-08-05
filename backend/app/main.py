from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="Multi-Modal Evidence Review API",
    description="Enterprise API for processing insurance claims via VLMs",
    version="1.0.0"
)

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
    images: List[UploadFile] = File(...)
):
    # TODO: Stream images to S3/GCS
    # TODO: Invoke AI pipeline orchestrator
    # TODO: Write results to DB
    
    return ClaimResponse(
        user_id=user_id,
        claim_status="supported",
        issue_type="scratch",
        object_part="door",
        severity="low",
        evidence_standard_met=True,
        risk_flags=[],
        claim_status_justification="Visual evidence matches claim."
    )
