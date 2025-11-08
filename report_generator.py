#!/usr/bin/env python3
"""
Report Generator Module
Generates formatted reports from log analysis results.
"""

import json
import csv
from datetime import datetime
from typing import Dict, List
import os


class ReportGenerator:
    """Generates various types of reports from analysis results."""

    def __init__(self, analysis_report: Dict):
        self.report = analysis_report
        self.output_dir = "output"
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_text_report(self, filename: str = None) -> str:
        """Generate a detailed text report."""
        if filename is None:
            filename = os.path.join(self.output_dir, f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")

        with open(filename, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("LOG ANALYSIS REPORT\n")
            f.write("=" * 80 + "\n\n")

            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Log File: {self.report['file']}\n")
            f.write(f"Total Entries Analyzed: {self.report['total_entries']:,}\n\n")

            # Severity Summary
            f.write("-" * 80 + "\n")
            f.write("SEVERITY BREAKDOWN\n")
            f.write("-" * 80 + "\n")
            severity_order = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'UNKNOWN']
            for severity in severity_order:
                count = self.report['severity_breakdown'].get(severity, 0)
                if count > 0:
                    percentage = (count / self.report['total_entries']) * 100
                    f.write(f"{severity:12} : {count:6,} ({percentage:5.2f}%)\n")

            # Critical Statistics
            f.write("\n" + "-" * 80 + "\n")
            f.write("CRITICAL STATISTICS\n")
            f.write("-" * 80 + "\n")
            f.write(f"Critical Events: {self.report.get('critical_count', 0):,}\n")
            f.write(f"Error Events:    {self.report.get('error_count', 0):,}\n")
            f.write(f"Warning Events:  {self.report.get('warning_count', 0):,}\n")
            total_issues = self.report.get('critical_count', 0) + self.report.get('error_count', 0)
            f.write(f"Total Issues:    {total_issues:,}\n")

            # Error Patterns
            f.write("\n" + "-" * 80 + "\n")
            f.write("ERROR PATTERNS DETECTED\n")
            f.write("-" * 80 + "\n")
            error_patterns = self.report.get('error_patterns', {})
            if error_patterns:
                sorted_patterns = sorted(error_patterns.items(), key=lambda x: x[1], reverse=True)
                for pattern, count in sorted_patterns:
                    if count > 0:
                        f.write(f"{pattern.replace('_', ' ').title():30} : {count:5} occurrences\n")
            else:
                f.write("No specific error patterns detected.\n")

            # Anomalies
            f.write("\n" + "-" * 80 + "\n")
            f.write("ANOMALIES AND ALERTS\n")
            f.write("-" * 80 + "\n")
            anomalies = self.report.get('anomalies', [])
            if anomalies:
                for i, anomaly in enumerate(anomalies, 1):
                    f.write(f"\n[{i}] {anomaly['type'].upper().replace('_', ' ')}\n")
                    if anomaly['type'] == 'error_spike':
                        f.write(f"    Timestamp: {anomaly['timestamp']}\n")
                        f.write(f"    Error Count: {anomaly['count']} (avg: {anomaly['average']:.2f})\n")
                        f.write(f"    Severity: {anomaly['severity']}\n")
                    elif anomaly['type'] == 'repeated_error':
                        f.write(f"    Message: {anomaly['message']}\n")
                        f.write(f"    Occurrences: {anomaly['count']}\n")
                        f.write(f"    Severity: {anomaly['severity']}\n")
            else:
                f.write("No anomalies detected.\n")

            # Top Error Details
            f.write("\n" + "-" * 80 + "\n")
            f.write("TOP ERROR SAMPLES\n")
            f.write("-" * 80 + "\n")
            error_details = self.report.get('error_pattern_details', {})
            for pattern_name, occurrences in list(error_details.items())[:5]:
                if occurrences:
                    f.write(f"\n{pattern_name.replace('_', ' ').title()}:\n")
                    for occ in occurrences[:3]:  # Show first 3 samples
                        f.write(f"  Line {occ['line']}: {occ['message'][:100]}\n")

            # Time Distribution Summary
            f.write("\n" + "-" * 80 + "\n")
            f.write("TIME DISTRIBUTION SUMMARY\n")
            f.write("-" * 80 + "\n")
            time_dist = self.report.get('time_distribution', {})
            if time_dist:
                f.write(f"Total Time Buckets: {len(time_dist)}\n")
                # Find peak error times
                peak_errors = []
                for bucket, severities in time_dist.items():
                    error_count = severities.get('ERROR', 0) + severities.get('CRITICAL', 0)
                    if error_count > 0:
                        peak_errors.append((bucket, error_count))

                if peak_errors:
                    peak_errors.sort(key=lambda x: x[1], reverse=True)
                    f.write("\nPeak Error Times:\n")
                    for bucket, count in peak_errors[:10]:
                        f.write(f"  {bucket}: {count} errors\n")
            else:
                f.write("No timestamp information available.\n")

            # Recommendations
            f.write("\n" + "-" * 80 + "\n")
            f.write("RECOMMENDATIONS\n")
            f.write("-" * 80 + "\n")
            self._write_recommendations(f)

            f.write("\n" + "=" * 80 + "\n")
            f.write("END OF REPORT\n")
            f.write("=" * 80 + "\n")

        print(f"Text report generated: {filename}")
        return filename

    def _write_recommendations(self, f):
        """Write automated recommendations based on analysis."""
        critical_count = self.report.get('critical_count', 0)
        error_count = self.report.get('error_count', 0)
        anomalies = self.report.get('anomalies', [])

        recommendations = []

        if critical_count > 0:
            recommendations.append(
                f"⚠ URGENT: {critical_count} critical events detected. Immediate attention required."
            )

        if error_count > 100:
            recommendations.append(
                f"⚠ HIGH: {error_count} errors detected. Consider investigating root causes."
            )

        error_patterns = self.report.get('error_patterns', {})
        if error_patterns.get('connection_error', 0) > 10:
            recommendations.append(
                "→ Connection errors detected. Check network stability and service availability."
            )

        if error_patterns.get('database_error', 0) > 10:
            recommendations.append(
                "→ Database errors detected. Review database connections and query performance."
            )

        if error_patterns.get('memory_error', 0) > 0:
            recommendations.append(
                "→ Memory errors detected. Consider increasing heap size or investigating memory leaks."
            )

        spike_anomalies = [a for a in anomalies if a['type'] == 'error_spike']
        if spike_anomalies:
            recommendations.append(
                f"→ {len(spike_anomalies)} error spikes detected. Investigate temporal patterns."
            )

        repeated_errors = [a for a in anomalies if a['type'] == 'repeated_error']
        if repeated_errors:
            recommendations.append(
                f"→ {len(repeated_errors)} repeated error patterns found. May indicate systematic issues."
            )

        if recommendations:
            for rec in recommendations:
                f.write(rec + "\n")
        else:
            f.write("✓ No critical issues detected. System appears healthy.\n")

    def generate_html_report(self, filename: str = None) -> str:
        """Generate an interactive HTML report."""
        if filename is None:
            filename = os.path.join(self.output_dir, f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")

        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Log Analysis Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        .content {{
            padding: 30px;
        }}
        .section {{
            margin-bottom: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }}
        .section h2 {{
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.5em;
        }}
        .stat-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .stat-value {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}
        .stat-label {{
            color: #666;
            margin-top: 5px;
        }}
        .critical {{ color: #dc3545; }}
        .error {{ color: #fd7e14; }}
        .warning {{ color: #ffc107; }}
        .info {{ color: #17a2b8; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 8px;
            overflow: hidden;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #dee2e6;
        }}
        th {{
            background: #667eea;
            color: white;
            font-weight: 600;
        }}
        tr:hover {{
            background: #f8f9fa;
        }}
        .anomaly {{
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 4px;
        }}
        .anomaly.high {{
            background: #f8d7da;
            border-left-color: #dc3545;
        }}
        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: 600;
        }}
        .badge-critical {{ background: #dc3545; color: white; }}
        .badge-error {{ background: #fd7e14; color: white; }}
        .badge-warning {{ background: #ffc107; color: #000; }}
        .badge-medium {{ background: #ffc107; color: #000; }}
        .badge-high {{ background: #dc3545; color: white; }}
        .footer {{
            text-align: center;
            padding: 20px;
            color: #666;
            border-top: 1px solid #dee2e6;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Log Analysis Report</h1>
            <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>Log File:</strong> {self.report['file']}</p>
        </div>

        <div class="content">
            <div class="section">
                <h2>📈 Overview</h2>
                <div class="stat-grid">
                    <div class="stat-card">
                        <div class="stat-value">{self.report['total_entries']:,}</div>
                        <div class="stat-label">Total Entries</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value critical">{self.report.get('critical_count', 0):,}</div>
                        <div class="stat-label">Critical</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value error">{self.report.get('error_count', 0):,}</div>
                        <div class="stat-label">Errors</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value warning">{self.report.get('warning_count', 0):,}</div>
                        <div class="stat-label">Warnings</div>
                    </div>
                </div>
            </div>

            <div class="section">
                <h2>🔍 Severity Breakdown</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Severity Level</th>
                            <th>Count</th>
                            <th>Percentage</th>
                        </tr>
                    </thead>
                    <tbody>
"""

        # Add severity breakdown
        severity_order = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'UNKNOWN']
        for severity in severity_order:
            count = self.report['severity_breakdown'].get(severity, 0)
            if count > 0:
                percentage = (count / self.report['total_entries']) * 100
                severity_class = severity.lower()
                html_content += f"""
                        <tr>
                            <td><span class="badge badge-{severity_class}">{severity}</span></td>
                            <td>{count:,}</td>
                            <td>{percentage:.2f}%</td>
                        </tr>
"""

        html_content += """
                    </tbody>
                </table>
            </div>

            <div class="section">
                <h2>⚠️ Error Patterns</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Pattern Type</th>
                            <th>Occurrences</th>
                        </tr>
                    </thead>
                    <tbody>
"""

        # Add error patterns
        error_patterns = self.report.get('error_patterns', {})
        sorted_patterns = sorted(error_patterns.items(), key=lambda x: x[1], reverse=True)
        for pattern, count in sorted_patterns:
            if count > 0:
                pattern_display = pattern.replace('_', ' ').title()
                html_content += f"""
                        <tr>
                            <td>{pattern_display}</td>
                            <td><strong>{count}</strong></td>
                        </tr>
"""

        html_content += """
                    </tbody>
                </table>
            </div>

            <div class="section">
                <h2>🚨 Anomalies Detected</h2>
"""

        anomalies = self.report.get('anomalies', [])
        if anomalies:
            for anomaly in anomalies:
                severity_class = 'high' if anomaly.get('severity') == 'HIGH' else ''
                anomaly_type = anomaly['type'].replace('_', ' ').title()

                if anomaly['type'] == 'error_spike':
                    html_content += f"""
                <div class="anomaly {severity_class}">
                    <strong>{anomaly_type}</strong>
                    <span class="badge badge-{anomaly.get('severity', 'medium').lower()}">{anomaly.get('severity', 'MEDIUM')}</span>
                    <p>Timestamp: {anomaly['timestamp']}<br>
                    Error Count: {anomaly['count']} (Average: {anomaly['average']:.2f})</p>
                </div>
"""
                elif anomaly['type'] == 'repeated_error':
                    html_content += f"""
                <div class="anomaly {severity_class}">
                    <strong>{anomaly_type}</strong>
                    <span class="badge badge-{anomaly.get('severity', 'medium').lower()}">{anomaly.get('severity', 'MEDIUM')}</span>
                    <p>Occurrences: {anomaly['count']}<br>
                    Message: {anomaly['message']}</p>
                </div>
"""
        else:
            html_content += "<p>No anomalies detected.</p>"

        html_content += """
            </div>
        </div>

        <div class="footer">
            <p>Generated by Log Pattern Detector</p>
        </div>
    </div>
</body>
</html>
"""

        with open(filename, 'w') as f:
            f.write(html_content)

        print(f"HTML report generated: {filename}")
        return filename

    def generate_csv_export(self, filename: str = None) -> str:
        """Export error patterns to CSV."""
        if filename is None:
            filename = os.path.join(self.output_dir, f"errors_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")

        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Pattern Type', 'Line Number', 'Timestamp', 'Severity', 'Message'])

            error_details = self.report.get('error_pattern_details', {})
            for pattern_name, occurrences in error_details.items():
                for occ in occurrences:
                    writer.writerow([
                        pattern_name,
                        occ['line'],
                        occ.get('timestamp', 'N/A'),
                        occ['severity'],
                        occ['message']
                    ])

        print(f"CSV export generated: {filename}")
        return filename

    def generate_json_export(self, filename: str = None) -> str:
        """Export full report as JSON."""
        if filename is None:
            filename = os.path.join(self.output_dir, f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

        # Convert datetime objects to strings for JSON serialization
        report_copy = self.report.copy()

        with open(filename, 'w') as f:
            json.dump(report_copy, f, indent=2, default=str)

        print(f"JSON export generated: {filename}")
        return filename
