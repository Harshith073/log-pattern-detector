#!/usr/bin/env python3
"""
Core Log Analyzer Module
Scans log files and identifies patterns, errors, and anomalies.
"""

import re
from datetime import datetime
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional
import os


class LogEntry:
    """Represents a single log entry."""

    def __init__(self, raw_line: str, line_number: int):
        self.raw_line = raw_line.strip()
        self.line_number = line_number
        self.timestamp = None
        self.severity = "UNKNOWN"
        self.message = ""
        self.source = ""
        self.parse()

    def parse(self):
        """Parse log entry using common log formats."""
        # Pattern 1: ISO timestamp with severity
        # 2024-01-15 10:23:45,123 [ERROR] com.example.Service - Database connection failed
        pattern1 = r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}(?:,\d+)?)\s+\[?(\w+)\]?\s+(.+?)\s+-\s+(.+)'

        # Pattern 2: Syslog format
        # Jan 15 10:23:45 hostname service[1234]: ERROR: message
        pattern2 = r'(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+\S+\s+\S+:\s+(\w+):\s+(.+)'

        # Pattern 3: Apache/Nginx access log
        # 192.168.1.1 - - [15/Jan/2024:10:23:45 +0000] "GET /api HTTP/1.1" 500 1234
        pattern3 = r'\S+\s+\S+\s+\S+\s+\[([^\]]+)\]\s+"(\w+)\s+([^"]+)"\s+(\d+)'

        # Pattern 4: Simple timestamp and level
        # 2024-01-15T10:23:45Z INFO Application started
        pattern4 = r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z?)\s+(\w+)\s+(.+)'

        # Try each pattern
        for pattern in [pattern1, pattern2, pattern3, pattern4]:
            match = re.match(pattern, self.raw_line)
            if match:
                if pattern == pattern1:
                    self.timestamp = self._parse_timestamp(match.group(1))
                    self.severity = match.group(2).upper()
                    self.source = match.group(3)
                    self.message = match.group(4)
                elif pattern == pattern2:
                    self.timestamp = self._parse_timestamp(match.group(1))
                    self.severity = match.group(2).upper()
                    self.message = match.group(3)
                elif pattern == pattern3:
                    self.timestamp = self._parse_timestamp(match.group(1))
                    status_code = int(match.group(4))
                    self.severity = self._status_to_severity(status_code)
                    self.message = f"{match.group(2)} {match.group(3)} - Status: {status_code}"
                elif pattern == pattern4:
                    self.timestamp = self._parse_timestamp(match.group(1))
                    self.severity = match.group(2).upper()
                    self.message = match.group(3)
                break

        # If no pattern matched, check for severity keywords
        if not self.timestamp:
            self._extract_severity_from_text()
            self.message = self.raw_line

    def _parse_timestamp(self, timestamp_str: str) -> Optional[datetime]:
        """Parse various timestamp formats."""
        formats = [
            '%Y-%m-%d %H:%M:%S,%f',
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%dT%H:%M:%SZ',
            '%Y-%m-%dT%H:%M:%S.%fZ',
            '%b %d %H:%M:%S',
            '%d/%b/%Y:%H:%M:%S %z',
        ]

        for fmt in formats:
            try:
                return datetime.strptime(timestamp_str, fmt)
            except ValueError:
                continue
        return None

    def _status_to_severity(self, status_code: int) -> str:
        """Convert HTTP status code to severity level."""
        if status_code < 300:
            return "INFO"
        elif status_code < 400:
            return "WARNING"
        elif status_code < 500:
            return "ERROR"
        else:
            return "CRITICAL"

    def _extract_severity_from_text(self):
        """Extract severity from text if not in standard format."""
        severity_keywords = {
            'CRITICAL': ['critical', 'fatal', 'panic'],
            'ERROR': ['error', 'err', 'failed', 'failure', 'exception'],
            'WARNING': ['warning', 'warn'],
            'INFO': ['info', 'information'],
            'DEBUG': ['debug', 'trace']
        }

        lower_line = self.raw_line.lower()
        for severity, keywords in severity_keywords.items():
            if any(keyword in lower_line for keyword in keywords):
                self.severity = severity
                break


