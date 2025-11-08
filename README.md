# 📊 Log Pattern Detector

A comprehensive system log analysis tool that scans through server or application log files to identify unusual activity, repeated errors, and performance issues. Using advanced regular expressions and pattern matching, it automatically detects recurring patterns, anomalies, and generates detailed reports with visualizations.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

### Core Functionality
- 🔍 **Multi-format Log Support** - Automatically detects and parses various log formats:
  - ISO timestamp logs (`2024-01-15 10:23:45,123 [ERROR] ...`)
  - Syslog format
  - Apache/Nginx access logs
  - Custom application logs

- 🎯 **Smart Pattern Detection** - Identifies common error patterns:
  - Connection errors
  - Database failures
  - Memory issues
  - Authentication failures
  - File system errors
  - Network problems
  - API errors
  - Null pointer exceptions

- 📊 **Severity Categorization**
  - CRITICAL
  - ERROR
  - WARNING
  - INFO
  - DEBUG

- 🚨 **Anomaly Detection**
  - Time-based error spikes
  - Repeated error patterns
  - Unusual activity detection
  - Performance degradation alerts

### Reporting & Visualization

- 📄 **Multiple Report Formats**
  - Text reports with detailed statistics
  - Interactive HTML dashboards
  - CSV exports for spreadsheet analysis
  - JSON exports for programmatic access

- 📈 **Rich Visualizations**
  - Severity distribution pie charts
  - Error pattern bar charts
  - Timeline graphs showing error trends
  - Heatmaps for temporal analysis
  - Comprehensive dashboards

- 🌐 **Web Dashboard**
  - Interactive Flask-based web interface
  - Real-time analysis
  - Visual exploration of logs
  - Report downloads in multiple formats

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Install Dependencies

```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install flask matplotlib pandas numpy python-dateutil plotly
```

## 📖 Usage

### Command Line Interface

#### Basic Analysis
Analyze a log file and display results in terminal:
```bash
python main.py sample_logs/application.log
```

#### Generate Text Report
```bash
python main.py sample_logs/application.log -o report.txt
```

#### Generate HTML Report
```bash
python main.py sample_logs/application.log --html report.html
```

#### Generate All Reports and Visualizations
```bash
python main.py sample_logs/application.log --all
```

#### Export to CSV
```bash
python main.py sample_logs/application.log --csv errors.csv
```

#### Export to JSON
```bash
python main.py sample_logs/application.log --json report.json
```

#### Create Visualizations Only
```bash
python main.py sample_logs/application.log --visualize
```

#### Quiet Mode (minimal output)
```bash
python main.py sample_logs/application.log --all --quiet
```

### Web Dashboard

Start the interactive web dashboard:
```bash
python dashboard.py
```

Then open your browser to `http://localhost:5000`

Features:
- Upload and analyze log files
- Interactive visualizations
- Download reports in any format
- Explore sample logs

### Python API

Use the analyzer programmatically:

```python
from log_analyzer import LogAnalyzer
from report_generator import ReportGenerator
from visualizer import LogVisualizer

# Analyze log file
analyzer = LogAnalyzer('path/to/logfile.log')
report = analyzer.analyze()

# Generate reports
generator = ReportGenerator(report)
generator.generate_text_report('report.txt')
generator.generate_html_report('report.html')
generator.generate_csv_export('errors.csv')

# Create visualizations
visualizer = LogVisualizer(report)
visualizer.generate_all_visualizations()

# Get top errors
top_errors = analyzer.get_top_errors(10)
for error in top_errors:
    print(f"{error['pattern']}: {error['count']} occurrences")
```

## 📁 Project Structure

```
log-pattern-detector/
├── main.py                 # Main CLI entry point
├── log_analyzer.py         # Core log analysis engine
├── report_generator.py     # Report generation module
├── visualizer.py          # Visualization creation
├── dashboard.py           # Flask web dashboard
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── sample_logs/          # Sample log files
│   ├── application.log   # Application server logs
│   └── webserver.log     # Web server access logs
├── templates/            # HTML templates for Flask
│   └── index.html       # Dashboard template
└── output/              # Generated reports and visualizations
    ├── *.txt            # Text reports
    ├── *.html           # HTML reports
    ├── *.csv            # CSV exports
    ├── *.json           # JSON exports
    └── *.png            # Visualization charts
```

