#!/usr/bin/env python3
"""
Visualization Module
Creates charts and graphs from log analysis data.
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from collections import Counter
import os
from typing import Dict, List


class LogVisualizer:
    """Creates visualizations from log analysis results."""

    def __init__(self, analysis_report: Dict):
        self.report = analysis_report
        self.output_dir = "output"
        os.makedirs(self.output_dir, exist_ok=True)

        # Set style
        plt.style.use('seaborn-v0_8-darkgrid')

    def create_severity_pie_chart(self, filename: str = None) -> str:
        """Create pie chart showing severity distribution."""
        if filename is None:
            filename = os.path.join(self.output_dir, "severity_distribution.png")

        severity_counts = self.report.get('severity_breakdown', {})
        if not severity_counts:
            print("No severity data to visualize")
            return None

        # Filter out zero counts
        severity_counts = {k: v for k, v in severity_counts.items() if v > 0}

        # Define colors for each severity
        colors = {
            'CRITICAL': '#dc3545',
            'ERROR': '#fd7e14',
            'WARNING': '#ffc107',
            'INFO': '#17a2b8',
            'DEBUG': '#6c757d',
            'UNKNOWN': '#adb5bd'
        }

        labels = list(severity_counts.keys())
        sizes = list(severity_counts.values())
        color_list = [colors.get(label, '#6c757d') for label in labels]

        fig, ax = plt.subplots(figsize=(10, 8))
        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            colors=color_list,
            autopct='%1.1f%%',
            startangle=90,
            textprops={'fontsize': 12, 'weight': 'bold'}
        )

        # Make percentage text white
        for autotext in autotexts:
            autotext.set_color('white')

        ax.set_title('Log Severity Distribution', fontsize=16, weight='bold', pad=20)
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"Severity pie chart saved: {filename}")
        return filename

    def create_error_pattern_bar_chart(self, filename: str = None) -> str:
        """Create bar chart showing error pattern frequencies."""
        if filename is None:
            filename = os.path.join(self.output_dir, "error_patterns.png")

        error_patterns = self.report.get('error_patterns', {})
        if not error_patterns:
            print("No error patterns to visualize")
            return None

        # Filter and sort patterns
        patterns = {k.replace('_', ' ').title(): v for k, v in error_patterns.items() if v > 0}
        if not patterns:
            print("No error patterns with occurrences")
            return None

        sorted_patterns = sorted(patterns.items(), key=lambda x: x[1], reverse=True)
        pattern_names = [p[0] for p in sorted_patterns[:10]]  # Top 10
        pattern_counts = [p[1] for p in sorted_patterns[:10]]

        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.barh(pattern_names, pattern_counts, color='#667eea')

        ax.set_xlabel('Number of Occurrences', fontsize=12, weight='bold')
        ax.set_ylabel('Error Pattern', fontsize=12, weight='bold')
        ax.set_title('Top Error Patterns', fontsize=16, weight='bold', pad=20)

        # Add value labels on bars
        for i, (bar, count) in enumerate(zip(bars, pattern_counts)):
            ax.text(count, bar.get_y() + bar.get_height()/2,
                   f' {count}', va='center', fontsize=10, weight='bold')

        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"Error pattern bar chart saved: {filename}")
        return filename

    def create_timeline_chart(self, filename: str = None) -> str:
        """Create timeline chart showing errors over time."""
        if filename is None:
            filename = os.path.join(self.output_dir, "timeline.png")

        time_dist = self.report.get('time_distribution', {})
        if not time_dist:
            print("No time distribution data to visualize")
            return None

        # Parse timestamps and aggregate data
        timestamps = []
        critical_counts = []
        error_counts = []
        warning_counts = []

        for bucket, severities in sorted(time_dist.items()):
            try:
                timestamp = datetime.strptime(bucket, '%Y-%m-%d %H:%M')
                timestamps.append(timestamp)
                critical_counts.append(severities.get('CRITICAL', 0))
                error_counts.append(severities.get('ERROR', 0))
                warning_counts.append(severities.get('WARNING', 0))
            except ValueError:
                continue

        if not timestamps:
            print("No valid timestamps for timeline")
            return None

        fig, ax = plt.subplots(figsize=(14, 6))

        # Create stacked area chart
        ax.fill_between(timestamps, 0, critical_counts, alpha=0.7, color='#dc3545', label='Critical')
        ax.fill_between(timestamps, critical_counts,
                        [c + e for c, e in zip(critical_counts, error_counts)],
                        alpha=0.7, color='#fd7e14', label='Error')
        ax.fill_between(timestamps,
                        [c + e for c, e in zip(critical_counts, error_counts)],
                        [c + e + w for c, e, w in zip(critical_counts, error_counts, warning_counts)],
                        alpha=0.7, color='#ffc107', label='Warning')

        ax.set_xlabel('Time', fontsize=12, weight='bold')
        ax.set_ylabel('Number of Events', fontsize=12, weight='bold')
        ax.set_title('Error Timeline', fontsize=16, weight='bold', pad=20)
        ax.legend(loc='upper left')
        ax.grid(True, alpha=0.3)

        # Format x-axis dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
        plt.xticks(rotation=45, ha='right')

        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"Timeline chart saved: {filename}")
        return filename

    def create_heatmap(self, filename: str = None) -> str:
        """Create heatmap showing error density over time."""
        if filename is None:
            filename = os.path.join(self.output_dir, "heatmap.png")

        time_dist = self.report.get('time_distribution', {})
        if not time_dist:
            print("No time distribution data for heatmap")
            return None

        # Organize data by day and hour
        day_hour_errors = {}
        for bucket, severities in time_dist.items():
            try:
                dt = datetime.strptime(bucket, '%Y-%m-%d %H:%M')
                day = dt.strftime('%Y-%m-%d')
                hour = dt.hour
                error_count = severities.get('ERROR', 0) + severities.get('CRITICAL', 0)

                if day not in day_hour_errors:
                    day_hour_errors[day] = [0] * 24
                day_hour_errors[day][hour] += error_count
            except ValueError:
                continue

        if not day_hour_errors:
            print("No valid data for heatmap")
            return None

        # Create matrix for heatmap
        days = sorted(day_hour_errors.keys())
        hours = list(range(24))
        data = [day_hour_errors[day] for day in days]

        fig, ax = plt.subplots(figsize=(14, len(days) * 0.5 + 2))
        im = ax.imshow(data, cmap='YlOrRd', aspect='auto')

        # Set ticks
        ax.set_xticks(hours)
        ax.set_yticks(range(len(days)))
        ax.set_xticklabels([f'{h:02d}:00' for h in hours], rotation=45, ha='right')
        ax.set_yticklabels(days)

        ax.set_xlabel('Hour of Day', fontsize=12, weight='bold')
        ax.set_ylabel('Date', fontsize=12, weight='bold')
        ax.set_title('Error Heatmap (By Day and Hour)', fontsize=16, weight='bold', pad=20)

        # Add colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Number of Errors', rotation=270, labelpad=20, weight='bold')

        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"Heatmap saved: {filename}")
        return filename

    def create_dashboard(self, filename: str = None) -> str:
        """Create comprehensive dashboard with multiple charts."""
        if filename is None:
            filename = os.path.join(self.output_dir, "dashboard.png")

        fig = plt.figure(figsize=(16, 12))
        gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)

        # 1. Severity Distribution (Pie Chart)
        ax1 = fig.add_subplot(gs[0, 0])
        severity_counts = self.report.get('severity_breakdown', {})
        severity_counts = {k: v for k, v in severity_counts.items() if v > 0}
        if severity_counts:
            colors = {
                'CRITICAL': '#dc3545', 'ERROR': '#fd7e14', 'WARNING': '#ffc107',
                'INFO': '#17a2b8', 'DEBUG': '#6c757d', 'UNKNOWN': '#adb5bd'
            }
            labels = list(severity_counts.keys())
            sizes = list(severity_counts.values())
            color_list = [colors.get(label, '#6c757d') for label in labels]
            ax1.pie(sizes, labels=labels, colors=color_list, autopct='%1.1f%%', startangle=90)
            ax1.set_title('Severity Distribution', fontsize=12, weight='bold')

        # 2. Error Patterns (Bar Chart)
        ax2 = fig.add_subplot(gs[0, 1])
        error_patterns = self.report.get('error_patterns', {})
        patterns = {k.replace('_', ' ').title(): v for k, v in error_patterns.items() if v > 0}
        if patterns:
            sorted_patterns = sorted(patterns.items(), key=lambda x: x[1], reverse=True)[:5]
            names = [p[0] for p in sorted_patterns]
            counts = [p[1] for p in sorted_patterns]
            ax2.barh(names, counts, color='#667eea')
            ax2.set_xlabel('Occurrences')
            ax2.set_title('Top 5 Error Patterns', fontsize=12, weight='bold')

        # 3. Timeline (Line Chart)
        ax3 = fig.add_subplot(gs[1, :])
        time_dist = self.report.get('time_distribution', {})
        if time_dist:
            timestamps = []
            error_counts = []
            for bucket, severities in sorted(time_dist.items()):
                try:
                    timestamp = datetime.strptime(bucket, '%Y-%m-%d %H:%M')
                    timestamps.append(timestamp)
                    error_counts.append(severities.get('ERROR', 0) + severities.get('CRITICAL', 0))
                except ValueError:
                    continue

            if timestamps:
                ax3.plot(timestamps, error_counts, color='#dc3545', linewidth=2, marker='o', markersize=4)
                ax3.fill_between(timestamps, error_counts, alpha=0.3, color='#dc3545')
                ax3.set_xlabel('Time')
                ax3.set_ylabel('Error Count')
                ax3.set_title('Error Timeline', fontsize=12, weight='bold')
                ax3.grid(True, alpha=0.3)
                plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45, ha='right')

        # 4. Statistics Summary
        ax4 = fig.add_subplot(gs[2, :])
        ax4.axis('off')

        stats_text = f"""
        ANALYSIS SUMMARY
        ════════════════════════════════════════════════════════════════
        Total Entries:     {self.report['total_entries']:,}
        Critical Events:   {self.report.get('critical_count', 0):,}
        Error Events:      {self.report.get('error_count', 0):,}
        Warning Events:    {self.report.get('warning_count', 0):,}
        Anomalies Detected: {len(self.report.get('anomalies', [])):,}
        ════════════════════════════════════════════════════════════════
        Log File: {os.path.basename(self.report['file'])}
        """

        ax4.text(0.1, 0.5, stats_text, fontsize=11, family='monospace',
                verticalalignment='center', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        # Main title
        fig.suptitle('Log Analysis Dashboard', fontsize=18, weight='bold', y=0.98)

        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"Dashboard saved: {filename}")
        return filename

    def generate_all_visualizations(self):
        """Generate all available visualizations."""
        print("\nGenerating visualizations...")
        self.create_severity_pie_chart()
        self.create_error_pattern_bar_chart()
        self.create_timeline_chart()
        self.create_heatmap()
        self.create_dashboard()
        print("All visualizations generated successfully!")
