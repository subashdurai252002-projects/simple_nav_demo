import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose2D
from std_msgs.msg import String


class MissionNode(Node):
    def __init__(self):
        super().__init__('mission_node')

        self.goal_publisher = self.create_publisher(Pose2D, '/goal_pose', 10)
        self.status_subscriber = self.create_subscription(
            String,
            '/nav_status',
            self.status_callback,
            10
        )

        self.goals = [
            ('A', 2.0, 0.0, 0.0),
            ('B', 2.0, 2.0, 0.0),
            ('Origin', 0.0, 0.0, 0.0)
        ]

        self.current_goal_index = 0
        self.waiting_for_reached = False

        self.timer = self.create_timer(1.0, self.start_mission)

        self.get_logger().info('Mission node started')

    def start_mission(self):
        if not self.waiting_for_reached and self.current_goal_index < len(self.goals):
            self.publish_goal()
            self.waiting_for_reached = True
            self.timer.cancel()

    def publish_goal(self):
        name, x, y, theta = self.goals[self.current_goal_index]

        msg = Pose2D()
        msg.x = x
        msg.y = y
        msg.theta = theta

        self.goal_publisher.publish(msg)
        self.get_logger().info(f'Published goal: {name} ({x}, {y})')

    def status_callback(self, msg):
        if msg.data == 'reached' and self.waiting_for_reached:
            reached_name = self.goals[self.current_goal_index][0]
            self.get_logger().info(f'Reached goal: {reached_name}')

            self.current_goal_index += 1
            self.waiting_for_reached = False

            if self.current_goal_index < len(self.goals):
                self.publish_goal()
                self.waiting_for_reached = True
            else:
                self.get_logger().info('Mission completed')


def main(args=None):
    rclpy.init(args=args)
    node = MissionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
