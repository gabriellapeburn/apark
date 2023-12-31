#!/usr/bin/env python3

#ROS2 library imports
import rclpy
from rclpy.node import Node

#System imports - not always used but necessary sometimes
import sys
import os

#Import the interfaces here
#for example, using the Header msg from the std_msgs package
from geometry_msgs.msg import Wrench
from sensor_msgs.msg import Imu

#Define your class - use package name with camel case capitalization
class PubSubPython(Node):
    #Initialize the class
    def __init__(self):
        #Create the node with whatever name (package name + node)
        super().__init__('force_torque_control starlink_controller')

        #Define the publishers here
        self.drive_pub_ = self.create_publisher(clearpath_platform_msgs/msg/Drive, '/cmd_vel', 10)

        #Define the subscribers here
        self.Imu_sub_ = self.create_subscription(Imu_data, '/Imu/data', self.Imu_callback, 10)
        self.des_speed_sub_ = self.create_subscription(Setpoint/speed, '/desired_speed', self.des_speed_callback, 10)
        self.des_head_sub_ = self.create_subscription(Setpoint/heading, '/desired_heading', self.des_headong_callback, 10)
        
        #Variable to track the current time
        self.current_time = self.get_clock().now()

        #Set the timer period and define the timer function that loops at the desired rate
        time_period = 1/10
        self.time = self.create_timer(time_period, self.timer_callback)

# This is the timer function that runs at the desired rate from above
    def timer_callback(self):

    #     #This is an example on how to create a message, fill in the header information and add some data, then publish
        self.Setpoint = SetpointStamped()
        self.Setpoint.speed.stamp = self.get_clock().now().to_msg()
        # self.twist_msg.twist.linear.x = 10.0
        # self.twist_pub_.publish(self.twist_msg)

        # #This is how to keep track of the current time in a ROS2 node
        self.current_time = self.get_clock().now()

    #Put your callback functions here - these are run whenever the node loops and when there are messages available to process.
    def feedback_callback(self, msg):
        feedback = msg.data

        #This is an example on how to compare the current time to the time in a message
        #This next line subtracts the two times, converts to nanoseconds then puts it in seconds and checks if its greater than 5 seconds
        d_time = (self.get_clock().now()-self.current_time).nanoseconds*(10**-9)

    def PID(Kp, Ki, Kd, desired_heading, actual_heading):
        error = desired_heading - actual_heading #i think we want to control the aacceleration but I am not sure about attitude
        Kp = 1
        Ki = 0
        Kd = 0
        p = Kp*error
        i = Ki*error*(d_time)
        d = Kd*error/(d_time)
        controller = p + i + d

#This is some boiler plate code that you slap at the bottom to make the node work.
#Make sure to update the name of the function and package to match your node
def main(args=None):
    rclpy.init(args=args)

    starlink_controller = PubSubPython()
    rclpy.spin(starlink_controller)
    starlink_controller.destroy_node()
    rclpy.shutdown()

if __name__ == 'main':
    main()
