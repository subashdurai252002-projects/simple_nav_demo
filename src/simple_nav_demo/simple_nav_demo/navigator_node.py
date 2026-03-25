import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, Pose2D
from std_msgs.msg import String


class NavigatorNode(Node):
    def __init__(self):
        super().__init__('navigator_node')

        self.pose_sub = self.create_subscription(
            Pose2D,
            '/robot_pose',
            self.pose_callback,
            10
        )

        self.goal_sub = self.create_subscription(
            Pose2D,
            '/goal_pose',
            self.goal_callback,
            10
        )

        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.status_pub = self.create_publisher(String, '/nav_status', 10)

        self.current_pose = None
        self.goal_pose = None

        self.last_goal = None
        self.last_status = None

        self.timer = self.create_timer(0.1, self.control_loop)

        self.get_logger().info('Navigator node started')

    def pose_callback(self, msg):
        self.current_pose = msg

    def goal_callback(self, msg):
        self.goal_pose = msg

        current_goal = (msg.x, msg.y)
        if current_goal != self.last_goal:
            self.get_logger().info(f'Received goal: x={msg.x}, y={msg.y}')
            self.last_goal = current_goal

    def control_loop(self):
        if self.current_pose is None or self.goal_pose is None:
            return

        dx = self.goal_pose.x - self.current_pose.x
        dy = self.goal_pose.y - self.current_pose.y
        distance = math.sqrt(dx**2 + dy**2)

        cmd = Twist()
        status = String()

        if distance < 0.05:
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0
            status.data = 'reached'
        else:
            angle_to_goal = math.atan2(dy, dx)
            angle_error = angle_to_goal - self.current_pose.theta

            # normalize angle to [-pi, pi]
            angle_error = math.atan2(math.sin(angle_error), math.cos(angle_error))

            cmd.linear.x = min(0.5 * distance, 0.5)
            cmd.angular.z = 2.0 * angle_error
            status.data = 'moving'

        self.cmd_pub.publish(cmd)
        self.status_pub.publish(status)

        if status.data != self.last_status:
            self.get_logger().info(f'Status: {status.data}')
            self.last_status = status.data


def main(args=None):
    rclpy.init(args=args)
    node = NavigatorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
