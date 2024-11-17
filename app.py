from flask import Flask, jsonify, request
import os
import redis
import requests
from dotenv import load_dotenv


load_dotenv()


app = Flask(__name__)


REDIS_HOST = "localhost"
REDIS_PORT = 6379
CACHE_EXPIRATION = 43200  # Cache expires after 12 hours (in seconds)
redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


API_KEY = os.getenv("WEATHER_API_KEY")
API_URL = os.getenv("WEATHER_API_URL")


@app.route("/")
def home():
    return "Welcome to the Weather API! Use the /weather endpoint to get weather data.", 200


@app.route("/weather", methods=['GET'])
def get_weather():
    city = request.args.get("city", default="London", type=str)
    if not city:
        return jsonify({"error": "City is required"}), 400
    # Check cache
    cached_data = redis_client.get(city)
    if cached_data:
        print("Cache hit!")  # Debugging message
        return jsonify({"city": city, "data": cached_data})
    try:
        url = f"{API_URL}/{city}?unitGroup=metric&key={API_KEY}"
        responce = requests.get(url)
        responce.raise_for_status()
        data = responce.json()
        weather_info = {
            "city": city,
            "temperature": data["currentConditions"]["temp"],
            "condition": data["currentConditions"]["conditions"]
        }
        return jsonify(weather_info), 200
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)