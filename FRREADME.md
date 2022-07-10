# LBOZO Rasomware | [English](https://github.com/Frikallo/LBOZO/blob/main/README.md) | [Français](https://github.com/Frikallo/LBOZO/blob/main/FRREADME.md) |

Dépôt original du ransomware LBOZO.

LBOZO est un ransomware Windows/Unix qui crypte tous les fichiers de l'utilisateur avec un schéma de cryptage fort.

Ce projet est OpenSource, n'hésitez pas à l'utiliser, à l'étudier et/ou à envoyer des demandes de modification.


[![Travis branch](https://github.com/frikallo/LBOZO/actions/workflows/main.yml/badge.svg)](https://github.com/Frikallo/LBOZO)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Travis branch](https://img.shields.io/badge/fait%20avec-%3C3-red.svg)](https://github.com/Frikallo/LBOZO)
    
-------------

**Comment fonctionne ce ransomware:**

Actuellement, le ransomware est dans une phase de développement précoce. Et malheureusement, il utilise actuellement un schéma de cryptage uniquement symétrique. Tous les fichiers sont cryptés avec AES-256-CBC qui est seulement décryptable en utilisant une clé qui est généré et crypté par notre ransomware. Cette clé ne peut être décryptée qu'à l'aide d'une clé publique correspondant à une clé privée qui est actuellement stockée sur l'ordinateur de la victime et qui n'est pas chiffrée. Dans les futures versions du ransomware, cette clé sera chiffrée avec une clé publique stockée sur le serveur du ransomware, ce qui rendra notre ransomware hybride et relativement plus difficile à décrypter.
    

**Mentions:**

https://github.com/tarcisio-marinho/GonnaCry

https://github.com/Blubbus/File-Encrypter

https://medium.com/@tarcisioma/how-ransomware-works-and-gonnacry-linux-ransomware-17f77a549114

-------------

# Avis de non-responsabilité

Ce Ransomware ne doit pas être utilisé pour nuire, menacer ou blesser l'ordinateur d'une autre personne.

Son but est seulement de partager les connaissances et la sensibilisation sur les logiciels malveillants / cryptographie / systèmes d'exploitation / programmation.

LBOZO est un ransomware académique conçu pour l'apprentissage et la sensibilisation à la sécurité/cryptographie.

**Attention, l'exécution de out/LBOZO.exe ou LBOZO/src/main.py sur votre ordinateur peut être préjudiciable.

-------------

# Qu'est-ce qu'un ransomware ?

Un ransomware est un type de logiciel malveillant qui empêche les utilisateurs légitimes d'accéder à leur appareil ou à leurs données.
leur appareil ou leurs données et demande un paiement en échange de la fonctionnalité volée.
Ils ont été utilisés à des fins d'extorsion de masse sous diverses formes, mais le
mais la plus réussie semble être le ransomware de cryptage : la plupart des données de l'utilisateur sont cryptées et la clé peut être récupérée.
chiffrées et la clé peut être obtenue en payant l'attaquant.
Pour connaître un large succès, un ransomware doit remplir trois propriétés :

**Propriété 1** : Le code binaire hostile ne doit contenir aucun secret (par exemple, les clés de déchiffrage).
clés de déchiffrement). Du moins pas sous une forme facilement récupérable, en effet la cryptographie en boîte blanche
peut être appliquée aux ransomwares.

**Propriété 2** : Seul l'auteur de l'attaque doit être en mesure de déchiffrer le
l'appareil infecté.

**Propriété 3** : Le décryptage d'un dispositif ne peut pas fournir d'informations utiles
pour les autres dispositifs infectés, en particulier la clé ne doit pas être partagée entre eux.

-------------

# Objectifs :

- [x] Chiffrer tous les fichiers utilisateurs avec AES-256-CBC.
- [x] Clé AES et IV aléatoires pour chaque fichier.
- [x] Fonctionne même sans connexion internet.
- [x] Communication avec le serveur pour décrypter la clé privée du client.
- [x] Chiffre la clé AES avec la clé publique du client RSA-2048.
- [x] Chiffre la clé privée du client avec la clé publique du serveur RSA-2048.
- [x] Le cryptage est rapide et fiable.
- [x] Fonctionne avec Windows et Linux.
- [ ] Indétectable par les antivirus.
- [ ] Indétectable par l'utilisateur.
- [ ] Daemon.
- [x] Dropper.
