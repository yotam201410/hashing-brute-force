import socket
import multiprocessing
import threading
import hashlib
from typing import List

AMOUNT_OF_CORES = multiprocessing.cpu_count()
IP = "192.168.1.106"
PORT = 5555
MAX_BYTES = 1024


def looping_found(start_value, end_value, thread, return_socket, results: List):
    print(f"thread {thread}\n start_value {start_value}\n end_value {end_value}")
    for i in range(start_value, end_value):
        hash_object = hashlib.md5(str(i).encode())
        hashed = hash_object.hexdigest()
        if hashed == "EC9C0F7EDCC18A98B1F31853B1813301".lower():
            print(f"{thread} Found")
            return_socket.send(str(i).encode())
            results[thread] = i
            return i
        if i == "3735928559":
            print("PROBLEM")
            raise AttributeError


def main():
    c = socket.socket()
    c.connect((IP, PORT))
    c.send(str(AMOUNT_OF_CORES).encode())
    message = c.recv(MAX_BYTES).decode()
    print(message)
    amount_of_numbers = int(float(c.recv(MAX_BYTES).decode()))
    start_point = int(float(c.recv(MAX_BYTES).decode()))
    threads = []
    results = [None] * AMOUNT_OF_CORES
    print(results)
    for i in range(AMOUNT_OF_CORES):
        thread = threading.Thread(target=looping_found,
                                  args=(3735928559 + i * amount_of_numbers, (i + 1) * amount_of_numbers + 3735928559, i,
                                        c, results))
        thread.start()
        threads.append(thread)
    print("GOT TO HEREE")
    while True:
        for _thread in threads:
            if not _thread.is_alive():
                del threads
                return None


if __name__ == "__main__":
    main()
