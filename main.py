# main.py

import asyncio
import re
from typing import Optional, Annotated

from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, constr
from services.agent_factory import create_business_analyst_agent
from auth.token_validator import validate_token

# นำเข้า logging
import logging

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TaskRequest(BaseModel):
    prompt: constr(min_length=1)

# Generator function สำหรับ stream เฉพาะข้อความที่เป็นคำตอบ
async def generate_response(request: Request, prompt: str):
    analyst_agent = create_business_analyst_agent()
    stream = analyst_agent.run_stream(task=prompt)
    
    # เป้าหมายที่เราต้องการ
    desired_source = "JR_BUDDY"

    async for chunk in stream:
        if await request.is_disconnected():
            logging.info("⚠️ Client disconnected. Stopping processing.")
            break
        
        # แสดงผลลัพธ์ของ chunk ทั้งหมดเพื่อดูการประมวลผล
        logging.info(f"Received chunk from Agent: {chunk}")
        
        # ใช้ regex เพื่อดึง 'source' และ 'content'
        source_match = re.search(r"source='(.*?)'", str(chunk))
        content_match = re.search(r"content='(.*?)'", str(chunk), re.DOTALL)
        
        # ถ้าพบ source และ content
        if source_match and content_match:
            source = source_match.group(1)
            content = content_match.group(1)
            
            # ตรวจสอบว่า source ตรงกับที่เราต้องการหรือไม่
            if source == desired_source:
                yield content

@app.post("/analyze")
async def analyze_business(
    payload: TaskRequest,
    request: Request,
    authorization: Annotated[Optional[str], Header(alias="Authorization")] = None,
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header format")

    token = authorization.removeprefix("Bearer ").strip()

    try:
        token_data = validate_token(token)
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token validation failed: {str(e)}")

    return StreamingResponse(generate_response(request, payload.prompt), media_type="text/plain")