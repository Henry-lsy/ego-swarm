#!/usr/bin/env python
import rospy
from nav_msgs.msg import Odometry
import numpy as np
import sys
import select
import tty
import termios
import yaml


# 全局变量，用于存储位置和方向
current_position = np.array([0.0, 0.0, 0.0])
current_orientation = 0.0  # 假设这是你获取的当前方向（yaw）

# 保存点的列表
saved_positions = []

def odom_callback(data):
    global current_position, current_orientation
    # 提取位置信息
    pos = data.pose.pose.position
    current_position = np.array([pos.x, pos.y, pos.z])
    # 假设你可以从四元数中提取yaw，这里只是一个示例
    yaw = data.pose.pose.orientation.z
    current_orientation = yaw  # 更新当前方向
    # rospy.loginfo("Current Position: %s", current_position)

def save_position():
    global current_position, current_orientation, saved_positions
    # 将当前位置和方向添加到列表中，包括假定的stay值
    saved_positions.append({
        'x': current_position[0].item(),
        'y': current_position[1].item(),
        'z': current_position[2].item(),
        'yaw': current_orientation,
        'stay': 1
    })
    rospy.loginfo("Position saved: %s", current_position)

def export_positions_to_yaml(filename):
    global saved_positions
    # 定义保存点位的YAML文件名
    with open(filename, 'w') as file:
        yaml.dump(saved_positions, file, default_flow_style=False, sort_keys=False)
    rospy.loginfo("Saved positions exported to %s", filename)

def keyboard_input():
    # 检查是否有键盘输入
    if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
        return sys.stdin.read(1)
    return None

def main():
    rospy.init_node('odom_listener', anonymous=True)
    odom_topic = rospy.get_param('~odom_topic', '/odom')
    file_path = rospy.get_param('~file_path', '/home/henry/waypoints1.yaml')
    # 保存原始终端设置
    old_attr = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())

    try:
        rospy.Subscriber(odom_topic, Odometry, odom_callback)
        rospy.loginfo("Press 'r' to save current position. Press 's' to export saved positions to a YAML file.")
        while not rospy.is_shutdown():
            key = keyboard_input()
            if key == 'r':
                save_position()
            elif key == 's':
                print(file_path)
                export_positions_to_yaml(file_path)
                break
            rospy.sleep(0.1)
    finally:
        # 恢复终端设置
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_attr)
        sys.exit(0)  # 正常退出程序

if __name__ == '__main__':
    main()