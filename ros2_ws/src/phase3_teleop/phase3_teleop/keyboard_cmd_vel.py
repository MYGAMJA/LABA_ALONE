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
    tty.setraw(KEY_INPUT.fileno())
    readable, _, _ = select.select([KEY_INPUT], [], [], 0.1)
    if readable:
        key = KEY_INPUT.read(1)
    else:
        key = ''
    termios.tcsetattr(KEY_INPUT, termios.TCSADRAIN, settings)
    return key


def resolve_key_input_stream():
    if sys.stdin.isatty():
        return sys.stdin
    try:
        return open('/dev/tty')
    except OSError:
        return None


KEY_INPUT = resolve_key_input_stream()

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
    rclpy.init()
    node = TeleopNode()
    if KEY_INPUT is None:
        node.get_logger().error('키보드 입력 TTY를 찾을 수 없습니다. 별도 터미널에서 teleop를 실행하세요.')
        node.destroy_node()
        rclpy.shutdown()
        return

    settings = termios.tcgetattr(KEY_INPUT)
    last_cmd = (0.0, 0.0)

    try:
        while True:
            key = get_key(settings)
            if key in move_bindings:
                lx, az = move_bindings[key]
                node.publish_twist(lx, az)
                last_cmd = (lx, az)
                print(f"입력: {key} | linear {lx} angular {az}")
            elif key == '':
                if last_cmd != (0.0, 0.0):
                    node.publish_twist(0.0, 0.0)
                    last_cmd = (0.0, 0.0)
            elif key == '\x03':
                break
    finally:
        node.publish_twist(0.0, 0.0)
        node.destroy_node()
        rclpy.shutdown()
        termios.tcsetattr(KEY_INPUT, termios.TCSADRAIN, settings)
        if KEY_INPUT is not sys.stdin:
            KEY_INPUT.close()

if __name__ == '__main__':
    main()