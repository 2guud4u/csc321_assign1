from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import binascii
import re
import urllib.parse

def pkcs7_pad(data):
    pad_len = 16 - len(data) % 16
    padding = bytes([pad_len] * pad_len)
    return data + padding

def submit(str, key, iv):
    
    
    str = urllib.parse.quote(str) #url encode
    msg = "userid=456; userdata=" + str +";session-id=31337"
    print("Sent Message:", msg, "\n")
    old_chunk = iv
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext= []
    ciphermsg = ""

    msg = bytes(msg, 'utf-8')
    for i in range(0, len(msg), 16):
        chunk = msg[i:i+16]
        
        if not chunk:  # end of file
            break
        # process the chunk here
        if len(chunk) != 16:
            chunk = pkcs7_pad(chunk)
        
        #xor chunk with IV
        
        chunk = bytes([x ^ y for x, y in zip(old_chunk, chunk)])
        chunk = cipher.encrypt(chunk)
        ciphertext.append(chunk)    
        
        
        old_chunk = chunk
    ciphermsg = b''.join(ciphertext)
    print("original cipher msg:", ciphermsg, "\n")
    return ciphermsg

def verify(msg, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    msg = cipher.decrypt(msg)
    pattern = ";admin=true;"
    print("Recieved Message:", msg, "\n")
    if msg.find(pattern.encode()) != -1:
        return True
    else:
        return False

    

key = get_random_bytes(16)
iv = get_random_bytes(16)

secret = submit("1admin1true", key, iv)
#bit hacking part
secret = bytearray(secret)
secret[5] = secret[5] ^ ord('1') ^ ord(";")
secret[11] = secret[11] ^ ord('1') ^ ord('=')
secret = bytes(secret)
print("Corrupted cipher msg:", secret, "\n")



print(verify(secret, key, iv))