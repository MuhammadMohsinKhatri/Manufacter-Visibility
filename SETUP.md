# Manufacturing Visibility - Setup Guide

This guide will help you set up and run both the frontend and backend applications.

## Prerequisites

- **Node.js** (v14 or higher) and npm
- **Python** (3.8 or higher)
- **MySQL** server (or use SQLite for development)

## Backend Setup

### Option 1: Using MySQL (Recommended for Production)

1. **Install and start MySQL server**
   - Install MySQL from https://dev.mysql.com/downloads/
   - Start the MySQL service
   - Create a database:
     ```sql
     CREATE DATABASE manufacter_visibility;
     ```

2. **Configure database connection**
   - Create a `.env` file in the `backend` directory:
     ```env
     DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/manufacter_visibility
     HOST=0.0.0.0
     PORT=8000
     ```
   - Replace `your_password` with your MySQL root password

3. **Set up Python virtual environment**
   ```bash
   cd backend
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/Mac:
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the backend**
   ```bash
   python run.py
   ```
   
   The backend will start on `http://localhost:8000`
   - API documentation: `http://localhost:8000/docs`
   - Health check: `http://localhost:8000/health`

### Option 2: Using SQLite (Easier for Development)

1. **Update database configuration**
   - Create a `.env` file in the `backend` directory:
     ```env
     DATABASE_URL=sqlite:///./manufacter_visibility.db
     HOST=0.0.0.0
     PORT=8000
     ```

2. **Note**: If using SQLite, you may need to adjust the database URL format in `app/database/database.py`

3. **Follow steps 3-5 from Option 1**

### Database Connection Issues

If you see connection errors:
- **MySQL not running**: Start the MySQL service
- **Wrong credentials**: Check your `.env` file
- **Database doesn't exist**: Create it with `CREATE DATABASE manufacter_visibility;`

**Note**: The backend will now start even if the database is not available, but API endpoints will fail until the database is connected.

## Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Run the frontend**
   ```bash
   npm start
   ```
   
   The frontend will start on `http://localhost:3000`

### Proxy Errors (Non-Critical)

If you see proxy errors for `/favicon.ico` or `/manifest.json`:
- These are harmless warnings
- The files are now created in the `public` folder
- These errors will disappear once the backend is running, or you can ignore them

## Running Both Applications

### Terminal 1 - Backend
```bash
cd backend
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Linux/Mac
python run.py
```

### Terminal 2 - Frontend
```bash
cd frontend
npm start
```

## Accessing the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Troubleshooting

### Backend Issues

1. **Database connection refused**
   - Ensure MySQL is running
   - Check `.env` file configuration
   - Verify database exists

2. **Port already in use**
   - Change the PORT in `.env` file
   - Or stop the process using port 8000

### Frontend Issues

1. **Module not found errors**
   - Delete `node_modules` and `package-lock.json`
   - Run `npm install` again

2. **Proxy errors**
   - These are warnings and won't prevent the app from running
   - Ensure backend is running for API calls to work

3. **Date picker errors**
   - If you see date-fns errors, ensure you ran `npm install` after the package.json update

## Environment Variables

### Backend (.env file)
```env
# Database (choose one)
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/manufacter_visibility
# OR for SQLite:
# DATABASE_URL=sqlite:///./manufacter_visibility.db

# Server
HOST=0.0.0.0
PORT=8000
```

## Development Notes

- The backend uses FastAPI with automatic API documentation at `/docs`
- The frontend uses React with Material-UI
- Both apps support hot reload during development
- Database tables are automatically created on first run

