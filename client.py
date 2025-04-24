import socket
import sys

class TupleSpaceClient:
    def __init__(self, host, port, file_path):
        self.host = host
        self.port = port
        self.file_path = file_path