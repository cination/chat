import socket  
import time

temp_host = socket.gethostname()
temp_port = 80

s_temp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s_temp.connect((temp_host, temp_port))

temp = s_temp.getsockname()[0]

s_temp.close()

host = temp
port = 5000

#names and addreses
clients = []

#some holder
alias = ''
message = ''

#sockets
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host,port))
#grabs data from stream , if nothing will drop error
s.setblocking(0)

#When we get a pakcet , we need to make sure that the load is the actual message and not just the alias
isMessage = False

quitting = False
print ('Server Started.')

while quitting != True:
    
    try:
        
        data, addr = s.recvfrom(1024)
        curAddr = addr[0]
        #print (addr)
        data = data.decode('utf-8')

        if data[:6] == "alias_":
            alias = data[6:]
            isMessage = False
        else:
            message = data[8:]
            isMessage = True
        
        #extractiong addresses
        addreses = [client[0] for client in clients]
                    
        #converting the list of tuples into a dictionary for easy access
        try:
            dict_clients = dict(clients)
            username = dict_clients[curAddr] 
            
        except:
            pass
        
        #Saving IP and ID
        if (addr[0] in addreses) ==  False:
        
            print ('Added : ' + str(addr))
            clients.append((addr[0],alias))
            print(clients)
            
        elif data[:6] == "alias_":
            # if someone has already logged in with a nickname
            # we are telling them that a nickname was already set
            s.sendto(('Logged in as ' + username).encode('utf-8'), addr)
            #print('sent')
            print(addr)
            
        #did we receive a message ?
        if isMessage == True:

            if "Quit" in str(message):
                quitting = True

            
            print (time.ctime(time.time()) + str(curAddr) + ': :' + str(username) + ' : ' + str(message))
            
            #send the message sent to the server to the clients
  
            for client in addreses:
            
                if curAddr != client:
                
                    try:
                    
                        s.sendto(message, client)
                        
                    except:
                    
                        print ('someerror')
            
           
        
    except:
    
        pass

#we want the client to terminate if the server if offline        
s.sendto('q_command'.encode('utf-8'), addr)
s.close()