from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os

print(">>> crypto_utils.py LOADED <<<")

# ✅ EXACTLY 32 BYTES (AES-256)
MASTER_KEY = b"\x01" * 32
print("AES KEY LENGTH =", len(MASTER_KEY))

def encrypt_file(data: bytes) -> bytes:
    iv = os.urandom(16)

    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()

    cipher = Cipher(
        algorithms.AES(MASTER_KEY),
        modes.CBC(iv),
        backend=default_backend()
    )
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(padded_data) + encryptor.finalize()

    return iv + encrypted


def decrypt_file(data: bytes) -> bytes:
    iv = data[:16]
    ciphertext = data[16:]

    cipher = Cipher(
        algorithms.AES(MASTER_KEY),
        modes.CBC(iv),
        backend=default_backend()
    )
    decryptor = cipher.decryptor()
    padded_plain = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    plain = unpadder.update(padded_plain) + unpadder.finalize()

    return plain