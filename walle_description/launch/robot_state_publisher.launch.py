import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.descriptions import ParameterValue


def generate_launch_description():
    description_file = LaunchConfiguration(
        "description_file",
        default="walle.urdf.xacro"
    )

    use_sim_time = LaunchConfiguration(
        "use_sim_time",
        default="false"
    )

    walle_description_pkg = FindPackageShare("walle_description")

    robot_description_content = Command([
        PathJoinSubstitution([FindExecutable(name="xacro")]),
        " ",
        PathJoinSubstitution([
            walle_description_pkg,
            "robots",
            description_file
        ])
    ])

    robot_description = ParameterValue(
        robot_description_content,
        value_type=str
    )

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[{
            "use_sim_time": use_sim_time,
            "robot_description": robot_description,
        }]
    )

    joint_state_publisher_gui_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        name="joint_state_publisher_gui",
        output="screen"
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        parameters=[{
            "use_sim_time": use_sim_time
        }],
        arguments=[
            "-d",
            PathJoinSubstitution([
                walle_description_pkg,
                "rviz",
                "robot.rviz"
            ])
        ]
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            "description_file",
            default_value="walle.urdf.xacro"
        ),
        DeclareLaunchArgument(
            "use_sim_time",
            default_value="true"
        ),
        robot_state_publisher_node,
        joint_state_publisher_gui_node,
        rviz_node
    ])