## 🎨 Visualization Examples

The tool generates various visualizations:

1. **Severity Distribution** - Pie chart showing breakdown by log level
2. **Error Patterns** - Bar chart of most common error types
3. **Timeline** - Time series showing error frequency over time
4. **Heatmap** - Error density by day and hour
5. **Dashboard** - Combined view with key metrics

## 🔧 Configuration

### Supported Log Formats

The analyzer automatically detects these formats:

**ISO Timestamp Format:**
```
2024-01-15 10:23:45,123 [ERROR] com.example.Service - Message
```

**Syslog Format:**
```
Jan 15 10:23:45 hostname service[1234]: ERROR: Message
```

**Apache/Nginx Access Logs:**
```
192.168.1.1 - - [15/Jan/2024:10:23:45 +0000] "GET /api HTTP/1.1" 500 1234
```

**ISO 8601 Format:**
```
2024-01-15T10:23:45Z INFO Application started
```

### Error Pattern Detection

The following patterns are automatically detected:

- **Connection Errors** - Connection refused, failed, timeout, reset
- **Database Errors** - Database, SQL, query failures
- **Memory Errors** - Out of memory, memory leaks, heap space
- **Timeout Errors** - Timeouts and timed out operations
- **Authentication Errors** - Auth failures, login denied
- **File Errors** - File not found, permission denied
- **Network Errors** - Network unreachable, socket failures
- **Null Pointer** - NullPointerException, nullptr
- **API Errors** - API/endpoint/service unavailable

## 📊 Sample Output

### Console Output
```
================================================================================
LOG PATTERN DETECTOR
================================================================================

Analyzing log file: sample_logs/application.log
Parsed 72 log entries

================================================================================
ANALYSIS SUMMARY
================================================================================
Total Entries: 72
Critical:      4
Errors:        31
Warnings:      16
Anomalies:     3

✓ Text report: output/report_20240115_120000.txt
✓ HTML report: output/report_20240115_120000.html
✓ CSV export:  output/errors_20240115_120000.csv
✓ JSON export: output/report_20240115_120000.json

Generating visualizations...
✓ All visualizations generated in 'output/' directory

================================================================================
TOP ERROR PATTERNS
================================================================================
1. Database Error: 8 occurrences
2. Network Error: 6 occurrences
3. Memory Error: 2 occurrences
4. Authentication Error: 4 occurrences
5. File Error: 2 occurrences

================================================================================
ANOMALIES DETECTED
================================================================================
⚠ Error Spike at 2024-01-15 08:00: 15 errors
⚠ Repeated Error: 12 occurrences
⚠ Error Spike at 2024-01-15 09:00: 18 errors
```

## 🎯 Use Cases

### For Developers
- Debug production issues by identifying error patterns
- Track application health over time
- Find performance bottlenecks
- Detect memory leaks and resource issues

### For System Administrators
- Monitor server health
- Identify security threats (failed logins, suspicious activity)
- Track system resource usage
- Automate log analysis workflows

### For Cybersecurity Learners
- Learn log analysis techniques
- Practice pattern recognition
- Understand attack signatures
- Develop security monitoring skills

### For DevOps Teams
- Automate incident detection
- Generate reports for stakeholders
- Track SLA compliance
- Monitor distributed systems

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with Python, Flask, and Matplotlib
- Inspired by real-world log analysis challenges
- Designed for developers, sysadmins, and security professionals

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact the maintainers

## 🚀 Future Enhancements

- [ ] Machine learning-based anomaly detection
- [ ] Real-time log streaming support
- [ ] Integration with popular logging systems (ELK, Splunk)
- [ ] Customizable alert rules
- [ ] Multi-file analysis and correlation
- [ ] Email notifications for critical events
- [ ] Database storage for historical analysis
- [ ] REST API for integration
- [ ] Docker containerization
- [ ] Cloud deployment support

## 📚 Additional Resources

- [Log Analysis Best Practices](https://example.com)
- [Regular Expression Guide](https://example.com)
- [Python Logging Documentation](https://docs.python.org/3/library/logging.html)

---

Made with ❤️ for the developer and security community
