#
VendorID
tpep_pickup_datetime
tpep_dropoff_datetime
passenger_count
trip_distance
RatecodeID
PULocationID
DOLocationID
payment_type
fare_amount
extra
mta_tax
tip_amount
tolls_amount
improvement_surcharge: en NY no puede ser 0 ni negativo
total_amount
congestion_surcharge
airport_fee
store_and_fwd_flag: not useful

# Cleanning steps

- Eliminar filas que no son 2022
- Eliminar filas con precios iguales o menores a 0 (preguntar a Mariano, puede ser 0?)
- Usar quartiles/stdr para eliminar outliers  en total_amount
  - Plotear los datos para ver si se encuentra

# Experimento 2, eliminando columnas que no parecen ser utiles
- Eliminar columna store_and_fwd_flag
