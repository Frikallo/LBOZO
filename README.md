# LBOZO Rasomware | [English](https://github.com/Frikallo/LBOZO/blob/main/README.md) | [Français](https://github.com/Frikallo/LBOZO/blob/main/FRREADME.md) |

Original Repository of the LBOZO Ransomware.

LBOZO is a Windows/Unix ransomware that encrypts all the user files with a strong encryption scheme.

This project is OpenSource, feel free to use, study and/or send pull request.


[![Travis branch](https://github.com/frikallo/LBOZO/actions/workflows/main.yml/badge.svg)](https://github.com/Frikallo/LBOZO)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Travis branch](https://img.shields.io/badge/made%20with-%3C3-red.svg)](https://github.com/Frikallo/LBOZO)
    
-------------

**How this ransomware works:**

In this verison of the ransomware, we first generate 4 key files; Two are generated on the fly on the victims machine(Cprivate.key, Cpublic.key) and the other two are generated on the server(Sprivate.key, Spublic.key). Then, we generate a random 16 byte AES key that we use to encrypt all found files with AES-256-CBC. We first disalocate this key on the victims machine and then we encrypt it with the Cprivate.key, which is in turned encrypted with Spublic.key; making our files relatively impossible to encrypt by researchers. Now that your files are encrypted, you can't decrypt them, but you can decrypt the AES key that we used to encrypt them. We send a request to our server to decrypt the AES key with the Sprivate.key, which will return to us the decrypted key. Now that we have the decrypted AES key and decrypt all the files.
    

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
