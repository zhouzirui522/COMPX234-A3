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

    def create_request(self, line):
        parts = line.split()
        if len(parts) < 2:
            print(f"Invalid operation: {line}")
            return None

        op = parts[0].upper()
        key = parts[1]

        if op == 'PUT':
            if len(parts) < 3:
                print(f"PUT requires a value: {line}")
                return None
            value = ' '.join(parts[2:])
            if len(key) + len(value) > 970:
                print(f"Key-value pair too long: {line}")
                return None
            request = f"P {key} {value}"
        elif op in ['READ', 'GET']:
            request = f"{op[0]} {key}"
        else:
            print(f"Unknown operation: {op}")
            return None

        size = len(request) + 4  # 3 for NNN + 1 for space
        return f"{size:03d} {request}"

    def send_request(self, sock, request, original_line):
        try:
            sock.sendall(request.encode())
            response = sock.recv(1024).decode()
            if not response:
               print(f"No response for: {original_line}")
               return

            response_size = int(response[:3])
            response_msg = response[4:]

            print(f"{original_line}: {response_msg}")

        except Exception as e:
            print(f"Error processing {original_line}: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python client.py <host> <port> <request_file>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    file_path = sys.argv[3]

    client = TupleSpaceClient(host, port, file_path)
    client.run()

