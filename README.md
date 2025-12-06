# SoilSageAI - Soil Analysis and Crop Recommendation System

A full-stack application that analyzes soil types and recommends suitable crops based on soil parameters using machine learning.

## Features

- 🖼️ Soil image analysis using InceptionV3 deep learning model
- 🌾 Crop recommendation based on soil type and environmental parameters
- 📊 Parameter analysis and assessment
- 🌐 REST API backend with Django
- ⚛️ Modern React frontend with Tailwind CSS
- 🗄️ SQLite database for storing analysis history

## Tech Stack

### Backend
- Django 6.0
- Django REST Framework
- TensorFlow/Keras
- NumPy & Pandas
- Pillow (Image processing)

### Frontend
- React 19
- Axios (HTTP client)
- Tailwind CSS
- React Scripts

## Local Development

### Prerequisites
- Python 3.12+
- Node.js 16+
- Git

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Start the development server:
```bash
python manage.py runserver
```

Backend will run on `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

Frontend will run on `http://localhost:5000`

## Deployment on Vercel

### Prerequisites
- Vercel account (https://vercel.com)
- GitHub repository with this project

### Deployment Steps

1. **Push to GitHub:**
```bash
cd path/to/SoilSageAI
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/SoilSageAI.git
git push -u origin main
```

2. **Deploy on Vercel:**
   - Go to https://vercel.com/new
   - Select "Import Git Repository"
   - Choose your SoilSageAI repository
   - Configure settings:
     - Framework: None (for Python/Django)
     - Root Directory: `.`
   - Add environment variables if needed
   - Click "Deploy"

3. **Backend API Deployment:**
   - The Django backend will be deployed as serverless functions
   - API endpoints will be available at your Vercel domain

4. **Frontend Deployment:**
   - React frontend will be automatically built and deployed
   - Update API URL in `frontend/src/components/SoilForm.js` to your Vercel domain

## API Endpoints

### POST `/api/predict/`
Predict soil type and recommend crops

**Request:**
```json
{
  "image": <file>,
  "nitrogen": 50,
  "phosphorus": 30,
  "potassium": 40,
  "ph": 6.5,
  "rainfall": 100,
  "humidity": 70,
  "temperature": 25
}
```

**Response:**
```json
{
  "soil_type": "Black",
  "recommended_crop": "Cotton",
  "parameter_analysis": {
    "Nitrogen": "Optimal - Good for most crops",
    "Phosphorus": "Optimal - Good for root development",
    ...
  }
}
```

## Project Structure

```
SoilSageAI/
├── backend/
│   ├── api/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── soil_analyzer.py
│   │   ├── urls.py
│   │   ├── data/
│   │   │   └── Crop_recommendation.csv
│   │   └── models/
│   │       ├── inceptionV3_traineddata.h5
│   │       └── soiltrained_data.h5
│   └── soil_analysis/
│       ├── settings.py
│       ├── urls.py
│       └── wsgi.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
├── vercel.json
├── pyproject.toml
└── requirements.txt
```

## Configuration

### Django Settings
- `DEBUG = True` (Change to `False` for production)
- `ALLOWED_HOSTS = ['*']` (Configure for production)
- CORS is enabled for all origins

### Environment Variables
- `DJANGO_SETTINGS_MODULE`: soil_analysis.settings
- `PYTHONUNBUFFERED`: 1 (For proper logging)

## Troubleshooting

### Issue: Model not loading
- Ensure `.h5` model files exist in `backend/api/models/`
- Check file permissions

### Issue: CSV file not found
- Verify `Crop_recommendation.csv` exists in `backend/api/data/`
- Check the relative path in `soil_analyzer.py`

### Issue: CORS errors
- CORS is already configured in Django settings
- Ensure frontend is sending requests to correct API URL

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Push to your fork
5. Submit a pull request

## License

MIT License - feel free to use this project for educational purposes

## Support

For issues or questions, please create an issue in the GitHub repository.
