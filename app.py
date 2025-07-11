import os
import sys
import logging
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from datetime import datetime
import tempfile

# Import the clinical ECG analyzer
from clinical_ecg_analyzer import ClinicalECGAnalyzer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='static', static_url_path='')

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'tiff', 'gif'}

# Initialize the clinical ECG analyzer
ecg_analyzer = ClinicalECGAnalyzer()

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Serve the main application page"""
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ECG Interpreter - Clinical Grade Analysis</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                overflow: hidden;
            }
            
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }
            
            .header h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
                font-weight: 300;
            }
            
            .header p {
                font-size: 1.1em;
                opacity: 0.9;
            }
            
            .content {
                padding: 40px;
            }
            
            .upload-area {
                border: 3px dashed #667eea;
                border-radius: 15px;
                padding: 40px;
                text-align: center;
                margin-bottom: 30px;
                transition: all 0.3s ease;
                cursor: pointer;
            }
            
            .upload-area:hover {
                border-color: #764ba2;
                background: #f8f9ff;
            }
            
            .upload-area.dragover {
                border-color: #764ba2;
                background: #f0f2ff;
                transform: scale(1.02);
            }
            
            .upload-icon {
                font-size: 3em;
                color: #667eea;
                margin-bottom: 20px;
            }
            
            .upload-text {
                font-size: 1.2em;
                color: #666;
                margin-bottom: 15px;
            }
            
            .upload-subtext {
                color: #999;
                font-size: 0.9em;
            }
            
            #fileInput {
                display: none;
            }
            
            .btn {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 12px 30px;
                border-radius: 25px;
                font-size: 1em;
                cursor: pointer;
                transition: all 0.3s ease;
                margin: 10px;
            }
            
            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
            }
            
            .btn:disabled {
                opacity: 0.6;
                cursor: not-allowed;
                transform: none;
            }
            
            .results {
                margin-top: 30px;
                padding: 25px;
                background: #f8f9ff;
                border-radius: 15px;
                border-left: 5px solid #667eea;
                display: none;
            }
            
            .results h3 {
                color: #333;
                margin-bottom: 20px;
                font-size: 1.4em;
            }
            
            .result-item {
                margin-bottom: 15px;
                padding: 10px;
                background: white;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
            }
            
            .result-label {
                font-weight: 600;
                color: #667eea;
                margin-bottom: 5px;
            }
            
            .result-value {
                color: #333;
                font-size: 1.1em;
            }
            
            .clinical-interpretation {
                background: #fff3cd;
                border: 1px solid #ffeaa7;
                border-radius: 8px;
                padding: 15px;
                margin: 15px 0;
            }
            
            .clinical-significance {
                padding: 10px 15px;
                border-radius: 8px;
                margin: 10px 0;
                font-weight: 600;
            }
            
            .significance-urgent {
                background: #f8d7da;
                color: #721c24;
                border: 1px solid #f5c6cb;
            }
            
            .significance-significant {
                background: #fff3cd;
                color: #856404;
                border: 1px solid #ffeaa7;
            }
            
            .significance-moderate {
                background: #d1ecf1;
                color: #0c5460;
                border: 1px solid #bee5eb;
            }
            
            .significance-routine {
                background: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
            }
            
            .loading {
                text-align: center;
                padding: 20px;
                display: none;
            }
            
            .spinner {
                border: 3px solid #f3f3f3;
                border-top: 3px solid #667eea;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin: 0 auto 15px;
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            .error {
                background: #f8d7da;
                color: #721c24;
                padding: 15px;
                border-radius: 8px;
                border: 1px solid #f5c6cb;
                margin: 15px 0;
                display: none;
            }
            
            .features {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin: 30px 0;
            }
            
            .feature {
                text-align: center;
                padding: 20px;
                background: white;
                border-radius: 10px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }
            
            .feature-icon {
                font-size: 2em;
                color: #667eea;
                margin-bottom: 10px;
            }
            
            .feature h4 {
                color: #333;
                margin-bottom: 10px;
            }
            
            .feature p {
                color: #666;
                font-size: 0.9em;
            }
            
            @media (max-width: 768px) {
                .container {
                    margin: 10px;
                    border-radius: 15px;
                }
                
                .header {
                    padding: 20px;
                }
                
                .header h1 {
                    font-size: 2em;
                }
                
                .content {
                    padding: 20px;
                }
                
                .upload-area {
                    padding: 30px 20px;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🫀 ECG Interpreter</h1>
                <p>Clinical Grade Analysis • Algorithm v5.0</p>
            </div>
            
            <div class="content">
                <div class="upload-area" onclick="document.getElementById('fileInput').click()">
                    <div class="upload-icon">📋</div>
                    <div class="upload-text">Click to upload ECG image</div>
                    <div class="upload-subtext">or drag and drop your ECG file here</div>
                    <div class="upload-subtext">Supports PNG, JPG, JPEG, BMP, TIFF (max 16MB)</div>
                </div>
                
                <input type="file" id="fileInput" accept=".png,.jpg,.jpeg,.bmp,.tiff,.gif" />
                
                <div class="loading" id="loading">
                    <div class="spinner"></div>
                    <p>Analyzing ECG with clinical-grade algorithm...</p>
                </div>
                
                <div class="error" id="error"></div>
                
                <div class="results" id="results">
                    <h3>📊 ECG Analysis Results</h3>
                    <div id="resultsContent"></div>
                </div>
                
                <div class="features">
                    <div class="feature">
                        <div class="feature-icon">🔬</div>
                        <h4>Clinical Grade</h4>
                        <p>Based on medical literature and systematic interpretation guidelines</p>
                    </div>
                    <div class="feature">
                        <div class="feature-icon">⚡</div>
                        <h4>Real-time Analysis</h4>
                        <p>Instant ECG interpretation with confidence scores</p>
                    </div>
                    <div class="feature">
                        <div class="feature-icon">🎯</div>
                        <h4>25+ Conditions</h4>
                        <p>Detects arrhythmias, conduction blocks, ischemia, and more</p>
                    </div>
                    <div class="feature">
                        <div class="feature-icon">📱</div>
                        <h4>Mobile Ready</h4>
                        <p>Works seamlessly on desktop and mobile devices</p>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            const fileInput = document.getElementById('fileInput');
            const uploadArea = document.querySelector('.upload-area');
            const loading = document.getElementById('loading');
            const error = document.getElementById('error');
            const results = document.getElementById('results');
            const resultsContent = document.getElementById('resultsContent');
            
            // Drag and drop functionality
            uploadArea.addEventListener('dragover', (e) => {
                e.preventDefault();
                uploadArea.classList.add('dragover');
            });
            
            uploadArea.addEventListener('dragleave', () => {
                uploadArea.classList.remove('dragover');
            });
            
            uploadArea.addEventListener('drop', (e) => {
                e.preventDefault();
                uploadArea.classList.remove('dragover');
                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    handleFile(files[0]);
                }
            });
            
            fileInput.addEventListener('change', (e) => {
                if (e.target.files.length > 0) {
                    handleFile(e.target.files[0]);
                }
            });
            
            function handleFile(file) {
                // Validate file type
                const allowedTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/bmp', 'image/tiff'];
                if (!allowedTypes.includes(file.type)) {
                    showError('Please upload a valid image file (PNG, JPG, JPEG, BMP, TIFF)');
                    return;
                }
                
                // Validate file size (16MB)
                if (file.size > 16 * 1024 * 1024) {
                    showError('File size must be less than 16MB');
                    return;
                }
                
                uploadECG(file);
            }
            
            function uploadECG(file) {
                const formData = new FormData();
                formData.append('file', file);
                
                // Show loading
                loading.style.display = 'block';
                results.style.display = 'none';
                error.style.display = 'none';
                
                fetch('/api/ecg/upload', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    loading.style.display = 'none';
                    
                    if (data.success) {
                        displayResults(data);
                    } else {
                        showError(data.error || 'Analysis failed');
                    }
                })
                .catch(err => {
                    loading.style.display = 'none';
                    showError('Network error: ' + err.message);
                });
            }
            
            function displayResults(data) {
                const significance = data.clinical_significance || '';
                let significanceClass = 'significance-routine';
                
                if (significance.includes('URGENT')) {
                    significanceClass = 'significance-urgent';
                } else if (significance.includes('SIGNIFICANT')) {
                    significanceClass = 'significance-significant';
                } else if (significance.includes('MODERATE')) {
                    significanceClass = 'significance-moderate';
                }
                
                resultsContent.innerHTML = `
                    <div class="result-item">
                        <div class="result-label">Heart Rate</div>
                        <div class="result-value">${data.heart_rate} bpm</div>
                    </div>
                    
                    <div class="result-item">
                        <div class="result-label">Rhythm</div>
                        <div class="result-value">${data.rhythm} (${data.rhythm_regularity})</div>
                    </div>
                    
                    <div class="result-item">
                        <div class="result-label">Intervals</div>
                        <div class="result-value">
                            PR: ${data.pr_interval} | QRS: ${data.qrs_duration} | QTc: ${data.qtc_interval}
                        </div>
                    </div>
                    
                    <div class="result-item">
                        <div class="result-label">Electrical Axis</div>
                        <div class="result-value">${data.electrical_axis}</div>
                    </div>
                    
                    <div class="clinical-interpretation">
                        <div class="result-label">Clinical Interpretation</div>
                        <div class="result-value">${data.clinical_interpretation}</div>
                    </div>
                    
                    <div class="clinical-significance ${significanceClass}">
                        ${data.clinical_significance}
                    </div>
                    
                    <div class="result-item">
                        <div class="result-label">Abnormalities Detected</div>
                        <div class="result-value">${data.abnormalities_detected.join(', ')}</div>
                    </div>
                    
                    <div class="result-item">
                        <div class="result-label">Analysis Confidence</div>
                        <div class="result-value">${Math.round(data.confidence_scores.overall * 100)}% overall</div>
                    </div>
                    
                    <div class="result-item">
                        <div class="result-label">Algorithm Version</div>
                        <div class="result-value">${data.algorithm_version}</div>
                    </div>
                `;
                
                results.style.display = 'block';
            }
            
            function showError(message) {
                error.textContent = message;
                error.style.display = 'block';
                results.style.display = 'none';
            }
        </script>
    </body>
    </html>
    '''

@app.route('/api/ecg/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'algorithm_version': '5.0 - Clinical Grade',
        'analyzer_type': 'Clinical ECG Analyzer',
        'supported_formats': list(ALLOWED_EXTENSIONS),
        'max_file_size': '16MB',
        'features': [
            'Systematic clinical interpretation',
            'Medical literature-based analysis',
            'Comprehensive abnormality detection',
            'Clinical significance assessment',
            'Confidence scoring',
            '25+ cardiac conditions'
        ]
    })

@app.route('/api/ecg/upload', methods=['POST'])
def upload_ecg():
    """Upload and analyze ECG image"""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'})
        
        # Validate file type
        if not allowed_file(file.filename):
            return jsonify({
                'success': False, 
                'error': 'Invalid file type. Please upload PNG, JPG, JPEG, BMP, or TIFF files.'
            })
        
        # Save file temporarily
        filename = secure_filename(file.filename)
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, f"ecg_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}")
        
        file.save(temp_path)
        
        try:
            # Analyze ECG using clinical algorithm
            analysis_results = ecg_analyzer.analyze_ecg(temp_path)
            
            # Clean up temporary file
            os.remove(temp_path)
            
            if 'error' in analysis_results:
                return jsonify({
                    'success': False,
                    'error': analysis_results['error']
                })
            
            return jsonify(analysis_results)
            
        except Exception as e:
            # Clean up temporary file on error
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise e
            
    except Exception as e:
        logger.error(f"ECG analysis error: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Analysis failed: {str(e)}'
        })

@app.route('/api/ecg/supported_conditions')
def supported_conditions():
    """Get list of supported ECG conditions"""
    return jsonify({
        'conditions': list(ecg_analyzer.conditions.values()),
        'total_conditions': len(ecg_analyzer.conditions),
        'categories': {
            'rhythm_disorders': [
                'Normal sinus rhythm', 'Sinus bradycardia', 'Sinus tachycardia',
                'Atrial fibrillation', 'Atrial flutter'
            ],
            'conduction_blocks': [
                'First-degree AV block', 'Second-degree AV block', 'Third-degree AV block',
                'Left bundle branch block', 'Right bundle branch block'
            ],
            'hypertrophy': [
                'Left ventricular hypertrophy', 'Right ventricular hypertrophy'
            ],
            'ischemia_infarction': [
                'Anterior myocardial infarction', 'Inferior myocardial infarction',
                'Lateral myocardial infarction', 'ST elevation', 'ST depression'
            ],
            'other_abnormalities': [
                'T-wave inversion', 'Prolonged QT interval', 'Left axis deviation',
                'Right axis deviation', 'Poor R-wave progression', 'Early repolarization pattern'
            ]
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

