import jwt
from jwt import InvalidTokenError, ExpiredSignatureError
from config import JWT_SECREAT

class UnauthorizedException(Exception):
    pass

class InternalServerErrorException(Exception):
    pass

def validate_token(token: str) -> dict:
    secret_key = JWT_SECREAT
    
    try:
        decoded_token = jwt.decode(
            token,
            secret_key,
            algorithms=["HS256"],
            options={
                'require': ['exp'],  # ไม่ต้องมี 'iss' และ 'aud'
                'verify_exp': True,  # ตรวจสอบการหมดอายุ
                'verify_iss': False, # ไม่ต้องตรวจสอบ issuer
                'verify_aud': False  # ไม่ต้องตรวจสอบ audience
            }
        )
        return decoded_token
    except (InvalidTokenError, ExpiredSignatureError) as e:
        raise UnauthorizedException("Invalid token: " + str(e))
    except Exception as ex:
        raise InternalServerErrorException(str(ex))