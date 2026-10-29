import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math

def euler_from_quaternion(x, y, z, w):
    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    return math.atan2(t3, t4)

class TrajectoryNode(Node):
    def __init__(self):
        super().__init__('trajectory_node')
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.odom_sub = self.create_subscription(
            Odometry, 
            '/odometry/filtered', 
            self.odom_callback, 
            10
        )
        self.desired_pub = self.create_publisher(Odometry, '/desired_state', 10)
        self.timer = self.create_timer(0.05, self.control_loop)
        
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.t = 0.0
        self.a = 2.0
        self.w = 0.1

    def odom_callback(self, msg):
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y
        q = msg.pose.pose.orientation
        self.theta = euler_from_quaternion(q.x, q.y, q.z, q.w)

    def control_loop(self):
        self.t += 0.05
        xd = self.a * math.sin(self.w * self.t)
        yd = self.a * math.sin(2 * self.w * self.t) / 2.0
        
        dxd = self.a * self.w * math.cos(self.w * self.t)
        dyd = self.a * self.w * math.cos(2 * self.w * self.t)
        thetad = math.atan2(dyd, dxd)
        
        des_msg = Odometry()
        des_msg.header.stamp = self.get_clock().now().to_msg()
        des_msg.header.frame_id = 'odom'
        des_msg.pose.pose.position.x = xd
        des_msg.pose.pose.position.y = yd
        self.desired_pub.publish(des_msg)
        
        k_v = 1.0
        k_w = 2.0
        ex = xd - self.x
        ey = yd - self.y
        
        v = k_v * (ex * math.cos(self.theta) + ey * math.sin(self.theta))
        e_theta = math.atan2(math.sin(thetad - self.theta), math.cos(thetad - self.theta))
        w_cmd = k_w * e_theta
        
        cmd = Twist()
        cmd.linear.x = v
        cmd.angular.z = w_cmd
        self.cmd_pub.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    node = TrajectoryNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
