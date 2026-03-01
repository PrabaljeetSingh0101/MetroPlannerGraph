import pandas as pd
from pyDatalog import pyDatalog
pyDatalog.clear()
pyDatalog.create_terms(
    'RouteHasStop, TripFare, DirectRoute, Transfer1Route, '
    'Transfer2Route, AvoidStopRoute, X, Y, Z, Z1, Z2, R, R1, R2, R3, P, P1, P2, P3, AvoidStop'
)
def create_mappings():
    """
    Task 1: Data Preparation (3 Marks)
    Create route-to-stops and fares mappings from GTFS data
    
    Returns:
    - route_to_stops: Dictionary mapping route_id to ordered list of stop_ids
    - fares: Dictionary mapping (route_id, origin_id, dest_id) to price
    """
    # TODO: Read and merge trip data (stop_times.txt and trips.txt)
    df_trips = pd.merge(
        pd.read_csv('stop_times.txt'),
        pd.read_csv('trips.txt'),
        on='trip_id'
    )[['trip_id', 'route_id', 'stop_id', 'stop_sequence']]
     
    # TODO: Read and merge fare data (fare_rules.txt and fare_attributes.txt)
    df_fare_rules = pd.read_csv('fare_rules.txt')
    df_fare_attributes = pd.read_csv('fare_attributes.txt')
    df_fare = pd.merge(df_fare_rules, df_fare_attributes, on='fare_id')
# Convert IDs to int and price to float
    df_trips[['route_id', 'stop_id']] = df_trips[['route_id', 'stop_id']].astype(int)
    df_fare[['route_id', 'origin_id', 'destination_id']] = df_fare[['route_id', 'origin_id', 'destination_id']].astype(int)
    df_fare['price'] = df_fare['price'].astype(float)
  
    # TODO: Create route_to_stops dictionary with ordered stops
    route_to_stops = {
        int(route): list(map(int, group.sort_values('stop_sequence')['stop_id']))
        for route, group in df_trips.groupby('route_id')
    }
   
    # TODO: Create fares dictionary
    fares = {
        (int(row['route_id']), int(row['origin_id']), int(row['destination_id'])): float(row['price'])
        for _, row in df_fare.iterrows()
    }
    
    return route_to_stops, fares

def setup_datalog(route_to_stops, fares):
    """
    Task 2: pyDatalog Knowledge Base Setup (2 Marks)
    Setup pyDatalog knowledge base with terms and facts
    """
    # TODO: Add facts for routes and stops
    for route, stops in route_to_stops.items():
        for stop in stops:
            + RouteHasStop(route, stop)  # Fixed assertion

    # TODO: Add facts for fares
    for (route, origin, dest), price in fares.items():
        + TripFare(route, origin, dest, price)  # Fixed assertion
def define_rules():
    """
    Task 3: Rule Implementation (4 Marks)
    Define pyDatalog rules for route finding
    
    Required Rules:
    1. DirectRoute(X, Y, R, P): Direct route R from X to Y with fare P
    2. Transfer1Route(X, Y, R1, Z, R2, P): 1-transfer route via Z using R1, R2 with fare P
    3. Transfer2Route(X, Y, R1, Z1, R2, Z2, R3, P): 2-transfer route via Z1, Z2 with fare P
    4. AvoidStopRoute(X, Y, AvoidStop, R, P): Direct route avoiding specific stop
    """
    # TODO: Implement DirectRoute rule
    DirectRoute(X, Y, R, P) <= (
        RouteHasStop(R, X) & RouteHasStop(R, Y) & TripFare(R, X, Y, P)
    )
    
    # TODO: Implement Transfer1Route rule
    Transfer1Route(X, Y, R1, Z, R2, P) <= (
        DirectRoute(X, Z, R1, P1) & DirectRoute(Z, Y, R2, P2) & 
        (P == P1 + P2) & (R1 != R2) & (X != Z) & (Z != Y)
    )
    
    # TODO: Implement Transfer2Route rule
    Transfer2Route(X, Y, R1, Z1, R2, Z2, R3, P) <= (
        DirectRoute(X, Z1, R1, P1) & DirectRoute(Z1, Z2, R2, P2) & 
        DirectRoute(Z2, Y, R3, P3) & (P == P1 + P2 + P3) &
        (R1 != R2) & (R2 != R3) & (X != Z1) & (Z1 != Z2) & (Z2 != Y)
    )
    
    # TODO: Implement AvoidStopRoute rule
    AvoidStopRoute(X, Y, AvoidStop, R, P) <= (
        DirectRoute(X, Y, R, P) & ~RouteHasStop(R, AvoidStop)
    )
    
    AvoidStopRoute(X, Y, AvoidStop, R1, Z, R2, P) <= (
        Transfer1Route(X, Y, R1, Z, R2, P) & ~RouteHasStop(R1, AvoidStop) & ~RouteHasStop(R2, AvoidStop)
    )
    
    AvoidStopRoute(X, Y, AvoidStop, R1, Z1, R2, Z2, R3, P) <= (
        Transfer2Route(X, Y, R1, Z1, R2, Z2, R3, P) & ~RouteHasStop(R1, AvoidStop) & ~RouteHasStop(R2, AvoidStop) & ~RouteHasStop(R3, AvoidStop)
    )

