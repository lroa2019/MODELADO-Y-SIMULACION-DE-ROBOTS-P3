from os.path import join
from os import environ, pathsep
from ament_index_python.packages import get_package_share_directory, get_package_prefix

from controller_manager.launch_utils import generate_load_controller_launch_description

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable, IncludeLaunchDescription, OpaqueFunction
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

from moveit_configs_utils import MoveItConfigsBuilder


def get_model_paths(packages_names):
    model_paths = ""
    for package_name in packages_names:
        if model_paths != "":
            model_paths += pathsep
        package_path = get_package_prefix(package_name)
        model_path = join(package_path, "share")
        model_paths += model_path
    if "GZ_SIM_RESOURCE_PATH" in environ:
        model_paths += pathsep + environ["GZ_SIM_RESOURCE_PATH"]
    return model_paths


def start_gazebo(context, *args, **kwargs):
    world_pkg = get_package_share_directory("urjc_excavation_world")
    world_name = LaunchConfiguration("world_name").perform(context)
    world = join(world_pkg, "worlds", world_name + ".world")

    gz_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            join(get_package_share_directory("ros_gz_sim"), "launch", "gz_sim.launch.py")
        ),
        launch_arguments={"gz_args": ["-r -s -v 4 ", world]}.items()
    )

    gz_client = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            join(get_package_share_directory("ros_gz_sim"), "launch", "gz_sim.launch.py")
        ),
        launch_arguments={"gz_args": ["-g"]}.items()
    )

    return [gz_server, gz_client]


def generate_launch_description():
    moveit_config = MoveItConfigsBuilder("walle", robot_description="walle_description", package_name="walle_moveit_config").to_moveit_configs()

    declare_sim_time = DeclareLaunchArgument(
        "use_sim_time",
        default_value="true",
        description="Use simulation time"
    )

    declare_world_name = DeclareLaunchArgument(
        "world_name",
        default_value="urjc_excavation_msr",
        description="World name without extension"
    )

    model_path = get_model_paths(["walle_description", "urjc_excavation_world"])

    pkg_path = get_package_share_directory("walle_description")

    # Robot state publisher from MoveIt2
    robot_description_launcher = IncludeLaunchDescription(
        PathJoinSubstitution(
            [FindPackageShare("walle_moveit_config"), "launch", "rsp.launch.py"]
        ),
        launch_arguments={
            "use_sim_time": "true"
        }.items()
    )

    # Spawn robot in Gazebo
    gazebo_spawn_robot = Node(
        package="ros_gz_sim",
        executable="create",
        output="screen",
        arguments=[
            "-model", "walle",
            "-topic", "/robot_description",
            "-x", "0.0",
            "-y", "0.0",
            "-z", "-2.0",
            "-Y", "0.0"
        ],
        parameters=[
            {"use_sim_time": True}
        ]
    )

    # RViz
    rviz_config_file = PathJoinSubstitution(
        [FindPackageShare("walle_description"), "rviz", "robot.rviz"]
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="log",
        arguments=["-d", rviz_config_file],
        parameters=[
            {"use_sim_time": True}
        ]
    )

    # Bridge Gazebo -> ROS
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='bridge_ros_gz',
        parameters=[
            {
                'config_file': join(pkg_path, 'config', 'walle_bridge.yaml'),
                'use_sim_time': True,
            }
        ],
        output='screen',
    )

    # Image bridge for cameras
    gz_image_bridge_node = Node(
        package="ros_gz_image",
        executable="image_bridge",
        arguments=[
            "/front_camera/image",
            "/arm_camera/image"
        ],
        output="screen",
        parameters=[
            {
                'use_sim_time': True,
                'camera.image.compressed.jpeg_quality': 75
            }
        ],
    )

    # Twist stamper for cmd_vel
    twist_stamped = Node(
        package="twist_stamper",
        executable="twist_stamper",
        name="twist_stamper",
        output="screen",
        parameters=[
            {
                "use_sim_time": True,
            }
        ],
        remappings=[
            ('cmd_vel_out', '/walle_base_control/cmd_vel'),
            ('cmd_vel_in', '/cmd_vel')
        ],
    )

    ld = LaunchDescription()
    ld.add_action(SetEnvironmentVariable("GZ_SIM_RESOURCE_PATH", model_path))
    ld.add_action(SetEnvironmentVariable("GZ_SIM_MODEL_PATH", model_path))
    ld.add_action(declare_sim_time)
    ld.add_action(declare_world_name)
    ld.add_action(robot_description_launcher)
    ld.add_action(bridge)
    ld.add_action(gz_image_bridge_node)
    ld.add_action(OpaqueFunction(function=start_gazebo))
    ld.add_action(gazebo_spawn_robot)
    ld.add_action(rviz_node)
    ld.add_action(twist_stamped)

    return ld
