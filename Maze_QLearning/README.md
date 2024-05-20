# 10x10 Grid Navigation with Q-learning
## Overview
This project demonstrates a simple implementation of Q-learning for navigating a 10x10 grid with obstacles using the Pygame library. The agent (player) learns to reach a target position while avoiding obstacles, receiving rewards and penalties based on its actions.

## Grid Definition
The grid is a 10x10 matrix where:
- 1 represents a clear path.
- 0 represents a blockage.

Example:

    ```css
    grid = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 1, 0, 1, 1, 0, 1, 1, 1, 0],
        [1, 1, 1, 1, 0, 1, 1, 0, 1, 1],
        [1, 0, 1, 0, 1, 1, 0, 1, 1, 1],
        [1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
        [0, 1, 0, 1, 1, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 0, 0, 1],
        [1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
        [1, 1, 1, 0, 1, 1, 0, 1, 0, 1]
    ]
```

## Q-learning Parameters
- *n_states*: 100 (10x10 grid)
- *n_actions*: 4 (Up, Down, Left, Right)
- *learning_rate*: 0.8
- *discount_factor*: 0.95
- *exploration_prob*: 0 (fully exploit the learned policy after training)
- *epochs*: 1000
- *time_limit*: 20 seconds per episode
## Rewards and Penalties
- *Target Position*: [9, 9]
- *Reward for reaching the target*: +10
- *Penalty for hitting a blockage*: -10 (and episode ends)
- *Small penalty for each move*: -0.1

## Visualization
- *Grid*: Displayed as a 10x10 grid where each cell represents a state.
- *Q-values*: Displayed in each cell.
- *Player Position*: Blue rectangle.
- *Target Position*: Red rectangle.
- *Blockages*: Black cells.
- *Clear Path*: White cells.

## Execution Flow
### Training:

- The agent explores the grid, updates the Q-table based on the rewards received, and learns the optimal policy over 1000 episodes.
After each episode, the total reward is printed.
Post-training:
- The learned Q-table is displayed.
- The agent navigates the grid using the learned policy, avoiding blockages and reaching the target.

### Output

- *Q-table*: The final Q-table is printed after training.
- *Episode Summary*: Total reward for each episode is printed.
- *Endgame Messages*: Indicates whether the target was reached or the agent hit a blockage.

This project provides a simple yet effective demonstration of Q-learning applied to a grid-based navigation problem, highlighting the core principles of reinforcement learning, such as exploration, exploitation, and reward-based learning.