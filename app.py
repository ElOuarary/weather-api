from flask import Flask, jsonify, request
import os
import redis
import requests
from dotenv import load_dotenv
from config import DevelopmentGonfig, TestingConfig, ProductionConfig


load_dotenv()


app = Flask(__name__)

env = os.getenv("ENV", "development")
if env == "production":
    app.config.from_object(ProductionConfig)
elif env == "testing":
    app.config.from_object(TestingConfig)
else:
    app.config.from_object(DevelopmentGonfig)


redis_client = redis.StrictRedis(
    host=app.config["Redis_Host"],
    port=app.config["Redis_Port"],
    decode_responses=True
)


API_KEY = os.getenv("WEATHER_API_KEY")
API_URL = os.getenv("WEATHER_API_URL")


if not API_KEY or not API_URL:
    raise Exception("API_KEY or API_URL is missing. Check your .env file.")


@app.route("/")
def home():
    return "Welcome to the Weather API! Use the /weather endpoint to get weather data.", 200


@app.route("/weather", methods=['GET'])
def get_weather():
    city = request.args.get("city")
    if not city:
        return jsonify({"error": "City parameter is required"}), 400
    # Check cache
    try:
        cached_data = redis_client.get(city)
        if cached_data:
            return jsonify({"city": city, "data": cached_data})
    
        url = f"{API_URL}/{city}?unitGroup=metric&key={API_KEY}"
        responce = requests.get(url)
        responce.raise_for_status()
        weather_data = responce.json()
        # Save data in cache
        redis_client.setex(city, 43200, str(weather_data))
        return jsonify({"city": city, "data": weather_data})
    except requests.exceptions.HTTPError as http_err:
        return jsonify({"error": f"HTTP error occurred: {http_err}"}), 500
    except redis.ConnectionError:
        return jsonify({"error": "Redis server is unavailable. Please try again later."}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)