# sqlalchemy-challenge
# Climate Analysis and Exploration

## Part 1: Analyze and Explore the Climate Data

1. Using Python and SQLAlchemy i made a basic climate analysis and data exploration of climat database.
2. Using the SQLAlchemy `create_engine()` function connected to  SQLite database.
3. Using the SQLAlchemy `automap_base()` function  reflected  tables into classes (`station` and `measurement`).
4. Linked Python to the database by creating a SQLAlchemy session.

### Precipitation Analysis
1. I found the most recent date in the dataset.
2. Get the previous 12 months of precipitation data by querying the previous 12 months of data.
    - Select only the "date" and "prcp" values.
    - Load the query results into a Pandas DataFrame. 
    - Sort the DataFrame values by "date".
3. Plot the results using the DataFrame plot method.
4. Using Pandas printed the summary statistics for the precipitation data.

### Station Analysis
1. Designed a query to calculate the total number of stations in the dataset.
2. Designed a query to find the most-active stations.
3. Design a query that calculates the lowest, highest, and average temperatures for the most-active station.
4. Design a query to get the previous 12 months of temperature observation (TOBS) data for the most-active station.
    

## Part 2: Design Your Climate App

### Using Flask API created Routes
1. `/`: Start at the homepage.
2. `/api/v1.0/precipitation`: Return the JSON representation of the last 12 months of precipitation data.
3. `/api/v1.0/stations`: Return a JSON list of stations from the dataset.
4. `/api/v1.0/tobs`: Return a JSON list of temperature observations for the previous year from the most-active station.
5. `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`: Return a JSON list of temperature statistics for a specified start or start-end range.
    
