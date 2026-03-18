# robot_control Gazebo 실행 가이드

## 목적
`simple_robot_gazebo.urdf` 로봇을 Gazebo Sim에 스폰하고, `/cmd_vel` 입력(키보드 텔레옵)으로 이동시킵니다.

## 준비
- ROS 2 Jazzy
- `ros_gz_sim` 설치
- Gazebo GUI는 UTM VM **로컬 터미널**에서 실행 권장

## 빌드
```bash
cd /home/ethan/Desktop/LABA_ALONE/ros2_ws
source /opt/ros/jazzy/setup.bash
colcon build --packages-select robot_control phase3_teleop
source install/setup.bash
```

## 실행
### 터미널 1: Gazebo + 로봇 스폰
```bash
cd /home/ethan/Desktop/LABA_ALONE/ros2_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch robot_control gazebo_sim.launch.py
```

### 터미널 2: 키보드 조종
```bash
cd /home/ethan/Desktop/LABA_ALONE/ros2_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 run phase3_teleop keyboard_cmd_vel
```

W/S: 전진/후진, A/D: 좌/우회전, Space: 정지

## 확인 포인트
- 로봇이 월드에 보이는지
- `/cmd_vel` 입력 시 전진/후진/회전 되는지
- 벽 충돌 시 물리적으로 밀리거나 멈추는지
