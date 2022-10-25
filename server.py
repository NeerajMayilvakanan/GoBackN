from base64 import encode
from secrets import choice
from socket import *
import random

serverport = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverport))
serverSocket.listen(1)
print("The Server is Ready to Receive\n")

connectionSocket, addr = serverSocket.accept()
ack=0
while True:
    choice = connectionSocket.recv(1024).decode()
    data = connectionSocket.recv(1024).decode()
    if(data == "end"):
        break
    data=data.split()
    original = data.copy()
    loss=random.randint(0,len(original)-1)
    if(choice=="2"):
        data.pop(loss)

    print("\nFrom Client : ", " ".join(data))
    ack=[]
    if(choice=='0' or choice=='3' or choice=='4'):
        for i in data:
            print("acknowledge for "+i+":"+i)
            ack.append(i)
    elif(choice=="2"):
        if(loss!=0):
            print("Original : ", original)
            for i in data:
                if(i>=original[loss]):
                    print("acknowledge for "+i+":"+original[loss-1])
                    ack.append(original[loss-1])
                else:
                    print("acknowledge for "+i+":"+i)
                    ack.append(i)
        else:
            for i in data:
                ack.append('')        
        
    connectionSocket.send(" ".join(ack).encode())
connectionSocket.close()
