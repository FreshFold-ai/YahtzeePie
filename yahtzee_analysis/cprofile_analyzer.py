import cProfile
import pstats
import io
from pathlib import Path
import sys

yahtzee_game_path = Path(__file__).parent.parent / 'yahtzee_game'
sys.path.insert(0, str(yahtzee_game_path))

from game import Game

def run_game_simulation():
    game = Game(2)
    
    for _ in range(10):
        game.roll_dice()
        game.set_frequency()
        game.calculate_score(0)
        game.calculate_score(6)
        game.calculate_score(11)

def profile_with_cprofile():
    print("Running cProfile analysis...")
    
    profiler = cProfile.Profile()
    profiler.enable()
    run_game_simulation()
    profiler.disable()
    
    output_dir = Path(__file__).parent / 'data'
    output_dir.mkdir(exist_ok=True)
    
    s = io.StringIO()
    stats = pstats.Stats(profiler, stream=s)
    stats.strip_dirs()
    stats.sort_stats('cumulative')
    stats.print_stats(30)
    
    with open(output_dir / 'cprofile_output.txt', 'w') as f:
        f.write(s.getvalue())
    
    print(f"cProfile results saved to: {output_dir / 'cprofile_output.txt'}")
    print("\nTop 15 functions by cumulative time:")
    print("-" * 80)
    stats.print_stats(15)

if __name__ == '__main__':
    profile_with_cprofile()
