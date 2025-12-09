import subprocess
import json
from pathlib import Path

def analyze_readability():
    print("Running readability analysis...")
    
    yahtzee_path = Path(__file__).parent.parent / 'yahtzee_game'
    output_dir = Path(__file__).parent / 'data'
    output_dir.mkdir(exist_ok=True)
    
    results = {}
    
    source_files = ['dice.py', 'scorecard.py', 'game.py', 'main.py']
    
    for file in source_files:
        file_path = yahtzee_path / file
        if not file_path.exists():
            continue
        
        with open(file_path) as f:
            content = f.read()
            lines = content.split('\n')
            
        results[file] = {
            'total_lines': len(lines),
            'code_lines': len([l for l in lines if l.strip() and not l.strip().startswith('#')]),
            'comment_lines': len([l for l in lines if l.strip().startswith('#')]),
            'blank_lines': len([l for l in lines if not l.strip()])
        }
    
    try:
        radon_cc = subprocess.run(
            ['radon', 'cc', str(yahtzee_path), '-a', '-j'],
            capture_output=True, text=True
        )
        if radon_cc.returncode == 0:
            results['cyclomatic_complexity'] = json.loads(radon_cc.stdout)
    except FileNotFoundError:
        results['cyclomatic_complexity'] = 'radon not installed'
    
    try:
        radon_mi = subprocess.run(
            ['radon', 'mi', str(yahtzee_path), '-j'],
            capture_output=True, text=True
        )
        if radon_mi.returncode == 0:
            results['maintainability_index'] = json.loads(radon_mi.stdout)
    except FileNotFoundError:
        results['maintainability_index'] = 'radon not installed'
    
    with open(output_dir / 'readability_metrics.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\nReadability Analysis Results:")
    print("=" * 70)
    for file, metrics in results.items():
        if isinstance(metrics, dict) and 'total_lines' in metrics:
            print(f"\n{file}:")
            print(f"  Total Lines:   {metrics['total_lines']}")
            print(f"  Code Lines:    {metrics['code_lines']}")
            print(f"  Comment Lines: {metrics['comment_lines']}")
            print(f"  Blank Lines:   {metrics['blank_lines']}")
    
    print(f"\nResults saved to: {output_dir / 'readability_metrics.json'}")
    return results

if __name__ == '__main__':
    analyze_readability()
