import requests
import os
from analyze import analyze_reviews_with_chatgpt

# Set your SerpApi key
SERPAPI_KEY = "ed845c7f43a20777ee0db35c059e49d1837a30ccb5f63ef8f5a6cba915f9b5ac"

# Function to fetch place IDs for a specific industry
def fetch_place_ids(zip_code, radius, industry):
    url = "https://serpapi.com/search"
    params = {
        "engine": "google_maps",
        "q": industry,
        "location": f"{zip_code}",
        "radius": radius * 1609.34,  # Convert miles to meters
        "api_key": SERPAPI_KEY,
    }
    response = requests.get(url, params=params)
    data = response.json()

    # Extract place IDs from the response
    return [result["place_id"] for result in data.get("local_results", []) if "place_id" in result]

# Function to fetch reviews for a specific place ID
def fetch_reviews(place_id):
    url = "https://serpapi.com/search"
    params = {
        "engine": "google_maps_reviews",
        "place_id": place_id,
        "api_key": SERPAPI_KEY,
    }
    response = requests.get(url, params=params)
    data = response.json()

    # Extract review snippets
    return [review.get("snippet", "No snippet available") for review in data.get("reviews", [])]

def main():
    zip_code = input("ZIP code: ")
    industry = input("Industry (e.g., restaurants, automotive): ")
    radius = 2  # Fixed radius in miles

    print("Fetching place IDs...")
    place_ids = fetch_place_ids(zip_code, radius, industry)
    if not place_ids:
        print("No places found. Try another industry or location.")
        return

    all_reviews = []
    print("Fetching reviews...")
    for place_id in place_ids[:1]:  # Limit to 1 place ID for testing
        reviews = fetch_reviews(place_id)
        all_reviews.extend(reviews[:3])  # Limit to 3 reviews

    if not all_reviews:
        print("No reviews found for the given criteria.")
        return

    # Save the limited reviews to a text file on the desktop
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "customer_reviews.txt")
    with open(desktop_path, "w") as file:
        for review in all_reviews:
            file.write(review + "\n\n")

    print(f"Reviews saved to '{desktop_path}'.")

    # Call the ChatGPT-based review analysis function
    print("\nAnalyzing reviews...")
    analyze_reviews_with_chatgpt(desktop_path)

if __name__ == "__main__":
    main()
