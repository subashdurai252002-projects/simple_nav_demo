import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose2D
from std_msgs.msg import String


class MissionNode(Node):
    def __init__(self):
        super().__init__('mission_node')

        self.goal_pub = self.create_publisher(Pose2D, '/goal_pose', 10)
        self.status_sub = self.create_subscription(
            String,
            '/nav_status',
            self.status_callback,
            10
        )

        self.goals = [
            ('A', 2.0, 0.0),
            ('B', 2.0, 2.0),
            ('Origin', 0.0, 0.0),
        ]

        self.current_goal_index = 0
        self.waiting_for_reached = False
        self.mission_done = False
        self.last_status = None

        self.timer = self.create_timer(0.5, self.publish_current_goal)

        self.get_logger().info('Mission node started')

    def publish_current_goal(self):
        if self.mission_done:
            return

        if self.current_goal_index >= len(self.goals):
            self.get_logger().info('Mission completed')
            self.mission_done = True
            return

        goal_name, x, y = self.goals[self.current_goal_index]

        goal_msg = Pose2D()
        goal_msg.x = x
        goal_msg.y = y
        goal_msg.theta = 0.0

        self.goal_pub.publish(goal_msg)

        if not self.waiting_for_reached:
            self.get_logger().info(f'Published goal: {goal_name} ({x}, {y})')
            self.waiting_for_reached = True

    def status_callback(self, msg):
        if msg.data == self.last_status:
            return

        self.last_status = msg.data

        if msg.data == 'reached' and self.waiting_for_reached:
            goal_name, _, _ = self.goals[self.current_goal_index]
            self.get_logger().info(f'Reached goal: {goal_name}')

            self.current_goal_index += 1
            self.waiting_for_reached = False

            if self.current_goal_index >= len(self.goals):
                self.get_logger().info('Mission completed')
                self.mission_done = True


def main(args=None):
    rclpy.init(args=args)
    node = MissionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
