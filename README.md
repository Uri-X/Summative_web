NYC Yellow Taxi Insights

Dashboard and API for analyzing NYC Yellow Taxi trip data (pickups, fares, zones, time patterns)

data source: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page:

# 🚕 NYC Taxi Dashboard

An enterprise-level fullstack web application for exploring urban mobility patterns using the NYC Taxi & Limousine Commission (TLC) trip dataset. Built with Flask, SQLite, and vanilla JavaScript with Chart.js and Leaflet.

---

## 📽️ Video Walkthrough

[Watch the video walkthrough here](#) ← replace with your link

---

## 📁 Project Structure

```
Summative_web/
├── backend/
│   ├── app.py                  # Flask application entry point
│   ├── nyc_taxi.db             # SQLite database
│   ├── requirements.txt        # Python dependencies
│   ├── db/
│   │   ├── connection.py       # Database connection module
│   │   ├── schema.sql          # Database schema
│   │   └── seed_data.py        # Data cleaning and seeding script
│   ├── routes/
│   │   ├── trips.py            # Trip API endpoints
│   │   └── zones.py            # Zones API endpoint
│   ├── static/
│   │   ├── dashboard.js        # Frontend JavaScript
│   │   └── styles.css          # Dashboard styling
│   ├── templates/
│   │   └── index.html          # Main dashboard HTML template
│   └── utils/
│       ├── data_cleaning.py    # Data cleaning pipeline
│       ├── feature_engineering.py  # Derived feature computation
│       └── logging_utils.py    # Logging excluded/suspicious records
└── data/
    ├── yellow_tripdata_2022-01.parquet  # Raw trip fact table
    ├── taxi_zone_lookup.csv             # Zone dimension table
    └── taxi_zones.shp                   # Spatial metadata
```

---

## ⚙️ Setup Instructions

### Prerequisites

- Python 3.10+
- pip

### 1. Clone the repository

```bash
git clone https://github.com/Uri-X/Summative_web.git
cd Summative_web
```

### 2. Install dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Seed the database

If the database is not already populated, run the seeding script:

```bash
cd db
python seed_data.py
cd ..
```

### 4. Run the application

```bash
cd backend
python app.py
```

### 5. Open the dashboard

Open your browser and go to:

```
http://127.0.0.1:5000/
```

---

## 🗄️ Database Schema

### `dim_zones` (Dimension Table)
| Column | Type | Description |
|---|---|---|
| LocationID | INTEGER | Primary key |
| Borough | TEXT | NYC borough name |
| Zone | TEXT | Taxi zone name |
| geom | TEXT | GeoJSON geometry |

### `fact_trips` (Fact Table)
| Column | Type | Description |
|---|---|---|
| trip_id | INTEGER | Primary key |
| pickup_datetime | TEXT | Trip start timestamp |
| dropoff_datetime | TEXT | Trip end timestamp |
| trip_distance | REAL | Distance in miles |
| fare_amount | REAL | Base fare in USD |
| total_amount | REAL | Total charge in USD |
| PULocationID | INTEGER | Pickup zone (FK) |
| DOLocationID | INTEGER | Drop-off zone (FK) |
| trip_duration | REAL | Duration in minutes |
| speed | REAL | Calculated speed |
| fare_per_mile | REAL | Derived fare efficiency |

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Dashboard home page |
| GET | `/zones` | All taxi zones |
| GET | `/trips` | First 1000 trip records |
| GET | `/trips/summary` | KPI metrics (total trips, avg fare, etc.) |
| GET | `/trips/by-hour` | Trip count and avg fare by hour |
| GET | `/trips/by-day` | Trip count by day of week |
| GET | `/trips/by-borough` | Trip count and avg fare by borough |
| GET | `/trips/top-zones` | Top 10 pickup zones |
| GET | `/trips/top-dropoff-zones` | Top 10 drop-off zones |
| GET | `/trips/fare-distribution` | Trips grouped by fare range |
| GET | `/trips/by-distance` | Trips grouped by distance range |
| GET | `/trips/duration-distribution` | Trips grouped by duration range |
| GET | `/trips/peak-vs-offpeak` | Peak vs off-peak hour comparison |
| GET | `/trips/long-vs-short` | Long vs short trip comparison |
| GET | `/trips/fare-per-mile-by-borough` | Avg fare per mile by borough |

---

## 📊 Dashboard Features

- **KPI Cards** — Total trips, average fare, distance, duration, and speed at a glance
- **Trips by Hour** — Line chart showing demand patterns throughout the day
- **Trips by Day of Week** — Bar chart of weekly trip distribution
- **Trips by Borough** — Bar chart comparing boroughs by volume and fare
- **Fare per Mile by Borough** — Efficiency comparison across boroughs
- **Fare Distribution** — Doughnut chart of fare range breakdown
- **Distance Distribution** — Doughnut chart of trip distance ranges
- **Duration Distribution** — Bar chart of trip duration ranges
- **Peak vs Off-Peak** — Pie chart comparing rush hour vs off-peak trips
- **Long vs Short Trips** — Comparison of trip types by count and fare
- **Top 10 Pickup Zones** — Horizontal bar chart of busiest pickup locations
- **Top 10 Drop-off Zones** — Horizontal bar chart of busiest drop-off locations
- **Interactive Map** — Leaflet map with clickable borough markers showing zone lists

---

## 🧪 Derived Features (Feature Engineering)

| Feature | Formula | Insight |
|---|---|---|
| `trip_duration` | `dropoff_datetime - pickup_datetime` (minutes) | Measures trip length in time |
| `speed` | `(trip_distance / trip_duration) * 60` | Estimates average travel speed in mph |
| `fare_per_mile` | `fare_amount / trip_distance` | Measures fare efficiency per mile |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Database | SQLite |
| Frontend | HTML, CSS, JavaScript |
| Charts | Chart.js |
| Map | Leaflet.js + OpenStreetMap |
| Data Processing | Pandas, PyArrow |

---

## 👥 Author

Philbert Kuria