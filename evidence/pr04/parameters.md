## Стадия 1 - Объявленные параметры и дефолты

| Параметр       | Дефолт | 
|----------------|--------|
| linear_speed   | 0.5    | 
| turn_rate      | 0.3    | 
| publish_hz     | 10.0   |

Команда проверки списка параметров:

`ros2 param list /patrol`:
```bash
    linear_speed
    publish_hz
    start_type_description_service
    turn_rate
    use_sim_time
```

## Стадия 2 - Сломать (проверка publish_hz отключена)

### Запуск ноды:

`ros2 run patrol patrol --ros-args -r cmd_vel:=/turtle1/cmd_vel`

### Попытка установить недопустимую частоту:

`ros2 param set /patrol publish_hz 0.0`

Команда зависла — нода упала с ZeroDivisionError.   

### Проверка, что нода мертва:

`ros2 node list`
```bash
    /turtlesim
```
 /patrol отсутствует — нода уничтожена

### Вывод ноды в момент падения:
```
Traceback (most recent call last):
  File "/repos/install/patrol/lib/patrol/patrol", line 33, in <module>
    sys.exit(load_entry_point('patrol', 'console_scripts', 'patrol')())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/repos/build/patrol/patrol/patrol.py", line 97, in main
    rclpy.shutdown()
  File "/opt/ros/jazzy/lib/python3.12/site-packages/rclpy/__init__.py", line 134, in shutdown
    _shutdown(context=context)
  File "/opt/ros/jazzy/lib/python3.12/site-packages/rclpy/utilities.py", line 82, in shutdown
    context.shutdown()
  File "/opt/ros/jazzy/lib/python3.12/site-packages/rclpy/context.py", line 129, in shutdown
    self.__context.shutdown()
rclpy._rclpy_pybind11.RCLError: failed to shutdown: rcl_shutdown already called on the given context, at ./src/rcl/init.c:333
[ros2run]: Process exited with failure 1
root@f21ee94357a6:/repos# ros2 run patrol patrol --ros-args -r cmd_vel:=/turtle1/cmd_vel
Traceback (most recent call last):
  File "/repos/install/patrol/lib/patrol/patrol", line 33, in <module>
    sys.exit(load_entry_point('patrol', 'console_scripts', 'patrol')())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/repos/build/patrol/patrol/patrol.py", line 92, in main
    rclpy.spin(node)
  File "/opt/ros/jazzy/lib/python3.12/site-packages/rclpy/__init__.py", line 247, in spin
    executor.spin_once()
  File "/opt/ros/jazzy/lib/python3.12/site-packages/rclpy/executors.py", line 926, in spin_once
    self._spin_once_impl(timeout_sec)
  File "/opt/ros/jazzy/lib/python3.12/site-packages/rclpy/executors.py", line 918, in _spin_once_impl
    raise handler.exception()
  File "/opt/ros/jazzy/lib/python3.12/site-packages/rclpy/task.py", line 286, in _execute_coroutine_step
    result = coro.send(None)
             ^^^^^^^^^^^^^^^
  File "/opt/ros/jazzy/lib/python3.12/site-packages/rclpy/executors.py", line 592, in handler
    await call_coroutine()
  File "/opt/ros/jazzy/lib/python3.12/site-packages/rclpy/executors.py", line 531, in _execute
    response = await await_or_execute(srv.callback, request, srv.srv_type.Response())
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/ros/jazzy/lib/python3.12/site-packages/rclpy/executors.py", line 115, in await_or_execute
    return callback(*args)
           ^^^^^^^^^^^^^^^
  File "/opt/ros/jazzy/lib/python3.12/site-packages/rclpy/parameter_service.py", line 117, in _set_parameters_callback
    result = node.set_parameters_atomically([param])
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/ros/jazzy/lib/python3.12/site-packages/rclpy/node.py", line 839, in set_parameters_atomically
    return self._set_parameters_atomically(parameter_list)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/ros/jazzy/lib/python3.12/site-packages/rclpy/node.py", line 859, in _set_parameters_atomically
    return self._set_parameters_atomically_common(parameter_list)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/ros/jazzy/lib/python3.12/site-packages/rclpy/node.py", line 909, in _set_parameters_atomically_common
    result = callback(parameter_list)
             ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/repos/build/patrol/patrol/patrol.py", line 80, in _on_set_parameters
    self.timer = self.create_timer(1.0 / self._publish_hz, self._on_timer)
                                   ~~~~^~~~~~~~~~~~~~~~~~
ZeroDivisionError: float division by zero
[ros2run]: Process exited with failure 1
```

Воспроизводимый отказ: недопустимое значение 0.0 прошло через отсутствующую
валидацию, привело к делению на ноль и уничтожило ноду.

## Стадия 3 · Исправление (проверка восстановлена)

### Успешная смена частоты 10 → 5 Гц

`ros2 param set /patrol publish_hz 5.0`
```bash
Set parameter successful
```

### В логе ноды:

```bash
[INFO] [patrol]: timer rebuilt, period=0.2000s
```

### Измерение реальной частоты публикации:

`ros2 topic hz /turtle1/cmd_vel -w 20`
```bash
average rate: 4.998
        min: 0.200s max: 0.201s std dev: 0.00030s window: 6
average rate: 4.999
        min: 0.199s max: 0.201s std dev: 0.00034s window: 11
average rate: 5.000
        min: 0.199s max: 0.201s std dev: 0.00030s window: 17
average rate: 5.001
        min: 0.199s max: 0.200s std dev: 0.00030s window: 20
average rate: 5.000
        min: 0.199s max: 0.200s std dev: 0.00033s window: 20
```
Старый таймер остановлен, новый таймер работает с периодом 0.2 с.

### Отклонение нуля

`ros2 param set /patrol publish_hz 0.0`
```bash
Setting parameters failed: publish_hz 0.0 out of [1, 30]
```

### Проверка, что старое значение сохранено:

`ros2 param get /patrol publish_hz`
```bash
Double value is: 5.0
```

Значение и поток команд остались прежними.

### Отрицательная скорость

`ros2 param set /patrol linear_speed -0.5`
```bash
Setting parameters failed: linear_speed -0.5 out of [0, 1]
```