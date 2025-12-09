import subprocess
import json
from pathlib import Path
import sys

yahtzee_game_path = Path(__file__).parent.parent / 'yahtzee_game'
sys.path.insert(0, str(yahtzee_game_path))

def run_pylint_analysis():
    print("Running pylint analysis...")
    
    yahtzee_path = Path(__file__).parent.parent / 'yahtzee_game'
    output_dir = Path(__file__).parent / 'data'
    output_dir.mkdir(exist_ok=True)
    
    source_files = ['dice.py', 'scorecard.py', 'game.py', 'main.py']
    results = {}
    
    for file in source_files:
        file_path = yahtzee_path / file
        if not file_path.exists():
            continue
        
        try:
            result = subprocess.run(
                ['pylint', str(file_path), '--output-format=json'],
                capture_output=True, text=True
            )
            
            if result.stdout:
                issues = json.loads(result.stdout)
                results[file] = {
                    'total_issues': len(issues),
                    'by_type': {},
                    'issues': issues
                }
                
                for issue in issues:
                    issue_type = issue.get('type', 'unknown')
                    results[file]['by_type'][issue_type] = results[file]['by_type'].get(issue_type, 0) + 1
            
        except FileNotFoundError:
            results[file] = 'pylint not installed'
        except json.JSONDecodeError:
            results[file] = 'Could not parse pylint output'
    
    with open(output_dir / 'pylint_metrics.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\nPylint Analysis Results:")
    print("=" * 70)
    for file, metrics in results.items():
        if isinstance(metrics, dict) and 'total_issues' in metrics:
            print(f"\n{file}:")
            print(f"  Total Issues: {metrics['total_issues']}")
            if metrics['by_type']:
                print("  By Type:")
                for issue_type, count in metrics['by_type'].items():
                    print(f"    {issue_type}: {count}")
    
    print(f"\nResults saved to: {output_dir / 'pylint_metrics.json'}")
    return results

def run_test_coverage():
    print("\nRunning test coverage analysis...")
    
    yahtzee_path = Path(__file__).parent.parent / 'yahtzee_game'
    output_dir = Path(__file__).parent / 'data'
    
    try:
        result = subprocess.run(
            ['coverage', 'run', '-m', 'unittest', 'discover', '-s', 'tests'],
            cwd=yahtzee_path,
            capture_output=True, text=True
        )
        
        coverage_report = subprocess.run(
            ['coverage', 'report'],
            cwd=yahtzee_path,
            capture_output=True, text=True
        )
        
        coverage_json = subprocess.run(
            ['coverage', 'json', '-o', str(output_dir / 'coverage.json')],
            cwd=yahtzee_path,
            capture_output=True, text=True
        )
        
        print("\nTest Coverage Report:")
        print("-" * 70)
        print(coverage_report.stdout)
        
        print(f"Coverage data saved to: {output_dir / 'coverage.json'}")
        
    except FileNotFoundError:
        print("coverage not installed - run: pip install coverage")

if __name__ == '__main__':
    run_pylint_analysis()
    run_test_coverage()
