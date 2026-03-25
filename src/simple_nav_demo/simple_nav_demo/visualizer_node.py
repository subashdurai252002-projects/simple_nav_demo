import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose2D
from std_msgs.msg import String

import matplotlib.pyplot as plt


class VisualizerNode(Node):
    def __init__(self):
        super().__init__('visualizer_node')

        # subscribers
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

        self.status_sub = self.create_subscription(
            String,
            '/nav_status',
            self.status_callback,
            10
        )

        # current robot pose
        self.current_x = 0.0
        self.current_y = 0.0
        self.current_theta = 0.0

        # current goal
        self.goal_x = 0.0
        self.goal_y = 0.0

        # mission status
        self.status = 'waiting'

        # exact waypoint path for clean graph
        self.path_x = [0.0]
        self.path_y = [0.0]

        # avoid duplicate waypoint entries
        self.last_added_point = (0.0, 0.0)

        # cleaner terminal output
        self.last_status = None
        self.last_goal = None

        # matplotlib setup
        plt.ion()
        self.fig, self.ax = plt.subplots()

        # update graph periodically
        self.timer = self.create_timer(0.1, self.update_plot)

        self.get_logger().info('Visualizer node started')

    def pose_callback(self, msg: Pose2D):
        self.current_x = msg.x
        self.current_y = msg.y
        self.current_theta = msg.theta

        self.path_x.append(msg.x)
        self.path_y.append(msg.y)

    def goal_callback(self, msg: Pose2D):
        self.goal_x = msg.x
        self.goal_y = msg.y

        # reset graph only when mission starts again from A
        if msg.x == 2.0 and msg.y == 0.0:
            self.path_x = [0.0]
            self.path_y = [0.0]
            self.last_added_point = (0.0, 0.0)

        goal_point = (msg.x, msg.y)


        if goal_point != self.last_goal:
            self.get_logger().info(f'New Goal → x={msg.x:.2f}, y={msg.y:.2f}')
            self.last_goal = goal_point

    def status_callback(self, msg: String):
        self.status = msg.data

        if self.status != self.last_status:
            self.get_logger().info(f'Status → {self.status}')
            self.last_status = self.status

    def update_plot(self):
        # if user closes plot window, stop node cleanly
        if not plt.fignum_exists(self.fig.number):
            rclpy.shutdown()
            return

        self.ax.clear()

        # fixed axis for clean graph
        self.ax.set_xlim(-0.2, 2.3)
        self.ax.set_ylim(-0.2, 2.3)
        self.ax.set_aspect('equal', adjustable='box')

        # exact mission path
        self.ax.plot(self.path_x, self.path_y, linewidth=2, label='Robot Path')

        # current robot position
        self.ax.plot(self.current_x, self.current_y, 'ro', label='Current Position')

        # current goal
        self.ax.plot(self.goal_x, self.goal_y, 'gx', markersize=10, label='Goal')

        # labels
        self.ax.text(0.0, 0.0, 'Origin (0,0)', fontsize=10, ha='right', va='top')
        self.ax.text(2.0, 0.0, 'A (2,0)', fontsize=10, ha='left', va='top')
        self.ax.text(2.0, 2.0, 'B (2,2)', fontsize=10, ha='left', va='bottom')

        self.ax.set_title(f'Robot Movement | Status: {self.status}')
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.grid(True)
        self.ax.legend()

        plt.draw()
        plt.pause(0.001)


def main(args=None):
    rclpy.init(args=args)
    node = VisualizerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
