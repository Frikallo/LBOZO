# LBOZO Rasomware

Original Repository of the LBOZO Ransomware.

LBOZO is a Windows/Unix ransomware that encrypts all the user files with a strong encryption scheme.

This project is OpenSource, feel free to use, study and/or send pull request.


[![Travis branch](https://github.com/frikallo/LBOZO/actions/workflows/main.yml/badge.svg)](https://github.com/Frikallo/LBOZO)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Travis branch](https://img.shields.io/badge/made%20with-%3C3-red.svg)](https://github.com/Frikallo/LBOZO)
    
-------------

**How this ransomware works:**

Currently, the ransomware is in a early development phase. And unfortunately, currently uses a solely symmetric encryption scheme. All files are encrypted with AES-256-CBC which is only decryptable using a key that is generated and encrypted by our ransomware. This key is only retreivable using a public key corresponding to a private key that is currently stored on the victims computer and is left unencrypted, in future versions of the ransomware, this key will be encrypted with a public key that is stored on the ransomware server; rendering our ransomware hybrid and relatively harder to decrypt.
    

**Mentions:**

https://github.com/tarcisio-marinho/GonnaCry

https://github.com/Blubbus/File-Encrypter

https://medium.com/@tarcisioma/how-ransomware-works-and-gonnacry-linux-ransomware-17f77a549114

-------------

# Disclaimer

This Ransomware mustn't be used to harm/threat/hurt other person's computer.

Its purpose is only to share knowledge and awareness about Malware/Cryptography/Operating Systems/Programming.

LBOZO is an academic ransomware made for learning and awareness about security/cryptography.

**Be aware running out/LBOZO.exe or LBOZO/src/main.py in your computer, it may harm.**

-------------

# What's a Ransomware?

A ransomware is a type of malware that prevents legitimate users from accessing
their device or data and asks for a payment in exchange for the stolen functionality.
They have been used for mass extortion in various forms, but the
most successful one seems to be encrypting ransomware: most of the user data are
encrypted and the key can be obtained paying the attacker.
To be widely successful a ransomware must fulfill three properties:

**Property 1**: The hostile binary code must not contain any secret (e.g. deciphering
keys). At least not in an easily retrievable form, indeed white box cryptography
can be applied to ransomware.

**Property 2**: Only the author of the attack should be able to decrypt the
infected device.

**Property 3**: Decrypting one device can not provide any useful information
for other infected devices, in particular the key must not be shared among them.

-------------

# Objectives:

- [x] Encrypts all user files with AES-256-CBC.
- [x] Random AES key and IV for each file.
- [x] Works even without internet connection.
- [x] Communication with the server to decrypt Client-private-key.
- [x] Encrypts AES key with client-public-key RSA-2048.
- [x] Encrypts client-private-key with RSA-2048 server-public-key.
- [x] Encryption is fast and reliable.
- [x] Works with Windows and Linux.
- [ ] Undetectable by antivirus.
- [ ] Undetectable by user.
- [ ] Daemon.
- [x] Dropper.
