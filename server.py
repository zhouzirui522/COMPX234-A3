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