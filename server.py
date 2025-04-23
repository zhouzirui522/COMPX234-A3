import socket
import threading
from datetime import datetime, timedelta

class TupleSpaceServer:
    def __init__(self, port):
        self.port = port
        self.tuple_space = {}  # Dictionary to store key-value pairs
        self.lock = threading.Lock()  # Lock for thread-safe operations
        self.stats = {
            'total_clients': 0,
            'total_ops': 0,
            'reads': 0,
            'gets': 0,
            'puts': 0,
            'errors': 0
        }
        self.last_stats_time = datetime.now()

        def start(self):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('', self.port))
                    s.listen()
                    print(f"Server started on port {self.port}")

                    while True:
                        conn, addr = s.accept()
                        self.stats['total_clients'] += 1
                        client_thread = threading.Thread(
                            target=self.handle_client,
                            args=(conn, addr)
                        )
                        client_thread.start()
            except Exception as e:
                print(f"Server error: {e}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])
    server = TupleSpaceServer(port)
    server.start()


    def handle_client(self, conn, addr):
        print(f"New connection from {addr}")
        try:
            with conn:
                while True:
                    data = conn.recv(1024).decode()
                    if not data:
                        break

                    response = self.process_request(data)
                    conn.sendall(response.encode())
        except Exception as e:
            print(f"Error with client {addr}: {e}")
        finally:
            print(f"Connection from {addr} closed")

            def process_request(self, request):
                self.stats['total_ops'] += 1
                self.print_stats_if_needed()

                try:
                    parts = request.split()
                    if len(parts) < 3:
                        return self.format_error("Invalid request format")

                    size = int(parts[0])
                    op = parts[1].upper()
                    key = parts[2]

                    if op == 'R':  # READ operation
                        return self.handle_read(key)
                    elif op == 'G':  # GET operation
                        return self.handle_get(key)
                    elif op == 'P':  # PUT operation
                        if len(parts) < 4:
                            return self.format_error("PUT requires a value")
                        value = ' '.join(parts[3:])
                        return self.handle_put(key, value)
                    else:
                        return self.format_error("Unknown operation")

                except Exception as e:
                    self.stats['errors'] += 1
                    return self.format_error(str(e))

    def handle_read(self, key):
        self.stats['reads'] += 1
        with self.lock:
            if key in self.tuple_space:
                value = self.tuple_space[key]
                return self.format_ok_read(key, value)
            else:
                self.stats['errors'] += 1
                return self.format_error(f"{key} does not exist")


    def handle_get(self, key):
        self.stats['gets'] += 1
        with self.lock:
            if key in self.tuple_space:
                value = self.tuple_space.pop(key)
                return self.format_ok_removed(key, value)
            else:
                self.stats['errors'] += 1
                return self.format_error(f"{key} does not exist")


    def handle_put(self, key, value):
        self.stats['puts'] += 1
        if len(key) + len(value) > 970:
            self.stats['errors'] += 1
            return self.format_error("Key-value pair too long")

        with self.lock:
            if key in self.tuple_space:
                self.stats['errors'] += 1
                return self.format_error(f"{key} already exists")
            else:
                self.tuple_space[key] = value
                return self.format_ok_added(key, value)

