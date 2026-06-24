# MODELADO-Y-SIMULACION-DE-ROBOTS-P3
Explicación detallada de las gráficas generadas, fotos de las ejecuciones y de las escenas e imagenes que se piden en el README de la carpeta Imagenes [(Explicacion detallada)](https://github.com/lroa2019/MODELADO-Y-SIMULACION-DE-ROBOTS-P3/blob/main/Imagenes/README.md).

## 1. Visualización en RViz

Una vez completado el modelo, se utilizó RViz para comprobar visualmente el robot y validar que todas las transformaciones funcionaban correctamente.

### 1.1. Lanzamiento del robot

Se creó un archivo launch encargado de procesar el XACRO y lanzar los nodos necesarios:

```bash
cd ~/modelado_ws
source ~/modelado_ws/install/setup.bash
colcon build --packages-select walle_description
ros2 launch walle_description robot_state_publisher.launch.py
```

### 1.2. Configuración personalizada

Se guardó una configuración propia de RViz en:

```text
rviz/robot.rviz
```

De esta forma, cada vez que se ejecuta el launch, RViz se abre automáticamente con la vista preparada.

## 2. Verificación del árbol TF

Una vez finalizado el modelo, se comprobó la estructura completa de transformaciones del robot mediante la herramienta `tf2_tools`.

### 2.1. Ejecución

Con el launch del robot en funcionamiento, se ejecutó en una segunda terminal:

```bash
cd ~/modelado_ws/src/walle_description
source ~/modelado_ws/install/setup.bash
ros2 run tf2_tools view_frames
````

### 2.2. Archivos generados

La herramienta generó automáticamente los siguientes archivos:

```text
frames.pdf
frames.yaml
```

## 3. Ejecución de la práctica
### Terminal 1:
```
source ~/modelado_ws/install/setup.bash
ros2 launch walle_description walle_sim.launch.py
```
Para cargar el Rviz y el gazebo.
### Terminal 2:
```
source ~/modelado_ws/install/setup.bash
ros2 launch walle_moveit_config move_group.launch.py
```
### Terminal 3:
```
source ~/modelado_ws/install/setup.bash
ros2 launch walle_description walle_controllers.launch.py
```
### Terminal 4:
```
source ~/modelado_ws/install/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```
Para mover el robot.

## 4. Grabación del rosbag

### Terminal 5:
```
source ~/modelado_ws/install/setup.bash

ros2 bag record -o rosbag_cubo_verde /cmd_vel /imu/IMU/data /joint_states
ros2 bag record -o rosbag_cubo_azul /cmd_vel /imu/IMU/data /joint_states
ros2 bag record -o rosbag_avance_10m /cmd_vel /imu/IMU/data /joint_states
```

## Generar las gráficas

### Terminal 6:
```
python3 generar_graficas.py rosbag_cubo_verde/rosbag_cubo_verde_0.mcap --output-dir result_cubo_verde
python3 generar_graficas.py rosbag_cubo_azul/rosbag_cubo_azul_0.mcap --output-dir result_cubo_azul
python3 generar_graficas.py rosbag_avance_10m/rosbag_avance_10m_0.mcap --output-dir result_avance_10m
```
