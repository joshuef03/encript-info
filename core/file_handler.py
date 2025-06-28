from pathlib import Path
from .crypto_utils import encriptar_bytes, desencriptar_bytes

OUTPUT_DIR = Path("./output")
RAW_DIR = Path("./raw_file")

OUTPUT_DIR.mkdir(exist_ok=True)
RAW_DIR.mkdir(exist_ok=True)

def encriptar_archivo(path: str, password: str) -> str:
    file_path = Path(path)
    with file_path.open('rb') as f:
        data = f.read()
    encrypted = encriptar_bytes(data, password)
    output_path = OUTPUT_DIR / (file_path.name + ".enc")
    with output_path.open('wb') as f:
        f.write(encrypted)
    return str(output_path)

def desencriptar_archivo(path: str, password: str) -> str:
    file_path = Path(path)
    with file_path.open('rb') as f:
        data = f.read()
    decrypted = desencriptar_bytes(data, password)
    if file_path.suffix == '.enc':
        original_name = file_path.stem
        output_path = RAW_DIR / original_name
    else:
        raise ValueError("Archivo no tiene extensión '.enc'")
    with output_path.open('wb') as f:
        f.write(decrypted)
    return str(output_path)