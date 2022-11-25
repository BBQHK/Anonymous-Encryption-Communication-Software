# Anonymous-Encryption-Communication-Software
This is my group project of COMP4334

## Background
Since the internet has become popular, the risk to users’ privacy and safety has grown along with it. So, we want to build a toy system to make secure communication between two computers.

We have five different objectives which can help us to meet our goal. First, we need to generate the secret key and public key for the message encryption function.  Also, we need to encrypt the secret key by using the public key. After that, we need to exchange the public key for message decryption. Finally, we also need the digital signature.

We have the server side and client side for our system. In this system, we applied the "Pretty Good Privacy (PGP)" for the system encryption protocol. That is an encryption system used for both sending encrypted emails and encrypting sensitive files. The communication between two parties will be encrypted by a hybrid encryption scheme (e.g., RSA + AES). For the key exchange, there would be a server to handle the public key distribution. Also, the message will be encrypted on the user side, the server only saves the public key of the user and does not keep any messages sent by the user. The client will communicate with the server, so to start the system, we need to execute the server side first.

## TODO
1. Exchange public keys (Done)
2. Secret key genaration for AES (Done)
3. Encrypt message using secret key (Done)
4. Encrypt secret key using private key (Done)
5. Hash value checking (Done)
6. Add signature to hash value (Done)

## Group Members
* Jason Leung
* [Oscar Ng](https://github.com/BBQHK)
* [Dicky Shek](https://github.com/HKSSY)
