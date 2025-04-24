import socket
import sys

class TupleSpaceClient:
    def __init__(self, host, port, file_path):
        self.host = host
        self.port = port
        self.file_path = file_path

    def run(self):
        try:
            with open(self.file_path, 'r') as file:
                operations = file.readlines()

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.host, self.port))

                for line in operations:
                    line = line.strip()
                    if not line:
                        continue

                    request = self.create_request(line)
                    if request:
                        self.send_request(s, request, line)

        except Exception as e:
            print(f"Client error: {e}")