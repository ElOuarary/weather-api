from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to the Weather API! Use the /weather endpoint to get weather data.", 200

@app.route("/weather", methods=['GET'])
def get_weather():
    response = {
        "city": "London",
        "temperature": "15°C",
        "condition": "Cloudy"
    }
    return jsonify(response), 200

if __name__ == "__main__":
    app.run(debug=True)