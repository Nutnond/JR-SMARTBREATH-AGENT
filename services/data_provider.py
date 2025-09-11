# data_fetcher.py

import requests
from typing import Dict, Union

from auth.client_token import generate_client_token 

# API_URL = "http://localhost:8080"
API_URL ="http://147.50.227.142:3000"
VERIFY_HTTPS = True

# -------------------------------------------------------------------
# ฟังก์ชันช่วยสำหรับ handle error ตาม status code
# -------------------------------------------------------------------
def handle_http_error(response: requests.Response) -> None:
    code = response.status_code
    try:
        detail = response.json()
    except Exception:
        detail = response.text

    if code == 400:
        print(f"[400 Bad Request] ข้อมูลที่ส่งไม่ถูกต้อง: {detail}")
    elif code == 401:
        print(f"[401 Unauthorized] Token ไม่ถูกต้องหรือหมดอายุ: {detail}")
    elif code == 403:
        print(f"[403 Forbidden] ไม่มีสิทธิ์เข้าถึง resource นี้: {detail}")
    elif code == 404:
        print(f"[404 Not Found] ไม่พบ resource ที่ต้องการ: {detail}")
    elif code >= 500:
        print(f"[{code} Server Error] เซิร์ฟเวอร์มีปัญหา: {detail}")
    else:
        print(f"[{code}] เกิดข้อผิดพลาด: {detail}")

# -------------------------------------------------------------------
def get_records(machine_id: str, page: int = 1, page_size: int = 5) -> Union[Dict, None]:
    if not machine_id:
        print("Error: ต้องระบุ Machine ID")
        return None

    try:
        token = generate_client_token()
        if not token:
            print("Error: ไม่พบ Token สำหรับการยืนยันตัวตน")
            return None

        params = {"machineId": machine_id, "page": page, "pageSize": page_size}
        headers = {"Authorization": f"Bearer {token}"}

        response = requests.get(
            f"{API_URL}/records", headers=headers, params=params, verify=VERIFY_HTTPS
        )

        if response.status_code != 200:
            handle_http_error(response)
            return None

        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

# -------------------------------------------------------------------
def get_record_by_id(record_id: str) -> Union[Dict, None]:
    if not record_id:
        print("Error: ต้องระบุ Record ID")
        return None

    try:
        token = generate_client_token()
        if not token:
            print("Error: ไม่พบ Token สำหรับการยืนยันตัวตน")
            return None

        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{API_URL}/records/{record_id}", headers=headers, verify=VERIFY_HTTPS
        )

        if response.status_code != 200:
            handle_http_error(response)
            return None

        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
