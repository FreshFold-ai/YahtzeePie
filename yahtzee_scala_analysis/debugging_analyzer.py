#!/usr/bin/env python3
import json
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

def run_scala_tests():
    """Run Scala tests and capture results."""
    scala_dir = Path(__file__).parent.parent / 'yahtzee_scala'
    
    try:
        result = subprocess.run(
            ['sbt', 'test'],
            cwd=scala_dir,
            capture_output=True,
            text=True,
            timeout=120
        )
        
        return {
            'success': result.returncode == 0,
            'output': result.stdout,
            'errors': result.stderr
        }
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'output': '',
            'errors': 'Test execution timed out'
        }
    except FileNotFoundError:
        return {
            'success': False,
            'output': '',
            'errors': 'SBT not found'
        }

def parse_test_reports():
    """Parse JUnit XML test reports."""
    scala_dir = Path(__file__).parent.parent / 'yahtzee_scala'
    test_reports_dir = scala_dir / 'target' / 'test-reports'
    
    if not test_reports_dir.exists():
        return None
    
    total_tests = 0
    total_failures = 0
    total_errors = 0
    total_skipped = 0
    total_time = 0.0
    test_suites = []
    
    for xml_file in test_reports_dir.glob('TEST-*.xml'):
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            
            suite_name = root.get('name', 'Unknown')
            tests = int(root.get('tests', 0))
            failures = int(root.get('failures', 0))
            errors = int(root.get('errors', 0))
            skipped = int(root.get('skipped', 0))
            time = float(root.get('time', 0.0))
            
            total_tests += tests
            total_failures += failures
            total_errors += errors
            total_skipped += skipped
            total_time += time
            
            test_suites.append({
                'name': suite_name,
                'tests': tests,
                'failures': failures,
                'errors': errors,
                'skipped': skipped,
                'time': time
            })
        except Exception as e:
            print(f"Error parsing {xml_file}: {e}")
    
    return {
        'total_tests': total_tests,
        'total_failures': total_failures,
        'total_errors': total_errors,
        'total_skipped': total_skipped,
        'total_time': total_time,
        'test_suites': test_suites,
        'pass_rate': ((total_tests - total_failures - total_errors) / total_tests * 100) if total_tests > 0 else 0
    }

def check_scalastyle():
    """Check code style with scalastyle if available."""
    scala_dir = Path(__file__).parent.parent / 'yahtzee_scala'
    
    try:
        result = subprocess.run(
            ['sbt', 'scalastyle'],
            cwd=scala_dir,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        # Parse output for warnings/errors
        output = result.stdout + result.stderr
        warnings = output.count('warning')
        errors = output.count('error')
        
        return {
            'available': True,
            'warnings': warnings,
            'errors': errors,
            'output': output
        }
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return {
            'available': False,
            'warnings': 0,
            'errors': 0,
            'output': 'Scalastyle not configured'
        }

def analyze_error_handling():
    """Analyze error handling patterns (Either, Try, Option)."""
    scala_dir = Path(__file__).parent.parent / 'yahtzee_scala' / 'src' / 'main' / 'scala' / 'yahtzee'
    
    stats = {
        'either_usage': 0,
        'option_usage': 0,
        'try_usage': 0,
        'require_usage': 0,
        'left_usage': 0,
        'right_usage': 0,
        'none_usage': 0,
        'some_usage': 0
    }
    
    for scala_file in scala_dir.glob('*.scala'):
        with open(scala_file, 'r') as f:
            content = f.read()
            
            stats['either_usage'] += content.count('Either[')
            stats['option_usage'] += content.count('Option[')
            stats['try_usage'] += content.count('Try[')
            stats['require_usage'] += content.count('require(')
            stats['left_usage'] += content.count('Left(')
            stats['right_usage'] += content.count('Right(')
            stats['none_usage'] += content.count('None')
            stats['some_usage'] += content.count('Some(')
    
    return stats

def run_debugging_analysis():
    print("Running Scala debugging analysis...")
    
    test_results = parse_test_reports()
    error_handling = analyze_error_handling()
    style_check = check_scalastyle()
    
    all_results = {
        'tests': test_results,
        'error_handling': error_handling,
        'style': style_check
    }
    
    # Save to JSON
    output_dir = Path(__file__).parent / 'data'
    output_dir.mkdir(exist_ok=True)
    
    with open(output_dir / 'debugging_metrics.json', 'w') as f:
        json.dump(all_results, f, indent=2)
    
    # Print results
    print("\nDebugging Analysis Results:")
    print("=" * 80)
    
    if test_results:
        print("\nTEST RESULTS:")
        print("-" * 80)
        print(f"  Total Tests     : {test_results['total_tests']}")
        print(f"  Passed          : {test_results['total_tests'] - test_results['total_failures'] - test_results['total_errors']}")
        print(f"  Failures        : {test_results['total_failures']}")
        print(f"  Errors          : {test_results['total_errors']}")
        print(f"  Skipped         : {test_results['total_skipped']}")
        print(f"  Pass Rate       : {test_results['pass_rate']:.1f}%")
        print(f"  Total Time      : {test_results['total_time']:.3f}s")
        
        print("\n  Test Suites:")
        for suite in test_results['test_suites']:
            status = "✓ PASS" if suite['failures'] == 0 and suite['errors'] == 0 else "✗ FAIL"
            print(f"    {suite['name']:30s} | Tests: {suite['tests']:2d} | {status}")
    else:
        print("\nTEST RESULTS:")
        print("-" * 80)
        print("  No test reports found. Run tests first: sbt test")
    
    print("\nERROR HANDLING PATTERNS:")
    print("-" * 80)
    for key, value in sorted(error_handling.items()):
        print(f"  {key.replace('_', ' ').title():25s} : {value}")
    
    if error_handling['either_usage'] > 0:
        print("  ✓ Using Either for explicit error handling")
    if error_handling['require_usage'] > 0:
        print("  ✓ Using require for preconditions")
    
    print("\nCODE STYLE:")
    print("-" * 80)
    if style_check['available']:
        print(f"  Warnings        : {style_check['warnings']}")
        print(f"  Errors          : {style_check['errors']}")
    else:
        print("  Scalastyle not configured")
    
    print(f"\nResults saved to: {output_dir / 'debugging_metrics.json'}")

if __name__ == '__main__':
    run_debugging_analysis()
