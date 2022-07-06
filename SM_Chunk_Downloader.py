from socket import *
import json
import os
from datetime import datetime

if not os.path.exists('./rec/'):
    os.mkdir('./rec/')

serverPort = 8000
while True:
    fileInput = input("Enter file name ")
    requestedFile = fileInput.split('.')[0]

    contentFile = open("contents.txt",'r')

    lookupJson = contentFile.read()
    contentFile.close()

    lookupDictionary = json.loads(lookupJson)
    chunkCount = 0
    for i in range(1,6):
        chunk = requestedFile + '_' + str(i)
        isChunkDownloaded = False
        for userIP in lookupDictionary[chunk]:
            clientSocket = socket(AF_INET, SOCK_STREAM)
            try:
                clientSocket.connect((userIP,serverPort))
                request = {
                    "requested_content": chunk
                }
                requestJson = json.dumps(request)

                clientSocket.send(requestJson.encode())
                print(f"Request sended for {chunk}")
                print("Downloading...")
                with open("./rec/"+"downloaded_" +requestedFile+"_"+str(i), "wb") as f:
                    chunkCount += 1
                    while True:
                        bytes_read = clientSocket.recv(4096)
                        # print(len(bytes_read))
                        if len(bytes_read) <= 0:
                            break
                        f.write(bytes_read)
                        isChunkDownloaded = True
            except:
                clientSocket.close()
                continue
            
        if not isChunkDownloaded:
            print(f"CHUNK {chunk} CANNOT BE DOWNLOADED FROM ONLINE PEERS.")
            continue

        if(isChunkDownloaded):
            now = datetime.now()
            current_time = now.strftime("%d/%m/%Y %H:%M:%S")

            with open("download_log.txt","a") as file:
                file.write(f"chunk {chunk} downloaded from {userIP} at {current_time} \n")
            print(f"Chunk {chunk} downloaded")
        
        else:
            print(f"Failed to download chunk {chunk}")


        clientSocket.close()


    if chunkCount == 5:
        content_name = "downloaded_" +requestedFile
        chunknames = [content_name+'_1', content_name+'_2', content_name+'_3', content_name+'_4', content_name+'_5']
        with open("./rec/"+"downloaded_" +requestedFile+".png", 'wb') as outfile:
            for chunk in chunknames: 
                with open("./rec/"+chunk, 'rb') as infile: 
                    outfile.write(infile.read() )
                infile.close()
        print("File successfully downloaded")

