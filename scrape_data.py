import requests
import scrapy
import time
import pandas as pd
import os
from sqlalchemy import create_engine, text, inspect
from datetime import datetime


def download_csv():
    url = "https://fasteignaskra.is/gogn/grunngogn-til-nidurhals/kaupskra-fasteigna/"
    resp = requests.get(url=url)
    response = scrapy.Selector(text=resp.text)
    csv_link = response.css(".btn.btn-lg::attr(href)").get()

    if csv_link.startswith("/"):
        csv_link = "https://fasteignaskra.is" + csv_link

    csv_resp = requests.get(url=csv_link)
    csv_resp.raise_for_status()

    with open("downloaded_file_raw.csv", "wb") as f:
        f.write(csv_resp.content)
    time.sleep(1)

    df = pd.read_csv("downloaded_file_raw.csv", sep=";", encoding="latin-1")
    df['DATE'] = datetime.now().strftime('%Y-%m-%d')
    df['SOURCE'] = "Dynamic"
    df.to_csv("downloaded_file.csv", index=False, sep=",", encoding="utf-8-sig")

    print("file downloaded successfully.")
    os.remove("downloaded_file_raw.csv")


def save_data():
    df = pd.read_csv("downloaded_file.csv", sep=",", encoding="utf-8-sig")

    # engine = create_engine("postgresql+psycopg2://saeed:django123@localhost:5432/fastinn_db")
    engine = create_engine("postgresql+psycopg2://postgres:ubuntu_1122@localhost:5432/fastinn_db")
    inspector = inspect(engine)

    # Create table with id if not exists
    with engine.begin() as conn:
        conn.execute(text("""
                CREATE TABLE IF NOT EXISTS fastinn_data (
                    id SERIAL PRIMARY KEY
                );
            """))

    # Check existing columns
    existing_cols = [col['name'] for col in inspector.get_columns("fastinn_data")]

    # Add any missing columns
    for col in df.columns:
        if col not in existing_cols:
            with engine.begin() as conn:
                conn.execute(text(f'ALTER TABLE fastinn_data ADD COLUMN "{col}" TEXT;'))
            print(f"Added missing column: {col}")

    # Append data
    df.to_sql("fastinn_data", engine, if_exists="append", index=False)

    print(f"Inserted {len(df)} records into Postgres.")
    os.remove("downloaded_file.csv")


if __name__ == "__main__":
    download_csv()
    save_data()
