from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import sys

def pkcs7_pad(data):
    pad_len = 16 - len(data) % 16
    padding = bytes([pad_len] * pad_len)
    return data + padding
def image_CBC_encrypt(input, output):
    key = get_random_bytes(16)
    iv = get_random_bytes(16)
    old_chunk = iv
    cipher = AES.new(key, AES.MODE_ECB)
    w = open(output, 'wb')
    with open(input, 'rb') as f:
        header=f.read(54)
        w.write(header)
        while True:
            chunk = f.read(16)  # read 16 bytes (128 bits) at a time
            
            if not chunk:  # end of file
                break
            # process the chunk here
            if len(chunk) != 16:
                chunk = pkcs7_pad(chunk)
            
            #xor chunk with IV
            
            chunk = bytes([x ^ y for x, y in zip(old_chunk, chunk)])
            chunk = cipher.encrypt(chunk)
                

            w.write(chunk)
            old_chunk = chunk
    #decrypt
    r = open(output, 'rb')
    d = open('new_image_dec.bmp', 'wb')
    cipher2 = AES.new(key, AES.MODE_CBC, iv)

    head2= r.read(54)
    data = r.read()
    d.write(head2)
    d.write(cipher2.decrypt(data))



