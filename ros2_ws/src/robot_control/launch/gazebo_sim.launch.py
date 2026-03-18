from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription, SetEnvironmentVariable, TimerAction
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    world = LaunchConfiguration('world')
    robot_name = LaunchConfiguration('robot_name')
    urdf_file = LaunchConfiguration('urdf_file')
    x = LaunchConfiguration('x')
    y = LaunchConfiguration('y')
    z = LaunchConfiguration('z')
    with_teleop = LaunchConfiguration('with_teleop')
    cleanup_existing = LaunchConfiguration('cleanup_existing')

    pkg_share = FindPackageShare('robot_control')
    urdf_path = PathJoinSubstitution([pkg_share, 'urdf', urdf_file])

    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([FindPackageShare('ros_gz_sim'), 'launch', 'gz_sim.launch.py'])
        ),
        launch_arguments={'gz_args': [world, ' -r']}.items(),
    )

    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        output='screen',
        arguments=[
            '-name', robot_name,
            '-allow_renaming', 'false',
            '-x', x,
            '-y', y,
            '-z', z,
            '-file', urdf_path,
        ],
    )

    delete_existing_robot = ExecuteProcess(
        cmd=['timeout', '2', '/opt/ros/jazzy/lib/ros_gz_sim/delete_entity', '--name', robot_name, '--type', '6'],
        output='screen',
        condition=IfCondition(cleanup_existing),
    )

    cleanup_robot = TimerAction(
        period=2.0,
        actions=[delete_existing_robot],
    )

    spawn_robot_after_cleanup = TimerAction(
        period=2.5,
        actions=[spawn_robot],
    )

    ros_gz_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        output='screen',
        arguments=[
            '/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',
            '/odom@nav_msgs/msg/Odometry@gz.msgs.Odometry',
            '/tf@tf2_msgs/msg/TFMessage@gz.msgs.Pose_V',
        ],
    )

    keyboard_teleop = Node(
        package='phase3_teleop',
        executable='keyboard_cmd_vel',
        output='screen',
        emulate_tty=True,
        condition=IfCondition(with_teleop),
    )

    return LaunchDescription([
        DeclareLaunchArgument('world', default_value='empty.sdf'),
        DeclareLaunchArgument('robot_name', default_value='simple_robot'),
        DeclareLaunchArgument('urdf_file', default_value='simple_robot_gazebo.urdf'),
        DeclareLaunchArgument('x', default_value='0.0'),
        DeclareLaunchArgument('y', default_value='0.0'),
        DeclareLaunchArgument('z', default_value='0.1'),
        DeclareLaunchArgument('with_teleop', default_value='true'),
        DeclareLaunchArgument('cleanup_existing', default_value='true'),
        SetEnvironmentVariable(
            name='GZ_SIM_RESOURCE_PATH',
            value=PathJoinSubstitution([pkg_share]),
        ),
        gz_sim,
        cleanup_robot,
        spawn_robot_after_cleanup,
        ros_gz_bridge,
        keyboard_teleop,
    ])
