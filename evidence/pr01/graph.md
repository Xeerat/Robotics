### ДО
1. `export ROS_DOMAIN_ID=89`
2. `ros2 node list --no-daemon --spin-time 2`
```
/teleop_turtle
/turtlesim
```
3. `ros2 topic list -t`
```
/parameter_events [rcl_interfaces/msg/ParameterEvent]
/rosout [rcl_interfaces/msg/Log]
/turtle1/cmd_vel [geometry_msgs/msg/Twist]
/turtle1/color_sensor [turtlesim/msg/Color]
/turtle1/pose [turtlesim/msg/Pose]
```
4. `ros2 node info /turtlesim`
```
/turtlesim
  Subscribers:
    /parameter_events: rcl_interfaces/msg/ParameterEvent
    /turtle1/cmd_vel: geometry_msgs/msg/Twist
  Publishers:
    /parameter_events: rcl_interfaces/msg/ParameterEvent
    /rosout: rcl_interfaces/msg/Log
    /turtle1/color_sensor: turtlesim/msg/Color
    /turtle1/pose: turtlesim/msg/Pose
  Service Servers:
    /clear: std_srvs/srv/Empty
    /kill: turtlesim/srv/Kill
    /reset: std_srvs/srv/Empty
    /spawn: turtlesim/srv/Spawn
    /turtle1/set_pen: turtlesim/srv/SetPen
    /turtle1/teleport_absolute: turtlesim/srv/TeleportAbsolute
    /turtle1/teleport_relative: turtlesim/srv/TeleportRelative
    /turtlesim/describe_parameters: rcl_interfaces/srv/DescribeParameters
    /turtlesim/get_parameter_types: rcl_interfaces/srv/GetParameterTypes
    /turtlesim/get_parameters: rcl_interfaces/srv/GetParameters
    /turtlesim/get_type_description: type_description_interfaces/srv/GetTypeDescription
    /turtlesim/list_parameters: rcl_interfaces/srv/ListParameters
    /turtlesim/set_parameters: rcl_interfaces/srv/SetParameters
    /turtlesim/set_parameters_atomically: rcl_interfaces/srv/SetParametersAtomically
  Service Clients:

  Action Servers:
    /turtle1/rotate_absolute: turtlesim/action/RotateAbsolute
  Action Clients:
```
5. `ros2 topic type /turtle1/pose`
```
turtlesim/msg/Pose
```
6. `ros2 topic echo /turtle1/pose --once`
```
x: 5.410860538482666
y: 6.3970046043396
theta: 0.671999990940094
linear_velocity: 0.0
angular_velocity: 0.0
```
7. `ros2 topic hz /turtle1/pose`
```
average rate: 62.478
        min: 0.015s max: 0.017s std dev: 0.00044s window: 64
average rate: 62.490
        min: 0.015s max: 0.017s std dev: 0.00043s window: 127
average rate: 62.475
        min: 0.015s max: 0.017s std dev: 0.00046s window: 190
average rate: 62.490
        min: 0.014s max: 0.017s std dev: 0.00047s window: 253
average rate: 62.486
        min: 0.014s max: 0.017s std dev: 0.00045s window: 316
average rate: 62.494
        min: 0.014s max: 0.017s std dev: 0.00044s window: 379
average rate: 62.489
        min: 0.014s max: 0.017s std dev: 0.00044s window: 442
average rate: 62.495
        min: 0.014s max: 0.017s std dev: 0.00044s window: 505
average rate: 62.496
        min: 0.014s max: 0.017s std dev: 0.00045s window: 568
average rate: 62.496
        min: 0.014s max: 0.018s std dev: 0.00046s window: 631
average rate: 62.495
        min: 0.014s max: 0.018s std dev: 0.00046s window: 694
average rate: 62.495
        min: 0.012s max: 0.021s std dev: 0.00051s window: 757
average rate: 62.507
        min: 0.012s max: 0.021s std dev: 0.00052s window: 820
```

### СБОЙ
1. `export ROS_DOMAIN_ID=17`
2. `ros2 node list --no-daemon --spin-time 2`
```
/teleop_turtle
```
3. `timeout 5s ros2 topic echo /turtle1/pose "$POSE_TYPE" --once > evidence/pr01/pose-broken.txt 2>&1`
```
```
4. `printf 'exit=%s\n' "$?"`
```
exit=124
```

### ПОСЛЕ
1. `export ROS_DOMAIN_ID=89`
2. `ros2 node list --no-daemon --spin-time 2`
```
/teleop_turtle
/turtlesim
```
3. `timeout 5s ros2 topic echo /turtle1/pose "$POSE_TYPE" --once > evidence/pr01/pose-fixed.txt 2>&1`
```
x: 3.7172365188598633
y: 7.167092323303223
theta: 0.9279999732971191
linear_velocity: 0.0
angular_velocity: 0.0
```
4. `printf 'exit=%s\n' "$?"`
```
exit=0
```