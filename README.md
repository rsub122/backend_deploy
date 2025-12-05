# Python Counselor Service

This service runs the EDSL Python script for the guidance counselor chat.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set your API key (if not already set):
```bash
export EXPECTED_PARROT_API_KEY=''
```

3. Run the service:
```bash
python counselor_service.py
```

The service will run on `http://localhost:5000`

## Deployment Options

### Option 1: Deploy to Railway
1. Create account at railway.app
2. Create new project from GitHub repo
3. Add environment variable: `EXPECTED_PARROT_API_KEY`
4. Railway will auto-detect Flask and deploy

### Option 2: Deploy to Render
1. Create account at render.com
2. Create new Web Service
3. Connect your repo
4. Set build command: `pip install -r python-service/requirements.txt`
5. Set start command: `python python-service/counselor_service.py`
6. Add environment variable: `EXPECTED_PARROT_API_KEY`

### Option 3: Deploy to Heroku
```bash
heroku create your-counselor-service
heroku config:set EXPECTED_PARROT_API_KEY='your_key_here'
git push heroku main
```

## Update Edge Function

After deploying, update the `PYTHON_SERVICE_URL` in your edge function to point to your deployed service URL.
