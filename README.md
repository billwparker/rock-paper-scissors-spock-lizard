# rock-paper-scissors-spock-lizard
Rock Paper Scissors Spock Lizard Game

If you've watched "The Big Bang Theory," then you've probably heard of the variant of the classic "Rock, Paper, Scissors" game—namely, "Rock, Paper, Scissors, Lizard, Spock" (RPSLS). It's a game with more outcomes, making it a perfect challenge for an AI model strategy to predict and counter the opponent's moves in a series of games. This blog post dives into a Python implementation that builds an AI capable of challenging any human or algorithmic opponent, while utilizing decision-making strategies to improve its odds of winning.

## Human Bias in Random Choices: Why We Struggle with True Randomness

One interesting psychological phenomenon that influences this game, as well as many others, is that people do not behave randomly when making what they believe are "equal weighted" choices. When asked to select a random number between 1 and 10, or even when playing Rock, Paper, Scissors, humans tend to fall into certain predictable patterns or biases. Despite their best efforts to be random, their behavior does not follow a true uniform distribution.

Research (https://hill.math.gatech.edu/publications/PAPER%20PDFS/RandomNumberGuessing_Hill_88.pdf) has shown that people are inherently biased in making supposedly random choices. For example, when asked to choose a number between 1 and 10, numbers like 3 or 7 tend to be selected more often, whereas numbers like 1 or 10 are underrepresented. This phenomenon occurs because humans are subconsciously influenced by their own preferences, cultural biases, and an inherent desire to avoid patterns that appear "too obvious" or "too simple."

In games like Rock, Paper, Scissors, this inability to behave randomly leads to non-uniform strategies. Players may try to avoid repeating a move they just played, thinking that it will be more unpredictable. They may also try to counter what they think their opponent expects, resulting in predictable tendencies over time. These biases provide a valuable opportunity for an algorithm to exploit through statistical and pattern-based analysis.

This enables the provided code to have a strong chance of winning — it can observe the human tendency to favor particular sequences or overuse certain moves, and adapt accordingly. By using techniques such as pattern detection, frequency bias analysis, and historical move analysis, the model can identify and capitalize on these human biases, increasing its odds of winning. Essentially, the model is leveraging the fact that humans struggle to achieve true randomness, and therefore tend to create exploitable patterns in their actions.

## The Game Rules
Before I get into the code, here’s a quick recap of the rules:

- Rock crushes Scissors and crushes Lizard.
- Paper covers Rock and disproves Spock.
- Scissors cuts Paper and decapitates Lizard.
- Lizard eats Paper and poisons Spock.
- Spock vaporizes Rock and smashes Scissors.

The goal of our model is to make moves that consistently beat the opponent, by learning from historical patterns, frequency biases, and recent moves. Let’s break down the key components and strategies used in this code.

## The PatternDetector Class
The PatternDetector purpose is to detect and exploit repeatable sequences or biases in the opponent’s gameplay.

Key Features of the PatternDetector:

1) Sliding Window Approach: The model uses a sliding window to look at a subset of the opponent's recent moves, treating these moves as a potential pattern.
2) Pattern Matching: The model looks for repeated sequences in its historical data to predict what the opponent is most likely to play next.
3) Frequency Bias Analysis: If it detects that an opponent tends to favor a specific move more often (e.g., using Spock 40% of the time), the model can use that information to counter effectively.
4) Pattern Cache: Once a pattern is detected, it’s stored in a cache for quick lookup. This reduces the computational effort needed for pattern recognition.

## Levels of Decision Making
The model employs a multi-tiered approach to decide its next move, which is what gives it a strategic edge over simple randomness.

1. Pattern Detection
The model’s first line of decision-making is detecting patterns in the opponent’s moves. The model examines recent moves to identify repeated sequences. When it identifies a pattern, it predicts the opponent's next move and selects a counter to that move.

