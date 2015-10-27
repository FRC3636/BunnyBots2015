import wpilib
import select
import socket
import threading
import struct

UDP_PORT = 1234
TCP_PORT = 1235

def encode_gyro(value):
    return struct.pack('>Bf', 0, value)

class Dashboard:
    def __init__(self):
        self.sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.tcp_listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcp_listener.bind(('0.0.0.0', TCP_PORT))
        self.tcp_listener.listen(1)
        self.computer_addr = None
        self.conn = None
        def connect_loop():
            while True:
                conn, addr = self.tcp_listener.accept()
                self.conn = conn
                self.conn.setblocking(False)
                self.computer_addr = addr[0]
                print("Got connection from {}".format(addr))
        t = threading.Thread(target=connect_loop)
        t.daemon = True
        t.start()

    def send_udp(self, message):
        if self.computer_addr is not None:
            self.sock_udp.sendto(message, (self.computer_addr, UDP_PORT))

    def get_msg(self):
        if self.conn is not None:
            inputs = [self.conn]
            input_ready, output_ready, errors = select.select(inputs, [], [])
            for sock in input_ready:
                data = sock.recv(1024)
                if data:
                    print(data)
