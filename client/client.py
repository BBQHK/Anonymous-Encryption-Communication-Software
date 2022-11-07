import ipaddress
import socket
import threading
import random
import string
letters = [string.ascii_lowercase,string.ascii_uppercase,string.ascii_letters,string.digits,string.punctuation]
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher
from Crypto.Signature import PKCS1_v1_5 as PKCS1_signature
from Crypto.Hash import SHA
from AES_CBC import AES_Encrypt, AES_Decrypt
import base64
from datetime import datetime

# Generate the public key and private key
random_generator = Random.new().read
rsa = RSA.generate(2048, random_generator)
 
private_key = rsa.exportKey()
with open("private_a.rsa", 'wb') as f:
    f.write(private_key)

public_key = rsa.publickey().exportKey()
with open("public_a.rsa", 'wb') as f:
    f.write(public_key)
    
# Read public and private key
with open('public_a.rsa') as f:
    public_key = f.read()
with open('private_a.rsa') as f:
    private_key = f.read()

print('           ______ _____  _____    _____ _ _            _   ')
print('     /\   |  ____/ ____|/ ____|  / ____| (_)          | |  ')
print('    /  \  | |__ | |    | (___   | |    | |_  ___ _ __ | |_ ')
print('   / /\ \ |  __|| |     \___ \  | |    | | |/ _ \ \'_ \| __|')
print('  / ____ \| |___| |____ ____) | | |____| | |  __/ | | | |_ ')
print(' /_/    \_\______\_____|_____/   \_____|_|_|\___|_| |_|\__|')
print('           AECS Client                       Ver 0.13')

#Reset variables
usernumber_count = 0
check_input_state = False
connection_error = False

# Choosing Nickname
server_ip = input("Input server ip: ")
port = input("Input port: ")
nickname = input("Input your name: ")

# Debug
# server_ip = "161.81.60.235"
# port = "12345"
# nickname = "Oscar"

#Check user input
while True:
    if server_ip == "" or port == "" or nickname == "":
        print("You must fill in all the fields.")
        server_ip = input("Input server ip: ")
        port = input("Input port: ")
        nickname = input("Input your name: ")
    elif server_ip != "" or port != "" or nickname != "":
        try:
            ipaddress.ip_address(server_ip)
            try:
                port_check = int(port)
                if port_check < 0 or port_check > 65353:
                    print("Invalid port number.")
                    port = input("Input port: ")
                elif str.isascii(nickname):
                    check_input_state = True
                    break
                else:
                    print("Invalid name. Only accept ASCII characters.")
                    nickname = input("Input your name: ")
            except ValueError:
                print("Invalid port number.")
                port = input("Input port: ")
        except ValueError:
            print("Invalid IP address.")
            server_ip = input("Input server ip: ")

# Connecting To Server
if check_input_state == True:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((server_ip, int(port)))
else:
    exit()

# Listening to Server and Sending Nickname
def receive():
    while True:
        try:
            # Receive Message From Server
            # If receive 'REQUEST_NICKNAME' Send Nickname
            message = server.recv(1024).decode('ascii')
            if message == 'REQUEST_NICKNAME':
                server.send(nickname.encode('ascii'))
            elif message == 'REQUEST_PUBLIC_KEY':
                server.send(public_key.encode('ascii'))
            elif message == 'GET_PUBLIC_KEY':
                pub_key = server.recv(1024).decode('ascii')

                f = open("public_b.rsa", "w+")
                f.write(pub_key)
                f.close()
            elif message[:14] == 'SYSTEM_MESSAGE':
                if message[:23] == 'SYSTEM_MESSAGE%USER_NUM':
                    global usernumber_count
                    usernumber_display = message[23:]
                    usernumber_count = int(usernumber_display[28:])
                    print(usernumber_display)
                else:
                    print(message[14:])
            else:
                temp = message.split("$#$#")
                encrypted_Message_and_encrypted_SecretKey = temp[0]
                signed_hash_value = temp[1]
                
                # verify signature
                f = open("public_b.rsa", "r")
                key = f.read()
                Pub_key = RSA.importKey(key)
                verifier = PKCS1_signature.new(Pub_key)
                digest = SHA.new()
                digest.update(encrypted_Message_and_encrypted_SecretKey.encode("ascii"))
                
                if(verifier.verify(digest, base64.b64decode(signed_hash_value))):
                    print("Message Authentication: PASS")
                else:
                    print("Message Authentication: FAILURE")
                    
                # Handle message
                temp = encrypted_Message_and_encrypted_SecretKey.split("@#@#")
                encrypted_Message = temp[0]
                encrypted_SecretKey = temp[1]
                
                # Recover AES key
                f = open("private_a.rsa", "r")
                key = f.read()
                Pri_key = RSA.importKey(key)
                cipher = PKCS1_cipher.new(Pri_key)
                SecretKey = cipher.decrypt(base64.b64decode(encrypted_SecretKey), 0)
                # print("Secret Key: " + SecretKey.decode('ascii'))
                
                # Show decrypted message
                print(AES_Decrypt(SecretKey.decode('ascii'), encrypted_Message))
        except:
            # Close Connection When Error
            print("An error occured!")
            global connection_error
            connection_error = True
            server.close()
            break

# Sending Messages To Server
def write():
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        message = '[{}] {}: {}'.format(current_time, nickname, input('Input your message: '))
        if usernumber_count < 2:
            print("Failed to send the message. Not enough clients online.")
        else:
            while True:
                if str.isascii(message):
                    break
                else:
                    print("Invalid message. Only accept ASCII characters.")
                    message = '[{}] {}: {}'.format(current_time, nickname, input('Input your message: '))
            
            if connection_error == True:
                break
            else:
                AES_key = ''.join(random.choice(letters[random.randint(0,4)]) for i in range(16)) # generate random AES key
                
                # Encrypt AES key
                f = open("public_b.rsa", "r")
                key = f.read()
                f.close()
                Pub_key = RSA.importKey(str(key))
                cipher = PKCS1_cipher.new(Pub_key)
                encrypted_AES_key = base64.b64encode(cipher.encrypt(bytes(AES_key.encode('ascii'))))
                
                message = AES_Encrypt(AES_key, message).encode('ascii') + "@#@#".encode('ascii') + encrypted_AES_key.decode('ascii').encode('ascii')
                
                # generate signature
                f = open("private_a.rsa", "r")
                key = f.read()
                f.close()
                Pri_key = RSA.importKey(str(key))
                signer = PKCS1_signature.new(Pri_key)
                digest = SHA.new()
                digest.update(message)
                signature = base64.b64encode(signer.sign(digest))

                server.send(message + "$#$#".encode('ascii') + signature)
                print("Message transmitted.")

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