def query_routes(start_stop, end_stop, avoid_stop=None):
    """
    Task 4: Query Execution (1 Mark)
    Execute queries and return results in required format
    """
    results = {
        'direct_routes': [],
        'one_transfer': [],
        'two_transfer': [],
        'avoid_stop': []
    }
    
    # TODO: Implement queries and format results
    # Remember to return at most 5 results per category, sorted by fare in ascending order
    start_stop, end_stop = int(start_stop), int(end_stop)

    # Query DirectRoute
    direct_routes = sorted(DirectRoute(start_stop, end_stop, R, P).data, key=lambda x: -x[1])[:5]
    if direct_routes:
        results['direct_routes'] = [(int(r), float(p)) for r, p in direct_routes]

    # Query 1-Transfer Route
    one_transfer_routes = sorted(Transfer1Route(start_stop, end_stop, R1, Z, R2, P).data, key=lambda x: -x[3])[:5]
    if one_transfer_routes:
        results['one_transfer'] = [(int(r1), int(z), int(r2), float(p)) for r1, z, r2, p in one_transfer_routes]

    # Query 2-Transfer Route
    two_transfer_routes = sorted(Transfer2Route(start_stop, end_stop, R1, Z1, R2, Z2, R3, P).data, key=lambda x: -x[5])[:5]
    if two_transfer_routes:
        results['two_transfer'] = [(int(r1), int(z1), int(r2), int(z2), int(r3), float(p)) for r1, z1, r2, z2, r3, p in two_transfer_routes]

    # Query AvoidStopRoute (only if avoid_stop is given)
    if avoid_stop:
        avoid_stop_routes = sorted(AvoidStopRoute(start_stop, end_stop, int(avoid_stop), R, P).data, key=lambda x: -x[1])[:5]
        if avoid_stop_routes:
            results['avoid_stop'] = [(int(r), float(p)) for r, p in avoid_stop_routes]
    
    return results

def main():
    # Create data mappings
    route_to_stops, fares = create_mappings()
    
    # Setup pyDatalog
    setup_datalog(route_to_stops, fares)
    
    # Define rules
    define_rules()
    
    # Example usage
    results = query_routes(146, 148, avoid_stop=233)
    
    # Print results
    print("Direct routes:", results['direct_routes'])
    print("1-transfer:", results['one_transfer'])
    print("2-transfer:", results['two_transfer'])
    print("Avoid Stop:", results['avoid_stop'])

if __name__ == "__main__":
    main()


#################### PUBLIC TEST CASES ###########################

# Test Case 1: query_routes(146, 148, avoid_stop=233)

# Direct routes: [(2044, 5.0), (1319, 5.0), (10595, 5.0), (1180, 5.0), (687, 5.0)]
# 1-transfer: [(2044, 488, 955, 10.0), (2044, 488, 1700, 10.0), (2044, 488, 10601, 10.0), (2044, 488, 10634, 10.0), (2044, 488, 1401, 10.0)]
# 2-transfer: [(10486, 2032, 10643, 488, 955, 15.0), (10486, 2032, 10643, 488, 1700, 15.0), (10486, 2032, 10643, 488, 10601, 15.0), (10486, 2032, 10643, 488, 10634, 15.0), (10486, 2032, 10643, 488, 1401, 15.0)]
# Avoid Stop: [(2044, 5.0), (1319, 5.0), (10595, 5.0), (1180, 5.0), (687, 5.0)]

# Test Case 2: query_routes(2161, 3569, avoid_stop=2162)

# Direct routes: [(149, 5.0), (10596, 5.0), (1249, 5.0), (456, 5.0), (10016, 5.0)]
# 1-transfer: [(149, 2162, 10006, 10.0), (149, 2162, 10643, 10.0), (149, 2162, 456, 10.0), (149, 2162, 10016, 10.0), (149, 2162, 320, 10.0)]
# 2-transfer: [(142, 2171, 674, 148, 1851, 30.0), (142, 2171, 674, 149, 1851, 30.0), (1851, 2171, 674, 149, 10006, 35.0), (1851, 2171, 674, 149, 456, 35.0), (1851, 2171, 674, 149, 10526, 35.0)]
# Avoid Stop: []

##################################################################