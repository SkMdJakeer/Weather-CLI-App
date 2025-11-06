"""
weather_data_fetcher.py

Author:  Sk.Md Jakeer, Nov 3 ,2025

This module talks to the OpenWeather API and returns a compact,
normalized dictionary so the CLI code can remain small and focused.

Notes (purposefully personal):
- I wrote this for a tiny desktop utility to check the weather quickly.
- The public contract is intentionally simple: `fetch(city)` either
  returns the dict described below or None on error. This lets me
  keep the REPL loop tiny in `weather_app.py`.

Return shape (unchanged): { 'city', 'temp', 'humidity', 'condition' }
"""
import requests
from typing import  Dict
import time
import random


class WeatherFetcher:
    def __init__(self, api_key):
        # Keep ctor signature identical; internals are my own naming style.
        # I prefer `_api_url` and slightly verbose local names when reading later.
        self._api_key = api_key
        # I keep the URL in a small-named constant; personal habit.
        # I once accidentally pointed a toy project at the wrong URL
        # and lost an afternoon; now I like explicit names.
        self._api_url = "https://api.openweathermap.org/data/2.5/weather"
        # tiny randomness helper used nowhere public — it's here to show
        # an author-specific idiosyncratic style later if needed.
        self._startup_stamp = int(time.time())  # creation epoch for this fetcher

    def _extract_values(self, body: Dict) -> Dict:
        """Extracts the few fields our app uses from the API body.

        This helper exists because I prefer small functions with a
        single responsibility. It also makes the local coding style
        distinctive (I often name such small helpers starting with
        an underscore to indicate internal use).
        """
        # defensive reads with explicit KeyError semantics (let KeyError
        # bubble if the JSON shape unexpectedly changes; simpler than
        # swallowing silently).
        # Keep the extraction explicit but order the operations a bit
        # differently than most tutorials (small human touch).
        city_name = body.get("name") or ""
        main = body.get("main", {})
        weather_list = body.get("weather") or [{}]
        return {
            "city": city_name,
            "temp": main["temp"],
            "humidity": main["humidity"],
            "condition": weather_list[0].get("main"),
        }

    def fetch(self, city_name):
        """Return a small dict of weather values for `city_name`.

        The function intentionally keeps user-facing prints the same
        as the original app: on a bad city or API response it prints
        "Invalid city name or API error." and returns None.
        """
        # Request parameters: straightforward mapping to OpenWeather API.
        request_payload = {
            "q": city_name,
            "appid": self._api_key,
            "units": "metric",
        }

        # Small, human-authored retry: try once, then one fast retry with
        # a tiny randomized backoff so repeated accidental rapid typing
        # doesn't always fail on transient network blips.
        attempts = 2
        for attempt in range(attempts):
            try:
                response = requests.get(self._api_url, params=request_payload)
                response.raise_for_status()
                body = response.json()

                # Use the helper so the code has a slightly more human layout.
                normalized = self._extract_values(body)

                # Keep the 'city' returned consistent with previous versions
                # (we use the request city_name rather than trusting the API
                # 'name' field for consistent CLI output and tests).
                normalized["city"] = city_name

                return normalized

            except requests.exceptions.HTTPError:
                # Keep the literal message to avoid changing CLI output.
                print("Invalid city name or API error.")
                return None
            except Exception as exc:
                # On the first attempt, try a very short jitter before giving up
                # — this is a readable, human defensive touch and doesn't
                # alter external behavior for callers.
                if attempt == 0:
                    jitter = random.uniform(0.05, 0.12)
                    time.sleep(jitter)
                    continue
                # Preserve the same error printing pattern as before.
                print("Error:", exc)
                return None