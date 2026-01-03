from passlib.context import CryptContext
import hashlib


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
def hash_password(password: str) -> str:
        sha = hashlib.sha256(password.encode("utf-8")).hexdigest()
        
        return pwd_context.hash(sha)
class Hash():
    def argon2_hash(self, password: str) -> str:
        sha = hashlib.sha256(password.encode("utf-8")).hexdigest()
        return pwd_context.hash(sha)
