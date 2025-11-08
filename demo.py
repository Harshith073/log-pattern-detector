#!/usr/bin/env python3
"""
Demo script showing various uses of the Log Pattern Detector API.
"""

from log_analyzer import LogAnalyzer
from report_generator import ReportGenerator
from visualizer import LogVisualizer
import os


def demo_basic_analysis():
    """Demonstrate basic log analysis."""
    print("=" * 80)
    print("DEMO 1: Basic Log Analysis")
    print("=" * 80)

    analyzer = LogAnalyzer('sample_logs/application.log')
    report = analyzer.analyze()

    print(f"\nTotal Entries: {report['total_entries']}")
    print(f"Critical:      {report.get('critical_count', 0)}")
    print(f"Errors:        {report.get('error_count', 0)}")
    print(f"Warnings:      {report.get('warning_count', 0)}")
    print(f"Anomalies:     {len(report.get('anomalies', []))}")


def demo_error_patterns():
    """Demonstrate error pattern detection."""
    print("\n" + "=" * 80)
    print("DEMO 2: Error Pattern Detection")
    print("=" * 80)

    analyzer = LogAnalyzer('sample_logs/application.log')
    report = analyzer.analyze()

    print("\nTop 5 Error Patterns:")
    top_errors = analyzer.get_top_errors(5)
    for i, error in enumerate(top_errors, 1):
        print(f"{i}. {error['pattern']}: {error['count']} occurrences")


def demo_report_generation():
    """Demonstrate report generation."""
    print("\n" + "=" * 80)
    print("DEMO 3: Report Generation")
    print("=" * 80)

    analyzer = LogAnalyzer('sample_logs/application.log')
    report = analyzer.analyze()
    generator = ReportGenerator(report)

    # Generate reports
    text_file = generator.generate_text_report('output/demo_report.txt')
    html_file = generator.generate_html_report('output/demo_report.html')
    csv_file = generator.generate_csv_export('output/demo_errors.csv')

    print(f"\n✓ Generated text report: {text_file}")
    print(f"✓ Generated HTML report: {html_file}")
    print(f"✓ Generated CSV export:  {csv_file}")


def demo_visualizations():
    """Demonstrate visualization generation."""
    print("\n" + "=" * 80)
    print("DEMO 4: Visualization Generation")
    print("=" * 80)

    analyzer = LogAnalyzer('sample_logs/application.log')
    report = analyzer.analyze()
    visualizer = LogVisualizer(report)

    print("\nGenerating visualizations...")
    visualizer.create_severity_pie_chart('output/demo_severity.png')
    visualizer.create_error_pattern_bar_chart('output/demo_patterns.png')
    visualizer.create_timeline_chart('output/demo_timeline.png')

    print("✓ Severity distribution chart created")
    print("✓ Error patterns chart created")
    print("✓ Timeline chart created")


def demo_anomaly_detection():
    """Demonstrate anomaly detection."""
    print("\n" + "=" * 80)
    print("DEMO 5: Anomaly Detection")
    print("=" * 80)

    analyzer = LogAnalyzer('sample_logs/webserver.log')
    report = analyzer.analyze()

    anomalies = report.get('anomalies', [])
    if anomalies:
        print(f"\nDetected {len(anomalies)} anomalies:")
        for i, anomaly in enumerate(anomalies, 1):
            print(f"\n{i}. {anomaly['type'].upper().replace('_', ' ')}")
            if anomaly['type'] == 'error_spike':
                print(f"   Time: {anomaly['timestamp']}")
                print(f"   Count: {anomaly['count']} (avg: {anomaly['average']:.2f})")
                print(f"   Severity: {anomaly['severity']}")
            elif anomaly['type'] == 'repeated_error':
                print(f"   Count: {anomaly['count']}")
                print(f"   Message: {anomaly['message'][:80]}...")
    else:
        print("\nNo anomalies detected in this log file.")


def demo_multi_file_comparison():
    """Demonstrate comparing multiple log files."""
    print("\n" + "=" * 80)
    print("DEMO 6: Multi-File Comparison")
    print("=" * 80)

    log_files = [
        'sample_logs/application.log',
        'sample_logs/webserver.log'
    ]

    print("\nAnalyzing multiple log files...\n")
    print(f"{'Log File':<30} {'Entries':>10} {'Errors':>10} {'Warnings':>10}")
    print("-" * 65)

    for log_file in log_files:
        if os.path.exists(log_file):
            analyzer = LogAnalyzer(log_file)
            report = analyzer.analyze()

            filename = os.path.basename(log_file)
            print(f"{filename:<30} {report['total_entries']:>10} "
                  f"{report.get('error_count', 0):>10} "
                  f"{report.get('warning_count', 0):>10}")


def main():
    """Run all demos."""
    print("\n")
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║       Log Pattern Detector - Interactive Demo                 ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print()

    # Ensure output directory exists
    os.makedirs('output', exist_ok=True)

    # Run all demos
    demo_basic_analysis()
    demo_error_patterns()
    demo_report_generation()
    demo_visualizations()
    demo_anomaly_detection()
    demo_multi_file_comparison()

    print("\n" + "=" * 80)
    print("Demo Complete!")
    print("=" * 80)
    print("\nCheck the 'output/' directory for generated reports and visualizations.")
    print("\nFor more examples, see USAGE.md")
    print()


if __name__ == '__main__':
    main()
