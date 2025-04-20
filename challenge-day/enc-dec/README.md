# DTLab Challange - Catch the flag

## Introduction
This challange is designed to be completed by students in 1h and 30 minutes. 
Students will have to learn on how to search for informations on the internet 
to get a result.

Main topics are:
* Cryptography
* Network security

Main goal is to reconstruct a private key and decrypt a message written in `decryptme.txt`. 
Plus there is an optional part in which students will use exploits to get some information 
on the system.

Flags **2.6**, **3.5** 

## Flag 1: Network discovery (8 pt)
You don't know anything about the network you are attacking. So you need to analyze the traffic.

### Flag 1.1: Asset enumeration (2 pt)
What are network address and netmask you are currently in?

### Flag 1.2: Asset enumeration (2 pt)
Based on your network configuration, how many hosts (except your PCs) are in the network?

### Flag 1.3: Asset details (3 pt) (optional)
Can you provide details about assets operating systems?

### Flag 1.4: Switch details (1 pt)
What it the switch ip address?

## Flag 2: Network credentials (14 pt)
You have to gain access to the network. Every good cybersecurity analyst will start from analyzing 
network traffic. There may be some leak of credentials. 

During this phase, you will focus on the gaining access to a network device and find the first part 
of the key.

### Flag 2.1: Sniffing (2 pt)
Excluding networking protocols, do you see something that can be related to an application? If yes,
what transport protocol and port number the application uses?

### Flag 2.2: Application analysis (1 pt) (optional)
Which are the sender and the receiver of the message?

### Flag 2.3: Secret (4 pt)
Look at the application message. Can you derive the secret?

### Flag 2.4: Network access (4 pt)
Using what have you found during asset enumeration, use the secret to gain access to a network device.
Get the user password and tell what hash algorithm is used.

### Flag 2.5: Network information (2 pt) (optional)
What is the VLAN ID you are currently using?

### Flag 2.6 Description (2 pt)
Grab the description of interface f0/23.

## Flag 3: Exploit (15 pt)
Based on what you found during discovery, you will have to hack into the server and 
perform some operations to gain the second part of the key.

### Flag 3.1: Server ip (1 pt)
What is the ip address of the server?

### Flag 3.2: Services (2 pt)
How many services there are on the server?

### Flag 3.3: Gain access (5 pt)
Based on your analysis, find a vulnerability in one of the services and open a shell 
in the server. What is the content of the file `imin.txt`?

### Flag 3.4: Password cracking (4 pt)
The string you found in the `imin.txt` file is an hashed password. Maybe it can be 
used as the current user password.

### Flag 3.5: File decryption (3 pt)
Look around. There might be some password-protected files that can be cracked.
What is the content of the file protected?


### Encrypt
Generate rsa key
```sh
openssl genrsa -out private.key 4096
openssl rsa -in private.key -pubout -out public.key
```

Encrypt:
```sh 
openssl pkeyutl -encrypt -pubin -inkey public.key -in plaintext.txt -out encrypted.txt
```

Decrypt:
```sh 
openssl pkeyutl -decrypt -inkey private.key -in encrypted.txt -out decrypted.txt
```
