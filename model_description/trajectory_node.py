import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import math

class Trajectory8Node(Node):
    def __init__(self):
        super().__init__('trajectory_8_node')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.t = 0.0

    def timer_callback(self):
        msg = Twist()
        Omega = 0.5
        msg.linear.x = 0.3
        msg.angular.z = 0.5 * math.cos(Omega * self.t)
        self.publisher_.publish(msg)
        self.t += 0.1

def main(args=None):
    rclpy.init(args=args)
    node = Trajectory8Node()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
