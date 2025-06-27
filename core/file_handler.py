from pathlib import Path
from .crypto_utils import encriptar_bytes, desencriptar_bytes

def encriptar_archivo(path: str, password: str) -> str:
    file_path = Path(path)
    with file_path.open('rb') as f:
        data = f.read()
    encrypted = encriptar_bytes(data, password)
    output_path = file_path.with_suffix(file_path.suffix + '.enc')
    with output_path.open('wb') as f:
        f.write(encrypted)
    return str(output_path)

def desencriptar_archivo(path: str, password: str) -> str:
    file_path = Path(path)
    with file_path.open('rb') as f:
        data = f.read()
    decrypted = desencriptar_bytes(data, password)
    output_path = file_path.with_name(file_path.stem + '.dec')
    with output_path.open('wb') as f:
        f.write(decrypted)
    return str(output_path)