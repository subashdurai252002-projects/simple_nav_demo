import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose2D
from std_msgs.msg import String


class NavigatorNode(Node):
    def __init__(self):
        super().__init__('navigator_node')

        self.goal_subscriber = self.create_subscription(
            Pose2D,
            '/goal_pose',
            self.goal_callback,
            10
        )

        self.status_publisher = self.create_publisher(String, '/nav_status', 10)

        self.get_logger().info('Navigator node started')

    def goal_callback(self, msg):
        self.get_logger().info(f'Received goal: x={msg.x}, y={msg.y}, theta={msg.theta}')

        status_msg = String()
        status_msg.data = 'reached'
        self.status_publisher.publish(status_msg)

        self.get_logger().info('Published status: reached')


def main(args=None):
    rclpy.init(args=args)
    node = NavigatorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
