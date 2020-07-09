import argparse
import socket
import sys
import ipaddress


class MySocket:
    
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
        self.sock.settimeout(5.0)

    
    def checkIP(self, host):
        try:
            ipaddress.ip_address(host)
        except ValueError:
            sys.exit("\nError: Inavlid IP Address")


    def checkPort(self, port):
        if port not in range(65536):
            sys.exit("\nError: Invalid Port Number")
    

    def connect(self, host, port=6653):
        print("\n\n[*] Establishing a connection...")
        try:
            self.sock.connect((host, port))
            print("\nConnected")
        except InterruptedError:
            print("\nConnection Interrupted")
    
    def sendData(self):
        print("\n\n[*] Sending data...")
        MSG = bytearray(b'\xf0\x00\x00\x14\x00')
        try:
            sent = self.sock.sendall(MSG)
        except InterruptedError:
            print("\nConnection Interrupted")
        if sent is None:
            print("\nData sent")
        else:
            raise RuntimeError("\nSocket Connection Broken")
    
    def receiveData(self):
        print("\n\n[*] Receiving data...")
        try:
            bytes_received = self.sock.recv(2048)
        except InterruptedError:
            print("\nConnection Interrupted")
        if bytes_received != b'':
            print("\nData received: ", bytes_received[:2])
        else:
            raise RuntimeError("\nSocket Connection Broken")

    def closeConnection(self):
        self.sock.close()
        print("\n\nConnection closed")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("ipaddress", help="Target IP address")
    parser.add_argument("-p", "--port", help="Target port")

    args = parser.parse_args()

    host = args.ipaddress

    new_socket = MySocket()

    new_socket.checkIP(host)

    if args.port is not None:
        port_number = int(args.port)
        new_socket.checkPort(port_number)
        new_socket.connect(host, port_number)
    else:
        new_socket.connect(host)

    new_socket.sendData()
    new_socket.receiveData()
    new_socket.closeConnection()


if __name__ == "__main__":
    main()