##Hawaii Climate API

#Overview

This project is a Flask-based API that serves climate data from a SQLite database containing weather observations from various stations in Hawaii. The API provides endpoints for retrieving precipitation data, station lists, temperature observations, and calculated temperature statistics for specific date ranges.

#Features

Precipitation Data: Retrieve the last 12 months of precipitation records.

Station List: Get a list of all weather stations.

Temperature Observations: Access the last 12 months of temperature observations for the most active station (USC00519281).

Temperature Statistics: Get minimum, average, and maximum temperatures for a given start date or date range.

#Technologies Used

Python

Flask (Web framework for building the API)

SQLAlchemy (ORM for database interactions)

SQLite (Database containing climate data)

Pandas (For data manipulation)

#API Endpoints

1. Landing Page

GET /

Displays a welcome message and lists available API routes.

2. Precipitation Data

GET /api/v1.0/precipitation

Returns a JSON object with dates as keys and precipitation amounts as values.

Only data from the last 12 months is included.

3. Station List

GET /api/v1.0/stations

Returns a JSON list of all weather stations in the database.

4. Temperature Observations

GET /api/v1.0/tobs

Returns a JSON list of temperature observations for station USC00519281 from the last 12 months.

5. Temperature Statistics (Start Date)

GET /api/v1.0/<start>

Returns the minimum, average, and maximum temperatures from the given start date to the most recent date in the dataset.

Format: YYYY-MM-DD

6. Temperature Statistics (Date Range)

GET /api/v1.0/<start>/<end>

Returns the minimum, average, and maximum temperatures for a specified date range.

Format: YYYY-MM-DD/YYYY-MM-DD
