from fastapi import FastAPI, UploadFile, File
import pandas as pd
from db import *
import uvicorn

app = FastAPI()

app.post("/upload")
def manage_data(file: UploadFile = File(...)):
    connection = connect_and_create()

    df = pd.read_csv(file.file)
    bins = [0, 20, 100, 300, 24000]
    labels = ["low", "medium", "high", "extreme"]
    df["risk_level"] = pd.cut(df["range_km"], bins=bins, labels=labels)
    df["manufacturer"] = df["manufacturer"].fillna("Uknown")
    for _, row in df.iterrows():
        print(row)
        connection.insert_into(row["weapon_id"], row["weapon_name"], row["weapon_type"], row["range_km"], row["weight_kg"], row["manufacturer"], row["origin_country"], row["storage_location"], row["year_estimated"], row["risk_level"])

    connection.close_connection()


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)