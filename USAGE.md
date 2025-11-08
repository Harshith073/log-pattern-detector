# Usage Guide - Log Pattern Detector

This guide provides detailed usage examples and best practices for the Log Pattern Detector.

## Table of Contents
1. [Quick Start](#quick-start)
2. [Command Line Examples](#command-line-examples)
3. [Web Dashboard Guide](#web-dashboard-guide)
4. [Python API Examples](#python-api-examples)
5. [Interpreting Results](#interpreting-results)
6. [Best Practices](#best-practices)

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Test with Sample Logs
```bash
python main.py sample_logs/application.log
```

### 3. View Results
Check the `output/` directory for generated reports and visualizations.

## Command Line Examples

### Example 1: Basic Analysis
Analyze a log file and view results in terminal:
```bash
python main.py /var/log/application.log
```

**Output:**
- Terminal display with summary statistics
- Error patterns identified
- Anomalies detected

### Example 2: Generate Complete Report Suite
Create all report types and visualizations:
```bash
python main.py /var/log/application.log --all
```

**Generates:**
- `output/report_*.txt` - Detailed text report
- `output/report_*.html` - Interactive HTML report
- `output/errors_*.csv` - Error data for Excel/Sheets
- `output/report_*.json` - Machine-readable JSON
- `output/*.png` - Visualization charts

### Example 3: Automated Daily Reports
Create a cron job for daily log analysis:

```bash
# Add to crontab (crontab -e)
0 2 * * * /usr/bin/python3 /path/to/main.py /var/log/app.log --all --quiet
```

This runs at 2 AM daily, generating reports quietly.

### Example 4: Custom Report Location
Specify where to save reports:
```bash
python main.py server.log -o /reports/daily/server_report.txt --html /reports/daily/server.html
```

### Example 5: Multiple Log Analysis
Analyze multiple log files:
```bash
for log in /var/log/*.log; do
    python main.py "$log" --all
done
```

## Web Dashboard Guide

### Starting the Dashboard
```bash
python dashboard.py
```

The dashboard will start on `http://localhost:5000`

### Dashboard Features

#### 1. Analyze Custom Logs
- Enter the full path to your log file
- Click "Analyze"
- Wait for processing to complete
- View interactive results

#### 2. Use Sample Logs
- Click on any sample log in the list
- Path auto-fills in the input field
- Click "Analyze" to process

#### 3. View Visualizations
The dashboard displays:
- **Stats Cards**: Quick overview of log statistics
- **Severity Chart**: Pie chart of log levels
- **Error Patterns**: Bar chart of common errors
- **Timeline**: Error frequency over time
- **Heatmap**: Error density by day/hour

#### 4. Download Reports
After analysis, download reports in any format:
- Text Report - For email/documentation
- HTML Report - For sharing with team
- CSV Export - For spreadsheet analysis
- JSON Export - For programmatic use

## Python API Examples

### Example 1: Basic Analysis Script
```python
#!/usr/bin/env python3
from log_analyzer import LogAnalyzer

# Analyze log file
analyzer = LogAnalyzer('/var/log/application.log')
report = analyzer.analyze()

# Print summary
print(f"Total Entries: {report['total_entries']}")
print(f"Errors: {report['error_count']}")
print(f"Warnings: {report['warning_count']}")

# Get top errors
top_errors = analyzer.get_top_errors(5)
for error in top_errors:
    print(f"{error['pattern']}: {error['count']}")
```

### Example 2: Automated Alert System
```python
#!/usr/bin/env python3
from log_analyzer import LogAnalyzer
import smtplib
from email.mime.text import MIMEText

# Analyze log
analyzer = LogAnalyzer('/var/log/critical.log')
report = analyzer.analyze()

# Check for critical issues
if report['critical_count'] > 0 or report['error_count'] > 100:
    # Send alert email
    msg = MIMEText(f"Critical issues detected!\n"
                   f"Critical: {report['critical_count']}\n"
                   f"Errors: {report['error_count']}")
    msg['Subject'] = 'ALERT: Critical Log Issues'
    msg['From'] = 'monitor@example.com'
    msg['To'] = 'admin@example.com'

    # Send email (configure SMTP settings)
    # smtp.sendmail(...)
    print("Alert sent!")
```

### Example 3: Custom Report Processing
```python
#!/usr/bin/env python3
from log_analyzer import LogAnalyzer
from report_generator import ReportGenerator
from visualizer import LogVisualizer
import datetime

# Analyze
analyzer = LogAnalyzer('/var/log/app.log')
report = analyzer.analyze()

# Generate dated reports
date_str = datetime.datetime.now().strftime('%Y-%m-%d')
generator = ReportGenerator(report)

# Create reports with custom names
generator.generate_text_report(f'reports/{date_str}_analysis.txt')
generator.generate_html_report(f'reports/{date_str}_dashboard.html')

# Create visualizations
visualizer = LogVisualizer(report)
visualizer.create_dashboard(f'reports/{date_str}_charts.png')

print(f"Reports generated for {date_str}")
```

### Example 4: Multi-Server Analysis
```python
#!/usr/bin/env python3
from log_analyzer import LogAnalyzer
import glob

servers = ['web1', 'web2', 'api1', 'api2']
summary = {}

for server in servers:
    log_file = f'/var/log/{server}/application.log'
    analyzer = LogAnalyzer(log_file)
    report = analyzer.analyze()

    summary[server] = {
        'errors': report['error_count'],
        'warnings': report['warning_count'],
        'anomalies': len(report['anomalies'])
    }

# Print comparison
print("Server Health Summary:")
print("-" * 60)
for server, stats in summary.items():
    print(f"{server:10} | Errors: {stats['errors']:4} | "
          f"Warnings: {stats['warnings']:4} | "
          f"Anomalies: {stats['anomalies']:2}")
```

## Interpreting Results

### Severity Levels

**CRITICAL**
- System failures
- Service crashes
- Data loss events
- Security breaches
→ **Action**: Immediate investigation required

**ERROR**
- Failed operations
- Exceptions
- Connection failures
- Database errors
→ **Action**: Investigate and fix within hours

**WARNING**
- Degraded performance
- Resource constraints
- Deprecated features
- Rate limits
→ **Action**: Monitor and plan fixes

**INFO**
- Normal operations
- Successful requests
- Status updates
→ **Action**: No action needed

### Understanding Anomalies

**Error Spikes**
- Sudden increase in errors
- Indicates: Service outage, deployment issue, or attack
- Example: "Error Spike at 2024-01-15 08:00: 50 errors (avg: 5)"

**Repeated Errors**
- Same error occurring many times
- Indicates: Systematic bug or configuration issue
- Example: "NullPointerException: 45 occurrences"

### Error Patterns

**Connection Errors**
- Network issues
- Service unavailability
- Firewall blocks

**Database Errors**
- Query failures
- Connection pool exhaustion
- Deadlocks

**Memory Errors**
- Out of memory
- Memory leaks
- GC pressure

**Authentication Errors**
- Failed logins
- Invalid credentials
- Possible brute force attacks

## Best Practices

### 1. Regular Monitoring
```bash
# Run analysis daily
python main.py /var/log/app.log --all

# Archive reports
mv output/* /archives/$(date +%Y-%m-%d)/
```

### 2. Focus on Trends
- Don't just look at totals
- Compare day-over-day changes
- Watch for increasing error rates
- Monitor anomaly frequency

### 3. Set Baselines
- Establish normal error levels
- Track typical patterns
- Alert on deviations

### 4. Combine with Logs
- Reports show WHAT and WHEN
- Check actual logs for WHY
- Use line numbers from reports

### 5. Automate Actions
```python
# Example: Auto-restart on critical errors
if report['critical_count'] > 5:
    os.system('systemctl restart myapp')
    send_alert("App restarted due to critical errors")
```

### 6. Regular Cleanup
```bash
# Clean old visualizations
find output/ -name "*.png" -mtime +7 -delete

# Archive old reports
find output/ -name "*.txt" -mtime +30 -exec gzip {} \;
```

### 7. Custom Patterns
Extend the analyzer for your specific needs:

```python
# In log_analyzer.py, add to patterns dict:
patterns = {
    'connection_error': r'...',
    'my_custom_error': r'(?i)my_app.*failed',  # Add custom pattern
}
```

## Troubleshooting

### Issue: No patterns detected
**Solution**: Check if log format is supported. Add custom patterns if needed.

### Issue: Timestamps not parsed
**Solution**: Check timestamp format. Add format to `_parse_timestamp()` method.

### Issue: Too many false positives
**Solution**: Adjust anomaly detection thresholds in `_detect_anomalies()`.

### Issue: Large files slow to process
**Solution**:
- Process only recent logs
- Increase system memory
- Use `--quiet` mode to reduce output overhead

### Issue: Visualizations not showing
**Solution**:
- Check matplotlib installation
- Ensure `output/` directory exists
- Verify file permissions

## Advanced Usage

### Environment Variables
```bash
export LOG_ANALYZER_OUTPUT_DIR="/custom/output"
export LOG_ANALYZER_QUIET=1
```

### Integration with Logging Systems

**Rsyslog**
```bash
# Send logs to analyzer
*.* action(type="omprog" binary="/path/to/analyzer_wrapper.sh")
```

**Docker**
```bash
docker logs mycontainer > /tmp/container.log
python main.py /tmp/container.log --all
```

**Kubernetes**
```bash
kubectl logs deployment/myapp > app.log
python main.py app.log --visualize
```

## Performance Tips

1. **Large Files**: Process in chunks or use `tail -n 10000 logfile.log`
2. **Multiple Files**: Use parallel processing (GNU parallel)
3. **Real-time**: Use log rotation and analyze daily files
4. **Network Logs**: Copy to local disk first for faster processing

## Getting Help

- Check README.md for overview
- Review this guide for detailed usage
- Check error messages for specific issues
- Open GitHub issues for bugs

---

Happy log analyzing! 📊
