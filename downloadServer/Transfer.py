import os
import struct


def send_files(conn, file_location):
    for file in os.listdir(file_location):
        waiting_message = receive_message(conn)
        print(waiting_message)
        if waiting_message == 'NEXT':
            print(file)
            send_message(conn, file)
            try:
                with open(file_location+file, 'rb') as f:
                    send_message(conn, b'file')
                    data = receive_message(conn)
                    if data == "ready":
                        print("sending file")
                        while True:
                            conn.sendfile(f, 0)
                            break
                        print("sending done message")
                        send_message(conn, b'done')
                        data = receive_message(conn)
                        print(data)
                        f.close()

            except IOError:
                send_message(conn, b'folder')
                data = receive_message(conn)
                print("folder Detected")
                send_files(conn, file_location + file + "/")


def upload_files(conn, addr, file_location):
    print('uploading files to ', addr)
    send_message(conn, b'ready')
    send_files(conn, file_location)
    print("sending finished")
    send_message(conn, b'finished')
    data = receive_message(conn)
    print(data)


# sends a message in 4 bytes making sure no doubling up on receiving
def send_message(conn, message):
    length = len(message)
    conn.sendall(struct.pack('!I', length))
    conn.sendall(message)


# receives the message and connects the messages together
def receive_message(conn):
    length_buf = receive_all(conn, 4)
    length, = struct.unpack('!I', length_buf)
    return receive_all(conn, length)


def receive_all(sock, count):
    buf = b''
    while count:
        new_buf = sock.recv(count)
        if not new_buf: 
            return None
        buf += new_buf
        count -= len(new_buf)
    return buf
