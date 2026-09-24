from geometry_msgs.msg import Twist
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose

from .command import choose_command


class PatrolNode(Node):
    def __init__(self):
        super().__init__('patrol')
        self.last_pose = None
        self.pose_sub = self.create_subscription(
            Pose, '/turtle1/pose', self._on_pose, 10)
        self.cmd_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.timer = self.create_timer(0.1, self._on_timer)

    def _on_pose(self, msg):
        self.last_pose = msg

    def _on_timer(self):
        twist = choose_command(self.last_pose)
        self.cmd_pub.publish(twist)


def main(args=None):
    rclpy.init(args=args)
    node = PatrolNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
