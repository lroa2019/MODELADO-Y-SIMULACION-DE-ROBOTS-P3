# Práctica 3 - Modelado y Simulación de Robots

## 1. Captura de RViz

A continuación se muestra el robot Wall-E visualizado en RViz con los TFs visibles y la interfaz de `joint_state_publisher_gui`.

![RViz capture](https://github.com/lroa2019/MODELADO-Y-SIMULACION-DE-ROBOTS-P3/blob/main/Imagenes/Fotos/rviz_capture.png)

![TFs capture](https://github.com/lroa2019/MODELADO-Y-SIMULACION-DE-ROBOTS-P3/blob/main/Imagenes/Fotos/TFs.png)

En la captura se puede observar:
- El modelo 3D del robot Wall-E cargado correctamente en RViz.
- Los TFs visibles en los distintos links del robot (representados por los ejes de coordenadas en rojo, verde y azul).
- El frame fijo establecido en `base_footprint`, conforme a REP-105.
- La interfaz de `joint_state_publisher_gui` en el panel derecho, mostrando todos los joints del robot: las cuatro ruedas, los joints del brazo y los joints de la pinza.

[RViz video](https://github.com/lroa2019/MODELADO-Y-SIMULACION-DE-ROBOTS-P3/blob/main/Imagenes/Videos/video_articulaciones_desplazadas.mp4)

[RViz video](https://github.com/user-attachments/assets/f8dbb5e3-9395-4b90-9a56-8fe1319e2d9d)

## 2. Árbol de transformadas

A continuación se muestra el árbol de transformadas entre los distintos links del robot Wall-E, obtenido mediante `tf2_tools` y el nodo `view_frames`.

[TF Tree PDF](https://github.com/lroa2019/MODELADO-Y-SIMULACION-DE-ROBOTS-P3/blob/main/Imagenes/tf_tree.pdf)

![TF Tree foto](https://github.com/lroa2019/MODELADO-Y-SIMULACION-DE-ROBOTS-P3/blob/main/Imagenes/Fotos/tf_tree.png)

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

![Cubo verde en el aire](https://github.com/lroa2019/MODELADO-Y-SIMULACION-DE-ROBOTS-P3/blob/main/Imagenes/Fotos/video_cubo_verde%20-%20frame_aire.jpg)

![Cubo verde depositado](https://github.com/lroa2019/MODELADO-Y-SIMULACION-DE-ROBOTS-P3/blob/main/Imagenes/Fotos/video_cubo_verde%20-%20frame_dentro.jpg)

[Cubo Verde Video](https://github.com/lroa2019/MODELADO-Y-SIMULACION-DE-ROBOTS-P3/blob/main/Imagenes/Videos/video_cubo_verde.mp4)

[Cubo Verde Video](https://github.com/user-attachments/assets/142bc84e-4bfd-40c6-bf96-12dd8e758d67)

### 3.2. Cubo azul

A continuación se muestra el robot a punto de colocar el cubo azul sobre el cubo rojo.

[Cubo Azul Video](https://github.com/lroa2019/MODELADO-Y-SIMULACION-DE-ROBOTS-P3/blob/main/Imagenes/Videos/video_cubo_azul.mp4)

[Cubo Azul Video](https://github.com/user-attachments/assets/f8e31801-8ce9-44f2-a491-785a91414b4e)

![Cubo azul sobre rojo](https://github.com/lroa2019/MODELADO-Y-SIMULACION-DE-ROBOTS-P3/blob/main/Imagenes/Fotos/foto_cubo_azul.png)

### 3.3. Avanzar 10 metros

[Avanzar 10m Video](https://github.com/lroa2019/MODELADO-Y-SIMULACION-DE-ROBOTS-P3/blob/main/Imagenes/Videos/video_avance_10m.mp4)

[Avanzar 10m Video](https://github.com/user-attachments/assets/25ee4b54-367b-46ef-91e8-8eddbca08e35)

## 4. Gráficas

### 4.1. Cubo verde

<div align="center">
  <img src="https://github.com/lroa2019/MODELADO-Y-SIMULACION-DE-ROBOTS-P3/blob/main/Imagenes/result_cubo_verde/01_wheel_positions.png" alt="cubo_verde_01_wheel_positions" width="330"/>
  <img src="https://github.com/lroa2019/MODELADO-Y-SIMULACION-DE-ROBOTS-P3/blob/main/Imagenes/result_cubo_verde/02_imu_acceleration.png" alt="cubo_verde_02_imu_acceleration" width="330"/>
  <img src="https://github.com/lroa2019/MODELADO-Y-SIMULACION-DE-ROBOTS-P3/blob/main/Imagenes/result_cubo_verde/03_arm_force_sum.png" alt="cubo_verde_03_arm_force_sum" width="330"/>
</div>

#### Posición de ruedas vs tiempo
La gráfica muestra la posición angular (en radianes) de las cuatro ruedas del robot a lo largo del tiempo durante la recogida del cubo verde. Se puede observar cómo las ruedas izquierdas (wheel_left_front_joint en naranja y wheel_left_back_joint en azul) acumulan posición positiva, mientras que las ruedas derechas (wheel_right_front_joint en rojo) acumulan posición negativa, lo que corresponde a un avance del robot para aproximarse al cubo verde, porque estan invertidas. A partir del segundo 40 aproximadamente las ruedas se estabilizan, indicando que el robot ha dejado de moverse para realizar la operación de agarre.

#### Aceleración vs tiempo
La gráfica muestra la aceleración lineal medida por la IMU en los tres ejes (x, y, z) y el módulo total |a| durante la teleoperación. Se pueden observar picos de aceleración en los momentos en que el robot arranca o frena bruscamente, especialmente entre los segundos 35 y 85, que corresponden a los movimientos de aproximación del robot. El eje z permanece prácticamente constante en torno a 10 m/s², lo que corresponde a la aceleración gravitatoria, indicando que la IMU está correctamente orientada.

#### Gasto G-parcial vs tiempo
La gráfica muestra el gasto G-parcial del mecanismo de pick and place, calculado como el sumatorio de los esfuerzos absolutos aplicados a cada joint del brazo en cada instante. Se observa que entre los segundos 0 y 60 el gasto es prácticamente nulo, ya que el brazo está en reposo mientras el robot se desplaza. A partir del segundo 60 se producen picos significativos de hasta 21000 unidades de esfuerzo, que corresponden a los momentos en que el brazo ejecuta los movimientos de agarre y deposición del cubo verde. A partir del segundo 90 el gasto vuelve a cero, indicando que el brazo ha regresado a su posición de reposo.

### 4.2. Cubo azul

<div align="center">
  <img src="https://github.com/lroa2019/MODELADO-Y-SIMULACION-DE-ROBOTS-P3/blob/main/Imagenes/result_cubo_azul/01_wheel_positions.png" alt="cubo_azul_01_wheel_positions" width="330"/>
  <img src="https://github.com/lroa2019/MODELADO-Y-SIMULACION-DE-ROBOTS-P3/blob/main/Imagenes/result_cubo_azul/02_imu_acceleration.png" alt="cubo_azul_02_imu_acceleration" width="330"/>
  <img src="https://github.com/lroa2019/MODELADO-Y-SIMULACION-DE-ROBOTS-P3/blob/main/Imagenes/result_cubo_azul/03_arm_force_sum.png" alt="cubo_azul_03_arm_force_sum" width="330"/>
</div>

#### Posición de ruedas vs tiempo
A diferencia del cubo verde, aquí se observa un movimiento mucho más complejo de las ruedas. Las cuatro ruedas muestran variaciones continuas de posición durante toda la operación, con cambios de dirección frecuentes entre los segundos 0 y 300, lo que refleja la dificultad de maniobrar para aproximarse al cubo azul situado a la izquierda del robot. Se aprecian varios giros y correcciones de trayectoria antes de conseguir posicionarse correctamente.

#### Aceleración vs tiempo
La gráfica de aceleración muestra una actividad mucho más intensa que en el caso del cubo verde, con picos frecuentes en los tres ejes durante toda la grabación. El módulo total |a| presenta picos de hasta 80 m/s² aproximadamente en torno al segundo 125, correspondientes a movimientos bruscos del robot durante las maniobras de aproximación. La mayor variabilidad respecto al cubo verde se debe a los frecuentes cambios de dirección necesarios para alcanzar el cubo azul y el cubo rojo.

#### Gasto G-parcial vs tiempo
El gasto del brazo muestra un comportamiento similar al del cubo verde, con un periodo inicial de reposo seguido de picos de esfuerzo cuando el brazo entra en acción. Se observan dos fases de actividad intensa: una primera alrededor del segundo 100 y una segunda más prolongada entre los segundos 175 y 210, que corresponden respectivamente al agarre del cubo azul y a su colocación sobre el cubo rojo entre los segundos 210 hasta que acaba la ejecución.

### 4.3. Avanzar 10 metros

<div align="center">
  <img src="https://github.com/lroa2019/MODELADO-Y-SIMULACION-DE-ROBOTS-P3/blob/main/Imagenes/result_avance_10m/01_wheel_positions.png" alt="avance_10m_01_wheel_positions" width="330"/>
  <img src="https://github.com/lroa2019/MODELADO-Y-SIMULACION-DE-ROBOTS-P3/blob/main/Imagenes/result_avance_10m/02_imu_acceleration.png" alt="avance_10m_02_imu_acceleration" width="330"/>
  <img src="https://github.com/lroa2019/MODELADO-Y-SIMULACION-DE-ROBOTS-P3/blob/main/Imagenes/result_avance_10m/03_arm_force_sum.png" alt="avance_10m_03_arm_force_sum" width="330"/>
</div>

#### Posición de ruedas vs tiempo
Esta gráfica es la más clara e ilustrativa de las tres acciones. Se observa un movimiento lineal y constante de las ruedas: las ruedas izquierdas acumulan posición positiva mientras que las derechas acumulan posición negativa, lo que indica una rotación continua en sentidos opuestos para avanzar en línea recta. La duración total es de unos 30 segundos y las posiciones alcanzan valores de hasta ±30 rad, lo que es coherente con un desplazamiento de 10 metros.

#### Aceleración vs tiempo
La gráfica de aceleración muestra un comportamiento mucho más limpio que en las acciones anteriores. El módulo |a| se mantiene prácticamente constante en torno a 10 m/s² (gravedad), con picos puntuales en los momentos de arranque (segundo 5) y frenada (segundo 27), correspondientes a las aceleraciones y deceleraciones del robot al iniciar y terminar el avance. Los ejes x e y permanecen casi a 0 durante el avance, confirmando que el movimiento es en línea recta.

#### Gasto G-parcial vs tiempo
El gasto del brazo durante el avance es muy bajo comparado con las acciones de pick and place, con picos puntuales de hasta 1000 unidades de esfuerzo frente a los 20000 del cubo verde o azul. Esto es esperable ya que el brazo no realiza ningún movimiento significativo durante el avance en línea recta, y los pequeños picos se deben a las vibraciones transmitidas al brazo por el movimiento de la base.
