import os
import urllib.request
import urllib.parse
import json
from flask import Flask, render_template, request, redirect, url_for, session

# Initialize the Flask application
app = Flask(__name__)

# Secret key is required to encrypt sessions (cookies) for storing search history
app.secret_key = 'weather_monitoring_secret_key_for_lab'

# API configuration
# We use the OpenWeatherMap API key provided in the original application
API_KEY = "cd210460aeb56354fd13bf8911d788b6"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather_data(city_name):
    """
    Fetches real-time weather data from OpenWeatherMap API using Python's built-in urllib.
    Using urllib ensures this function works out of the box without extra library dependencies.
    """
    try:
        # Properly encode the city name to handle spaces or special characters in URL
        safe_city = urllib.parse.quote(city_name)
        url = f"{BASE_URL}?q={safe_city}&appid={API_KEY}"
        
        # Open URL and read the JSON response
        with urllib.request.urlopen(url, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                return data, None
            else:
                return None, "Failed to retrieve weather data."
                
    except urllib.error.HTTPError as e:
        # Handle specific API errors (e.g. 404 City Not Found, 401 Unauthorized)
        if e.code == 404:
            return None, f"City '{city_name}' not found. Please check spelling."
        elif e.code == 401:
            return None, "Invalid API Key."
        else:
            return None, f"API Error: HTTP {e.code} received."
            
    except urllib.error.URLError as e:
        # Handle connection failures (e.g. no internet connection)
        return None, "Network error: Unable to connect to weather server."
        
    except Exception as e:
        # Catch-all for other unexpected python exceptions
        return None, f"Unexpected error occurred: {str(e)}"


def generate_recommendations(temp_c, condition, wind_speed):
    """
    Analyzes weather metrics and generates human-like suggestions for clothing and activities.
    This demonstrates Python conditional logic (if-elif-else) in a practical way.
    """
    recommendations = {
        "clothing": "",
        "activity": "",
        "health_tip": ""
    }
    
    # 1. Clothing advice based on temperature
    if temp_c < 10:
        recommendations["clothing"] = "Wear a heavy jacket, thermal layers, and a beanie to stay warm."
    elif temp_c < 18:
        recommendations["clothing"] = "A light sweater, jacket, or sweatshirt over jeans would be comfortable."
    elif temp_c < 28:
        recommendations["clothing"] = "Perfect for casual clothing: a simple T-shirt, shirt, or comfortable top."
    else:
        recommendations["clothing"] = "Wear light, breathable cotton clothes. Prefereably light colors to stay cool."

    # 2. Activity advice based on weather conditions
    cond_lower = condition.lower()
    if "rain" in cond_lower or "drizzle" in cond_lower:
        recommendations["activity"] = "Outdoor activities are not recommended. Keep an umbrella or raincoat handy."
    elif "thunderstorm" in cond_lower:
        recommendations["activity"] = "Severe weather warning! Stay indoors and avoid using electrical devices."
    elif "snow" in cond_lower:
        recommendations["activity"] = "Enjoy the snow but stay dry. Good day for indoor board games or building a snowman!"
    elif wind_speed > 10:
        recommendations["activity"] = "High winds detected. Keep outdoor activities to a minimum; secure loose items."
    elif temp_c > 33:
        recommendations["activity"] = "Extremely hot. Limit strenuous outdoor work or sports during peak sun hours."
    else:
        recommendations["activity"] = "Excellent weather for outdoor sports, a walk in the park, or sightseeing."

    # 3. Health / General tip
    if temp_c > 30:
        recommendations["health_tip"] = "Stay hydrated! Drink plenty of water throughout the day to avoid heatstroke."
    elif temp_c < 8:
        recommendations["health_tip"] = "Keep warm and drink hot beverages (tea/coffee) to maintain core body temperature."
    elif "rain" in cond_lower or "humidity" in cond_lower:
        recommendations["health_tip"] = "High moisture content in the air. Dry clothes indoors to avoid mold."
    else:
        recommendations["health_tip"] = "Wear sunscreen if going out in direct sunlight."
        
    return recommendations


def determine_theme(temp_c, condition):
    """
    Selects a CSS class theme based on the current weather condition and temperature.
    This creates an elegant dynamic layout where colors shift softly based on the environment.
    """
    cond_lower = condition.lower()
    
    if "rain" in cond_lower or "drizzle" in cond_lower or "thunderstorm" in cond_lower:
        return "theme-rainy"  # Cool slate/grey tones
    elif "cloud" in cond_lower or "mist" in cond_lower or "fog" in cond_lower or "haze" in cond_lower:
        return "theme-cloudy"  # Soft neutral grey/blue tones
    elif "snow" in cond_lower:
        return "theme-snowy"   # Very light blue/white tones
    elif temp_c >= 25:
        return "theme-sunny"   # Soft warm sand/gold tones
    else:
        return "theme-pleasant" # Sage green/light teal tones


@app.route("/", methods=["GET", "POST"])
def index():
    # Retrieve search history list from the user's session, defaulting to an empty list
    history = session.get("history", [])
    
    # Handle POST request (when the user submits the search form)
    if request.method == "POST":
        city = request.form.get("city", "").strip()
        units = request.form.get("units", "c")
        if city:
            # Redirect to GET request with query arguments for clean URL shareability
            return redirect(url_for("index", city=city, units=units))
        return redirect(url_for("index"))
        
    # Handle GET request (either initial page load, or page loaded with a city query parameter)
    city_query = request.args.get("city", "").strip()
    unit_query = request.args.get("units", "c")
    
    weather_info = None
    error_msg = None
    theme_class = "theme-default"
    
    if city_query:
        # Call API to fetch real-time data
        api_data, err = get_weather_data(city_query)
        
        if api_data:
            # Parse metrics from JSON dictionary
            name = api_data.get("name")
            sys_data = api_data.get("sys", {})
            country = sys_data.get("country", "")
            
            # Primary weather details
            weather_desc = api_data["weather"][0]["description"].capitalize()
            weather_main = api_data["weather"][0]["main"]
            
            # OpenWeatherMap returns temp in Kelvin. Convert to Celsius.
            temp_k = api_data["main"]["temp"]
            temp_c = temp_k - 273.15
            
            # Unit formatting logic
            if unit_query == "f":
                temp_display = round((temp_c * 9/5) + 32)
                unit_symbol = "°F"
            else:
                temp_display = round(temp_c)
                unit_symbol = "°C"
                
            # Secondary details
            coord = api_data.get("coord", {})
            wind = api_data.get("wind", {})
            main = api_data.get("main", {})
            
            # Generate recommendations based on the Celsius metrics
            recs = generate_recommendations(temp_c, weather_main, wind.get("speed", 0))
            
            # Determine background/accent theme based on the weather
            theme_class = determine_theme(temp_c, weather_main)
            
            # Compile weather data packet for rendering
            weather_info = {
                "city": name,
                "country": country,
                "description": weather_desc,
                "condition": weather_main,
                "temp": temp_display,
                "unit": unit_symbol,
                "lat": coord.get("lat"),
                "lon": coord.get("lon"),
                "humidity": main.get("humidity"),
                "pressure": main.get("pressure"),
                "grnd_level": main.get("grnd_level", "N/A"),
                "sea_level": main.get("sea_level", "N/A"),
                "wind_speed": wind.get("speed"),
                "wind_deg": wind.get("deg"),
                "recommendations": recs
            }
            
            # Update search history in session
            # Form clean name e.g. "Mumbai, IN"
            history_entry = f"{name}, {country}"
            if history_entry in history:
                history.remove(history_entry) # Move to front of list if already exists
            history.insert(0, history_entry)
            
            # Keep history capped at 5 items
            history = history[:5]
            session["history"] = history
            
        else:
            error_msg = err
            
    return render_template(
        "index.html", 
        weather=weather_info, 
        error=error_msg, 
        history=history, 
        current_city=city_query,
        current_unit=unit_query,
        theme=theme_class
    )

@app.route("/clear-history")
def clear_history():
    """Route to reset recent searches from browser session."""
    session.pop("history", None)
    # Redirect back to home page, preserving city query parameter if any
    city = request.args.get("city", "")
    units = request.args.get("units", "c")
    if city:
        return redirect(url_for("index", city=city, units=units))
    return redirect(url_for("index"))

if __name__ == "__main__":
    # Run the server on localhost, port 5000.
    # debug=True enables live code reloading as you save changes, helpful during development.
    app.run(debug=True, host="127.0.0.1", port=5000)
