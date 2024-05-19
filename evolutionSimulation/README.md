# Evolution Simulation

## Overview
This project involves simulating a population of autonomous players in a 2D environment using neural networks. The players aim to collect food and reach the edges of the screen after eating. The players' actions are controlled by neural networks, which are evolved over generations to improve their performance based on specific scoring criteria.

## Key Components

### Neural Networks
Each player is controlled by a neural network that decides actions based on the player's current state. The state includes the player's position, the nearest food position, distances to the three closest food items, and the nearest screen edge.

### Player
Players are represented as sprites with properties like position, status (alive or not), and whether they have eaten food. Players receive a score based on their actions, and their movements are updated according to the neural network's output.

### Food
Food items are scattered around the screen. Players aim to collect these items. The state includes normalized distances to the three closest food items.

### Evaluation Function
The `evaluate_population` function runs the simulation, updating player states, handling collisions with food, and applying scoring rules. Players receive points for eating food and reaching the screen edge after eating. Negative points are given for not moving and for eating more than one food item. Players that do not eat within a time limit are marked as not alive.

### Evolutionary Algorithm
Players' neural networks are evolved across generations using a genetic algorithm. The best-performing networks are selected and modified to form the next generation.

## Scoring System

### Positive Scores
- **Eating food**: +100 points
- **Reaching the edge after eating**: +100 points (plus bonus based on time)

### Negative Scores
- **Eating more than one food**: -150 points
- **Not moving**: -1 point per frame
- **Reaching the edge without eating**: -150 points

## Time Constraint
Players must eat food within 30 seconds (1200 frames) or they will be marked as not alive.

## Visualization
The simulation displays the current generation, maximum score, and elapsed time on the screen. Players and food are drawn using the Pygame library.

## Usage

1. **Initialize Neural Networks**: Create and initialize neural networks for the population of players.
2. **Run Simulation**: Use the `evaluate_population` function to run the simulation for each generation.
3. **Evolve Networks**: Apply an evolutionary algorithm to evolve the neural networks based on their performance scores.
4. **Repeat**: Iterate through multiple generations to improve the performance of the players.

## Technologies Used

- **Python**: Core programming language.
- **Pygame**: Library for handling graphics and game loop.
- **Neural Networks**: Custom neural network class for decision-making.
- **Evolutionary Algorithms**: For evolving the neural networks over generations.

This project showcases the use of artificial intelligence and evolutionary algorithms to train agents in a simulated environment, providing insights into the dynamics of learning and adaptation.
