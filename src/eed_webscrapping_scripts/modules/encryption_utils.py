import base64
import os

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

home_dir = os.path.expanduser("~")


def get_encryption_pasword() -> str:
    """Reads password either from disk or from a github secret.

    Args:

    Returns:
        str: password -> use it in functions encrypt and decrypt
    """
    try:
        with open(os.path.join(home_dir, ".encryption_key")) as f:
            encryption_pasword = f.read()
    except Exception:
        encryption_pasword = os.getenv("ENCRYPTION_PASWORD")  # TODO
    return encryption_pasword.strip()


def get_encryption_salt() -> bytes:
    """Reads password either from disk or from a github secret.

    Args:

    Returns:
        str: password -> use it in functions encrypt and decrypt
    """
    try:
        with open(os.path.join(home_dir, ".encryption_salt")) as f:
            encryption_salt = f.read()
    except Exception:
        encryption_salt = os.getenv("ENCRYPTION_SALT")
    return bytes(encryption_salt.strip(), encoding="utf-8")


def generate_key(password: str) -> bytes:
    salt = get_encryption_salt()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=1_200_000,
    )
    password_kdf = kdf.derive(password.encode("utf-8"))
    key = base64.urlsafe_b64encode(password_kdf)

    return key


def encrypt(phrase: str, key) -> str:
    fernet = Fernet(key)
    encrypted_phrase = fernet.encrypt(phrase.encode())
    return encrypted_phrase


def encrypt_direct(phrase: str) -> str:
    encrypted_phrase = encrypt(phrase, generate_key(get_encryption_pasword()))
    return encrypted_phrase


def decrypt(enc_phrase: str, key, encoding: str = "utf-8") -> str:
    fernet = Fernet(key)
    phrase = fernet.decrypt(enc_phrase)
    return phrase.decode(encoding)


def decrypt_direct(enc_phrase: str) -> str:
    decrypted_phrase = decrypt(enc_phrase, generate_key(get_encryption_pasword()))
    return decrypted_phrase


def encrypt_file(file):
    phrase = file.read_text()
    encrypted_phrase = encrypt_direct(phrase).decode("utf-8")
    file.write_text(encrypted_phrase)


def decrypt_file(file):
    phrase = file.read_text()

    decrypted_phrase = decrypt_direct(bytes(phrase, encoding="utf-8"))

    file.write_text(decrypted_phrase)
