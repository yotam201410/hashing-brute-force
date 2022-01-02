import socket
import threading
from typing import *

import select
import msvcrt
from Computer import Computer

MAX_MSG_LENGTH = 1024  # KB of data to transfer.
SERVER_PORT = 5555
SERVER_IP = '10.168.63.118'  # this computer IP.
MIN = 10 ** 9  # minimal search zone.
MAX = 10 ** 10  # maximal search zone.


def get_computer(computers: List[Computer], __socket):  # creating Computer object.
    host, port = __socket.getpeername()
    for __computer in computers:
        if __computer.port == port and host == __computer.ip:
            return __computer
    return None


def print_result(computer: Computer, __socket):  # The result from a thread will be send here.
    result = __socket.recv(MAX_MSG_LENGTH).decode()
    print("RESULT " + result)
    print(f"The Result, {result}, Found At {computer}")


def main():
    print("[+] Setting Up Server...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen()
    print("[+] Listening For Clients...")
    computers_connected = []
    client_sockets = []
    messages_to_send = []
    while not msvcrt.kbhit():  # letting clients to connect until something pressed.
        rlist, wlist, xlist = select.select([server_socket] + client_sockets, client_sockets, [])
        for current_socket in rlist:
            if current_socket is server_socket:
                connection, client_address = current_socket.accept()
                print("[+] New Client Joined!", client_address)
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
    print(f"The Amount Of Possible Numbers Per Thread Is: {amount_of_numbers_per_thread}")

    for __socket in wlist:  # giving numbers per thread per computer cores.
        computer = get_computer(computers_connected, __socket)
        __socket.send(str(amount_of_numbers_per_thread).encode())
        __socket.send(str(current_range).encode())
        current_range += amount_of_numbers_per_thread * computer.cores
        threading.Thread(target=print_result, args=(computer, __socket)).start()


if __name__ == '__main__':
    main()
