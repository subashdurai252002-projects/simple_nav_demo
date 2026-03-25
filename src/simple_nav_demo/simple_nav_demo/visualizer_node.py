import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Pose2D
from std_msgs.msg import String


class VisualizerNode(Node):

    def __init__(self):
        super().__init__('visualizer_node')

        # subscribe to robot pose
        self.create_subscription(
            Pose2D,
            '/robot_pose',
            self.robot_pose_callback,
            10
        )

        # subscribe to goal
        self.create_subscription(
            Pose2D,
            '/goal_pose',
            self.goal_callback,
            10
        )

        # subscribe to status
        self.create_subscription(
            String,
            '/nav_status',
            self.status_callback,
            10
        )

    def robot_pose_callback(self, msg):
        self.get_logger().info(
            f'Robot Pose → x={msg.x:.2f}, y={msg.y:.2f}, theta={msg.theta:.2f}'
        )

    def goal_callback(self, msg):
        self.get_logger().info(
            f'Goal → x={msg.x:.2f}, y={msg.y:.2f}'
        )

    def status_callback(self, msg):
        self.get_logger().info(
            f'Status → {msg.data}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = VisualizerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()