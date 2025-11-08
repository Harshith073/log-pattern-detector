#!/usr/bin/env python3
"""
Main CLI tool for Log Pattern Detector
Comprehensive log analysis with reporting and visualization.
"""

import argparse
import sys
import os
from log_analyzer import LogAnalyzer
from report_generator import ReportGenerator
from visualizer import LogVisualizer


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description='Log Pattern Detector - Analyze logs for patterns and anomalies',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s server.log                           # Analyze log file
  %(prog)s server.log -o report.txt             # Save text report
  %(prog)s server.log --html report.html        # Generate HTML report
  %(prog)s server.log --visualize               # Create visualizations
  %(prog)s server.log --all                     # Generate everything
  %(prog)s server.log --dashboard               # Start web dashboard

For more information, visit: https://github.com/yourusername/log-pattern-detector
        """
    )

    parser.add_argument('log_file', help='Path to the log file to analyze')
    parser.add_argument('-o', '--output', help='Output file for text report')
    parser.add_argument('--html', help='Generate HTML report')
    parser.add_argument('--csv', help='Export errors to CSV')
    parser.add_argument('--json', help='Export report as JSON')
    parser.add_argument('-v', '--visualize', action='store_true',
                       help='Generate visualization charts')
    parser.add_argument('-a', '--all', action='store_true',
                       help='Generate all reports and visualizations')
    parser.add_argument('--dashboard', action='store_true',
                       help='Start web dashboard (requires Flask)')
    parser.add_argument('--quiet', action='store_true',
                       help='Suppress console output')

    args = parser.parse_args()

    # Validate log file
    if not os.path.exists(args.log_file):
        print(f"Error: Log file not found: {args.log_file}", file=sys.stderr)
        sys.exit(1)

    try:
        # Analyze log file
        if not args.quiet:
            print("=" * 80)
            print("LOG PATTERN DETECTOR")
            print("=" * 80)
            print()

        analyzer = LogAnalyzer(args.log_file)
        report = analyzer.analyze()

        if not args.quiet:
            print("\n" + "=" * 80)
            print("ANALYSIS SUMMARY")
            print("=" * 80)
            print(f"Total Entries: {report['total_entries']:,}")
            print(f"Critical:      {report.get('critical_count', 0):,}")
            print(f"Errors:        {report.get('error_count', 0):,}")
            print(f"Warnings:      {report.get('warning_count', 0):,}")
            print(f"Anomalies:     {len(report.get('anomalies', [])):,}")

        # Generate reports
        generator = ReportGenerator(report)

        if args.output or args.all:
            output_file = args.output if args.output else None
            text_file = generator.generate_text_report(output_file)
            if not args.quiet:
                print(f"\n✓ Text report: {text_file}")

        if args.html or args.all:
            html_file = args.html if args.html else None
            html_file = generator.generate_html_report(html_file)
            if not args.quiet:
                print(f"✓ HTML report: {html_file}")

        if args.csv or args.all:
            csv_file = args.csv if args.csv else None
            csv_file = generator.generate_csv_export(csv_file)
            if not args.quiet:
                print(f"✓ CSV export:  {csv_file}")

        if args.json or args.all:
            json_file = args.json if args.json else None
            json_file = generator.generate_json_export(json_file)
            if not args.quiet:
                print(f"✓ JSON export: {json_file}")

        # Generate visualizations
        if args.visualize or args.all:
            if not args.quiet:
                print("\nGenerating visualizations...")

            visualizer = LogVisualizer(report)
            visualizer.generate_all_visualizations()

            if not args.quiet:
                print("✓ All visualizations generated in 'output/' directory")

        # Show top errors
        if not args.quiet:
            top_errors = analyzer.get_top_errors(5)
            if top_errors:
                print("\n" + "=" * 80)
                print("TOP ERROR PATTERNS")
                print("=" * 80)
                for i, error in enumerate(top_errors, 1):
                    print(f"{i}. {error['pattern'].replace('_', ' ').title()}: {error['count']} occurrences")

        # Show anomalies
        if not args.quiet and report.get('anomalies'):
            print("\n" + "=" * 80)
            print("ANOMALIES DETECTED")
            print("=" * 80)
            for anomaly in report['anomalies'][:3]:
                if anomaly['type'] == 'error_spike':
                    print(f"⚠ Error Spike at {anomaly['timestamp']}: {anomaly['count']} errors")
                elif anomaly['type'] == 'repeated_error':
                    print(f"⚠ Repeated Error: {anomaly['count']} occurrences")

        if not args.quiet:
            print("\n" + "=" * 80)
            print("Analysis complete!")
            print("=" * 80)

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"\nError during analysis: {e}", file=sys.stderr)
        if not args.quiet:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
