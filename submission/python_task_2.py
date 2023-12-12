import pandas as pd
import datetime
import numpy as np
import networkx as netx

# Question 1: Distance Matrix Calculation
def calculate_distance_matrix_custom():
    df_custom = pd.read_csv('dataset-3.csv')
    G_custom = netx.Graph()

    for row_custom in df_custom.itertuples(index=False):
        G_custom.add_edge(row_custom.id_start, row_custom.id_end, distance=row_custom.distance)
        G_custom.add_edge(row_custom.id_end, row_custom.id_start, distance=row_custom.distance)  # Bidirectional

    distance_matrix_custom = pd.DataFrame(index=G_custom.nodes, columns=G_custom.nodes, dtype=float)
    distance_matrix_custom = distance_matrix_custom.fillna(0)

    for source_custom in G_custom.nodes:
        for destination_custom in G_custom.nodes:
            if source_custom != destination_custom:
                if netx.has_path(G_custom, source_custom, destination_custom):
                    distance_matrix_custom.at[source_custom, destination_custom] = netx.shortest_path_length(
                        G_custom, source_custom, destination_custom, weight='distance')

    distance_matrix_custom = (distance_matrix_custom + distance_matrix_custom.T) / 2
    return distance_matrix_custom

# Question 2: Unroll Distance Matrix
def unroll_distance_matrix(distance_matrix):
    unrolled_data = []

    for id_start in distance_matrix.index:
        for id_end in distance_matrix.columns:
            if id_start != id_end:
                distance = distance_matrix.at[id_start, id_end]
                unrolled_data.append({'id_start': id_start, 'id_end': id_end, 'distance': distance})

    unrolled_df = pd.DataFrame(unrolled_data)
    return unrolled_df

# Question 3: Finding IDs within Percentage Threshold
def find_ids_within_ten_percentage_threshold(distance_df, reference_value):
    avg_distance = distance_df[distance_df['id_start'] == reference_value]['distance'].mean()
    lower_threshold = avg_distance - 0.1 * avg_distance
    upper_threshold = avg_distance + 0.1 * avg_distance
    filtered_df = distance_df[(distance_df['distance'] >= lower_threshold) &
                              (distance_df['distance'] <= upper_threshold)]
    result_ids = sorted(filtered_df['id_start'].unique())
    return result_ids

# Question 4: Calculate Toll Rate
def calculate_toll_rate(distance_df):
    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}

    for vehicle_type, rate_coefficient in rate_coefficients.items():
        distance_df[vehicle_type] = distance_df['distance'] * rate_coefficient
    return distance_df

# Question 5: Calculate Time-Based Toll Rates
def calculate_time_based_toll_rates(df):
    weekday_ranges = [
        (datetime.time(0, 0, 0), datetime.time(10, 0, 0), 0.8),
        (datetime.time(10, 0, 0), datetime.time(18, 0, 0), 1.2),
        (datetime.time(18, 0, 0), datetime.time(23, 59, 59), 0.8)
    ]

    weekend_ranges = [(datetime.time(0, 0, 0), datetime.time(23, 59, 59), 0.7)]
    time_based_toll_df = pd.DataFrame(columns=df.columns.tolist() + ['start_day', 'start_time', 'end_day', 'end_time'])

    for (_, group_df), start_day in zip(df.groupby(['id_start', 'id_end']), range(7)):
        for start_time, end_time, discount_factor in get_time_ranges(start_day, weekday_ranges, weekend_ranges):
            end_day = (start_day + 1) % 7 
            toll_rates = group_df.loc[:, 'moto':'truck'] * discount_factor
            time_based_toll_df = time_based_toll_df.append({
                **group_df.to_dict('records')[0],
                'start_day': get_day_name(start_day),
                'start_time': start_time,
                'end_day': get_day_name(end_day),
                'end_time': end_time,
                **toll_rates.to_dict('records')[0]
            }, ignore_index=True)
    return time_based_toll_df

def get_time_ranges(start_day, weekday_ranges, weekend_ranges):
    if start_day < 5:  # Weekdays
        return weekday_ranges
    else:  
        return weekend_ranges

def get_day_name(day_number):
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    return day_names[day_number]

# Task 2

# Question 1: Distance Matrix Calculation
result_matrix_custom = calculate_distance_matrix_custom()
print("Task 1: Distance Matrix Calculation\n", result_matrix_custom, end="\n\n")

# Question 2: Unroll Distance Matrix
result_unrolled = unroll_distance_matrix(result_matrix_custom)
print("Task 2: Unroll Distance Matrix\n", result_unrolled, end="\n\n")

# Question 3: Finding IDs within Percentage Threshold
reference_value = 1  # Replace with the desired reference value
result_within_threshold = find_ids_within_ten_percentage_threshold(result_unrolled, reference_value)
print("Task 3: Finding IDs within Percentage Threshold\n", result_within_threshold, end="\n\n")

# Question 4: Calculate Toll Rate
result_with_toll_rates = calculate_toll_rate(result_unrolled)
print("Task 4: Calculate Toll Rate\n", result_with_toll_rates, end="\n\n")

# Question 5: Calculate Time-Based Toll Rates
result_time_based_toll = calculate_time_based_toll_rates
