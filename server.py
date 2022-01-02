import socket
import threading
from typing import *

import select
import msvcrt
from Computer import Computer

MAX_MSG_LENGTH = 1024
SERVER_PORT = 5555
SERVER_IP = '192.168.1.106'
MIN = 10 ** 9
MAX = 10 ** 10


def get_computer(computers: List[Computer], __socket) -> Computer | None:
    host, port = __socket.getpeername()
    for __computer in computers:
        if __computer.port == port and host == __computer.ip:
            return __computer
    return None


def print_result(computer: Computer, __socket):
    result = __socket.recv(MAX_MSG_LENGTH).decode()
    print("RESULT " + result)
    print(f"{__socket.recv(MAX_MSG_LENGTH).decode()} found at {computer}")


def main():
    print("Setting up server...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen()
    print("Listening for clients...")
    computers_connected = []
    client_sockets = []
    messages_to_send = []
    while not msvcrt.kbhit():
        rlist, wlist, xlist = select.select([server_socket] + client_sockets, client_sockets, [])
        for current_socket in rlist:
            if current_socket is server_socket:
                connection, client_address = current_socket.accept()
                print("New client joined!", client_address)
                client_sockets.append(connection)
            else:
                data = current_socket.recv(MAX_MSG_LENGTH).decode()
                if data == "":
                    pass
                else:
                    computers_connected.append(
                        Computer(socket, data, current_socket.getpeername()[0], current_socket.getpeername()[1]))
                    messages_to_send.append((current_socket, data))
        for message in messages_to_send:
            current_socket, data = message
            if current_socket in wlist:
                current_socket.send(data.encode())
                messages_to_send.remove(message)
    amount_of_available_cores = sum([int(x.cores) for x in computers_connected])
    amount_of_numbers_per_thread = (MAX - MIN) / amount_of_available_cores
    current_range = MIN
    print(amount_of_numbers_per_thread)

    for i, __socket in enumerate(wlist):
        computer = get_computer(computers_connected, __socket)
        __socket.send(str(amount_of_numbers_per_thread).encode())
        __socket.send(str(current_range).encode())
        current_range += amount_of_numbers_per_thread * computer.cores
        threading.Thread(target=print_result, args=(computer, __socket)).start()


if __name__ == '__main__':
    main()
