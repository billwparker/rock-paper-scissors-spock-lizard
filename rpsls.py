from collections import Counter, deque
import random
import matplotlib.pyplot as plt
from typing import List, Dict, Optional

class RPSLSState:
    MOVES = ['rock', 'paper', 'scissors', 'lizard', 'spock']
    
    WINS_AGAINST = {
        'rock': ['scissors', 'lizard'],
        'paper': ['rock', 'spock'],
        'scissors': ['paper', 'lizard'],
        'lizard': ['paper', 'spock'],
        'spock': ['rock', 'scissors']
    }
    
    def __init__(self):
        self.player_history = []
        self.opponent_history = []
    
    def get_result(self, move1: str, move2: str) -> int:
        if move1 == move2:
            return 0  # Draw
        elif move2 in self.WINS_AGAINST[move1]:
            return 1  # Win
        else:
            return -1  # Loss

class PatternDetector:
    def __init__(self, window_size: int = 3, frequency_threshold: float = 0.3):
        self.window_size = window_size
        self.frequency_threshold = frequency_threshold
        # Keep last 50 moves for pattern analysis
        self.move_history = deque(maxlen=50)  
        # Cache detected patterns
        self.pattern_cache: Dict[str, str] = {}  
        
    def add_move(self, move: str):
        self.move_history.append(move)
        
    def get_pattern_prediction(self) -> Optional[str]:
        if len(self.move_history) < self.window_size:
            return None
            
        # Convert recent moves to a string for pattern matching
        recent_moves = list(self.move_history)[-self.window_size:]
        pattern_key = ''.join(recent_moves)
        
        # Check cache first
        if pattern_key in self.pattern_cache:
            return self.pattern_cache[pattern_key]
            
        # Look for this pattern in history
        pattern_occurrences = []
        for i in range(len(self.move_history) - self.window_size):
            window = list(self.move_history)[i:i + self.window_size]
            if window == recent_moves and i + self.window_size < len(self.move_history):
                pattern_occurrences.append(list(self.move_history)[i + self.window_size])
        
        if pattern_occurrences:
            prediction = Counter(pattern_occurrences).most_common(1)[0][0]
            self.pattern_cache[pattern_key] = prediction
            return prediction
        return None

    def get_frequency_bias(self) -> Optional[str]:
        if not self.move_history:
            return None
            
        move_counts = Counter(self.move_history)
        total_moves = len(self.move_history)
        
        for move, count in move_counts.items():
            if count / total_moves >= self.frequency_threshold:
                return move
        return None

class RPSLSGame:
    def __init__(self):
        self.state = RPSLSState()
        self.pattern_detector = PatternDetector()
        
    def get_counter_move(self, move: str) -> str:
        """Returns a move that beats the given move"""
        possible_counters = [m for m in RPSLSState.MOVES 
                           if move in RPSLSState.WINS_AGAINST[m]]
        return random.choice(possible_counters)
        
    def get_ai_move(self) -> str:
        # First check for patterns
        pattern_prediction = self.pattern_detector.get_pattern_prediction()
        if pattern_prediction:
            return self.get_counter_move(pattern_prediction)
            
        # Then check for frequency bias
        frequency_bias = self.pattern_detector.get_frequency_bias()
        if frequency_bias:
            return self.get_counter_move(frequency_bias)
            
        # If no patterns detected, use recent history analysis
        if self.state.opponent_history:
            recent_moves = Counter(self.state.opponent_history[-5:])
            most_common = recent_moves.most_common(1)[0][0]
            return self.get_counter_move(most_common)
            
        # Fallback to random
        return random.choice(RPSLSState.MOVES)
        
    def play_round(self, opponent_strategy: str = "random", 
                  custom_moves: List[str] = None, 
                  round_number: int = 0) -> tuple:
      
        # Get opponent's move
        if opponent_strategy == "random":
            opponent_move = random.choice(RPSLSState.MOVES)
        elif opponent_strategy == "repeating":
            opponent_move = (self.state.opponent_history[-1] 
                           if self.state.opponent_history 
                           else random.choice(RPSLSState.MOVES))
        elif opponent_strategy == "cycling":
            moves = RPSLSState.MOVES
            if self.state.opponent_history:
                last_move = self.state.opponent_history[-1]
                idx = (moves.index(last_move) + 1) % len(moves)
            else:
                idx = 0
            opponent_move = moves[idx]
        elif opponent_strategy == "custom":
            if custom_moves and round_number < len(custom_moves):
                opponent_move = custom_moves[round_number]
            else:
                opponent_move = random.choice(RPSLSState.MOVES)
        else:
            opponent_move = random.choice(RPSLSState.MOVES)
            
        # Update pattern detector and get AI move
        self.pattern_detector.add_move(opponent_move)
        ai_move = self.get_ai_move()
        
        # Update histories
        self.state.opponent_history.append(opponent_move)
        self.state.player_history.append(ai_move)
        
        result = self.state.get_result(ai_move, opponent_move)
        
        return ai_move, opponent_move, result

