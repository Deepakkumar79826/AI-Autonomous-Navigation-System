# AI-Based Autonomous Navigation System

A simulation-based autonomous navigation project that demonstrates how a robot/vehicle agent can move from a start point to a destination while avoiding obstacles and dynamically re-planning its path when the environment changes.

---

## Project Overview

This project is a **virtual AI-Based Autonomous Navigation System** built using Python. It simulates a robot or autonomous vehicle navigating inside a 2D environment by:

- detecting obstacles
- planning the shortest safe path
- avoiding collisions
- re-planning when a new obstacle appears
- visualizing the full navigation process in real time

This project is designed to be:
- beginner-friendly
- fully executable on a laptop
- strong enough for GitHub portfolio proof
- useful for placements, internships, and interview discussion

---

## Problem Statement

Autonomous systems such as self-driving vehicles, warehouse robots, delivery bots, and industrial robots must move safely in environments that contain obstacles and changing conditions.

The goal of this project is to simulate an intelligent navigation system that can:

- understand the environment
- find a safe route to the goal
- avoid blocked paths
- update its decisions dynamically
- reach the destination without collision

---

## Industry Relevance

Autonomous navigation is used in:

- self-driving cars
- warehouse automation
- delivery robots
- industrial robotics
- drones
- smart mobility systems
- autonomous campus/factory vehicles

This project demonstrates the core navigation logic behind such systems in a simplified and understandable way.

---

## Features

- 2D grid-based simulation environment
- obstacle detection
- shortest path planning using **A\***
- obstacle avoidance
- dynamic re-planning
- real-time visualization using Pygame
- metrics saving for each run
- modular Python code structure
- beginner-friendly implementation

---

## Tech Stack

- **Python**
- **NumPy**
- **Pygame**
- **Matplotlib**
- **Pytest**
- **A\* Path Planning Algorithm**

---

## Project Workflow

1. Create a 2D environment
2. Place start point and goal point
3. Add obstacles to the map
4. Use A\* to calculate the shortest safe path
5. Move the agent step by step
6. Detect if the path is blocked
7. Re-plan dynamically when needed
8. Reach the destination
9. Save screenshots and run metrics

---

## Architecture

```text
User Input -> Grid World -> Perception -> Obstacle Detection -> A* Planner
-> Navigation Controller -> Visualization -> Metrics Output
