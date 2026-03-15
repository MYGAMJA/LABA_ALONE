import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys, select, termios, tty

move_bindings = {
    'w': (0.5, 0.0),
    's': (-0.5, 0.0),
    'a': (0.0, 1.0),
    'd': (0.0, -1.0),
    ' ': (0.0, 0.0),
}

def get_key(settings):
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0.1)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

class TeleopNode(Node):

    def __init__(self):
        super().__init__('keyboard_cmd_vel')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.get_logger().info("WASD 키로 로봇을 조종합니다")

    def publish_twist(self, lx, az):
        msg = Twist()
        msg.linear.x = lx
        msg.angular.z = az
        self.publisher_.publish(msg)

def main():
    settings = termios.tcgetattr(sys.stdin)
    rclpy.init()
    node = TeleopNode()

    try:
        while True:
            key = get_key(settings)
            if key in move_bindings:
                lx, az = move_bindings[key]
                node.publish_twist(lx, az)
                print(f"입력: {key} | linear {lx} angular {az}")
            elif key == '\x03':
                break
    finally:
        node.publish_twist(0.0, 0.0)
        node.destroy_node()
        rclpy.shutdown()
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

if __name__ == '__main__':
    main()