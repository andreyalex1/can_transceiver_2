#!/usr/bin/env python3

#Developed by Andrei Smirnov. 2024
#MSU Rover Team. Voltbro. NIIMech 

import os
import can
import numpy as np
import rclpy
from rclpy.node import Node

from std_msgs.msg import UInt8MultiArray
import atexit

def exit_handler():
    os.system('ip link set can0 down')



    
class can_transceiver(Node):

    def __init__(self):
        os.system('ip link set can0 up type can bitrate 1000000 restart-ms 1000')
        os.system('ip link set can0 txqueuelen 10000')
        self.can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan')  # socketcan_native
        super().__init__('can_transceiver')
        self.pub = self.create_publisher(UInt8MultiArray, '/can_rx', 10)
        self.sub = self.create_subscription(UInt8MultiArray, '/can_tx', self.callback, 10)
        timer_period = 0.002  # seconds
        self.timer = self.create_timer(timer_period, self.spin)
        self.get_logger().info("CAN Started!")
    def __del__(self):
        self.get_logger().info("CAN Killed!")
    def callback(self, msg):
      #  if(msg.data[0] == 12):
    #    try:
        send = can.Message(arbitration_id = msg.data[0],data = msg.data[1:9] , is_extended_id=False)
        self.can0.send(send)
        print(msg.data)
     #   except Exception as e :
      #      self.get_logger().error(str(e))
    def spin(self):
        arr = UInt8MultiArray()
        msg = self.can0.recv(10.0)
        if((msg is not  None) and(0 <= int(msg.arbitration_id) < 256 ) and all(0 <= int(item) < 256 for item in msg.data)):
            arr.data = bytearray([msg.arbitration_id]) + bytearray(msg.data)
            self.pub.publish(arr)   


def main(args=None):
    atexit.register(exit_handler)
    rclpy.init()
    ct = can_transceiver()
    rclpy.spin(ct)

    
    ct.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()