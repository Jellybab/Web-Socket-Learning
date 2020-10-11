import os
import pickle
import socket
import sys
from _thread import *
from Transfer import *

####################Server Commands######################################
#########################################################################
#########################################################################


def client_connection_thread(conn, addr):
    # welcomes the new client
    send_message(conn, b'Welcome to the Server, please login\n')
    while True:
        # tells client to send a command
        send_message(conn, b'please input a command')
        data = receive_message(conn)
        # if nothing received then ends link
        if not data:
            break
        # gets the data
        data_split = pickle._loads(data)
        data_split[0] = data_split[0].upper()
        print(data_split[0])
        if data_split[0] == 'DISCONNECT':
            print('Connection from ', addr, ' has disconnected')
            conn.close()
            break
        else:
            server_commands(data_split, conn)


def server_commands(data, conn):
    if data[0] == "HELP":
        send_message(conn, b'Current commands available are: --Data not found--')
    elif (data[0]) == 'DOWNLOAD':
        print('user downloading files')
    else:
        send_message(conn, b'invalid command\n')


######## Listen Server loop ##############################################
##########################################################################
##########################################################################


def main():
    host = ''
    port = 12345

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Created a Socket')

    try:
        server.bind((host, port))
    except socket.error:
        print('Socket binding Failed')
        sys.exit()

    print('socket is now bounded to ip and port')
    server.listen(5)
    print('Server is now online')
    while True:
        conn, addr = server.accept()
        print('incoming connection from ', addr)
        start_new_thread(client_connection_thread, (conn, addr))


if __name__ == '__main__':
    main()
