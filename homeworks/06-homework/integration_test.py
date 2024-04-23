import pandas as pd
from datetime import datetime


def dt(hour, minute, second=0):
    return datetime(2022, 1, 1, hour, minute, second)


def save_input_data():
    data = [
        (None, None, dt(1, 2), dt(1, 10)),
        (1, None, dt(1, 2), dt(1, 10)),
        (1, 2, dt(2, 2), dt(2, 3)),
        (None, 1, dt(1, 2, 0), dt(1, 2, 50)),
        (2, 3, dt(1, 2, 0), dt(1, 2, 59)),
        (3, 4, dt(1, 2, 0), dt(2, 2, 1)),
    ]

    columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
    df = pd.DataFrame(data, columns=columns)
    options = {
        'profile': 'localstack',
        'key': 'abc',
        'secret': 'xyz'
    }
    year = 2022
    month = 1
    input_file = f's3://nyc-duration/in/yellow_tripdata_{year:04d}-{month:02d}.parquet'

    df.to_parquet(
        input_file,
        engine='pyarrow',
        compression=None,
        index=False,
        storage_options=options
    )


if __name__ == "__main__":
    save_input_data()
