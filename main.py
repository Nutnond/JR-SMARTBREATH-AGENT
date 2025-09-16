# main.py
import logging
from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, constr
from typing import Optional, Annotated

from services.agent_factory import create_business_analyst_agent
from auth.token_validator import validate_token
from services.streaming import stream_agent_replies

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # ถ้าจะจำกัด origin ค่อยมาแก้ทีหลัง
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TaskRequest(BaseModel):
    prompt: constr(min_length=1)

@app.post("/agent/analyze", response_class=StreamingResponse)
async def analyze_business(
    payload: TaskRequest,
    request: Request,
    authorization: Annotated[Optional[str], Header(alias="Authorization")] = None,
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing/Invalid Authorization header")

    token = authorization.removeprefix("Bearer ").strip()
    try:
        _ = validate_token(token)
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token validation failed: {str(e)}")

    agent = create_business_analyst_agent()

    return StreamingResponse(
        stream_agent_replies(request, agent, payload.prompt, desired_source="nong_khun"),
        media_type="text/plain; charset=utf-8",
        headers={
            # กัน proxy บางตัวบัฟเฟอร์
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",  # ถ้าอยู่หลัง Nginx
        }
    )
