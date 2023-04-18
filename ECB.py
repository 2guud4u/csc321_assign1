from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import sys

def pkcs7_pad(data):
    pad_len = 16 - len(data) % 16
    padding = bytes([pad_len] * pad_len)
    return data + padding

def image_ECB_encrypt(inFile, outFile):
    key = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_ECB)
    w = open(outFile, 'wb')
    with open(inFile, 'rb') as f:
        header=f.read(54)
        w.write(header)
        while True:
            chunk = f.read(16)  # read 16 bytes (128 bits) at a time
            
            if not chunk:  # end of file
                break
            # process the chunk here
            if len(chunk) != 16:
                chunk = pkcs7_pad(chunk)
            
            chunk = cipher.encrypt(chunk)
                

            w.write(chunk)


        


