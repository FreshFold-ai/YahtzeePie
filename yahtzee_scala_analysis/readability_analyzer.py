#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

def count_lines_in_file(file_path):
    """Count lines of code, comments, and blank lines in a Scala file."""
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    total = len(lines)
    blank = sum(1 for line in lines if line.strip() == '')
    comments = sum(1 for line in lines if line.strip().startswith('//'))
    code = total - blank - comments
    
    return {
        'total': total,
        'code': code,
        'comments': comments,
        'blank': blank
    }

def analyze_scala_files():
    """Analyze all Scala source files."""
    scala_dir = Path(__file__).parent.parent / 'yahtzee_scala' / 'src' / 'main' / 'scala' / 'yahtzee'
    
    results = {}
    total_stats = {'total': 0, 'code': 0, 'comments': 0, 'blank': 0}
    
    for scala_file in scala_dir.glob('*.scala'):
        stats = count_lines_in_file(scala_file)
        results[scala_file.name] = stats
        
        for key in total_stats:
            total_stats[key] += stats[key]
    
    results['_total'] = total_stats
    
    return results

def run_scalafmt_check():
    """Check code formatting with scalafmt."""
    try:
        scala_dir = Path(__file__).parent.parent / 'yahtzee_scala'
        result = subprocess.run(
            ['scalafmt', '--test'],
            cwd=scala_dir,
            capture_output=True,
            text=True,
            timeout=30
        )
        return {
            'available': True,
            'formatted': result.returncode == 0,
            'output': result.stdout + result.stderr
        }
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return {
            'available': False,
            'formatted': None,
            'output': 'scalafmt not available'
        }

def count_functions_and_classes():
    """Count functions, classes, and case classes in Scala files."""
    scala_dir = Path(__file__).parent.parent / 'yahtzee_scala' / 'src' / 'main' / 'scala' / 'yahtzee'
    
    stats = {
        'objects': 0,
        'case_classes': 0,
        'classes': 0,
        'def_functions': 0,
        'extension_methods': 0,
        'opaque_types': 0
    }
    
    for scala_file in scala_dir.glob('*.scala'):
        with open(scala_file, 'r') as f:
            content = f.read()
            lines = content.split('\n')
            
            for line in lines:
                stripped = line.strip()
                if stripped.startswith('object '):
                    stats['objects'] += 1
                elif stripped.startswith('case class '):
                    stats['case_classes'] += 1
                elif stripped.startswith('class '):
                    stats['classes'] += 1
                elif stripped.startswith('def '):
                    stats['def_functions'] += 1
                elif 'extension' in stripped:
                    stats['extension_methods'] += 1
                elif 'opaque type' in stripped:
                    stats['opaque_types'] += 1
    
    return stats

def analyze_immutability():
    """Analyze immutability patterns in Scala code."""
    scala_dir = Path(__file__).parent.parent / 'yahtzee_scala' / 'src' / 'main' / 'scala' / 'yahtzee'
    
    stats = {
        'val_count': 0,
        'var_count': 0,
        'case_class_count': 0,
        'copy_usage': 0,
        'map_usage': 0
    }
    
    for scala_file in scala_dir.glob('*.scala'):
        with open(scala_file, 'r') as f:
            content = f.read()
            
            stats['val_count'] += content.count(' val ')
            stats['var_count'] += content.count(' var ')
            stats['case_class_count'] += content.count('case class')
            stats['copy_usage'] += content.count('.copy(')
            stats['map_usage'] += content.count('.map(')
    
    return stats

def run_readability_analysis():
    print("Running Scala readability analysis...")
    
    line_counts = analyze_scala_files()
    structure_stats = count_functions_and_classes()
    immutability_stats = analyze_immutability()
    formatting = run_scalafmt_check()
    
    all_results = {
        'line_counts': line_counts,
        'structure': structure_stats,
        'immutability': immutability_stats,
        'formatting': formatting
    }
    
    # Save to JSON
    output_dir = Path(__file__).parent / 'data'
    output_dir.mkdir(exist_ok=True)
    
    with open(output_dir / 'readability_metrics.json', 'w') as f:
        json.dump(all_results, f, indent=2)
    
    # Print results
    print("\nReadability Analysis Results:")
    print("=" * 80)
    
    print("\nLINE COUNTS:")
    print("-" * 80)
    for filename, stats in sorted(line_counts.items()):
        if filename != '_total':
            print(f"  {filename:25s} | Total: {stats['total']:4d} | Code: {stats['code']:4d} | Comments: {stats['comments']:3d} | Blank: {stats['blank']:3d}")
    
    total = line_counts['_total']
    print(f"  {'TOTAL':25s} | Total: {total['total']:4d} | Code: {total['code']:4d} | Comments: {total['comments']:3d} | Blank: {total['blank']:3d}")
    
    print("\nSTRUCTURE:")
    print("-" * 80)
    for key, value in sorted(structure_stats.items()):
        print(f"  {key.replace('_', ' ').title():25s} : {value}")
    
    print("\nIMMUTABILITY PATTERNS:")
    print("-" * 80)
    for key, value in sorted(immutability_stats.items()):
        print(f"  {key.replace('_', ' ').title():25s} : {value}")
    
    if immutability_stats['var_count'] == 0:
        print("  ✓ No mutable variables (var) found - Pure functional!")
    
    print(f"\nResults saved to: {output_dir / 'readability_metrics.json'}")

if __name__ == '__main__':
    run_readability_analysis()
