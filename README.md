# Delhi Metro Route Planner

A logic-based route planner implemented in Python using the `pyDatalog` library and GTFS transit data. This project calculates optimized transit routes, including direct paths and multi-transfer journeys, while prioritizing the lowest fare.

## 👥 Contributors
* **Just me, Prabal, solo project** 

## ✨ Features
* **Direct Routes:** Finds direct connections between an origin and destination stop.
* **Transfer Logic:** Calculates complex 1-transfer and 2-transfer routes across different lines.
* **Avoid Stops:** Includes functionality to explicitly bypass specific stops during pathfinding.
* **Cost Optimization:** Sorts all results by fare in ascending order (lowest fare first).
* **Capped Results:** Limits output to the top 5 most optimal routes per category for clean data retrieval.

## 🛠️ Tech Stack
* **Python 3.x**
* **Pandas:** Used for robust data preparation, cleaning, and merging of GTFS text files.
* **pyDatalog:** Used to establish a declarative knowledge base and define logic rules for route traversal.

## 📂 Dataset (GTFS)
This project requires standard GTFS (General Transit Feed Specification) files to run. Place the following files in the root directory:
* `routes.txt`
* `trips.txt`
* `stop_times.txt`
* `stops.txt`
* `fare_rules.txt`
* `fare_attributes.txt`

## 🚀 How to Run
1. Ensure you have Python installed, along with the required libraries:
   ```bash
   pip install pandas pyDatalog

```

2. Place the required GTFS `.txt` files in the same directory as the script.
3. Run the application:
```bash
python IIS_q2_2024415.py

```



## 🔍 Example Query

The system allows you to query routes by providing the starting stop ID, ending stop ID, and an optional stop ID to avoid.

```python
# Example: Finding a route from Stop 146 to Stop 148, avoiding Stop 233
results = query_routes(146, 148, avoid_stop=233)

```
