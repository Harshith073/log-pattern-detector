#!/usr/bin/env python3
"""
Flask Dashboard for Interactive Log Analysis
Provides a web interface for exploring log analysis results.
"""

from flask import Flask, render_template, request, jsonify, send_file
import os
import json
from datetime import datetime
from log_analyzer import LogAnalyzer
from report_generator import ReportGenerator
from visualizer import LogVisualizer

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

# Store analysis results in memory (for demo purposes)
current_analysis = None


@app.route('/')
def index():
    """Main dashboard page."""
    return render_template('index.html')


@app.route('/api/analyze', methods=['POST'])
def analyze_log():
    """API endpoint to analyze a log file."""
    global current_analysis

    data = request.get_json()
    log_file = data.get('log_file')

    if not log_file or not os.path.exists(log_file):
        return jsonify({'error': 'Invalid log file path'}), 400

    try:
        # Perform analysis
        analyzer = LogAnalyzer(log_file)
        report = analyzer.analyze()

        # Generate visualizations
        visualizer = LogVisualizer(report)
        visualizer.generate_all_visualizations()

        # Store current analysis
        current_analysis = report

        return jsonify({
            'status': 'success',
            'report': {
                'total_entries': report['total_entries'],
                'severity_breakdown': report['severity_breakdown'],
                'error_patterns': report['error_patterns'],
                'critical_count': report.get('critical_count', 0),
                'error_count': report.get('error_count', 0),
                'warning_count': report.get('warning_count', 0),
                'anomalies_count': len(report.get('anomalies', []))
            }
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/report/details')
def get_report_details():
    """Get detailed analysis report."""
    global current_analysis

    if not current_analysis:
        return jsonify({'error': 'No analysis available'}), 404

    return jsonify(current_analysis)


@app.route('/api/report/download/<format>')
def download_report(format):
    """Download report in specified format."""
    global current_analysis

    if not current_analysis:
        return jsonify({'error': 'No analysis available'}), 404

    try:
        generator = ReportGenerator(current_analysis)

        if format == 'text':
            filename = generator.generate_text_report()
        elif format == 'html':
            filename = generator.generate_html_report()
        elif format == 'csv':
            filename = generator.generate_csv_export()
        elif format == 'json':
            filename = generator.generate_json_export()
        else:
            return jsonify({'error': 'Invalid format'}), 400

        return send_file(filename, as_attachment=True)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/visualizations/<chart_type>')
def get_visualization(chart_type):
    """Get specific visualization."""
    chart_files = {
        'severity': 'output/severity_distribution.png',
        'patterns': 'output/error_patterns.png',
        'timeline': 'output/timeline.png',
        'heatmap': 'output/heatmap.png',
        'dashboard': 'output/dashboard.png'
    }

    filename = chart_files.get(chart_type)
    if not filename or not os.path.exists(filename):
        return jsonify({'error': 'Visualization not found'}), 404

    return send_file(filename, mimetype='image/png')


@app.route('/api/sample-logs')
def list_sample_logs():
    """List available sample log files."""
    sample_dir = 'sample_logs'
    if not os.path.exists(sample_dir):
        return jsonify({'samples': []})

    samples = []
    for filename in os.listdir(sample_dir):
        if filename.endswith('.log'):
            filepath = os.path.join(sample_dir, filename)
            samples.append({
                'name': filename,
                'path': filepath,
                'size': os.path.getsize(filepath)
            })

    return jsonify({'samples': samples})


if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('output', exist_ok=True)
    os.makedirs('templates', exist_ok=True)

    print("""
    ╔════════════════════════════════════════════════════════════════╗
    ║          Log Pattern Detector - Web Dashboard                  ║
    ╚════════════════════════════════════════════════════════════════╝

    Dashboard running at: http://localhost:5000
    Press CTRL+C to stop the server
    """)

    app.run(debug=True, host='0.0.0.0', port=5000)
