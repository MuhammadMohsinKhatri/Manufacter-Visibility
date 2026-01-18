# Manufacturing Visibility System

A comprehensive manufacturing visibility system that addresses critical gaps in order management, inventory, production capacity, and supply chain visibility.

## Overview

This system solves three critical visibility gaps in manufacturing operations:

1. **Order-to-Commitment Visibility Gap**: Real-time feasibility checking for new orders based on inventory, production capacity, and supply chain risks.
2. **Inventory-Production Synchronization Gap**: Dynamic connection between component availability and production scheduling.
3. **Supply Chain Risk Visibility Gap**: Integration of external factors (weather, logistics, market conditions) into planning.

## System Architecture

### Backend (Python/FastAPI)
- RESTful API for all manufacturing visibility operations
- Real-time data processing and integration
- Risk assessment and predictive analytics

### Frontend (React)
- Responsive dashboard interface
- Interactive visualizations
- Role-based access control

### Database (MySQL)
- Relational database for structured manufacturing data
- Comprehensive data model covering orders, inventory, production, and supply chain

## Features

- **Order Feasibility Assessment**: Real-time checking of order feasibility with confidence scoring
- **Inventory Management**: Track component availability, allocations, and reorder thresholds
- **Production Scheduling**: Optimize production capacity and schedule management
- **Supply Chain Risk Monitoring**: Integrate external risk factors into planning
- **Dashboard Visualizations**: Real-time visibility across all operations

## Setup Instructions

### Prerequisites

- Python 3.8+
- MySQL 8.0+
- Node.js 14+
- npm 6+

### Backend Setup

1. Create and activate a virtual environment:

```bash
cd manufacter_visibility/backend
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a MySQL database:

```sql
CREATE DATABASE manufacter_visibility;
```

4. Create a `.env` file in the backend directory with the following content:

```
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/manufacter_visibility
SECRET_KEY=your_secret_key_here
WEATHER_API_KEY=your_weather_api_key
LOGISTICS_API_KEY=your_logistics_api_key
```

5. Seed the database with demo data:

```bash
python -m app.utils.seed_data
```

6. Run the backend server:

```bash
python run.py
```

The API will be available at http://localhost:8000. API documentation is available at http://localhost:8000/docs.

### Frontend Setup

1. Install dependencies:

```bash
cd manufacter_visibility/frontend
npm install
```

2. Create a `.env` file in the frontend directory:

```
REACT_APP_API_URL=http://localhost:8000
```

3. Run the development server:

```bash
npm start
```

The frontend will be available at http://localhost:3000.

## API Documentation

The API documentation is available at http://localhost:8000/docs when the backend server is running. This provides a comprehensive interactive documentation of all available endpoints.

## Demo Credentials

The following demo users are available:

| Username | Password | Role |
|----------|----------|------|
| admin | secret | Administrator |
| sales_manager | secret | Sales Manager |
| production_manager | secret | Production Manager |
| inventory_manager | secret | Inventory Manager |
| sales_rep | secret | Sales Representative |

## License

This project is licensed under the MIT License - see the LICENSE file for details.