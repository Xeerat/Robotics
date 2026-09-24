from patrol.command import choose_command
from turtlesim.msg import Pose


def test_no_pose_returns_zero():
    t = choose_command(None)
    assert t.linear.x == 0.0 and t.angular.z == 0.0


def test_with_pose_returns_motion():
    pose = Pose()
    pose.x = 1.0
    pose.y = 2.0
    t = choose_command(pose)
    assert t.linear.x == 0.5
    assert t.angular.z == 0.3
