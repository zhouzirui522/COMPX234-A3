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