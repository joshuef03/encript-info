from cryptography.fernet import InvalidToken

def validar_contraseña(pwd: str) -> None:
    if not pwd:
        raise ValueError("La contraseña no puede estar vacía.")

def manejar_error(e: Exception) -> str:
    if isinstance(e, InvalidToken):
        return "Contraseña incorrecta o datos corruptos."
    return str(e)