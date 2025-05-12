#!/usr/bin/env python3
# Web-based Analyzer for Onion De-anonymization Toolkit
# For educational and research purposes only

import os
import json
import glob
import datetime
import logging
import matplotlib
matplotlib.use('Agg')  # Use Agg backend for matplotlib to work without GUI
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("web_analyzer.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("web_analyzer")

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload
app.config['OUTPUT_DIR'] = 'output'
app.config['ALLOWED_EXTENSIONS'] = {'html', 'js', 'json', 'png'}

# Ensure directories exist
for directory in [app.config['UPLOAD_FOLDER'], 'static/img', 'static/temp']:
    if not os.path.exists(directory):
        os.makedirs(directory)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def find_latest_run():
    """Find the latest analysis run directory"""
    run_dirs = glob.glob(os.path.join(app.config['OUTPUT_DIR'], 'run_*'))
    if not run_dirs:
        return None
    return max(run_dirs, key=os.path.getctime)

def get_run_list():
    """Get a list of all analysis runs"""
    run_dirs = glob.glob(os.path.join(app.config['OUTPUT_DIR'], 'run_*'))
    runs = []
    for run_dir in sorted(run_dirs, key=os.path.getctime, reverse=True):
        run_name = os.path.basename(run_dir)
        timestamp = run_name.replace('run_', '')
        # Try to find a report file to extract target information
        report_files = glob.glob(os.path.join(run_dir, 'reports', 'comprehensive_report_*.json'))
        target = "Unknown"
        if report_files:
            try:
                with open(report_files[0], 'r') as f:
                    report_data = json.load(f)
                    target = report_data.get('target', 'Unknown')
            except:
                pass
        
        # Format timestamp for display
        try:
            dt = datetime.datetime.strptime(timestamp, '%Y%m%d_%H%M%S')
            formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S')
        except:
            formatted_time = timestamp
        
        runs.append({
            'id': run_name,
            'timestamp': formatted_time,
            'target': target,
            'path': run_dir
        })
    return runs

def get_run_summary(run_id):
    """Get a summary of analysis results for a specific run"""
    run_dir = os.path.join(app.config['OUTPUT_DIR'], run_id)
    if not os.path.exists(run_dir):
        return None
    
    summary = {
        'id': run_id,
        'reports': [],
        'payloads': [],
        'traffic_analyses': [],
        'browser_exploits': []
    }
    
    # Find reports
    report_files = glob.glob(os.path.join(run_dir, 'reports', '*.json'))
    for report_file in report_files:
        try:
            with open(report_file, 'r') as f:
                report_data = json.load(f)
            summary['reports'].append({
                'filename': os.path.basename(report_file),
                'path': report_file,
                'target': report_data.get('target_onion', report_data.get('target', 'Unknown')),
                'timestamp': report_data.get('timestamp', report_data.get('analysis_time', 'Unknown')),
                'techniques': report_data.get('techniques_applied', [])
            })
        except:
            summary['reports'].append({
                'filename': os.path.basename(report_file),
                'path': report_file,
                'target': 'Error parsing report',
                'timestamp': 'Unknown',
                'techniques': []
            })
    
    # Find payloads
    payload_files = glob.glob(os.path.join(run_dir, 'payloads', '*.*'))
    for payload_file in payload_files:
        file_ext = os.path.splitext(payload_file)[1].lower()
        summary['payloads'].append({
            'filename': os.path.basename(payload_file),
            'path': payload_file,
            'type': file_ext[1:] if file_ext.startswith('.') else file_ext
        })
    
    # Find traffic analyses
    traffic_files = glob.glob(os.path.join(run_dir, 'traffic', '*.json'))
    traffic_plots = glob.glob(os.path.join(run_dir, 'traffic', '*.png'))
    
    for traffic_file in traffic_files:
        if 'correlation_summary' in traffic_file:
            try:
                with open(traffic_file, 'r') as f:
                    traffic_data = json.load(f)
                summary['traffic_analyses'].append({
                    'filename': os.path.basename(traffic_file),
                    'path': traffic_file,
                    'target': traffic_data.get('target_onion', 'Unknown'),
                    'best_match': traffic_data.get('best_match', 'Unknown'),
                    'correlation': traffic_data.get('highest_correlation', 0)
                })
            except:
                summary['traffic_analyses'].append({
                    'filename': os.path.basename(traffic_file),
                    'path': traffic_file,
                    'target': 'Error parsing traffic data',
                    'best_match': 'Unknown',
                    'correlation': 0
                })
    
    for plot_file in traffic_plots:
        summary['traffic_analyses'].append({
            'filename': os.path.basename(plot_file),
            'path': plot_file,
            'type': 'visualization'
        })
    
    # Find browser exploits
    exploit_files = glob.glob(os.path.join(run_dir, 'browser', '*.html'))
    for exploit_file in exploit_files:
        summary['browser_exploits'].append({
            'filename': os.path.basename(exploit_file),
            'path': exploit_file
        })
    
    # Extract identified IPs from reports
    summary['identified_ips'] = []
    for report in summary['reports']:
        if 'comprehensive' in report['filename'].lower():
            try:
                with open(report['path'], 'r') as f:
                    report_data = json.load(f)
                if 'identified_ips' in report_data:
                    for ip_data in report_data['identified_ips']:
                        summary['identified_ips'].append({
                            'ip': ip_data['ip'],
                            'confidence': ip_data['confidence'],
                            'source': ip_data['source']
                        })
                elif 'potential_identifiers' in report_data and 'ip_addresses' in report_data['potential_identifiers']:
                    for ip in report_data['potential_identifiers']['ip_addresses']:
                        summary['identified_ips'].append({
                            'ip': ip,
                            'confidence': report_data.get('overall_confidence', 0.5),
                            'source': 'core_techniques'
                        })
            except:
                pass
    
    return summary

@app.route('/')
def index():
    """Main page with list of runs"""
    runs = get_run_list()
    return render_template('index.html', runs=runs)

@app.route('/run/<run_id>')
def view_run(run_id):
    """View details of a specific run"""
    summary = get_run_summary(run_id)
    if not summary:
        flash('Run not found', 'error')
        return redirect(url_for('index'))
    return render_template('run_details.html', summary=summary)

@app.route('/file/<path:filepath>')
def view_file(filepath):
    """View a file's contents"""
    if not os.path.exists(filepath):
        flash('File not found', 'error')
        return redirect(url_for('index'))
    
    file_ext = os.path.splitext(filepath)[1].lower()
    
    # Handle different file types
    if file_ext == '.json':
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            return render_template('json_viewer.html', 
                                filename=os.path.basename(filepath),
                                filepath=filepath,
                                content=json.dumps(data, indent=2))
        except Exception as e:
            return render_template('text_viewer.html', 
                                filename=os.path.basename(filepath),
                                filepath=filepath,
                                error=str(e))
    
    elif file_ext == '.html':
        try:
            with open(filepath, 'r') as f:
                content = f.read()
            return render_template('html_viewer.html', 
                                filename=os.path.basename(filepath),
                                filepath=filepath,
                                content=content)
        except Exception as e:
            return render_template('text_viewer.html', 
                                filename=os.path.basename(filepath),
                                filepath=filepath,
                                error=str(e))
    
    elif file_ext == '.png':
        # For static files, copy to a location Flask can serve
        static_path = os.path.join('static', 'temp', os.path.basename(filepath))
        if os.path.exists(os.path.join(app.root_path, static_path)):
            os.remove(os.path.join(app.root_path, static_path))
        import shutil
        shutil.copy2(filepath, os.path.join(app.root_path, static_path))
        return render_template('image_viewer.html', 
                              filename=os.path.basename(filepath),
                              filepath=filepath,
                              image_url=url_for('static', filename=f'temp/{os.path.basename(filepath)}'))
    
    else:
        try:
            with open(filepath, 'r') as f:
                content = f.read()
            return render_template('text_viewer.html', 
                                filename=os.path.basename(filepath),
                                filepath=filepath,
                                content=content)
        except Exception as e:
            return render_template('text_viewer.html', 
                                filename=os.path.basename(filepath),
                                filepath=filepath,
                                error=str(e))

@app.route('/test/<path:payload_path>')
def test_payload(payload_path):
    """View to test a generated payload"""
    if not os.path.exists(payload_path):
        flash('Payload file not found', 'error')
        return redirect(url_for('index'))
    
    file_ext = os.path.splitext(payload_path)[1].lower()
    if file_ext not in ['.html', '.js']:
        flash('Only HTML and JS payloads can be tested', 'error')
        return redirect(url_for('index'))
    
    # For testing, we'll serve the file directly with warning banners
    try:
        with open(payload_path, 'r') as f:
            content = f.read()
        
        # Add a warning banner for safety
        if file_ext == '.html':
            warning = """
            <div style="position: fixed; top: 0; left: 0; right: 0; background-color: #f8d7da; color: #721c24; 
                        padding: 10px; text-align: center; z-index: 9999; font-family: Arial, sans-serif; font-weight: bold;">
                ⚠️ TESTING MODE: This is a de-anonymization payload being tested in a controlled environment. ⚠️
            </div>
            <div style="height: 60px;"></div>
            """
            # Insert the warning after the body tag
            if '<body' in content:
                body_pos = content.find('<body')
                body_end = content.find('>', body_pos)
                content = content[:body_end+1] + warning + content[body_end+1:]
            else:
                content = warning + content
        
        # Pass the raw content to the template - the template will handle it with tojson filter
        return render_template('payload_tester.html',
                              filename=os.path.basename(payload_path),
                              content=content,
                              file_type=file_ext[1:])
    except Exception as e:
        flash(f'Error testing payload: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/api/runs')
def api_runs():
    """API endpoint to get list of runs"""
    runs = get_run_list()
    return jsonify(runs)

@app.route('/api/run/<run_id>')
def api_run(run_id):
    """API endpoint to get details of a run"""
    summary = get_run_summary(run_id)
    if not summary:
        return jsonify({'error': 'Run not found'}), 404
    return jsonify(summary)

@app.route('/visualize/<run_id>')
def visualize_run(run_id):
    """Generate visualizations for a run"""
    summary = get_run_summary(run_id)
    if not summary:
        flash('Run not found', 'error')
        return redirect(url_for('index'))
    
    # Create visualization for identified IPs
    if summary['identified_ips']:
        # Create a bar chart showing confidence for each IP
        ips = [ip_data['ip'] for ip_data in summary['identified_ips']]
        confidences = [ip_data['confidence'] for ip_data in summary['identified_ips']]
        sources = [ip_data['source'] for ip_data in summary['identified_ips']]
        
        # Color bars based on confidence level
        colors = []
        for confidence in confidences:
            if confidence >= 0.8:
                colors.append('green')
            elif confidence >= 0.6:
                colors.append('orange')
            else:
                colors.append('red')
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(ips, confidences, color=colors)
        
        # Add a horizontal line for 0.7 confidence threshold
        plt.axhline(y=0.7, color='r', linestyle='-', label='Confidence Threshold')
        
        # Add labels
        plt.xlabel('IP Address')
        plt.ylabel('Confidence Score')
        plt.title('Identified IP Addresses with Confidence Scores')
        plt.ylim(0, 1)
        
        # Add labels above bars
        for i, bar in enumerate(bars):
            plt.text(bar.get_x() + bar.get_width()/2., 
                    bar.get_height() + 0.02,
                    sources[i],
                    ha='center', va='bottom', rotation=45, fontsize=8)
        
        # Save the figure
        vis_file = os.path.join('static', 'img', f'visualization_{run_id}_ips.png')
        plt.tight_layout()
        plt.savefig(os.path.join(app.root_path, vis_file))
        plt.close()
        
        summary['ip_visualization'] = url_for('static', filename=f'img/visualization_{run_id}_ips.png')
    
    return render_template('visualizations.html', summary=summary)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    """Upload a file for analysis"""
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            flash(f'File {filename} uploaded successfully', 'success')
            return redirect(url_for('view_file', filepath=filepath))
    
    return render_template('upload.html')

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
        
    app.run(debug=True, host='0.0.0.0', port=5000) 