Example:
If the opponent has played "Rock, Paper, Scissors" multiple times in a row, the model will predict Rock as the next move and counter it accordingly—by playing Paper.

2. Frequency Bias Analysis
If no specific pattern is found, the model falls back on analyzing the opponent's overall move frequency. For instance, if the model detects that the opponent tends to use Spock more than 30% of the time, it will prioritize moves that can defeat Spock. This is achieved through the get_frequency_bias() function, which looks at the most frequent moves and calculates the probability.

Example:
If the opponent often plays Lizard, the model will frequently choose Rock or Scissors to increase its chances of winning.

3. Recent History Analysis
When neither patterns nor biases are apparent, the model checks the recent history to determine the most common recent move and selects a counter to it. This is based on the assumption that players may fall into short-term habits.

4. Random Move (Last Resort)
If no useful patterns or biases are found, the model defaults to making a random move, ensuring that its behavior remains unpredictable and cannot easily be exploited by an opponent.

## Game Implementation
Now, let’s explore how these strategies are implemented in practice. The code is built around two main classes: RPSLSState and PatternDetector, while RPSLSGame encapsulates the decision-making strategies.

## RPSLSState Class
This class is responsible for managing game state. It keeps track of the moves made by both the player and the opponent and provides functionality to determine the outcome of a round.

## RPSLSGame Class
This class uses the PatternDetector to decide on the best move to play in each round. Here's a brief breakdown of its main components:

- get_counter_move(): Given a move, it returns a random counter move that will beat it.
- get_ai_move(): This function follows the AI's decision-making process:

  1) Tries to predict using patterns.
  2) Checks for frequency bias.
  3) Uses recent history analysis.
  4) Falls back to a random move.

## Strategies in Action: Understanding the Decision Layers

### Layer 1: Pattern-Based Strategy
The sliding window approach is key here. It checks if the recent moves form a recognizable pattern within the move_history. If it finds that, for example, the opponent tends to follow a sequence of Rock, Paper, Scissors, it can anticipate the next move in the sequence. The model exploits this to stay one step ahead.

### Layer 2: Frequency Bias Exploitation
People often have unconscious biases, even in games of chance. The algorithm exploits these biases by analyzing the historical frequencies of moves and identifying overused strategies. For instance, if Spock appears more often than the threshold (30%), the model can predict this move and play accordingly.

### Layer 3: Recent History Adaptation
This fallback is a way to counter short-term tendencies. If a player has been cycling between Lizard and Spock in the last five moves, the algorithm adapts to this local trend and tries to counter it effectively.

### Random Move as a Last Resort
Finally, to maintain unpredictability and prevent the opponent from exploiting the algorithm, the model can play a random move. This adds an element of chaos, preventing the opponent from gaining the upper hand through a predictable response pattern.

## Visualizing Performance
The code also includes functions to visualize the performance of the model:

- Result Distribution Plot: Shows the number of wins, losses, and draws, helping to understand the overall effectiveness of the strategies.
- Cumulative Win Rate Plot: Tracks the AI's win rate across multiple rounds. A rising curve would indicate that the model is successfully adapting to the opponent.

## Demonstration
To see the model in action, the demonstrate_game() function allows you to pit the model against various opponent strategies. For example:

A cycling strategy where the opponent cycles through all five moves.
A custom strategy with a predefined list of moves, allowing you to test how well the model adapts to specific patterns or biases.

In the provided demonstration, the model faces an opponent who heavily favors Spock. This scenario tests how well the model can detect frequency bias and use it to its advantage.

## Summary
The code for this "Rock, Paper, Scissors, Lizard, Spock" game presents an approach to building a strategic AI. The layered decision-making process makes the model versatile and adaptive, capable of dealing with a range of opponent behaviors—from strict repetition to pure randomness. By employing pattern detection, frequency bias exploitation, and recent history analysis, the AI becomes a formidable opponent in this game of chance and strategy. 