import socket
import select
import threading
import hashlib

import msvcrt
while not msvcrt.kbhit():
    pass