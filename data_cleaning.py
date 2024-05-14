# Validate that empty (NaN) values ​​in multiple columns belong to the same rows
columns_to_validate = ['passenger_count', 'RatecodeID', 'store_and_fwd_flag', 'congestion_surcharge', 'airport_fee']

# Create a new column indicating whether all columns are empty in a specific row
trips['empty_columns'] = trips[columns_to_validate].isnull().all(axis=1)

# Check for rows where all columns are empty
rows_with_empty_values = trips[trips['empty_columns'] == True]

# Imprimir el numero de filas con valores vacíos en las columnas especificadas
print(rows_with_empty_values.empty_columns.value_counts())

# The number of rows with empty values in the specified columns is 129524, so we can say all 
# rows with missing values in the columns are the same


# Remove rows with multiple empty columns, as they only represents 3% of the dataset
trips = trips[trips['empty_columns'] == False]
trips.drop(columns=['empty_columns'], inplace=True)


# Remove rows that are not from 2022
# it is easy to visualize and analiza training data from the same month
trips = trips[(trips['tpep_pickup_datetime'].dt.year == 2022) & (trips['tpep_dropoff_datetime'].dt.year == 2022)]
trips.info()

# Remove all rows with trip_distance > 50 because they are outliers in the graphic
# TODO: check how to achieve it matematically and not arbitrialy
trips = trips[trips['trip_distance'] < 50]
plot_hist(trips['trip_distance'], 'trip_distance Distribution', 'Values', 'Frequency')

# Remove all rows with RatecodeID > 6 because according to docs RatecodeID can only goes from 1 to 6
trips = trips[trips['RatecodeID'] < 7]

# Removing rows with PULocationID > 263 or DOLocationID > 263 because according to the documentation, the maximum value is 265
# and 264 = Unnown and 265 = NA, they do not add value to the model 

# In total 57190 rows removed
trips  = trips[(trips['PULocationID'] < 263) | (trips['DOLocationID'] < 263)]

#------------------------------------------
# Replace tpep_pickup_datetime and tpep_dropoff_datetime columns with new columns
trips['pickup_day'] = trips['tpep_pickup_datetime'].dt.day
trips['pickup_hour'] = trips['tpep_pickup_datetime'].dt.hour
trips['pickup_minute'] = trips['tpep_pickup_datetime'].dt.minute

trips['dropoff_day'] = trips['tpep_dropoff_datetime'].dt.day
trips['dropoff_hour'] = trips['tpep_dropoff_datetime'].dt.hour
trips['dropoff_minute'] = trips['tpep_dropoff_datetime'].dt.minute

trips.drop(columns=['tpep_pickup_datetime', 'tpep_dropoff_datetime'], inplace=True)
#---------------------------------------------