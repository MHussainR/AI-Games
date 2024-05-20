# 2R Manipulator with Q-learning

This project implements a 2-link robotic manipulator (2R manipulator) using Pygame and applies Q-learning to control the manipulator to reach a random target within its workspace.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Implementation Details](#implementation-details)
- [Future Improvements](#future-improvements)
- [Contributing](#contributing)

## Introduction

This project demonstrates the application of reinforcement learning, specifically Q-learning, to control a 2R manipulator. The objective is for the manipulator's end effector to reach a randomly placed target within its reachable workspace within a specified time limit.

## Features

- Simulate a 2R manipulator with adjustable link lengths.
- Visualize the manipulator, target, and end effector using Pygame.
- Apply Q-learning to train the manipulator to reach random targets.
- Display relevant information on the screen, including the episode number, total reward, remaining time, and positions of the target and end effector.

## Requirements

- Python 3.x
- Pygame
- NumPy

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/2R-Manipulator-Q-learning.git
   cd 2R-Manipulator-Q-learning

2. Install the required packages:

    ```sh
    pip install pygame numpy

## Usage

To run the simulation and start training the manipulator, execute the following command:
    ```sh
    python 2r_manipulator_qlearning.py


The Pygame window will open, and the training process will begin. The manipulator will attempt to reach a random target within its workspace, and the Q-learning algorithm will update the policy based on the rewards.

## Implementation Details

- *Q-learning Algorithm*: The Q-learning algorithm is used to learn the optimal policy for controlling the manipulator. The state space is discretized based on the angles of the manipulator's links.

- *Reward Function*: The reward is based on the distance between the end effector and the target. If the end effector reaches the target, a positive reward is given. If the time limit is exceeded, a negative reward is assigned. During each step, a small negative reward proportional to the distance to the target is given to encourage the manipulator to move closer.

- *Exploration Strategy*: An epsilon-greedy strategy is employed to balance exploration and exploitation during training.

## Future Improvements
- Implement continuous action spaces using advanced algorithms like DDPG, PPO, or SAC.
- Add obstacles to the workspace to increase the complexity of the task.
- Optimize the state representation and discretization to improve learning efficiency.
- Include more detailed visualizations and logging for better analysis of the training process.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.