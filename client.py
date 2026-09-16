import argparse
import sys
import socket, struct

###########################################################
####################### YOUR CODE #########################
###########################################################


def send_data(server_ip, server_port, data: bytes):
    '''
    Send data to server in address (server_ip, server_port).
    '''

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, server_port))
    # packed_message = struct.pack(f"<I{len(data)}s", len(data), data.encode())
    header = struct.pack("<I", len(data))
    client.sendall(header + data)


###########################################################
##################### END OF YOUR CODE ####################
###########################################################


def get_args():
    parser = argparse.ArgumentParser(description='Send data to server.')
    parser.add_argument('server_ip', type=str,
                        help="the server's ip")
    parser.add_argument('server_port', type=int,
                        help="the server's port")
    parser.add_argument('data', type=str,
                        help="the data")
    return parser.parse_args()


def main():
    '''
    Implementation of CLI and sending data to server.
    '''
    args = get_args()
    try:
        send_data(args.server_ip, args.server_port, args.data.encode())
        print('Done.')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
