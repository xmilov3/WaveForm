import hashlib
import os
import binascii

def hash_password(password):
    salt = os.urandom(32)
    
    hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000,
        dklen=32
    )
    
    hash_hex = binascii.hexlify(hash).decode('utf-8')
    salt_hex = binascii.hexlify(salt).decode('utf-8')
    
    return f"{hash_hex}:{salt_hex}"

def verify_password(stored_password, provided_password):
    try:
        hash_hex, salt_hex = stored_password.split(':')
        
        salt = binascii.unhexlify(salt_hex)
        
        new_hash = hashlib.pbkdf2_hmac(
            'sha256',
            provided_password.encode('utf-8'),
            salt,
            100000,
            dklen=32
        )
        
        new_hash_hex = binascii.hexlify(new_hash).decode('utf-8')
        
        return hash_hex == new_hash_hex
    except Exception as e:
        print(f"Error verifying password: {e}")
        return False