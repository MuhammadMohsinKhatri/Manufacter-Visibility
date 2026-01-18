# Manufacturing Visibility Application

A full-stack application for managing manufacturing operations including orders, inventory, production, and supply chain visibility.

## Quick Start

### Prerequisites
- **Python 3.8+**
- **Node.js 14+** and npm

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies (includes AI libraries)**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure AI API Keys (OPTIONAL - for AI features)**
   ```bash
   # Copy the example file
   cp .env.example.txt .env
   
   # Edit .env and add your API keys:
   # - OPENAI_API_KEY (get from https://platform.openai.com/api-keys)
   # - OPENWEATHER_API_KEY (get from https://openweathermap.org/api)
   ```
   
   **Note:** App works without API keys but AI features will use fallback logic

5. **Seed the database (OPTIONAL - but recommended for demo data)**
   ```bash
   python -m app.utils.seed_data
   ```
   This will create the database file (`manufacter_visibility.db`) and populate it with sample data.

6. **Run the backend**
   ```bash
   python run.py
   ```
   
   Backend will start on `http://localhost:8000`
   - API Docs: http://localhost:8000/docs
   - **Try AI endpoints:** `/orders/check-feasibility`, `/shipment-tracking/predict-delay`

### Frontend Setup

1. **Navigate to frontend directory** (in a new terminal)
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
   
   Frontend will start on `http://localhost:3000`

## Database

- **Default**: SQLite (no setup required)
- Database file: `backend/manufacter_visibility.db` (auto-created)
- No MySQL or external database needed!

## Seed Data

The seed script (`backend/app/utils/seed_data.py`) creates sample data including:
- 5 Customers
- 10 Components
- 3 Products
- Sample Orders, Inventory, Production Schedules, and Supply Chain Risks

**Run the seed script once before using the app** to have demo data:
```bash
cd backend
python -m app.utils.seed_data
```

The script is safe to run multiple times - it will skip seeding if data already exists.

## Running the Application

1. **Terminal 1 - Backend**
   ```bash
   cd backend
   venv\Scripts\activate  # Windows
   # or: source venv/bin/activate  # Linux/Mac
   python run.py
   ```

2. **Terminal 2 - Frontend**
   ```bash
   cd frontend
   npm start
   ```

3. **Open browser**: http://localhost:3000

## Project Structure

```
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── database/       # Database configuration (SQLite)
│   │   ├── models/         # SQLAlchemy models
│   │   ├── routers/        # API routes
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   └── utils/          # Utilities (seed_data.py)
│   ├── requirements.txt
│   └── run.py
│
└── frontend/               # React frontend
    ├── public/
    ├── src/
    │   ├── components/     # React components
    │   ├── pages/          # Page components
    │   ├── services/       # API services
    │   └── context/        # React context
    ├── package.json
    └── src/
```

## Features

### Core Features
- **Order Management**: Create, view, update, and track orders
- **Inventory Management**: Track components, stock levels, and allocations
- **Production Scheduling**: Manage production lines and schedules
- **Supply Chain Risk**: Monitor and assess supply chain risks
- **Dashboard**: Overview of orders, inventory, production, and risks

### 🤖 AI-Powered Features (NEW!)
- **AI Order Feasibility Analysis**: GPT-4 powered intelligent recommendations
- **Weather-Based Shipment Tracking**: Real-time delay predictions using weather APIs
- **LLM Risk Mitigation**: AI-generated strategies for supply chain risks
- **Intelligent Decision Support**: Context-aware recommendations for operations

**See [AI_FEATURES.md](AI_FEATURES.md) for detailed AI capabilities**

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Troubleshooting

### Backend won't start
- Make sure virtual environment is activated
- Check that all dependencies are installed: `pip install -r requirements.txt`

### Frontend won't start
- Delete `node_modules` and `package-lock.json`, then run `npm install` again
- Make sure you ran `npm install` after the date-fns package update

### No data showing
- Run the seed script: `python -m app.utils.seed_data`
- Check that the database file exists: `backend/manufacter_visibility.db`

### Database errors
- Delete `backend/manufacter_visibility.db` and run the seed script again
- The database will be automatically recreated

## Notes

- SQLite database file is created automatically in the `backend` directory
- Seed data is optional but recommended for a complete demo experience
- Both apps support hot-reload during development
