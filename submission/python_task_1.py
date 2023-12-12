import pandas as pd

# Question 1: Car Matrix Generation
def generate_car_matrix(dataset):
    df = pd.read_csv(dataset)
    car_matrix = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)
    
    for idx in car_matrix.index:
        car_matrix.at[idx, idx] = 0

    return car_matrix

# Question 2: Car Type Count Calculation
def get_type_count(dataset_path):
    df = pd.read_csv(dataset_path)
    df['car_type'] = pd.cut(df['car'], bins=[-float('inf'), 15, 25, float('inf')], labels=['low', 'medium', 'high'])
    
    return dict(df['car_type'].value_counts().sort_index())

# Question 3: Bus Count Index Retrieval
def get_bus_indexes(dataset):
    df = pd.read_csv(dataset)
    bus_mean = df['bus'].mean()
    bus_indexes = df[df['bus'] > 2 * bus_mean].index.tolist()
    bus_indexes.sort()

    return bus_indexes

# Question 4: Route Filtering
def filter_routes(dataset):
    df = pd.read_csv(dataset)
    selected_routes = df.groupby('route')['truck'].mean().loc[lambda x: x > 7].index.tolist()
    selected_routes.sort()

    return selected_routes

# Question 5: Matrix Value Modification
def multiply_matrix(car_matrix):
    modified_matrix = car_matrix.copy()
    
    for row in modified_matrix.index:
        for col in modified_matrix.columns:
            value = modified_matrix.at[row, col]
            if value > 20:
                modified_matrix.at[row, col] = round(value * 0.75, 1)
            else:
                modified_matrix.at[row, col] = round(value * 1.25, 1)

    return modified_matrix

# Question 6: Time Check
def verify_timestamps(df):
    df['timestamp'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'], format='%Y-%m-%d %I:%M:%S %p', errors='coerce')
    df['day_of_week'] = df['timestamp'].dt.day_name()
    df['hour'] = df['timestamp'].dt.hour

    incorrect_timestamps = df.groupby(['id', 'id_2']).apply(lambda group: not (
        group['day_of_week'].nunique() == 7 and
        group['hour'].nunique() == 24
    )).rename('incorrect_timestamps')

    return incorrect_timestamps

# Question 1: Car Matrix Generation
dataset_path = '/Users/anshulshokeen/Desktop/Submission/dataset-1.csv'
result_matrix = generate_car_matrix(dataset_path)
print("Task 1: Car Matrix Generation\n", result_matrix, end="\n\n")

# Question 2: Car Type Count Calculation
result_type_count = get_type_count(dataset_path)
print("Task 2: Car Type Count Calculation\n", result_type_count, end="\n\n")

# Question 3: Bus Count Index Retrieval
result_bus_indexes = get_bus_indexes(dataset_path)
print("Task 3: Bus Count Index Retrieval\n", result_bus_indexes, end="\n\n")

# Question 4: Route Filtering
result_filter_routes = filter_routes(dataset_path)
print("Task 4: Route Filtering\n", result_filter_routes, end="\n\n")

# Question 5: Matrix Value Modification
result_modified_matrix = multiply_matrix(result_matrix)
print("Task 5: Matrix Value Modification\n", result_modified_matrix, end="\n\n")

# Question 6: Time Check
dataset_path2 = '/Users/anshulshokeen/Desktop/Submission/dataset-2.csv'
df_dataset2 = pd.read_csv(dataset_path2)
result_timestamps = verify_timestamps(df_dataset2)
print("Task 6: Time Check\n", result_timestamps, end="\n\n")
