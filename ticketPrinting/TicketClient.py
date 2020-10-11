import socket, pickle               # Import socket module

connected = False
def Main():
    while True:

        if connected == False:
            commands = GetUserInput(input("->"))
            if commands[0].upper() == 'CONNECT':
                print(commands[1])
                Connection(commands[1], commands[2])
            elif commands[0].upper() == "CLOSE":
                break

            else:
                print("to connect to server type in connect then ip and port e.g Connect 127.0.0.1 12345")



def GetUserInput(usrInput):
    usrInput.upper()
    commands = usrInput.split()
    return commands


def Connection(host, port):

    s = socket.socket()
    s.connect((host,int(port)))
    print("Connected to Server: " + host)
    connected = True
    while connected == True:
        commands = GetUserInput(input("->"))
        if commands[0].upper() == "DISCONNECT":
            print("Disconnecting from server: "+ host)
            connected == False
            s.close()
            break
        else:
            data = pickle.dumps(commands)
            s.send(data)







if __name__  == '__main__':
    Main()

