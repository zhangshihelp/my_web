import base64
from Crypto.Cipher import AES

KEY = 'KjP5snp7DWnYsdZyrYGDtiRxn3dkkYHC'
IV = '7SmcasDxBnY5Hh4w'


def pkcs7padding(text):
    bs = AES.block_size
    length = len(text)
    bytes_length = len(bytes(text, encoding='utf-8'))
    padding_size = length if (bytes_length == length) else bytes_length
    padding = bs - padding_size % bs
    padding_text = chr(padding) * padding
    return text + padding_text


def pkcs7un_padding(text):
    length = len(text)
    un_padding = ord(text[length - 1])
    return text[0:length - un_padding]


def encrypt(content):
    key_bytes = bytes(KEY, encoding='utf-8')
    iv = bytes(IV, encoding='utf-8')
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
    content_padding = pkcs7padding(content)
    encrypt_bytes = cipher.encrypt(bytes(content_padding, encoding='utf-8'))
    result = str(base64.b64encode(encrypt_bytes), encoding='utf-8')
    return result


def decrypt(content):
    key_bytes = bytes(KEY, encoding='utf-8')
    iv = bytes(IV, encoding='utf-8')
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
    encrypt_bytes = base64.b64decode(content)
    decrypt_bytes = cipher.decrypt(encrypt_bytes)
    result = str(decrypt_bytes, encoding='utf-8')
    result = pkcs7un_padding(result)
    return result


if __name__ == '__main__':
    print(encrypt(input()))
