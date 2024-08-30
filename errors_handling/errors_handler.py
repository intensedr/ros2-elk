from rclpy.node import Node
import socket
import json
import traceback
import sys

class ErrorHandler:
    def __init__(self, host='localhost', port=5044):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

    def log_error(self, error_msg, exception=None):
        log_entry = {
            "message": f"ROS_ERROR: {error_msg}",
            "severity": "error",
            "exception": str(exception) if exception else None,
            "traceback": traceback.format_exc() if exception else None
        }
        self.sock.sendall((json.dumps(log_entry) + "\n").encode('utf-8'))

    def close(self):
        self.sock.close()

    def handle_exception(self, exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        self.log_error("Unhandled exception", exc_value)
        self.close()


def setup_error_handler():
    error_handler = ErrorHandler()
    sys.excepthook = error_handler.handle_exception
    return error_handler