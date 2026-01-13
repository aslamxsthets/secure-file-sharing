import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

KEY = os.environ.get("AES_SECRET_KEY", "this_is_32_bytes_secret_key!!").encode()

def encrypt_file(data: bytes) -> bytes:
    cipher = AES.new(KEY, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return cipher.nonce + tag + ciphertext

def decrypt_file(enc_data: bytes) -> bytes:
    nonce = enc_data[:16]
    tag = enc_data[16:32]
    ciphertext = enc_data[32:]
    cipher = AES.new(KEY, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)
