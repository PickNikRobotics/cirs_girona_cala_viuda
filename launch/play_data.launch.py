import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
import launch
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    pkg_name = 'cirs_girona_cala_viuda'
    my_package_dir = get_package_share_directory(pkg_name)

    urdf_file_name = 'sparus.urdf'
    urdf = os.path.join(my_package_dir,'rviz2',urdf_file_name)

    with open(urdf, 'r') as infp:
        robot_desc = infp.read()

    return LaunchDescription([
            launch.actions.ExecuteProcess(
                cmd=['ros2', 'bag', 'play', os.path.join(my_package_dir,'data','full_dataset.db3')],
                output='screen'
            ),

            Node(
                package='robot_state_publisher',
                executable='robot_state_publisher',
                name='robot_state_publisher',
                output='screen',
                parameters=[{'use_sim_time': use_sim_time, 'robot_description': robot_desc}],
                arguments=[urdf]
            ),
            Node(
                package='rviz2',
                namespace='',
                executable='rviz2',
                name='rviz2',
                arguments=['-d', os.path.join(my_package_dir, 'rviz2', 'cala_viuda.rviz')]
            ),
            Node(
                package='tf2_ros',
                name='rviz_to_world',
                executable='static_transform_publisher',
                arguments = ['0.0', '0.0', '0.0', '0.0', '0.0', '3.14159', '/rviz', '/world']
            ),
            Node(
                package='tf2_ros',
                name='sparus_to_mesh',
                executable='static_transform_publisher',
                arguments = ['-0.535', '0.0', '-0.12', '0', '0.0', '0.0', '/sparus', '/mesh']
            ),
    ])