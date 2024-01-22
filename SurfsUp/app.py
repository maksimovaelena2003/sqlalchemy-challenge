# # Import necessary libraries
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, distinct

from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session


# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")  

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route('/')
def home():
    """Homepage - Lists all available routes."""
    return (
        f"Welcome to the Climate App API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )


# Precipitation route
@app.route("/api/v1.0/precipitation")

def precipitation():
    # Create session 
    session = Session(engine)
    # Perform precipitation query for the last 12 months
    last_year_precipitation = session.query(Measurement.date, Measurement.prcp)\
        .filter(Measurement.date >= '2016-08-23')\
        .all()
    session.close()
    # Convert query results to a dictionary using date as the key and prcp as the value
    precipitation_dict = {date: prcp for date, prcp in last_year_precipitation}

    # Return JSON representation of the dictionary
    return jsonify(precipitation_dict)



# Stations route
@app.route("/api/v1.0/stations")
def stations():
    # Create session
    session = Session(engine)
    # Perform stations query
    station_results = session.query(station.station, station.name).all()
    session.close()

    # Create a list of dictionaries containing station information
    stations_list = [{"station": station, "name": name} for station, name in station_results]

    # Return JSON list of stations
    return jsonify(stations_list)


# TOBS route
@app.route("/api/v1.0/tobs")
def tobs():
    # Create  session
    session = Session(engine)
    # Find the most active station
    most_active_station = session.query(Measurement.station)\
        .group_by(Measurement.station)\
        .order_by(func.count(Measurement.station).desc())\
        .first()

    # Perform TOBS query for the most active station in the last year
    tobs_data = session.query(Measurement.date, Measurement.tobs)\
        .filter(Measurement.station == most_active_station[0])\
        .filter(Measurement.date >= '2016-08-23')\
        .all()
    session.close()
    # Create a list of dictionaries containing date and temperature observations
    tobs_list = [{"date": date, "tobs": tobs} for date, tobs in tobs_data]

    # Return JSON list of temperature observations for the most active station
    return jsonify(tobs_list)


# Start and Start-End range route
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temperature_stats(start, end=None):

    session = Session(engine)
    # If end date is not provided, calculate stats from start date to the last date in the dataset
    if end is None:
        temperature_stats = session.query(func.min(Measurement.tobs).label("TMIN"),
                                          func.avg(Measurement.tobs).label("TAVG"),
                                          func.max(Measurement.tobs).label("TMAX"))\
            .filter(Measurement.date >= start)\
            .all()
    else:
        # If both start and end dates are provided, calculate stats for the specified range
        temperature_stats = session.query(func.min(Measurement.tobs).label("TMIN"),
                                          func.avg(Measurement.tobs).label("TAVG"),
                                          func.max(Measurement.tobs).label("TMAX"))\
            .filter(Measurement.date >= start)\
            .filter(Measurement.date <= end)\
            .all()

    # Create a list of dictionaries containing temperature statistics
    stats_list = [{"TMIN": tmin, "TAVG": tavg, "TMAX": tmax} for tmin, tavg, tmax in temperature_stats]
    session.close()
    # Return JSON list of temperature statistics
    return jsonify(stats_list)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)






