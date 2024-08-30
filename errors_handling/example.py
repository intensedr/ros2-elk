#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from errors_handling.errors_handler import setup_error_handler


def main(args=None):
    rclpy.init(args=args)
    error_handler = setup_error_handler()

    try:
        rclpy.spin()
    except Exception as e:
        error_handler.log_error("Missing argument", e)
    finally:
        rclpy.shutdown()
        error_handler.close()


if __name__ == '__main__':
    main()
