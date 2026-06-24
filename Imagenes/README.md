# Práctica 3 - Modelado y Simulación de Robots

## 1. Captura de RViz

A continuación se muestra el robot Wall-E visualizado en RViz con los TFs visibles y la interfaz de `joint_state_publisher_gui`.

![RViz capture](https://github.com/lroa2019/MODELADO-Y-SIMULACION-DE-ROBOTS/blob/main/Practica3/Imagenes/rviz_capture.png)

![TFs capture](https://github.com/lroa2019/MODELADO-Y-SIMULACION-DE-ROBOTS/blob/main/Practica3/Imagenes/TFs.png)

En la captura se puede observar:
- El modelo 3D del robot Wall-E cargado correctamente en RViz.
- Los TFs visibles en los distintos links del robot (representados por los ejes de coordenadas en rojo, verde y azul).
- El frame fijo establecido en `base_footprint`, conforme a REP-105.
- La interfaz de `joint_state_publisher_gui` en el panel derecho, mostrando todos los joints del robot: las cuatro ruedas, los joints del brazo y los joints de la pinza.

[RViz video](https://github.com/lroa2019/MODELADO-Y-SIMULACION-DE-ROBOTS/blob/main/Practica3/Imagenes/video_articulaciones_desplazadas.mp4)

[RViz video](https://github.com/user-attachments/assets/eb4674b0-9214-4c21-b51d-076819966ba1)

## 2. Árbol de transformadas

A continuación se muestra el árbol de transformadas entre los distintos links del robot Wall-E, obtenido mediante `tf2_tools` y el nodo `view_frames`.

[TF Tree PDF](https://github.com/lroa2019/MODELADO-Y-SIMULACION-DE-ROBOTS/blob/main/Practica3/Imagenes/tf_tree.pdf)

![TF Tree foto](https://github.com/lroa2019/MODELADO-Y-SIMULACION-DE-ROBOTS/blob/main/Practica3/Imagenes/tf_tree.png)

El árbol tiene la siguiente estructura jerárquica:

- `base_footprint` es el link raíz del robot, conforme a REP-105.
- De `base_footprint` cuelga `base_link`, que es el padre del resto de links.
- Desde `base_link` se ramifica hacia:
  - Los links de la base: `cover_base_link`, `base_IMU_link`, `front_camera_link`.
  - Los compartimentos: `box_1_base_link`, `box_2_base_link`, `box_3_base_link`, `box_4_base_link`.
  - Las ruedas: `wheel_left_back_link`, `wheel_left_front_link`, `wheel_right_back_link`, `wheel_right_front_link`, con sus correspondientes ejes.
  - La cadena del brazo: `arm_base_link` → `wrist_1_link` → `arm_1_link` → `wrist_2_link` → `wrist_3_link` → `arm_2_link` → `wrist_4_link` → `wrist_5_link` → `arm_3_link` → `gripper_platform_link`, desde donde cuelgan los links de la pinza (`finger_x_negative_link`, `finger_x_positive_link`, `finger_y_negative_link`, `finger_y_positive_link`) y la cámara del brazo (`arm_camera_link`).

## 3. Imágenes de la simulación

### 3.1. Cubo verde

A continuación se muestran dos momentos de la recogida del cubo verde: el robot sujetándolo en el aire y depositándolo en su compartimento.

![Cubo verde en el aire](https://github.com/lroa2019/MODELADO-Y-SIMULACION-DE-ROBOTS/blob/main/Practica3/Imagenes/video_cubo_verde%20-%20frame_aire.jpg)

![Cubo verde depositado](https://github.com/lroa2019/MODELADO-Y-SIMULACION-DE-ROBOTS/blob/main/Practica3/Imagenes/video_cubo_verde%20-%20frame_dentro.jpg)

[Cubo Verde Video](https://github.com/lroa2019/MODELADO-Y-SIMULACION-DE-ROBOTS/blob/main/Practica3/Imagenes/video_cubo_verde.mp4)

[Cubo Verde Video](https://github.com/user-attachments/assets/d87fe476-37c8-46bc-ae26-d4b52eae002f)


### 3.2. Cubo azul

A continuación se muestra el robot a punto de colocar el cubo azul sobre el cubo rojo.

[Cubo Azul Video](https://github.com/lroa2019/MODELADO-Y-SIMULACION-DE-ROBOTS/blob/main/Practica3/Imagenes/video_cubo_azul.mp4)

[Cubo Azul Video](https://github.com/user-attachments/assets/8c20e840-691d-4c33-a087-c83227dda65b)

![Cubo azul sobre rojo](https://github.com/lroa2019/MODELADO-Y-SIMULACION-DE-ROBOTS/blob/main/Practica3/Imagenes/foto_cubo_azul.png)

### 3.3. Avanzar 10 metros

[Avanzar 10m Video](https://github.com/lroa2019/MODELADO-Y-SIMULACION-DE-ROBOTS/blob/main/Practica3/Imagenes/video_avance_10m.mp4)

[Avanzar 10m Video](https://github.com/user-attachments/assets/7888811d-a32d-46c4-883d-d299eeb6f711)
