#!/usr/bin/env python3

#Developed by Andrei Smirnov. 2024
#MSU Rover Team. Voltbro. NIIMech 

import os
import can
import numpy as np
import rclpy
from rclpy.node import Node

from std_msgs.msg import UInt8MultiArray


class can_transceiver(Node):

    def __init__(self):
        os.system('ip link set can1 up type can bitrate 1000000 restart-ms 1000')
        self.can0 = can.interface.Bus(channel = 'can1', bustype = 'socketcan')  # socketcan_native
        super().__init__('can_transceiver')
        self.pub = self.create_publisher(UInt8MultiArray, 'can_rx', 10)
        self.sub = self.create_subscription(UInt8MultiArray, 'can_tx', self.callback, 10)
        timer_period = 0.002  # seconds
        self.timer = self.create_timer(timer_period, self.spin)
        self.get_logger().info("CAN Started!")
    def __del__(self):
        os.system('ifconfig can1 down')
        self.get_logger().info("CAN Killed!")
    def callback(self, data):
        send = can.Message(arbitration_id = msg.data[0],data = msg.data[1:9] , extended_id=False)
        self.can0.send(send)
    def spin(self):
        arr = UInt8MultiArray()
        msg = self.can0.recv(10.0)
        if(msg is not  None):
            arr.data = bytearray([msg.arbitration_id]) + bytearray(msg.data)
            self.pub.publish(arr)   


def main(args=None):
    rclpy.init()
    ct = can_transceiver()
    rclpy.spin(ct)


    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()