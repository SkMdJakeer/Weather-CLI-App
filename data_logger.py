"""
data_logger.py

Author: Sk.Md Jakeer, Nov 3 ,2025

Purpose: record each successful weather lookup into a small SQLite
database. Kept intentionally minimal so it fits offline usage.

"""
import sqlite3
from datetime import datetime
import os


# Personal note : I prefer predictable local filenames and a
# slightly verbose internal API for the logger so that if I come back
# in a year I remember why things were done this way.


class WeatherLogger:
    def __init__(self, database_file="data_log.db"):
        # private connection handle — I usually prefix privates with `_`
        self._db_path = database_file
        # create parent dir if someone passes a path; defensive behavior
        parent = os.path.dirname(self._db_path)
        if parent:
            try:
                os.makedirs(parent, exist_ok=True)
            except Exception:
                # If the folder cannot be created, fall back to current dir
                self._db_path = os.path.basename(self._db_path)
        # Open the DB connection now; this keeps behavior identical but
        # ensures the attribute is set from inside __init__ where `self`
        # is defined. This is a small, intentional rearrangement.
        self._connection = sqlite3.connect(self._db_path)
        # ensure the table is present immediately so the file is usable
        self._create_table_if_missing()

    def _create_table_if_missing(self):
        # Create a tiny schema that matches my quick-report workflow.
        with self._connection:
            self._connection.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY,
                    city TEXT,
                    temp REAL,
                    humidity INTEGER,
                    condition TEXT,
                    timestamp TEXT
                )
            """)

    def log(self, weather_data):
        """Append a weather snapshot to the `logs` table.

        The function expects the same dictionary keys as the rest of the
        application. I purposely kept the same insert order so old tools
        that expect this column ordering still work.
        """
        ts = self._format_timestamp()
        # Use the connection context manager to commit automatically.
        with self._connection:
            self._connection.execute(
                """
                INSERT INTO logs (city, temp, humidity, condition, timestamp)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    weather_data["city"],
                    weather_data["temp"],
                    weather_data["humidity"],
                    weather_data["condition"],
                    ts,
                ),
            )

    def close(self):
        """Explicitly close the DB connection if a caller wants to.

        This is a small, human-friendly nicety — it doesn't change
        the log behavior or the printed output of the CLI.
        """
        try:
            self._connection.close()
        except Exception:
            # Best-effort close; nothing else to do.
            pass

    def _format_timestamp(self) -> str:
        # I like this timestamp format; having a small helper makes the
        # code more explicit and testable (if I had tests).
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")