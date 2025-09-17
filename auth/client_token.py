import jwt
import datetime
from config import JWT_SECRET

def generate_client_token():
    claims = { "id": "11111111-1111-1111-1111-111111111111","username":"CLIENT_TOKEN" }
    secret_key = JWT_SECRET
    
    # Check if the key meets minimum length requirement (128 bits = 16 bytes)
    if len(secret_key.encode('utf-8')) < 16:
        raise Exception("The secret key must be at least 128 bits long (16 characters).")
    
    token = jwt.encode(
        payload={
            # # Standard JWT claims
            # "iss": JWT_ISSUER,        # issuer
            # "aud":JWT_AUDIENCE,      # audience
            "exp": datetime.datetime.now() + datetime.timedelta(minutes=15),  # expiration time
            # Custom claims
            **claims
        },
        key=secret_key,
        algorithm="HS256"
    )
    return token    