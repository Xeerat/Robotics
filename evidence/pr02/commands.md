# Команды, их назначение и результат

### 1. `pwd`
```
Выводит абсолютный путь к текущей рабочей директории.
```
#### Результат 
```bash
/repos
```

### 2. `ls -a`
```
Выводит список файлов и директорий (флаг -a для показа скрытых файлов).
```
#### Результат
```bash
.            .github      evidence
..           .gitignore   robotics-course-kit-v1.tar.gz
.course-kit  AI_USAGE.md  robotics-course-kit-v1.tar.gz.sha256.txt
.git         Readme.md
```

### 3. `mkdir -p src evidence/pr02`
```
Cоздает новые директории (флаг -p позволяет создавать вложенные папки и не выдавать ошибку, если они уже существуют).
```
#### Результат
```bash
evidence/pr02
```

### 4. `printenv ROS_DISTRO ROS_DOMAIN_ID`
```
Выводит значения указанных переменных окружения.
```
#### Результат
```bash
jazzy
89
```

# Чем отличается > от |?
### Символ >:
```
Сохраняет результат команды в файл на диске.
```
#### Пример:

`ls > list.txt` 
```
Список файлов запишется в файл, ничего на экран не выведется.
```
### Символ |:
```
Передает результат первой команды сразу на вход второй команде (ничего не сохраняет в файл).
```
#### Пример:

`ls | grep "txt"` 

```
Найти слово "txt" в списке файлов.
```

# source против запуска программы

###  Запуск (./скрипт.sh): 
```
Создает новый и временный процесс. Скрипт заканчивает работу и "умирает". Все изменения исчезают и не влияют на текущий терминал.
```

### source скрипт.sh: 
```
Выполняет команды скрипта прямо в текущем терминале. Все изменения сохраняются и продолжают работать.
```

# Запуск

`ros2 launch turtle_bringup sim.launch.py`

```
Запустилась нода turtlesim_node — появилось окно с черепахой (turtle1) в координатах (5.54, 5.54).
```
```
[INFO] [launch]: All log files can be found below /root/.ros/log/2026-09-22-07-49-19-676934-b27837597e43-231
[INFO] [launch]: Default logging verbosity is set to INFO
[INFO] [turtlesim_node-1]: process started with pid [234]
[turtlesim_node-1] QStandardPaths: XDG_RUNTIME_DIR not set, defaulting to '/tmp/runtime-root'
[turtlesim_node-1] [INFO] [1790063360.871247649] [turtlesim]: Starting turtlesim with node name /turtlesim
[turtlesim_node-1] [INFO] [1790063360.902715504] [turtlesim]: Spawning turtle [turtle1] at x=[5.544445], y=[5.544445], theta=[0.000000]
```

# Проверка графа

`ros2 node list --no-daemon --spin-time 2`

```
Вывела список активных нод
```
```
/turtlesim
```

# Остановка

```
Ctrl+C в терминале с launch — нода получила сигнал SIGINT и завершилась корректно.
```
```
[WARNING] [launch]: user interrupted with ctrl-c (SIGINT)
[turtlesim_node-1] [INFO] [1790063742.143518138] [rclcpp]: signal_handler(SIGINT/SIGTERM)
[INFO] [turtlesim_node-1]: process has finished cleanly [pid 234]
```

# Ожидаемое направление 

```
Команда linear: {x: 1.0}, angular: {z: 0.5} должна двигать черепаху вперёд и поворачивать против часовой стрелки (влево).
```

# Фактическая поза

### До:
```
x: 5.544444561004639
y: 5.544444561004639
theta: 0.0
linear_velocity: 0.0
angular_velocity: 0.0
```

### После:
```
x: 6.509308815002441
y: 5.796990871429443
theta: 0.5040000081062317
linear_velocity: 0.0
angular_velocity: 0.0
```

### Результат:
```
Черепаха сместилась вперёд (x увеличился) и вверх (y увеличился), повернулась против часовой стрелки (theta стал положительным). Поведение соответствует ожидаемому.
```

# Команды 

### До (сбой)

```
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 1.0}, angular: {z: 0.5}}"
```

### После (исправление)
```
ros2 topic pub /turtle1/cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 1.0}, angular: {z: 0.5}}"
```

## Сравнение конечных точек

| Топик | Publisher | Subscriber |
|----|----|----|
| `/cmd_vel` | `_ros2cli` | `0` |
|`/turtle1/cmd_vel` | `0 → _ros2cli`  | `turtlesim` |

## Выводы
```
До: Тип сообщения geometry_msgs/msg/Twist совпадает у publisher и subscriber, но они работают на разных топиках — связь не устанавливается, черепаха не двигается.

После: Publisher и subscriber работают на одном топике /turtle1/cmd_vel с одинаковым типом сообщения — связь установлена, команды доходят до turtlesim.
```
## Почему типа сообщения недостаточно

```
Для установления связи в ROS 2 нужно совпадение трёх параметров:

1. Имя топика (например, /turtle1/cmd_vel)
2. Тип сообщения (например, geometry_msgs/msg/Twist)
3. QoS-профиль (надёжность, история и т.д.)

Если хотя бы один параметр не совпадает — publisher и subscriber не соединятся, даже если тип сообщения правильный. В этом случае не совпало имя топика.
```