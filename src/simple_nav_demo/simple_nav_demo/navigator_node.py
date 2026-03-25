import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose2D, Twist
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

        self.pose_subscriber = self.create_subscription(
            Pose2D,
            '/robot_pose',
            self.pose_callback,
            10
        )

        self.cmd_publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.status_publisher = self.create_publisher(String, '/nav_status', 10)

        self.current_goal = None
        self.current_pose = None
        self.goal_reached = True

        self.control_timer = self.create_timer(0.1, self.control_loop)

        self.get_logger().info('Navigator node started')

    def goal_callback(self, msg):
        self.current_goal = msg
        self.goal_reached = False
        self.get_logger().info(
            f'Received goal: x={msg.x}, y={msg.y}, theta={msg.theta}'
        )

    def pose_callback(self, msg):
        self.current_pose = msg

    def control_loop(self):
        if self.current_goal is None or self.current_pose is None or self.goal_reached:
            return

        dx = self.current_goal.x - self.current_pose.x
        dy = self.current_goal.y - self.current_pose.y
        distance = math.sqrt(dx * dx + dy * dy)

        cmd = Twist()

        if distance < 0.1:
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0
            self.cmd_publisher.publish(cmd)

            status_msg = String()
            status_msg.data = 'reached'
            self.status_publisher.publish(status_msg)

            self.goal_reached = True
            self.get_logger().info('Published status: reached')
            return

        target_angle = math.atan2(dy, dx)
        angle_error = target_angle - self.current_pose.theta
        angle_error = math.atan2(math.sin(angle_error), math.cos(angle_error))

        if abs(angle_error) > 0.1:
            cmd.linear.x = 0.0
            cmd.angular.z = 0.8 * angle_error
        else:
            cmd.linear.x = min(0.5 * distance, 0.5)
            cmd.angular.z = 0.5 * angle_error

        self.cmd_publisher.publish(cmd)

        status_msg = String()
        status_msg.data = 'moving'
        self.status_publisher.publish(status_msg)


def main(args=None):
    rclpy.init(args=args)
    node = NavigatorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
