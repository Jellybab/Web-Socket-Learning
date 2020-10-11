import socket, pickle, os  # Import socket module

datasize = 1024
messagesize = 1024
multiplier = 1
fileDir = "./downloads/"


def Main():
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
    host = '127.0.0.1'  # Get local machine name
    port = 12345  # Reserve a port for your service.

    try:  # try to connect to host if fails prints error.
        conn.connect((host, port))
        message = conn.recv(messagesize)
        print(message)
    except Exception as e:
        print("Cannot connect to the server:", e)
    while True:  # if connected to server
        message = conn.recv(messagesize).decode()  # recieve message from server
        print(message)
        command = GetUserInput(input("->"))  # user inputs commands and sends to server
        if command[0] == "DISCONNECT":  # tells server and disconnects from server
            print("Disconnecting from server: " + host)
            data = pickle.dumps(command)
            conn.send(data)
            conn.close()
            break
        elif command[0] == "DOWNLOAD":  # tells server it wants to download the website from server
            ReceiveWebsite(conn, command)
        else:
            data = pickle.dumps(command)
            conn.send(data)


def GetUserInput(usrInput):  # makes everything the user inputs into capitals and then splits it for chunks to send
    usrInput = usrInput.upper()
    commands = usrInput.split()
    return commands


def ReceiveWebsite(conn, command):  # downloads website from server
    # global transfer
    print("Transferring Website")
    data = pickle.dumps(command)
    conn.send(data)  # sends download command to server
    response = conn.recv(messagesize)  # waits for okay message frm server
    print(response)
    if response == b'1':  # if server responds with 1 then will procead
        print("server responded")
        print("starting to transfer requested file")

        # while transfer:
        # #makes a variable called transfer while transfer is true then precedes to download files from website.
        ReceiveFile(conn, fileDir)
    #  transfer = True
    else:
        print("failed to get proper response from server")


def ReceiveFile(conn, fileDirectory):
    conn.send("NEXT".encode())  # tells server to send next file.
    filename = conn.recv(messagesize).decode()  # receives name of next file from server and decodes it
    print("filename received: " + filename)

    data = conn.recv(1024)
    print(data)
    conn.send(b" ")
    if data.decode() == "file":
        with open(fileDirectory + filename, "wb") as f:  # opens current file and prepares it to written to
            print("opened file")
            data = conn.recv(datasize * multiplier)
            while data:
                if data.endswith(
                        b'done'):  # if current sent data ends with done will write rest of data and prepares next file.
                    print('writing to file and finishing')
                    data = data[:-7]
                    f.write(data)
                    conn.send(b'done')
                    break
                    # if not finish write current data and receive more.
                print("writing to file")
                f.write(data)
                print("receive more")
                data = conn.recv(datasize * multiplier)
            f.close()
    elif data.decode() == "folder":
        try:
            os.makedirs(fileDirectory + filename)
        except:
            print("folder already exists")
            ReceiveFile(conn, fileDirectory + filename + "/")
    else:
        print("ending transfer")


if __name__ == '__main__':
    Main()
