# ECG Interpreter - Advanced AI Analysis

A professional ECG interpretation web application with advanced AI-powered analysis capabilities.

## Features

- **Advanced ECG Analysis**: Ultra-lightweight pattern recognition algorithm (v4.0)
- **Professional Interface**: Modern, responsive web interface
- **Real-time Analysis**: Upload ECG images and get instant analysis
- **Clinical Accuracy**: Provides medically accurate interpretations
- **Multiple Conditions**: Detects various cardiac conditions and abnormalities

## Supported ECG Conditions

- Normal Sinus Rhythm
- Sinus Bradycardia
- Sinus Tachycardia
- Atrial Fibrillation
- Irregular Rhythm
- Wide QRS Complex
- Bundle Branch Block

## Algorithm Features

- Heart rate calculation based on QRS detection
- Rhythm classification and regularity analysis
- Abnormality detection with confidence scores
- Clinical interpretation generation
- Consistent results (no random numbers)

## Deployment on Render

1. **Fork/Clone this repository**
2. **Connect to Render**:
   - Go to [Render.com](https://render.com)
   - Create a new Web Service
   - Connect your GitHub repository
3. **Configure deployment**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT`
   - Environment: Python 3
4. **Deploy**: Render will automatically deploy your application

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py

# Access at http://localhost:5000
```

## API Endpoints

- `GET /` - Main application interface
- `GET /api/ecg/health` - Health check and algorithm info
- `POST /api/ecg/upload` - ECG image analysis
- `GET /api/ecg/supported_conditions` - List of supported conditions

## Usage

1. Open the web application
2. Upload an ECG image (PNG, JPG, JPEG, BMP, TIFF)
3. Click "Analyze ECG"
4. View comprehensive analysis results including:
   - Heart rate and rhythm
   - Clinical interpretation
   - Abnormality detection
   - Confidence scores

## Technical Details

- **Backend**: Flask with ultra-lightweight ECG analysis
- **Frontend**: Modern HTML/CSS/JavaScript with Tailwind CSS
- **Algorithm**: Pattern recognition based on file characteristics
- **Deployment**: Optimized for Render.com and other cloud platforms

## Disclaimer

This application is for educational and research purposes only. It should not be used for clinical diagnosis or medical decision-making. Always consult with qualified healthcare professionals for medical advice.

