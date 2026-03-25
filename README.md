# 🧭 Simple Navigation Demo (ROS2)

## 📌 Overview
This project demonstrates a basic robot navigation system using ROS2.  
The robot moves between predefined waypoints and visualizes its motion in real-time using Matplotlib.

---

## 🧠 System Architecture

The system consists of four ROS2 nodes:

- **mission_node**
  - Publishes navigation goals

- **navigator_node**
  - Computes velocity commands to reach the goal

- **robot_pose_node**
  - Simulates robot movement and publishes current position

- **visualizer_node**
  - Displays robot movement and path in real-time

---

## 📡 Communication

This project uses **ROS2 Topics (Publish–Subscribe model)**:

| Topic          | Message Type | Description                  |
|----------------|-------------|------------------------------|
| `/goal_pose`   | Pose2D      | Target goal position         |
| `/robot_pose`  | Pose2D      | Current robot position       |
| `/cmd_vel`     | Twist       | Velocity commands            |
| `/nav_status`  | String      | Navigation status            |

---

## 🎯 Robot Behavior

The robot follows a predefined path:

1. Start at **Origin (0,0)**
2. Move to **Point A (2,0)**
3. Move to **Point B (2,2)**
4. Return to **Origin**

---

## 📊 Visualization Features

- Real-time path plotting
- Current position shown as 🔴
- Goal shown as ❌
- Path drawn dynamically (no pre-drawing issue fixed)

---

## ⚙️ How to Run

# Terminal 1
ros2 run simple_nav_demo robot_pose_node

# Terminal 2
ros2 run simple_nav_demo navigator_node

# Terminal 3
ros2 run simple_nav_demo mission_node

# Terminal 4
ros2 run simple_nav_demo visualizer_node
