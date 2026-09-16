import argparse
import sys
import socket, struct

# Helper function to recieve an exact amount of bytes
def recv_exactly(serv, length: int):
    buffer = bytearray()
    while len(buffer) < length:
        chunk = serv.recv(length - len(buffer)) # Recieve the expeceted amount of bytes left
        if not chunk:
            return None  # remote end closed the connection
        buffer.extend(chunk)
    return bytes(buffer)

def run_server(ip, port):
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv.bind((ip, port))
    serv.listen(5)
    while True:
        conn, addr = serv.accept()

        # Using the recv_exactly helper function, get the expected length of the message
        length_buffer = recv_exactly(conn, 4)
        if (length_buffer is None):
            break
        length = struct.unpack('<I', length_buffer)[0]

        # Recieve the message with the exact expected length
        data =  recv_exactly(conn, length)
        if not data: break

        print(f"Recieved data: {data.decode('utf-8')}")
        conn.close()
        # print(f'{addr} left.')



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
