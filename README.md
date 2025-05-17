# Rehab Metrics

A comprehensive rehabilitation tracking application that helps patients monitor their recovery progress after surgery. The application integrates with Google Sheets to store patient data and provide clinical guidelines based on recovery timeline.

## Features

- User registration and authentication
- Surgery date validation (within 2 years)
- Progress tracking for:
  - Pain levels
  - Range of motion
  - Complications
  - Weight bearing status
- Clinical guidelines based on recovery timeline
- Data persistence using Google Sheets
- Comprehensive error handling and input validation

## Setup

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up Google Sheets API:
   - Create a project in Google Cloud Console
   - Enable Google Sheets API
   - Create service account credentials
   - Download credentials as `creds.json`
   - Share your Google Sheet with the service account email

## Usage

Run the application:
```
python run.py
```

Follow the prompts to:
1. Register or log in
2. Enter your surgery date
3. Track your rehabilitation progress
4. View clinical guidelines

## Important Notes

- This tool is for educational and self-tracking purposes only
- It does not provide medical advice, diagnosis, or treatment
- Consult healthcare professionals for medical concerns
- Data is stored in Google Sheets for easy access and sharing

## Technical Details

- Python 3.8+
- Google Sheets API integration via `gspread`
- Command-line interface
- Data validation and sanitization
- Error handling for API operations

## Deployment

The application can be deployed to Heroku:

1. Create a new Heroku app
2. Add buildpacks:
   - `heroku/python`
   - `heroku/nodejs`
3. Set config vars:
   - `PORT`: 8000
   - `CREDS`: Contents of your `creds.json`
4. Deploy from GitHub repository

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
