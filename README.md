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

TODO:
V2:

- CREAR DB (LEONARDO)
- REVISAR QUE COLUMNAS TENEMOS DISPONIBLES ANTES DE TOMAR EL VIAJE Y SOLO USAR ESAS PARA EL ENTRENAMIENTO (RAFAEL)
- IDENTIFICAR LA FORMULA PARA CALCULAR TIP_AMOUNT PARA VIAJES CON TC (JAIME)
- ITERAR SOBRE EL F ENGINEER, PROBAR MODELOS PARA SUBIR EL SCORE (ALEXANDER) (JAIME)
- PRENTACION (JHON)
- MEJORAR LA UI (YULI)

COLUMNAS A INCLUIR EN MODELOS:

// NO, porque no se tienen al momento de realizar la prediccion
'tpep_dropoff_datetime'
'fare_amount'
total_amount
'store_and_fwd_flag'
'VendorID'
'trip_distance'
'RatecodeID'

// SI, porque si se tienen
'tpep_pickup_datetime'
'passenger_count'
'airport_fee'
'PULocationID'
'DOLocationID'
'payment_type'
'tip_amount'


// Pendiente identificar si se tienen antes del viaje
'extra'
'mta_tax'
'tolls_amount'
'improvement_surcharge'
'congestion_surcharge'


V3

- hiperparamtros
- mapa ui
- wheather
