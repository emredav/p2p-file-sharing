from socket import *
import json
from datetime import datetime


serverPort = 8000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(5)

print('The server is ready to upload')


while True:
    connection , (addr,port) = serverSocket.accept()
    print(f"Connection from {addr} has been established")
    requestJson =  connection.recv(4096).decode()

    requestedFile = json.loads(requestJson)
    print(f"Requiest received for {requestedFile['requested_content']}")

    filename = requestedFile['requested_content']
    print("Uploading...")
    with open(filename,'rb') as file:
        l = file.read(4096)
        while (l):
            connection.send(l)
            l = file.read(4096)

        # connection.sendall(file.read())
    print(f"Chunk {filename} uploaded")
    
    now = datetime.now()
    current_time = now.strftime("%d/%m/%Y %H:%M:%S")

    with open("upload_log.txt","a") as file:
        file.write(f"chunk {filename} sended to {addr} at {current_time} \n")

    connection.close()