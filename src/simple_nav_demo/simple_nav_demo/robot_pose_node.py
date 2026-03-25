import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, Pose2D


class RobotPoseNode(Node):
    def __init__(self):
        super().__init__('robot_pose_node')

        # robot state
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        # latest commanded velocities
        self.linear_vel = 0.0
        self.angular_vel = 0.0

        # subscribe to velocity command
        self.cmd_sub = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_vel_callback,
            10
        )

        # publish robot pose
        self.pose_pub = self.create_publisher(
            Pose2D,
            '/robot_pose',
            10
        )

        # timer for simulation update
        self.dt = 0.1
        self.timer = self.create_timer(self.dt, self.update_pose)

        self.get_logger().info('Robot pose node started')

    def cmd_vel_callback(self, msg: Twist):
        self.linear_vel = msg.linear.x
        self.angular_vel = msg.angular.z

    def update_pose(self):
        # update heading
        self.theta += self.angular_vel * self.dt
        self.theta = math.atan2(math.sin(self.theta), math.cos(self.theta))

        # update position
        self.x += self.linear_vel * math.cos(self.theta) * self.dt
        self.y += self.linear_vel * math.sin(self.theta) * self.dt

        pose = Pose2D()
        pose.x = self.x
        pose.y = self.y
        pose.theta = self.theta

        self.pose_pub.publish(pose)


def main(args=None):
    rclpy.init(args=args)
    node = RobotPoseNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
