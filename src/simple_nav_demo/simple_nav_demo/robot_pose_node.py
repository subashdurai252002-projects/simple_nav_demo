import rclpy
import math
from rclpy.node import Node

from geometry_msgs.msg import Twist, Pose2D


class RobotPoseNode(Node):

    def __init__(self):
        super().__init__('robot_pose_node')

        # initial position
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.linear_vel = 0.0
        self.angular_vel = 0.0
        # subscriber → /cmd_vel
        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_vel_callback,
            10
        )

        # publisher → /robot_pose
        self.publisher = self.create_publisher(
            Pose2D,
            '/robot_pose',
            10
        )

        # timer (publish pose regularly)
        self.timer = self.create_timer(0.1, self.update_pose)

    def cmd_vel_callback(self, msg):
        # store incoming velocity
        self.linear_vel = msg.linear.x
        self.angular_vel = msg.angular.z

    def update_pose(self):
        # simple motion update
        self.theta += self.angular_vel * 0.1
        self.x += self.linear_vel * math.cos(self.theta) * 0.1
        self.y += self.linear_vel * math.sin(self.theta) * 0.1

        pose = Pose2D()
        pose.x = self.x
        pose.y = self.y
        pose.theta = self.theta

        self.publisher.publish(pose)

        self.get_logger().info(f'Pose: x={self.x:.2f}, y={self.y:.2f}, theta={self.theta:.2f}')

def main(args=None):
    rclpy.init(args=args)
    node = RobotPoseNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()