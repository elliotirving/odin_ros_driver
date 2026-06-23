import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    package_dir = get_package_share_directory('odin_ros_driver')
    config = os.path.join(package_dir, 'config', 'control_command.yaml')

    config_file_arg = DeclareLaunchArgument(
        'config_file',
        default_value=config,
        description='Path to the control config YAML file'
    )

    return LaunchDescription([
        config_file_arg,
        Node(
            package='odin_ros_driver',
            executable='host_sdk_sample',
            name='host_sdk_sample',
            output='screen',
            parameters=[{'config_file': LaunchConfiguration('config_file')}]
        ),
    ])
