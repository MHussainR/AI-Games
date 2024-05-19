from neuralNetworks import NeuralNetwork
import numpy as np
import random


# Genetic Algorithm for evolving the neural networks
def crossover(parent1, parent2):
    # Perform crossover between two parent networks to generate a child network
    child = NeuralNetwork(parent1.input_size, parent1.hidden_size, parent1.output_size)
    for attr in ['weights_ih', 'weights_ho', 'bias_h', 'bias_o']:
        child_attr = getattr(child, attr)
        parent1_attr = getattr(parent1, attr)
        parent2_attr = getattr(parent2, attr)
        mask = np.random.rand(*child_attr.shape) < 0.5
        child_attr[mask] = parent1_attr[mask]
        child_attr[~mask] = parent2_attr[~mask]
    return child

def mutate(network, mutation_rate=0.01):
    # Mutate the weights and biases of the network with a certain mutation rate
    for attr in ['weights_ih', 'weights_ho', 'bias_h', 'bias_o']:
        tensor = getattr(network, attr)
        mutation_mask = np.random.rand(*tensor.shape) < mutation_rate
        tensor[mutation_mask] += np.random.randn(*tensor[mutation_mask].shape)

def next_generation(population, fitnesses, elite_size=5, mutation_rate=0.01):
    # Generate the next generation of networks based on fitness scores of the current population
    sorted_indices = np.argsort(fitnesses)[::-1]
    next_population = [population[i] for i in sorted_indices[:elite_size]]
    while len(next_population) < len(population):
        parent1, parent2 = random.choices(next_population, k=2)
        child = crossover(parent1, parent2)
        mutate(child, mutation_rate)
        next_population.append(child)
    return next_population