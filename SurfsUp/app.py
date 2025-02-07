# Import dependencies
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import datetime as dt

#################################################
# Database Setup
#################################################
# Create engine to connect to SQLite database
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    """List all available API routes."""
    return (
        f"Welcome to the Hawaii Climate API!<br/><br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation - Last 12 months of precipitation data<br/>"
        f"/api/v1.0/stations - List of weather stations<br/>"
        f"/api/v1.0/tobs - Temperature observations for station USC00519281 (Last 12 months)<br/>"
        f"/api/v1.0/<start> - Min, Avg, and Max temperatures from a start date (YYYY-MM-DD)<br/>"
        f"/api/v1.0/<start>/<end> - Min, Avg, and Max temperatures for a date range (YYYY-MM-DD to YYYY-MM-DD)<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the last 12 months of precipitation data as JSON."""
    session = Session(engine)
    
    # Find the most recent date in the dataset
    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    latest_date = dt.datetime.strptime(latest_date, "%Y-%m-%d")
    one_year_ago = latest_date - dt.timedelta(days=365)
    
    # Query precipitation data
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).all()
    session.close()
    
    # Convert results into a dictionary
    precipitation_dict = {date: prcp for date, prcp in results}
    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of weather stations."""
    session = Session(engine)
    results = session.query(Station.station).all()
    session.close()
    
    stations_list = [station[0] for station in results]
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return temperature observations for station USC00519281 in the last 12 months."""
    session = Session(engine)
    
    # Find the latest date and calculate one year back
    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    latest_date = dt.datetime.strptime(latest_date, "%Y-%m-%d")
    one_year_ago = latest_date - dt.timedelta(days=365)
    
    # Query temperature observations for station USC00519281
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == "USC00519281").\
        filter(Measurement.date >= one_year_ago).all()
    session.close()
    
    temps = [{"date": date, "temperature": temp} for date, temp in results]
    return jsonify(temps)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temperature_range(start, end=None):
    """Return min, avg, and max temperature for a given date range."""
    session = Session(engine)
    
    if not end:
        # Query temperatures from start date onwards
        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).all()
    else:
        # Query temperatures for the given start-end range
        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()
    
    temp_stats = {
        "Start Date": start,
        "End Date": end if end else "Latest Data",
        "Min Temperature": results[0][0],
        "Avg Temperature": results[0][1],
        "Max Temperature": results[0][2]
    }
    return jsonify(temp_stats)

if __name__ == "__main__":
    app.run(debug=True)