# main.py
import asyncio
import re
from typing import Optional, Annotated

from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, constr
from services.agent_factory import create_business_analyst_agent
from auth.token_validator import validate_token

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # โปรดระบุ origin จริงใน production
    allow_credentials=True,        # ถ้าใช้ credentials ควรระบุ allow_origins เป็นโดเมนจริง (ไม่ใช่ "*")
    allow_methods=["*"],
    allow_headers=["*"],
)

class TaskRequest(BaseModel):
    task: constr(min_length=1)     # กันเคสส่ง string ว่าง

@app.post("/analyze")
async def analyze_business(
    payload: TaskRequest,
    request: Request,
    authorization: Annotated[Optional[str], Header(alias="Authorization")] = None,
):
    # ตรวจ header
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header format")

    token = authorization.removeprefix("Bearer ").strip()

    # ตรวจ token
    try:
        token_data = validate_token(token)
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token validation failed: {str(e)}")

    # Run the agent
    analyst_agent = create_business_analyst_agent()
    stream = analyst_agent.run_stream(task=payload.task)

    last_chunk = None
    summary = None
    async for chunk in stream:
        if await request.is_disconnected():
            print("⚠️ Client disconnected. Stopping processing.")
            break
        summary = last_chunk
        match = re.search(r"content='(.*?)'", str(chunk), re.DOTALL)
        last_chunk = match.group(1) if match else str(chunk)
        print(last_chunk)

    return {"result": summary or ""}
