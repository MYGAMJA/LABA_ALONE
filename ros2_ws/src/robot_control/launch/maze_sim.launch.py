from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    headless = LaunchConfiguration('headless')

    return LaunchDescription([
        DeclareLaunchArgument('headless', default_value='true'),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution([
                    FindPackageShare('robot_control'),
                    'launch',
                    'gazebo_sim.launch.py',
                ])
            ),
            launch_arguments={
                'world': PathJoinSubstitution([
                    FindPackageShare('robot_control'),
                    'worlds',
                    'maze_world.world',
                ]),
                'x': '-3.50',
                'y': '0.90',
                'z': '0.2',
                'with_teleop': 'true',
                'cleanup_existing': 'false',
                'headless': headless,
            }.items(),
        )
    ])
