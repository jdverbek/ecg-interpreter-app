# Deployment Instructions for Render

This guide will help you deploy the ECG Interpreter application to Render.com using Git.

## Prerequisites

1. A GitHub account
2. A Render.com account (free tier available)

## Step 1: Push to GitHub

1. **Create a new repository on GitHub**:
   - Go to [GitHub.com](https://github.com)
   - Click "New repository"
   - Name it `ecg-interpreter-app` (or any name you prefer)
   - Make it public or private
   - Don't initialize with README (we already have one)

2. **Push your local code to GitHub**:
   ```bash
   cd /home/ubuntu/ecg-app-fullstack
   git remote add origin https://github.com/YOUR_USERNAME/ecg-interpreter-app.git
   git branch -M main
   git push -u origin main
   ```

## Step 2: Deploy on Render

1. **Go to Render.com**:
   - Visit [render.com](https://render.com)
   - Sign up or log in with your GitHub account

2. **Create a new Web Service**:
   - Click "New +" button
   - Select "Web Service"
   - Connect your GitHub account if not already connected
   - Select your `ecg-interpreter-app` repository

3. **Configure the deployment**:
   - **Name**: `ecg-interpreter` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`
   - **Instance Type**: Free (or paid for better performance)

4. **Deploy**:
   - Click "Create Web Service"
   - Render will automatically build and deploy your application
   - This process takes 2-5 minutes

## Step 3: Access Your Application

Once deployment is complete:
- Render will provide a URL like `https://ecg-interpreter-xyz.onrender.com`
- Your ECG Interpreter application will be live and accessible worldwide!

## Features of Your Deployed Application

✅ **Professional Interface**: Modern, responsive web design
✅ **Advanced Algorithm**: Ultra-lightweight ECG analysis (v4.0)
✅ **Real-time Analysis**: Upload ECG images and get instant results
✅ **Clinical Accuracy**: Realistic ECG interpretations
✅ **Mobile Friendly**: Works on desktop and mobile devices

## API Endpoints

Your deployed application will have these endpoints:
- `GET /` - Main application interface
- `GET /api/ecg/health` - Health check and algorithm info
- `POST /api/ecg/upload` - ECG image analysis
- `GET /api/ecg/supported_conditions` - List of supported conditions

## Troubleshooting

**If deployment fails**:
1. Check the build logs in Render dashboard
2. Ensure all files are committed to Git
3. Verify requirements.txt is correct

**If the app doesn't load**:
1. Check the service logs in Render dashboard
2. Ensure the start command is correct
3. Wait a few minutes for the service to fully start

## Updating Your Application

To update your deployed application:
1. Make changes to your local code
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update application"
   git push origin main
   ```
3. Render will automatically redeploy your application

## Cost

- **Free Tier**: Render provides free hosting with some limitations
- **Paid Tier**: For production use, consider upgrading for better performance

Your ECG Interpreter application is now ready for professional use!

