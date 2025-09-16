# services/streaming.py
import asyncio
import logging
from typing import Any, AsyncGenerator
from starlette.requests import Request

async def stream_agent_replies(
    request: Request,
    agent: Any,
    prompt: str,
    desired_source: str = "nong_khun"
) -> AsyncGenerator[bytes, None]:
    """
    สร้าง stream การตอบกลับจาก Agent โดยกรองเอาเฉพาะข้อมูลที่เป็นข้อความ (string)
    และข้ามข้อมูลประเภทอื่น เช่น tool calls ที่อาจมาในรูปแบบ list.
    """
    try:
        stream = agent.run_stream(task=prompt)

        async for event in stream:
            if await request.is_disconnected():
                logging.info("⚠️ Client disconnected. Stop streaming.")
                break

            try:
                # --- START: ตรรกะการกรองและเลือกข้อมูลใหม่ ---
                
                text_chunk = None

                # 1. พยายามดึงข้อมูลที่เป็น string จาก attribute ที่เป็นไปได้
                # โดยทั่วไป `delta` จะเป็น string ที่ทยอยส่งมา
                if hasattr(event, 'delta') and isinstance(event.delta, str):
                    text_chunk = event.delta
                
                # `content` อาจเป็น string (คำตอบสุดท้าย) หรือ list (ข้อมูลอื่น)
                # เราจะเอาเฉพาะกรณีที่เป็น string
                elif hasattr(event, 'content') and isinstance(event.content, str):
                    text_chunk = event.content
                
                # โครงสร้างสำรองที่อาจพบได้
                elif (hasattr(event, 'message') and 
                      hasattr(event.message, 'content') and 
                      isinstance(event.message.content, str)):
                    text_chunk = event.message.content

                # 2. ถ้าเจอ text_chunk ที่เป็น string แล้วเท่านั้น ถึงจะนำไปประมวลผลต่อ
                if text_chunk:
                    # (Optional) หากยังต้องการกรอง source อยู่
                    src = getattr(event, "source", None)
                    if desired_source and src is not None and src != desired_source:
                        continue
                    
                    # ส่งข้อมูลที่เป็น string ออกไป
                    yield (text_chunk + "\n").encode("utf-8")

                # ถ้า event ที่เข้ามามีข้อมูลเป็น list หรือชนิดข้อมูลอื่นที่เราไม่ต้องการ
                # โค้ดจะข้าม event นี้ไปโดยอัตโนมัติ และรอรับ event ถัดไป
                
                # --- END: ตรรกะการกรองและเลือกข้อมูลใหม่ ---

            except Exception as e:
                logging.exception(f"Error processing stream event: {e}")
                continue
            
            await asyncio.sleep(0)

    except Exception as e:
        logging.error(f"🔴 Failed to start agent stream: {e}")
        error_message = f"Error: ไม่สามารถเริ่มการสนทนาได้\n"
        yield error_message.encode("utf-8")