import argparse
import sys
import socket, struct
import threading

def recv_exactly(serv, length: int):
    """
    Helper function to recieve an exact amount of bytes
    """
    buffer = bytearray()
    while len(buffer) < length:
        chunk = serv.recv(length - len(buffer)) # Recieve the expeceted amount of bytes left
        if not chunk:
            return None  # remote end closed the connection
        buffer.extend(chunk)
    return bytes(buffer)

def handle_conn(conn: socket, addr: tuple):
    """
    Function to be run on a thread to handle communication with a client
    Closes the connection at the end of the communication
    Expecting a 4 byte header for the length of the message, then the message data
    """
    length_buffer = recv_exactly(conn, 4)
    if (length_buffer is None):
        conn.close()
        return
    length = struct.unpack('<I', length_buffer)[0]

    # Recieve the message with the exact expected length
    data =  recv_exactly(conn, length)
    if not data:
        conn.close()
        return

    print(f"Recieved data: {data.decode('utf-8')}")
    conn.close()
    # print(f'{addr} left.')

def run_server(ip, port):
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv.bind((ip, port))
    serv.listen(5)
    while True:
        conn, addr = serv.accept()
        if not (conn is None):
            t = threading.Thread(target=handle_conn, args=(conn, addr))
            t.start()



def get_args():
    parser = argparse.ArgumentParser(description='Send data to server.')
    parser.add_argument('ip', type=str,
                        help="the ip to listen on")
    parser.add_argument('port', type=int,
                        help="the port to listen on")
    return parser.parse_args()


def main():
    '''
    Implementation of CLI and recieving data from clients.
    '''
    args = get_args()
    try:
        run_server(args.ip, args.port)
        print('Done.')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
