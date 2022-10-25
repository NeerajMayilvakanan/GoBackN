from socket import *
import random

serverName = '127.0.0.1'
serverport = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)

bits=int(input("Enter sequence no of bits\n"))
n = int(input("enter window size\n"))
i = 0
div=2
data = random.randint(1000,9000)
inp=data
size=data+(pow(2,bits))
print("no of packets to send",pow(2,bits))
print()
iteration = 1
clientSocket.connect((serverName, serverport))
ch = int(input("1.send frames 2.end choice: "))
if(ch==1):
    choice=input('1.No loss 2.Packet Loss 3.ACK Loss 4.Cumulative ACK \n Your Choice : ')
    while data<size:
        copyChoice="0"
        packets=[]
        while(i<n and data<size):
            data+=1
            packets.append(data)
            i+=1
        if(iteration%div==0):
            copyChoice=choice
            div+=div
                
        packets=list(map(str, packets))
        print("\nsent: "," ".join(packets))
        clientSocket.send(copyChoice.encode())
        clientSocket.send(" ".join(packets).encode())
        ack = clientSocket.recv(1024).decode()
        ack=list(map(int,ack.split()))
        packets=list(map(int, packets))
        iteration+=1
        if(copyChoice=='0'):
            print("acknowledgement: ",*ack)
        elif(copyChoice=='2'):
            print("acknowledgement: ",*ack)
            brFlag=True
            for i,j in zip(packets,ack):
                if(len(ack)==0 or i!=j):
                    print('Packet Loss')
                    print('Resending data from ',i)
                    data=i-1
                    brFlag=False
                    break
            if packets[-1] not in ack and brFlag:
                data = packets[0] if (packets[0] not in ack) else packets[-1]
                print('Packet Loss')
                print('Resending data from ',data)
                data-=1
        elif (copyChoice=='3' or copyChoice=='4'):
            original = ack.copy()
            loss=random.randint(0,len(original)-1)
            ack.pop(loss)
            print("acknowledgement: ",*ack)
            print('Acknowledgement Loss ')
            if(loss==len(ack) or copyChoice=='3'):
                print('Resending data from ',original[loss])
                data=original[loss]-1
            else:
                print('Cumulative Acknowledgement Success')
        else:
            print("Sorry!!! Invalid input")

        i=0 #Window size
        print()
        if(data==size):
            clientSocket.send("0".encode())
            clientSocket.send("end".encode())
            break
    print("all packets sent")
else:
    clientSocket.send("0".encode())

    clientSocket.send("end".encode())

clientSocket.close()
