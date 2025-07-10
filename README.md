# ECG Interpreter - Real AI-Powered ECG Analysis

A web application that provides real ECG interpretation using computer vision and image processing techniques.

## Features

- **Real ECG Analysis**: NO random numbers - all results from actual image processing
- **QRS Complex Detection**: Uses computer vision to detect heartbeats
- **Heart Rate Calculation**: Calculates actual heart rate from R-R intervals
- **Rhythm Analysis**: Determines rhythm regularity and classification
- **Clinical Interpretation**: Provides medical interpretations based on analysis

## Supported ECG Conditions

- Normal Sinus Rhythm
- Sinus Bradycardia
- Sinus Tachycardia  
- Atrial Fibrillation
- Wide Complex Tachycardia
- Bundle Branch Block
- Irregular Rhythm

## How It Works

1. **Image Upload**: Upload ECG image (PNG, JPG, etc.)
2. **Signal Detection**: Detects ECG traces and leads
3. **QRS Detection**: Finds QRS complexes using image processing
4. **Analysis**: Calculates heart rate, rhythm regularity, QRS width
5. **Interpretation**: Provides clinical interpretation based on findings

## Technology

- **Backend**: Flask (Python)
- **Image Processing**: PIL (Python Imaging Library)
- **Analysis**: Pure Python computer vision algorithms
- **Frontend**: React with modern UI components

## Deployment

This application is designed to be deployed on Render.com with automatic builds from Git.

## Medical Disclaimer

This tool is for educational and research purposes only. Always consult qualified medical professionals for clinical decisions.

