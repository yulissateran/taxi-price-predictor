# taxi-price-predictor

# Requirements

- Python (3.11.7)

With conda:
`conda create -n <env-name> python=3.11.7`

# Install

`pip install -r requirements.txt`

# Run with docker

`docker compose up`

UI will run in http://localhost:8080/
API will run on http://localhost:5001/


TODO Semana 3:

- Slides (JHON)
- Corregir data cleaning (justificar eliminacion de outliers usando quartiles) Leonardo, Rafael
- Volver a correr modelo, mejorar score (up to 80%, using) Jaime
- Hiperparametrizacion (Jaime, Alexander)
- UI Incluir mapa que indique direccion de pickup y dropoff (Leo, Yuli)

COLUMNAS A INCLUIR EN MODELOS:

// NO, porque no se tienen al momento de realizar la prediccion
'tpep_dropoff_datetime'
'fare_amount'
total_amount
'store_and_fwd_flag'
'VendorID'
'trip_distance'
'RatecodeID'
'tolls_amount'

// SI, porque si se tienen
'tpep_pickup_datetime'
'passenger_count'
'airport_fee'
'PULocationID'
'DOLocationID'
'payment_type'
'tip_amount'
'extra'
'mta_tax'
'improvement_surcharge'
'congestion_surcharge'


- hiperparamtros
- mapa ui
- wheather
