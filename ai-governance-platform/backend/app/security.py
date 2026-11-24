from datetime import datetime, timedelta, timezone
import jwt
from pwdlib import PasswordHash
from app.core.config import settings

password_hash = PasswordHash.recommended()
def hash_password(value: str) -> str:
    return password_hash.hash(value)
def verify_password(value: str, hashed: str) -> bool:
    return password_hash.verify(value, hashed)
def make_token(user_id: int) -> str:
    expiry = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({"sub": str(user_id), "exp": expiry}, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
def read_token(token: str):
    return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
