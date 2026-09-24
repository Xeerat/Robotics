from geometry_msgs.msg import Twist


def choose_command(pose):
    """Чистая функция: возвращает команду на основе позы."""
    twist = Twist()
    if pose is None:
        twist.linear.x = 0.0
        twist.angular.z = 0.0
    else:
        twist.linear.x = 0.5
        twist.angular.z = 0.3
    return twist
