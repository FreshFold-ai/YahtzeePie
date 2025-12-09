import time
import tracemalloc
import json
from pathlib import Path
import sys

yahtzee_game_path = Path(__file__).parent.parent / 'yahtzee_game'
sys.path.insert(0, str(yahtzee_game_path))

from dice import Dice
from scorecard import Scorecard
from game import Game

def profile_method(func, *args, **kwargs):
    tracemalloc.start()
    start_time = time.perf_counter()
    start_memory = tracemalloc.get_traced_memory()[0]
    
    result = func(*args, **kwargs)
    
    end_time = time.perf_counter()
    current_memory, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    return {
        'execution_time_ms': (end_time - start_time) * 1000,
        'memory_used_kb': (current_memory - start_memory) / 1024,
        'peak_memory_kb': peak_memory / 1024
    }

def profile_dice():
    results = {}
    
    dice = Dice()
    results['dice_init'] = profile_method(Dice)
    results['dice_roll'] = profile_method(dice.roll)
    results['dice_face_value_get'] = profile_method(lambda: dice.face_value)
    results['dice_face_value_set'] = profile_method(setattr, dice, '_face_value', 3)
    
    return results

def profile_scorecard():
    results = {}
    
    results['scorecard_init'] = profile_method(Scorecard, 2)
    scorecard = Scorecard(2)
    results['scorecard_get_score'] = profile_method(scorecard.get_score, 0, 0)
    results['scorecard_set_score'] = profile_method(scorecard.set_score, 0, 0, 10)
    results['scorecard_get_player_card'] = profile_method(scorecard.get_player_card, 0)
    
    return results

def profile_game():
    results = {}
    
    # Initialization
    results['game_init'] = profile_method(Game, 2)
    game = Game(2)
    
    # Dice rolling and value management
    results['game_roll_dice'] = profile_method(game.roll_dice)
    results['game_get_dice_values'] = profile_method(game.get_dice_values)
    results['game_set_dice_values'] = profile_method(game.set_dice_values)
    
    # Sorted dice operations
    results['game_get_sorted_dice'] = profile_method(game.get_sorted_dice)
    results['game_set_sorted_dice'] = profile_method(game.set_sorted_dice)
    
    # Frequency operations
    results['game_get_frequency'] = profile_method(game.get_frequency)
    results['game_set_frequency'] = profile_method(game.set_frequency)
    
    # Scoring calculations (all categories)
    results['game_calculate_score_ones'] = profile_method(game.calculate_score, 0)
    results['game_calculate_score_twos'] = profile_method(game.calculate_score, 1)
    results['game_calculate_score_threes'] = profile_method(game.calculate_score, 2)
    results['game_calculate_score_fours'] = profile_method(game.calculate_score, 3)
    results['game_calculate_score_fives'] = profile_method(game.calculate_score, 4)
    results['game_calculate_score_sixes'] = profile_method(game.calculate_score, 5)
    results['game_calculate_score_three_of_kind'] = profile_method(game.calculate_score, 6)
    results['game_calculate_score_four_of_kind'] = profile_method(game.calculate_score, 7)
    results['game_calculate_score_full_house'] = profile_method(game.calculate_score, 8)
    results['game_calculate_score_small_straight'] = profile_method(game.calculate_score, 9)
    results['game_calculate_score_large_straight'] = profile_method(game.calculate_score, 10)
    results['game_calculate_score_yahtzee'] = profile_method(game.calculate_score, 11)
    results['game_calculate_score_chance'] = profile_method(game.calculate_score, 12)
    
    # Straight detection helpers
    results['game_is_small_straight'] = profile_method(game.is_small_straight, [1, 2, 3, 4, 5])
    results['game_is_large_straight'] = profile_method(game.is_large_straight, [1, 2, 3, 4, 5])
    
    # Display methods (using StringIO to capture output without printing)
    from io import StringIO
    import sys
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    try:
        results['game_display_dice'] = profile_method(game.display_dice, set())
        results['game_display_scorecard'] = profile_method(game.display_scorecard, 0)
    finally:
        sys.stdout = old_stdout
    
    return results

def run_performance_analysis():
    print("Running performance analysis...")
    
    all_results = {
        'dice': profile_dice(),
        'scorecard': profile_scorecard(),
        'game': profile_game()
    }
    
    output_dir = Path(__file__).parent / 'data'
    output_dir.mkdir(exist_ok=True)
    
    with open(output_dir / 'performance_metrics.json', 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print("\nPerformance Analysis Results:")
    print("=" * 70)
    for module, methods in all_results.items():
        print(f"\n{module.upper()}")
        print("-" * 70)
        for method, metrics in methods.items():
            print(f"  {method:30s} | Time: {metrics['execution_time_ms']:8.4f}ms | Memory: {metrics['memory_used_kb']:8.2f}KB")
    
    print(f"\nResults saved to: {output_dir / 'performance_metrics.json'}")
    return all_results

if __name__ == '__main__':
    run_performance_analysis()
