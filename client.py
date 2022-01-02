import socket
import multiprocessing
import threading
import hashlib
from typing import List

AMOUNT_OF_CORES = multiprocessing.cpu_count()
IP = "10.168.63.118"
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
        


def main():
    c = socket.socket()
    c.connect((IP, PORT))
    print("Connected")
    c.send(str(AMOUNT_OF_CORES).encode())
    message = c.recv(MAX_BYTES).decode()
    amount_of_numbers = int(float(c.recv(MAX_BYTES).decode()))
    start_point = int(float(c.recv(MAX_BYTES).decode()))
    threads = []
    print(f"{start_point} - {start_point + AMOUNT_OF_CORES*amount_of_numbers}")
    results = [None] * AMOUNT_OF_CORES
    for i in range(AMOUNT_OF_CORES):
        thread = threading.Thread(target=looping_found,
                                  args=(start_point + i * amount_of_numbers, (i + 1) * amount_of_numbers + start_point, i,
                                        c, results))
        thread.start()
        threads.append(thread)
    print("GOT TO HERE")
    while True:
        for _thread in threads:
            if not _thread.is_alive():
                del threads
                return None


if __name__ == "__main__":
    main()
