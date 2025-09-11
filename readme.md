

## Prerequisites (สิ่งที่ต้องมี)

ก่อนที่จะเริ่ม คุณต้องติดตั้งโปรแกรมต่อไปนี้บนเครื่องของคุณ:

1.  **Python 3.12**: ตรวจสอบเวอร์ชันได้ด้วยคำสั่ง `python --version`
2.  **Ollama**: โปรเจกต์นี้จำเป็นต้องใช้ Ollama service ทำงานอยู่เบื้องหลัง
      * **ดาวน์โหลดและติดตั้ง Ollama for Windows** ได้ที่: [https://ollama.com/](https://ollama.com/)
      * หลังจากติดตั้งเสร็จ ให้เปิด Command Prompt หรือ PowerShell แล้วรันโมเดลที่คุณต้องการเพื่อดาวน์โหลดและทดสอบ (เช่น Llama 3) คำสั่งนี้จะดาวน์โหลดโมเดลมาเก็บไว้ในเครื่องของคุณ:
        ```bash
        ollama run qwen3:1.7b
        ```

-----

## ⚙️ Installation (ขั้นตอนการติดตั้ง)

ทำตามขั้นตอนต่อไปนี้เพื่อตั้งค่าโปรเจกต์บนเครื่องของคุณ


### 1\. สร้างและ Activate Virtual Environment

เราจะสร้าง Virtual Environment เพื่อแยกสภาพแวดล้อมของโปรเจกต์นี้ออกจาก Python หลักในเครื่องของคุณ

  * **สร้าง Virtual Environment** ชื่อ `.venv`:

    ```bash
    python -m venv .venv
    ```

  * **Activate Virtual Environment**:

      * สำหรับ **Windows** (ใน Command Prompt หรือ PowerShell):
        ```bash
        .\.venv\Scripts\activate
        ```
      * สำหรับ **macOS/Linux**:
        ```bash
        source .venv/bin/activate
        ```

    เมื่อ activate สำเร็จ คุณจะเห็น `(.venv)` นำหน้าบรรทัดคำสั่งของคุณ

### 2\. ติดตั้ง Packages ที่จำเป็น

ติดตั้ง Python libraries ทั้งหมดที่โปรเจกต์ต้องการจากไฟล์ `requirements.txt`

```bash
pip install -U -r requirements.txt
```

  * คำสั่ง `-U` หรือ `--upgrade` จะช่วยอัปเกรด package ให้เป็นเวอร์ชันล่าสุดที่เข้ากันได้

-----

## ▶️ Running the Program (การรันโปรแกรม)

1.  **ตรวจสอบให้แน่ใจว่า Ollama service กำลังทำงานอยู่** (ปกติจะทำงานอัตโนมัติหลังจากติดตั้ง)
2.  รันสคริปต์ Python หลักของโปรแกรม (ในตัวอย่างนี้ใช้ชื่อ `agent.py`)

<!-- end list -->

```bash
uvicorn main:app --reload
```

เมื่อรันโปรแกรมแล้ว แอปพลิเคชันของคุณจะเริ่มทำงานและสามารถสื่อสารกับ Ollama service ได้