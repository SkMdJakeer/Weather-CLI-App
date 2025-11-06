# 🌤️ Weather CLI App

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

A **minimal, elegant, and offline-capable Python command-line application** that retrieves live weather data from the **OpenWeatherMap API** and logs every successful lookup into a **local SQLite database** for historical tracking.

---

## 🧭 Overview

This project blends simplicity with practicality — built to check real-time weather quickly via the terminal while maintaining a local record of lookups.

**Highlights:**

* Fetches real-time weather data for any city 🌦️
* Stores query history locally in SQLite 💾
* Minimal dependencies & clean modular design 🧩
* Built-in retry logic and graceful error handling 🧠

---

## 📁 Project Structure

```
.
├── weather.py                # CLI entry point
├── weather_data_fetcher.py   # Handles OpenWeather API integration
├── data_logger.py            # SQLite-based logging module
├── data_log.db               # Auto-created local database file
└── __pycache__/              # Cache directory (auto-generated)
```

---

## ⚙️ Requirements

* Python **3.8+**
* `requests` library

Install dependencies using:

```bash
pip install requests
```

---

## 🔑 Setup Instructions

1. **Get your API Key**
   Sign up at [OpenWeatherMap](https://home.openweathermap.org/users/sign_up) and copy your API key.

2. **Configure the Key**
   Open `weather.py` and replace the placeholder with your own key:

   ```python
   API_KEY = "your_api_key_here"
   ```

3. **Run the Application**

   ```bash
   python weather.py
   ```

---

## 🧩 Usage Example

### 💻 Running the App in VS Code

Below are screenshots showing the application in action inside **Visual Studio Code Terminal**:

#### ▶️ App Launch

![Weather App Launch](./Screenshot%202025-11-03%20192946.png)

#### 🌦️ Query Example (City: Guntur)

![Weather App Guntur Result](./Screenshot%202025-11-03%20193008.png)

---

### Sample Terminal Session

```bash
$ python weather.py
Enter city name (or 'exit' to quit): guntur
guntur: 26.3°C, Humidity: 82%, Conditions: Clouds
Enter city name (or 'exit' to quit): exit
Exiting application.
```

Each query is logged automatically to `data_log.db`.

---

## 💾 Data Logging

Weather lookups are stored under the **`logs`** table in SQLite:

| Column    | Type    | Description                      |
| --------- | ------- | -------------------------------- |
| id        | INTEGER | Auto-incremented record ID       |
| city      | TEXT    | Queried city name                |
| temp      | REAL    | Temperature (°C)                 |
| humidity  | INTEGER | Humidity percentage              |
| condition | TEXT    | Weather condition (e.g., Clouds) |
| timestamp | TEXT    | When the data was recorded       |

Inspect stored data using:

```bash
sqlite3 data_log.db
SELECT * FROM logs;
```

---

## 🧠 Code Breakdown

### 🔹 `weather_data_fetcher.py`

Handles the OpenWeatherMap API request and parses the response into a simple dictionary:

```python
{
  "city": "London",
  "temp": 15.3,
  "humidity": 67,
  "condition": "Clouds"
}
```

### 🔹 `data_logger.py`

Responsible for SQLite database management.

* Automatically creates the database and table.
* Logs every successful weather fetch with timestamps.

### 🔹 `weather.py`

The main command-line interface that ties everything together.

* Prompts the user for input.
* Displays formatted weather information.
* Logs each successful response locally.

---

## 🌐 Example Output

```
Enter city name (or 'exit' to quit): London
London: 15°C, Humidity: 68%, Conditions: Clear

Enter city name (or 'exit' to quit): exit
Exiting application.
```

---

## 👨‍💻 Author

**Sk. Md Jakeer**
*Created on Nov 3, 2025*

> A small project designed for everyday use — simple, portable, and human-readable.

---


## 🪪 License

This project is licensed under the **MIT License** — feel free to modify and distribute.

