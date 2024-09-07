#src/shared/Authentication
import hashlib, uuid
from Crypto.Cipher import AES
import base64

class Encryptor():
    @staticmethod
    def generate_hash(msg):
        # salt = uuid.uuid4().hex
        salt = "^SEb[$b@QH2yfx)*"
        hashed_password = hashlib.sha512(msg + salt).hexdigest()
        return hashed_password


    @staticmethod
    def encrypt(msg):
        return msg

    @staticmethod
    def decrypt(msg):
        return msg
