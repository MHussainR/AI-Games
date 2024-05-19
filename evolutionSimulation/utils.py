def weights_to_color(weights):
    # Ensure we only take the first 3 weights
    weights = weights[:3]

    # Normalize weights to the range [0, 255]
    min_weight = min(weights)
    max_weight = max(weights)
    normalized_weights = [(w - min_weight) / (max_weight - min_weight) * 255 for w in weights]

    # Convert the first three normalized weights to an RGB tuple
    rgb_color = (int(normalized_weights[0]), int(normalized_weights[1]), int(normalized_weights[2]))

    return rgb_color