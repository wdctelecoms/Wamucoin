# FinShield AI - Financial Fraud Detection System

A professional AI-powered web application that detects and analyzes financial scams and fraud in real-time using advanced pattern recognition.

## Features

✅ **Real-Time Fraud Detection** - Instantly identify suspicious transactions and investment schemes
✅ **User Authentication** - Secure login and registration system
✅ **Text Analysis** - AI-powered analysis of suspicious messages and emails
✅ **Community Reporting** - Report and share fraud threats with the community
✅ **Active Alerts Feed** - Stay informed with live scam threat updates
✅ **Professional UI** - Modern, responsive design with professional styling

## Tech Stack

- **Backend:** Flask 3.0.0
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript
- **Authentication:** Session-based with password hashing

## Installation

### Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/wdctelecoms/Wamucoin.git
   cd Wamucoin/finshield-ai
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   cd app
   python app.py
   ```

5. **Access the application:**
   Open your browser and go to `http://127.0.0.1:5000`

## Deployment on Vercel

### Quick Deploy

1. **Push to GitHub:**
   ```bash
   git push origin main
   ```

2. **Connect to Vercel:**
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository
   - Select the root directory: `finshield-ai`
   - Click "Deploy"

### Environment Variables (if needed)

If you add environment-specific variables, set them in Vercel project settings:

- `FLASK_ENV=production`
- `FLASK_APP=app/app.py`

## Project Structure

```
finshield-ai/
├── app/
│   ├── app.py                 # Main Flask application
│   ├── database.db            # SQLite database
│   ├── static/
│   │   └── style.css          # Professional styling
│   └── templates/
│       ├── base.html          # Base template with navbar
│       ├── intro.html         # Introduction page
│       ├── login.html         # Login page
│       ├── register.html      # Registration page
│       ├── dashboard.html     # User dashboard
│       ├── check.html         # Fraud check page
│       ├── report.html        # Report scam page
│       └── alerts.html        # Alerts feed page
├── requirements.txt           # Python dependencies
├── vercel.json               # Vercel deployment config
├── README.md                 # This file
└── .gitignore               # Git ignore file
```

## Usage

### For Users

1. **Create Account** - Register with username and password
2. **Login** - Access your secure account
3. **Check Text** - Paste suspicious content for AI analysis
4. **View Alerts** - See community-reported fraud threats
5. **Report Scam** - Contribute to community knowledge base

### For Developers

The application uses:
- **Session-based Authentication** - Secure user sessions
- **Password Hashing** - SHA-256 encryption for passwords
- **AI Detection** - Pattern-based fraud detection engine
- **Database** - SQLite for data persistence

## API Routes

- `GET /` - Redirect to intro page
- `GET /intro` - Introduction page
- `GET/POST /register` - User registration
- `GET/POST /login` - User login
- `GET /dashboard` - User dashboard (protected)
- `GET/POST /check` - Fraud detection (protected)
- `GET/POST /report` - Report fraud (protected)
- `GET /alerts` - View alerts feed (protected)
- `GET /logout` - Logout

## Security Features

✓ Password hashing with SHA-256
✓ Session-based authentication
✓ Protected routes requiring login
✓ CSRF protection via Flask sessions
✓ Secure cookie handling

## Future Enhancements

- Machine learning model integration
- Advanced pattern recognition
- Email notifications
- User profiles and preferences
- Blockchain-based fraud verification
- Multi-language support
- Mobile app

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is part of the WamuCoin initiative. Please refer to the main repository for license information.

## Support

For issues, questions, or suggestions, please open an issue on the GitHub repository.

---

**FinShield AI** - Protecting Financial Security in the Digital Age
