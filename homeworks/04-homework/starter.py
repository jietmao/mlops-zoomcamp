import pickle
import sys

import pandas as pd
from pathlib import Path


categorical = ['PULocationID', 'DOLocationID']


def read_data(filename):
    df = pd.read_parquet(filename)

    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')

    return df


def load_data(year, month):
    with open('model.bin', 'rb') as f_in:
        dv, model = pickle.load(f_in)

    df = read_data(fr'data/yellow_tripdata_{year}-{month:02}.parquet')

    return dv, model, df


def predict(dv, model, df):
    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = model.predict(X_val)

    print(f"Predicted Mean: {y_pred.mean()}")
    return y_pred


def generate_result(df, y_pred, year, month):
    df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')
    df['prediction'] = y_pred
    df = df[['ride_id', 'prediction']]
    return df


def save_result(df, year, month):
    output_file = fr'output/{year}/{month}/result.parquet'
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)

    df.to_parquet(
        output_file,
        engine='pyarrow',
        compression=None,
        index=False
    )


def main():
    year = int(sys.argv[1])
    month = int(sys.argv[2])

    dv, model, df = load_data(year, month)
    prediction = predict(dv, model, df)
    df_result = generate_result(df, prediction, year, month)
    save_result(df_result, year, month)


if __name__ == "__main__":
    main()

