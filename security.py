import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import random
import string

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Cargar la clave de encriptación desde la variable de entorno
key = os.getenv('ENCRYPTION_KEY')

if not key:
    raise ValueError("La clave de encriptación no está configurada")

# Verificar que la clave sea válida
try:
    cipher = Fernet(key.encode())  # Asegúrate de codificar la clave
except Exception as e:
    raise ValueError("La clave de encriptación no es válida. Verifica el formato de la clave.") from e

# Función para encriptar datos
def encrypt_data(data: str) -> str:
    """Encripta un dato con la clave secreta."""
    return cipher.encrypt(data.encode()).decode()

# Función para desencriptar datos
def decrypt_data(encrypted_data: str) -> str:
    """Desencripta un dato encriptado con la clave secreta."""
    return cipher.decrypt(encrypted_data.encode()).decode()

# Función para anonimizar datos
def anonymize_data(data: str) -> str:
    """Genera un valor aleatorio para anonimizar datos."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))
