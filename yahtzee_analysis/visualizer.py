import json
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def load_json_data(filename):
    data_dir = Path(__file__).parent / 'data'
    filepath = data_dir / filename
    if filepath.exists():
        with open(filepath) as f:
            return json.load(f)
    return None

def visualize_performance():
    data = load_json_data('performance_metrics.json')
    if not data:
        print("No performance data found. Run performance_profiler.py first.")
        return
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Performance Analysis', fontsize=16, fontweight='bold')
    
    methods = []
    times = []
    memory = []
    
    for module, module_data in data.items():
        for method, metrics in module_data.items():
            methods.append(f"{module}.{method}")
            times.append(metrics['execution_time_ms'])
            memory.append(metrics['memory_used_kb'])
    
    y_pos = np.arange(len(methods))
    
    ax1.barh(y_pos, times, color='steelblue')
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(methods, fontsize=8)
    ax1.set_xlabel('Execution Time (ms)')
    ax1.set_title('Method Execution Time')
    ax1.invert_yaxis()
    
    ax2.barh(y_pos, memory, color='coral')
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(methods, fontsize=8)
    ax2.set_xlabel('Memory Used (KB)')
    ax2.set_title('Memory Usage')
    ax2.invert_yaxis()
    
    plt.tight_layout()
    
    output_dir = Path(__file__).parent / 'visualizations'
    output_dir.mkdir(exist_ok=True)
    plt.savefig(output_dir / 'performance_metrics.png', dpi=300, bbox_inches='tight')
    print(f"Performance visualization saved to: {output_dir / 'performance_metrics.png'}")
    plt.close()

def visualize_readability():
    data = load_json_data('readability_metrics.json')
    if not data:
        print("No readability data found. Run readability_analyzer.py first.")
        return
    
    files = []
    code_lines = []
    comment_lines = []
    blank_lines = []
    
    for file, metrics in data.items():
        if isinstance(metrics, dict) and 'total_lines' in metrics:
            files.append(file)
            code_lines.append(metrics['code_lines'])
            comment_lines.append(metrics['comment_lines'])
            blank_lines.append(metrics['blank_lines'])
    
    if not files:
        return
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Readability Analysis', fontsize=16, fontweight='bold')
    
    x = np.arange(len(files))
    width = 0.25
    
    ax1.bar(x - width, code_lines, width, label='Code Lines', color='steelblue')
    ax1.bar(x, comment_lines, width, label='Comment Lines', color='lightgreen')
    ax1.bar(x + width, blank_lines, width, label='Blank Lines', color='lightgray')
    ax1.set_xlabel('Files')
    ax1.set_ylabel('Lines of Code')
    ax1.set_title('Lines of Code by Type')
    ax1.set_xticks(x)
    ax1.set_xticklabels(files, rotation=45, ha='right')
    ax1.legend()
    
    total_lines = [code_lines[i] + comment_lines[i] + blank_lines[i] for i in range(len(files))]
    colors = ['steelblue', 'coral', 'lightgreen', 'gold']
    ax2.pie(total_lines, labels=files, autopct='%1.1f%%', colors=colors, startangle=90)
    ax2.set_title('Code Distribution by File')
    
    plt.tight_layout()
    
    output_dir = Path(__file__).parent / 'visualizations'
    output_dir.mkdir(exist_ok=True)
    plt.savefig(output_dir / 'readability_metrics.png', dpi=300, bbox_inches='tight')
    print(f"Readability visualization saved to: {output_dir / 'readability_metrics.png'}")
    plt.close()

def visualize_pylint():
    data = load_json_data('pylint_metrics.json')
    if not data:
        print("No pylint data found. Run debugging_analyzer.py first.")
        return
    
    files = []
    total_issues = []
    issue_types = {}
    
    for file, metrics in data.items():
        if isinstance(metrics, dict) and 'total_issues' in metrics:
            files.append(file)
            total_issues.append(metrics['total_issues'])
            for issue_type, count in metrics.get('by_type', {}).items():
                if issue_type not in issue_types:
                    issue_types[issue_type] = []
                issue_types[issue_type].append(count)
    
    if not files:
        return
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Debugging Analysis - Pylint Issues', fontsize=16, fontweight='bold')
    
    ax1.bar(files, total_issues, color='coral')
    ax1.set_xlabel('Files')
    ax1.set_ylabel('Total Issues')
    ax1.set_title('Pylint Issues by File')
    ax1.tick_params(axis='x', rotation=45)
    
    if issue_types:
        issue_type_names = list(issue_types.keys())
        issue_counts = [sum(issue_types[t]) for t in issue_type_names]
        colors = plt.cm.Set3(np.linspace(0, 1, len(issue_type_names)))
        ax2.pie(issue_counts, labels=issue_type_names, autopct='%1.1f%%', colors=colors, startangle=90)
        ax2.set_title('Issues by Type')
    
    plt.tight_layout()
    
    output_dir = Path(__file__).parent / 'visualizations'
    output_dir.mkdir(exist_ok=True)
    plt.savefig(output_dir / 'debugging_metrics.png', dpi=300, bbox_inches='tight')
    print(f"Debugging visualization saved to: {output_dir / 'debugging_metrics.png'}")
    plt.close()

def create_summary_visualization():
    perf_data = load_json_data('performance_metrics.json')
    read_data = load_json_data('readability_metrics.json')
    
    if not perf_data or not read_data:
        return
    
    fig = plt.figure(figsize=(16, 10))
    fig.suptitle('Yahtzee Python Implementation - Analysis Summary', fontsize=18, fontweight='bold')
    
    total_methods = sum(len(module_data) for module_data in perf_data.values())
    total_lines = sum(m['total_lines'] for m in read_data.values() if isinstance(m, dict) and 'total_lines' in m)
    total_code_lines = sum(m['code_lines'] for m in read_data.values() if isinstance(m, dict) and 'code_lines' in m)
    
    summary_text = f"""
    Analysis Summary
    ================
    
    Performance:
    - Methods Analyzed: {total_methods}
    - Avg Execution Time: {np.mean([m['execution_time_ms'] for mod in perf_data.values() for m in mod.values()]):.4f} ms
    
    Readability:
    - Total Lines: {total_lines}
    - Code Lines: {total_code_lines}
    - Files Analyzed: {len([f for f, m in read_data.items() if isinstance(m, dict) and 'total_lines' in m])}
    """
    
    ax = fig.add_subplot(111)
    ax.text(0.5, 0.5, summary_text, fontsize=14, family='monospace',
            verticalalignment='center', horizontalalignment='center',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    ax.axis('off')
    
    output_dir = Path(__file__).parent / 'visualizations'
    output_dir.mkdir(exist_ok=True)
    plt.savefig(output_dir / 'summary.png', dpi=300, bbox_inches='tight')
    print(f"Summary visualization saved to: {output_dir / 'summary.png'}")
    plt.close()

if __name__ == '__main__':
    print("Generating visualizations...")
    visualize_performance()
    visualize_readability()
    visualize_pylint()
    create_summary_visualization()
    print("\nAll visualizations generated successfully!")
