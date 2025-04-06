# 🧭 Nearest Hotel Locator API

A fast and typo-tolerant backend API built using **FastAPI** that helps tele-calling agents find hotel properties within 50 km of a user-input location. The system gracefully handles spelling errors and responds in under 2 seconds.

---

## 🧠 Initial Thought Process

When I first read the problem, I realized the key task was to **find the nearest hotel properties** to a user-input location — even if the input contained typos — and return results within **2 seconds**.

I broke the problem into the following components:

1. **Query Understanding and Error Correction**  
   Users might type city names incorrectly, so I needed a way to recognize and correct these typos quickly.

2. **Location Geocoding**  
   Once the location is corrected, I needed to find its corresponding latitude and longitude efficiently.

3. **Distance Calculation**  
   With the input location's coordinates and the coordinates of all hotel properties, I needed to calculate distances using the **Haversine formula**.

4. **Filtering Results**  
   After calculating distances, I needed to filter and return only the properties within **50 km**.

5. **Building a Fast API**  
   The system exposes an endpoint where a user can enter a location (possibly with typos) and receive a list of nearby properties quickly and accurately.

---

## 🧰 Tools & Libraries Used

| Tool / Library      | Why It Was Chosen |
|---------------------|-------------------|
| **FastAPI**         | High-performance async API framework, perfect for real-time queries. |
| **uvicorn**         | Lightweight ASGI server compatible with FastAPI. |
| **pandas**          | Used for handling and processing the in-memory CSV data. |
| **geopy**           | Provided accurate distance calculation using geodesic formula. |
| **fuzzywuzzy**      | Used for fuzzy matching to correct user typos. |
| **city-coordinates CSV** | Preloaded list of 150 Indian cities with lat/lon for fast, offline geocoding. |

---

## ⚠️ Key Challenge & Final Solution

### Challenge:
Handling **misspelled location inputs** while maintaining a **response time under 2 seconds**.

Even with just 150 cities, fuzzy matching can introduce delay, especially when trying to preserve accuracy.

### Solution:
- Loaded a cleaned list of 150 Indian city names and their coordinates from a CSV file **into memory** at startup.
- Used **fuzzywuzzy** for typo correction. While not the fastest, it provided good enough accuracy for a small dataset.
- Implemented a **simple caching mechanism** using a dictionary to store previously queried locations.


This helped maintain low latency and ensured accurate, typo-tolerant results.

---

## 🚀 Future Improvements

If given more time, here’s how the system could be enhanced:

1. **Use Embeddings for Semantic Matching**  
   Convert user queries into vector embeddings using models from **OpenAI** or **HuggingFace** to better understand vague queries like *"hill station near Delhi"*.

2. **Pre-calculate Distances Using GeoHash or KD-Tree**  
   Implement **spatial indexing** to reduce the number of real-time distance calculations.

3. **Use Redis + Vector Search**  
   Store city embeddings in **Redis** and support high-speed typo + semantic nearest-neighbor search.

4. **Leverage LLMs (Optional)**  
   Use LLMs to extract intent from more complex or conversational inputs like *"a peaceful place near Manali"*.

5. **Use Google Maps API for Geocoding**  
   For higher accuracy and better coverage (especially in rural or lesser-known areas), integrate the **Google Maps Geocoding API**.

These additions would improve **accuracy**, **scalability**, and **user experience** as the dataset and user base grow.

---


## 🔗 Endpoint Example

http://127.0.0.1:8000/nearest-properties?query=jaipur



## Results

{
  "matched_city": "Jaipur",
  "results": [
    {
      "property": "Moustache Jaipur",
      "distance_km": 43.35
    }
  ],
  "response_time_seconds": 0.007
}

## How to run locally

pip install -r requirements.txt
uvicorn main:app --reload