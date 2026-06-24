#!/usr/bin/env python3

import argparse
import os
import numpy as np
import matplotlib.pyplot as plt

import rclpy
from rclpy.serialization import deserialize_message

from rosbag2_py import SequentialReader
from rosbag2_py import StorageOptions
from rosbag2_py import ConverterOptions

from rosidl_runtime_py.utilities import get_message


WHEEL_JOINTS = [
  "wheel_left_back_joint",
  "wheel_left_front_joint",
  "wheel_right_back_joint",
  "wheel_right_front_joint"
]

ARM_JOINTS = [
  "arm_3_joint",
  "wrist_1_joint",
  "wrist_3_joint",
  "wrist_5_joint",
  "finger_x_negative_joint",
  "finger_y_negative_joint",
  "finger_x_positive_joint",
  "finger_y_positive_joint"
]


def read_rosbag(bag_path, storage_id="mcap"):
  reader = SequentialReader()

  storage_options = StorageOptions(
    uri=bag_path,
    storage_id=storage_id
  )

  converter_options = ConverterOptions(
    input_serialization_format="cdr",
    output_serialization_format="cdr"
  )

  reader.open(storage_options, converter_options)

  topic_types = {
    topic.name: topic.type
    for topic in reader.get_all_topics_and_types()
  }

  bag_data = {}
  t0 = None

  while reader.has_next():
    topic, data, timestamp = reader.read_next()

    if t0 is None:
      t0 = timestamp

    if topic not in topic_types:
      continue

    msg_type = get_message(topic_types[topic])
    msg = deserialize_message(data, msg_type)

    t = (timestamp - t0) * 1e-9

    if topic not in bag_data:
      bag_data[topic] = []

    bag_data[topic].append(
      {
        "time": t,
        "msg": msg,
      }
    )

  return bag_data


def plot_wheel_positions(bag_data, joint_states_topic, output_dir):
  if joint_states_topic not in bag_data:
    print(f"[WARN] No existe el tópico: {joint_states_topic}")
    return

  time = []
  wheel_positions = {joint: [] for joint in WHEEL_JOINTS}

  for sample in bag_data[joint_states_topic]:
    msg = sample["msg"]

    names = list(msg.name)
    positions = list(msg.position)

    if not all(joint in names for joint in WHEEL_JOINTS):
      continue

    time.append(sample["time"])

    for joint in WHEEL_JOINTS:
      idx = names.index(joint)
      wheel_positions[joint].append(positions[idx])

  if len(time) == 0:
    print("[WARN] No se encontraron posiciones de ruedas.")
    return

  plt.figure()

  for joint in WHEEL_JOINTS:
    plt.plot(time, wheel_positions[joint], label=joint)

  plt.xlabel("Tiempo [s]")
  plt.ylabel("Posición [rad]")
  plt.title("Posición de ruedas vs tiempo")
  plt.grid(True)
  plt.legend()
  plt.tight_layout()

  output_file = os.path.join(output_dir, "01_wheel_positions.png")
  plt.savefig(output_file, dpi=300)
  plt.close()

  print(f"[OK] {output_file}")


def plot_acceleration(bag_data, imu_topic, output_dir):
  if imu_topic not in bag_data:
    print(f"[WARN] No existe el tópico: {imu_topic}")
    return

  time = []
  acc_x = []
  acc_y = []
  acc_z = []
  acc_norm = []

  for sample in bag_data[imu_topic]:
    msg = sample["msg"]

    ax = msg.linear_acceleration.x
    ay = msg.linear_acceleration.y
    az = msg.linear_acceleration.z

    time.append(sample["time"])
    acc_x.append(ax)
    acc_y.append(ay)
    acc_z.append(az)
    acc_norm.append(np.sqrt(ax**2 + ay**2 + az**2))

  if len(time) == 0:
    print("[WARN] No se encontraron datos de aceleración.")
    return

  plt.figure()

  plt.plot(time, acc_x, label="a_x")
  plt.plot(time, acc_y, label="a_y")
  plt.plot(time, acc_z, label="a_z")
  plt.plot(time, acc_norm, label="|a|")

  plt.xlabel("Tiempo [s]")
  plt.ylabel("Aceleración [m/s²]")
  plt.title("Aceleración IMU vs tiempo")
  plt.grid(True)
  plt.legend()
  plt.tight_layout()

  output_file = os.path.join(output_dir, "02_imu_acceleration.png")
  plt.savefig(output_file, dpi=300)
  plt.close()

  print(f"[OK] {output_file}")


def plot_forces(bag_data, joint_states_topic, output_dir):
  if joint_states_topic not in bag_data:
    print(f"[WARN] No existe el tópico: {joint_states_topic}")
    return

  time = []
  force_sum = []

  for sample in bag_data[joint_states_topic]:
    msg = sample["msg"]

    names = list(msg.name)
    efforts = list(msg.effort)
    
    if len(efforts) != len(names):
      continue

    if not all(joint in names for joint in ARM_JOINTS):
      continue

    total_force = 0.0

    for joint in ARM_JOINTS:
      idx = names.index(joint)
      effort = abs(efforts[idx])
      if not np.isnan(effort):
        total_force += effort
    
    time.append(sample["time"])
    force_sum.append(total_force)

  if len(time) == 0:
    print("[WARN] No se encontraron esfuerzos del brazo.")
    print("[WARN] Revisa que /joint_states.effort venga relleno.")
    return

  plt.figure()

  plt.plot(time, force_sum, label="sumatorio esfuerzos brazo")

  plt.xlabel("Tiempo [s]")
  plt.ylabel("Sumatorio |effort|")
  plt.title("Gasto del brazo vs tiempo")
  plt.grid(True)
  plt.legend()
  plt.tight_layout()

  output_file = os.path.join(output_dir, "03_arm_force_sum.png")
  plt.savefig(output_file, dpi=300)
  plt.close()

  print(f"[OK] {output_file}")


def parse_args():
  parser = argparse.ArgumentParser()

  parser.add_argument("bag_path", help="Ruta a la carpeta del rosbag ROS 2")
  parser.add_argument("--joint-topic", default="/joint_states")
  parser.add_argument("--imu-topic", default="/imu/IMU/data")
  parser.add_argument("--output-dir", default="results")
  parser.add_argument("--storage-id", default="mcap")
  return parser.parse_args()


def main():
  args = parse_args()

  os.makedirs(args.output_dir, exist_ok=True)

  bag_data = read_rosbag(args.bag_path, args.storage_id)

  plot_wheel_positions(bag_data, args.joint_topic, args.output_dir)

  plot_acceleration(bag_data, args.imu_topic, args.output_dir)

  plot_forces(bag_data, args.joint_topic, args.output_dir )


if __name__ == "__main__":
  rclpy.init()
  main()
  rclpy.shutdown()
