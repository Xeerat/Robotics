# Дерево tf2 модели course_ackermann

Владелец публикаций: `robot_state_publisher` (нода `/robot_state_publisher`).
Один издатель на `/tf_static` — это обязательное требование.

| Joint         | Parent    | Child        | Тип    | Offset (xyz)                     | Владелец              |
|---------------|-----------|--------------|--------|----------------------------------|-----------------------|
| lidar_joint   | base_link | lidar_link   | fixed  | (wheelbase/2-0.05, 0, ...)       | robot_state_publisher |
| camera_joint  | base_link | camera_link  | fixed  | (base_length/2, 0, 0)            | robot_state_publisher |
| imu_joint     | base_link | imu_link     | fixed  | (0, 0, base_height/2+imu_size/2) | robot_state_publisher |

Все три сенсора имеют родителя `base_link`. Это означает, что их положение
задаётся относительно корпуса и не зависит друг от друга.

Подвижные звенья (колёса) в этой модели не описаны, поэтому `/tf` пуст —
публикуются только фиксированные преобразования через `/tf_static`.