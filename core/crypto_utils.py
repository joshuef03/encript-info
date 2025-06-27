import hashlib
import base64
from cryptography.fernet import Fernet, InvalidToken

def generar_clave(password: str) -> bytes:
    sha = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(sha)

def encriptar_texto(texto: str, password: str) -> str:
    clave = generar_clave(password)
    f = Fernet(clave)
    return f.encrypt(texto.encode()).decode()

def desencriptar_texto(token: str, password: str) -> str:
    clave = generar_clave(password)
    f = Fernet(clave)
    return f.decrypt(token.encode()).decode()

def encriptar_bytes(data: bytes, password: str) -> bytes:
    clave = generar_clave(password)
    return Fernet(clave).encrypt(data)

def desencriptar_bytes(data: bytes, password: str) -> bytes:
    clave = generar_clave(password)
    return Fernet(clave).decrypt(data)