class LogAnalyzer:
    """Main log analysis engine."""

    def __init__(self, log_file: str):
        self.log_file = log_file
        self.entries: List[LogEntry] = []
        self.severity_counts = Counter()
        self.error_patterns = defaultdict(list)
        self.time_buckets = defaultdict(lambda: defaultdict(int))
        self.anomalies = []

    def analyze(self) -> Dict:
        """Perform complete log analysis."""
        print(f"Analyzing log file: {self.log_file}")

        # Read and parse log file
        self._read_log_file()

        # Perform various analyses
        self._count_severities()
        self._detect_error_patterns()
        self._analyze_time_distribution()
        self._detect_anomalies()

        # Generate analysis report
        return self._generate_report()

    def _read_log_file(self):
        """Read and parse log file."""
        if not os.path.exists(self.log_file):
            raise FileNotFoundError(f"Log file not found: {self.log_file}")

        with open(self.log_file, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                if line.strip():  # Skip empty lines
                    entry = LogEntry(line, line_num)
                    self.entries.append(entry)

        print(f"Parsed {len(self.entries)} log entries")

    def _count_severities(self):
        """Count occurrences of each severity level."""
        for entry in self.entries:
            self.severity_counts[entry.severity] += 1

    def _detect_error_patterns(self):
        """Detect recurring error patterns using regex."""
        # Common error patterns to look for
        patterns = {
            'connection_error': r'(?i)(connection\s+(?:refused|failed|timeout|reset))',
            'database_error': r'(?i)(database|sql|query).*?(error|failed|exception)',
            'memory_error': r'(?i)(out\s+of\s+memory|memory\s+(?:leak|error)|heap\s+space)',
            'timeout_error': r'(?i)(timeout|timed\s+out)',
            'authentication_error': r'(?i)(auth(?:entication)?|login|credential).*?(failed|error|denied)',
            'file_error': r'(?i)(file|disk).*?(not\s+found|permission\s+denied|read\s+error)',
            'network_error': r'(?i)(network|socket).*?(error|unreachable|failed)',
            'null_pointer': r'(?i)(null\s+pointer|nullpointerexception|nullptr)',
            'api_error': r'(?i)(api|endpoint|service).*?(error|failed|unavailable)',
        }

        for entry in self.entries:
            if entry.severity in ['ERROR', 'CRITICAL', 'WARNING']:
                for pattern_name, pattern in patterns.items():
                    if re.search(pattern, entry.message):
                        self.error_patterns[pattern_name].append({
                            'line': entry.line_number,
                            'timestamp': entry.timestamp,
                            'message': entry.message[:100],  # Truncate long messages
                            'severity': entry.severity
                        })

    def _analyze_time_distribution(self):
        """Analyze log entries over time to find spikes."""
        for entry in self.entries:
            if entry.timestamp:
                # Bucket by hour
                hour_key = entry.timestamp.strftime('%Y-%m-%d %H:00')
                self.time_buckets[hour_key][entry.severity] += 1

    def _detect_anomalies(self):
        """Detect anomalies like error spikes or unusual patterns."""
        # Calculate average errors per time bucket
        if not self.time_buckets:
            return

        error_counts = []
        for bucket, severities in self.time_buckets.items():
            error_count = severities.get('ERROR', 0) + severities.get('CRITICAL', 0)
            error_counts.append((bucket, error_count))

        if error_counts:
            avg_errors = sum(count for _, count in error_counts) / len(error_counts)
            threshold = avg_errors * 2  # 2x average is considered a spike

            for bucket, count in error_counts:
                if count > threshold and count > 5:  # At least 5 errors
                    self.anomalies.append({
                        'type': 'error_spike',
                        'timestamp': bucket,
                        'count': count,
                        'average': avg_errors,
                        'severity': 'HIGH' if count > avg_errors * 3 else 'MEDIUM'
                    })

        # Detect repeated identical errors
        message_counts = Counter()
        for entry in self.entries:
            if entry.severity in ['ERROR', 'CRITICAL']:
                # Normalize message by removing numbers and timestamps
                normalized = re.sub(r'\d+', 'N', entry.message[:100])
                message_counts[normalized] += 1

        # Flag messages that appear more than 10 times
        for message, count in message_counts.most_common(10):
            if count > 10:
                self.anomalies.append({
                    'type': 'repeated_error',
                    'message': message,
                    'count': count,
                    'severity': 'HIGH' if count > 50 else 'MEDIUM'
                })

    def _generate_report(self) -> Dict:
        """Generate comprehensive analysis report."""
        return {
            'file': self.log_file,
            'total_entries': len(self.entries),
            'severity_breakdown': dict(self.severity_counts),
            'error_patterns': {k: len(v) for k, v in self.error_patterns.items()},
            'error_pattern_details': dict(self.error_patterns),
            'time_distribution': dict(self.time_buckets),
            'anomalies': self.anomalies,
            'critical_count': self.severity_counts.get('CRITICAL', 0),
            'error_count': self.severity_counts.get('ERROR', 0),
            'warning_count': self.severity_counts.get('WARNING', 0),
        }

    def get_top_errors(self, n: int = 10) -> List[Dict]:
        """Get top N most frequent error patterns."""
        top_errors = []
        for pattern_name, occurrences in self.error_patterns.items():
            if occurrences:
                top_errors.append({
                    'pattern': pattern_name,
                    'count': len(occurrences),
                    'sample': occurrences[0]['message'] if occurrences else ''
                })

        return sorted(top_errors, key=lambda x: x['count'], reverse=True)[:n]


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python log_analyzer.py <log_file>")
        sys.exit(1)

    analyzer = LogAnalyzer(sys.argv[1])
    report = analyzer.analyze()

    print("\n=== Analysis Report ===")
    print(f"Total Entries: {report['total_entries']}")
    print(f"\nSeverity Breakdown:")
    for severity, count in sorted(report['severity_breakdown'].items()):
        print(f"  {severity}: {count}")

    print(f"\nError Patterns Detected:")
    for pattern, count in report['error_patterns'].items():
        if count > 0:
            print(f"  {pattern}: {count} occurrences")

    print(f"\nAnomalies Detected: {len(report['anomalies'])}")
    for anomaly in report['anomalies'][:5]:
        print(f"  - {anomaly}")
