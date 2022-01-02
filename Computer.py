class Computer:
    def __init__(self, socket, cores, ip: str, port: int):
        self._cores: int = int(cores)
        self._socket = socket
        self._ip: str = ip
        self._port = port

    def __str__(self):
        return f"({self._ip},{self._port}) \n {self.cores}"

    @property
    def port(self) -> int:
        return self._port

    @property
    def ip(self) -> str:
        return self._ip

    @property
    def cores(self) -> int:
        return self._cores

    @property
    def socket(self):
        return self._socket
