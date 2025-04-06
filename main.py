from fastapi import FastAPI, Query
import pandas as pd
from geopy.distance import geodesic
from fuzzywuzzy import process
import time

app = FastAPI()

# Load data
properties_df = pd.read_csv("properties.csv")
cities_df = pd.read_csv("cities.csv")

# Build a lookup dictionary for fast access
city_coords = {row["city"].lower(): (row["latitude"], row["longitude"]) for _, row in cities_df.iterrows()}



def find_nearest_city(input_query: str) -> tuple:
    # Fuzzy match city name
    matched_city, score = process.extractOne(input_query.lower(), city_coords.keys())
    print(f"Input query: {input_query}, Matched city: {matched_city}, Score: {score}")
    if score < 80:
        return None
    return matched_city, city_coords[matched_city]


@app.get("/nearest-properties")
def get_nearest_properties(query: str = Query(..., description="City or area name")):
    start_time = time.time()
    
    match = find_nearest_city(query)
    if not match:
        return {"message": "Could not recognize the city. Please try again."}

    matched_city_name, input_coords = match
    results = []

    for _, row in properties_df.iterrows():
        prop_coords = (row["latitude"], row["longitude"])
        dist_km = geodesic(input_coords, prop_coords).km
        if dist_km <= 50:
            results.append({
                "property": row["property"],
                "distance_km": round(dist_km, 2)
            })

    if not results:
        return {"message": f"No properties found within 50km of '{matched_city_name.title()}'."}

    response_time = round(time.time() - start_time, 3)
    return {
        "matched_city": matched_city_name.title(),
        "results": results,
        "response_time_seconds": response_time
    }
