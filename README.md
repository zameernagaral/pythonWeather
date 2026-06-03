# Python Real-Time Weather Monitoring

A lightweight, elegant Python web application built using **Flask**, **HTML**, and **CSS**. It queries the OpenWeatherMap API for live, real-time weather information of any city, processes and enhances this data with smart outdoor recommendations, tracks search history, and displays everything in a clean, human-centered UI.

This project is tailored for **first-year engineering lab evaluations** with highly readable, well-commented code, and zero complex JavaScript.

---

## 🌟 Key Features

1. **Real-Time API Fetching**: Connects directly to the live OpenWeatherMap API to retrieve current conditions.
2. **Detailed Metrics**: Displays temperature, atmospheric pressure, humidity, wind speed, wind degree, ground/sea level, and coordinates.
3. **Smart Clothing & Activity Recommendations**: Analyzes weather variables (temperature, weather status, wind speed) in Python and generates recommendations (e.g. what to wear, outdoor activity warnings).
4. **Dynamic Theme Switching**: Page colors automatically adapt to the city's actual weather condition (e.g. sunset colors for sunny, soft grays for clouds, cool slate for rain) using standard CSS class bindings.
5. **Search History Tracker**: Saves the user's last 5 successfully searched cities in the browser session (using Flask cookies) so they can click and re-search instantly.
6. **Celsius ↔ Fahrenheit Toggle**: Easily switch units in one click.
7. **Lab Teacher Presentation Card**: A dedicated section on the bottom of the page showing an overview of the system architecture, how the APIs work, and the code structure.

---

## 🛠️ Tech Stack

- **Backend**: Python 3 & Flask (Micro Web Framework)
- **Frontend**: HTML5 & Vanilla CSS3 (No JavaScript files, making it simple to explain as a pure Python-driven web project)
- **Data Source**: OpenWeatherMap API

---

## 🚀 How to Run Locally

### 1. Install Dependencies
Open your terminal in this directory and run:
```bash
pip install -r requirements.txt
```

### 2. Run the Flask Server
Start the application:
```bash
python app.py
```

### 3. Open in Browser
Open your browser and navigate to:
`http://127.0.0.1:5000`

---

## 🎓 Lab Viva / Teacher Q&A Preparation

Here are questions your Python Lab Teacher might ask and how to answer them:

1. **What is Flask?**
   * *Answer:* Flask is a lightweight "micro-framework" for Python. It provides the tools to handle web requests, routing (mapping URL paths to Python functions), and rendering HTML templates.

2. **How does Python fetch the weather data?**
   * *Answer:* We use Python's `requests` library to make an HTTP `GET` request to the OpenWeatherMap API. The API returns a response in JSON format, which Python automatically parses into a standard dictionary (`dict`).

3. **How does the unit conversion work?**
   * *Answer:* We pass a query parameter in the URL (e.g., `?units=f`). Our Python backend checks this value. If it's `'f'`, Python applies the formula `(Celsius * 9/5) + 32` to convert temperatures before rendering them in the HTML.

4. **Where is the search history stored?**
   * *Answer:* It is stored in the Flask `session` object. Flask encrypts the session data and stores it in a secure cookie in the user's browser, which means the search history persists even if the server is restarted!

5. **How does the website change color automatically?**
   * *Answer:* The Python backend looks at the weather category (like `Clear`, `Rain`, `Clouds`) and passes a theme keyword to the HTML template. In CSS, we defined special styling rules for classes like `.theme-warm`, `.theme-cool`, and `.theme-cloudy`.