def plot_cumulative_win_rate(results: List[int]):
    wins = 0
    win_rates = []
    for i, result in enumerate(results):
        if result == 1:
            wins += 1
        win_rate = wins / (i + 1)
        win_rates.append(win_rate)
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(results) + 1), win_rates)
    plt.xlabel('Number of Rounds')
    plt.ylabel('Cumulative Win Rate')
    plt.title('AI Cumulative Win Rate Over Time')
    plt.grid(True)
    plt.savefig('cumulative_win_rate.png')
    plt.close()

def plot_result_distribution(results: List[int]):
    counts = Counter(results)
    labels = ['Wins', 'Draws', 'Losses']
    values = [counts[1], counts[0], counts[-1]]
    plt.figure(figsize=(8, 6))
    plt.bar(labels, values, color=['green', 'gray', 'red'])
    plt.xlabel('Results')
    plt.ylabel('Number of Occurrences')
    plt.title('AI Performance Distribution')
    plt.grid(True, axis='y')
    plt.savefig('result_distribution.png')
    plt.close()

def demonstrate_game(rounds: int = 10, 
                    opponent_strategy: str = "cycling", 
                    custom_moves: List[str] = None):
    game = RPSLSGame()
    results = []
    wins = 0
    
    print(f"Playing against a {opponent_strategy} opponent...")
    
    for i in range(rounds):
        ai_move, opponent_move, result = game.play_round(opponent_strategy, 
                                                        custom_moves, i)
        results.append(result)
        if result == 1:
            wins += 1
        cumulative_win_pct = wins / (i + 1) * 100
        
        print(f"Round {i+1}:")
        print(f"AI played: {ai_move}")
        print(f"Opponent played: {opponent_move}")
        print(f"Result: {'Win' if result == 1 else 'Loss' if result == -1 else 'Draw'}")
        print(f"Cumulative Win Percentage: {cumulative_win_pct:.2f}%")
        print()
    
    total_wins = results.count(1)
    draws = results.count(0)
    losses = results.count(-1)
    print(f"\nFinal stats - AI Wins: {total_wins}, "
          f"AI Draws: {draws}, AI Losses: {losses}")
    
    plot_cumulative_win_rate(results)
    plot_result_distribution(results)

if __name__ == "__main__":
  
    # Example usage with a biased opponent who favors spock
    num_rounds = 100
    # Let's create a user with a move list that is 50% spock random distributed
    custom_moves_list = ["spock"] * 50 + ["rock"] * 15 + ["paper"] * 15 + \
                       ["scissors"] * 5 + ["lizard"] * 15  
                                                                     
    random.shuffle(custom_moves_list)
    
    print(custom_moves_list)
    
    demonstrate_game(rounds=num_rounds, 
                    opponent_strategy="custom", 
                    custom_moves=custom_moves_list)