import os
import yaml
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

    pcd2depth_params = yaml.safe_load(open(config))
    # calib.yaml is downloaded from device at runtime into the source config dir,
    # not the install/share dir, so resolve via this launch file's real path.
    source_package_dir = os.path.dirname(os.path.dirname(os.path.realpath(os.path.abspath(__file__))))
    pcd2depth_params['calib_file_path'] = os.path.join(source_package_dir, 'config', 'calib.yaml')

    return LaunchDescription([
        config_file_arg,
        Node(
            package='odin_ros_driver',
            executable='host_sdk_sample',
            name='host_sdk_sample',
            output='screen',
            parameters=[{'config_file': LaunchConfiguration('config_file')}]
        ),
        Node(
            package='odin_ros_driver',
            executable='pcd2depth_ros2_node',
            name='pcd2depth_ros2_node',
            output='screen',
            parameters=[pcd2depth_params]
        ),
    ])
