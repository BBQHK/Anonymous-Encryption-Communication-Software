# tutorial link: https://blog.csdn.net/hh775313602/article/details/78991340
import base64
from Crypto.Cipher import AES
# 密鑰（key）, 密斯偏移量（iv） CBC模式加密

def AES_Encrypt(key, data):
    vi = '0102030405060708'
    pad = lambda s: s + (16 - len(s)%16) * chr(16 - len(s)%16)
    data = pad(data)
    # 字符串補位
    cipher = AES.new(key.encode('utf8'), AES.MODE_CBC, vi.encode('utf8'))
    encryptedbytes = cipher.encrypt(data.encode('utf8'))
    # 加密後得到的是bytes類型的數據
    encodestrs = base64.b64encode(encryptedbytes)
    # 使用Base64進行編碼,返回byte字符串
    enctext = encodestrs.decode('utf8')
    # 對byte字符串按utf-8進行解碼
    return enctext

def AES_Decrypt(key, data):
    vi = '0102030405060708'
    data = data.encode('utf8')
    encodebytes = base64.decodebytes(data)
    # 將加密數據轉換位bytes類型數據
    cipher = AES.new(key.encode('utf8'), AES.MODE_CBC, vi.encode('utf8'))
    text_decrypted = cipher.decrypt(encodebytes)
    unpad = lambda s: s[0:-s[-1]]
    text_decrypted = unpad(text_decrypted)
    # 去補位
    text_decrypted = text_decrypted.decode('utf8')
    return text_decrypted

# key = '0CoJUm6Qyw8W8jud'
# data = 'testtest'

# text_encrypted = AES_Encrypt(key, data)
# print(text_encrypted)

# text_decrypted = AES_Decrypt(key, text_encrypted)
# print(text_decrypted)

# print(AES_Decrypt(key, 'sQdNwsBkbHb3otf/GmNfXg=='))
