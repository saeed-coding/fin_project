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
    df['DATE'] = datetime.now().strftime('%d-%m-%Y')
    df['SOURCE'] = "Dynamic"
    df.to_csv("downloaded_file.csv", index=False, sep=",", encoding="utf-8-sig")

    print("file downloaded successfully.")
    os.remove("downloaded_file_raw.csv")


def save_data():
    df = pd.read_csv("downloaded_file.csv", sep=",", encoding="utf-8-sig")
    df["KAUPVERD"] = pd.to_numeric(df["KAUPVERD"], errors="coerce")
    df["KAUPVERD"] = df["KAUPVERD"] * 1000
    df["EINFLM"] = pd.to_numeric(df["EINFLM"], errors="coerce").astype(float)
    df["BYGGAR"] = pd.to_numeric(df["BYGGAR"], errors="coerce")
    df["fermetravera"] = (df["KAUPVERD"].astype(float) / df["EINFLM"].astype(float)).round(2)

    df["id"] = (
            df["FAERSLUNUMER"].astype(str) + "_" +
            df["EMNR"].astype(str) + "_" +
            df["FASTNUM"].astype(str)
    )

    # engine = create_engine("postgresql+psycopg2://saeed:django123@localhost:5432/fastinn_db")
    engine = create_engine("postgresql+psycopg2://postgres:ubuntu_1122@localhost:5432/fastinn_db")
    inspector = inspect(engine)

    # Create table with id if not exists
    with engine.begin() as conn:
        conn.execute(text("""
                CREATE TABLE IF NOT EXISTS fastinn_data (
                    id TEXT PRIMARY KEY
                );
            """))

    # Check existing columns
    existing_cols = [col['name'] for col in inspector.get_columns("fastinn_data")]
    dtype_map = {
        "int64": "BIGINT",
        "float64": "DOUBLE PRECISION",
        "object": "TEXT",
        "datetime64[ns]": "TIMESTAMP",
        "bool": "BOOLEAN"
    }
    # Add missing columns with correct type
    for col in df.columns:
        if col not in existing_cols:
            # Get dtype of current column
            dtype = str(df[col].dtype)

            # Map pandas dtype to PostgreSQL type
            sql_type = dtype_map.get(dtype, "TEXT")  # fallback to TEXT

            with engine.begin() as conn:
                conn.execute(text(f'ALTER TABLE fastinn_data ADD COLUMN "{col}" {sql_type};'))
            print(f"Added missing column: {col} ({sql_type})")

    today = datetime.now().strftime('%d-%m-%Y')

    # ✅ Check if data already exists for today with SOURCE='Manual'
    with engine.begin() as conn:
        result = conn.execute(
            text("SELECT COUNT(*) FROM fastinn_data WHERE \"DATE\" = :date AND \"SOURCE\" = 'Manual'"),
            {"date": today}
        ).scalar()

    if result and result > 0:
        print(f"⚠️ Data for {today} with SOURCE='Manual' already exists. Skipping insertion.")
    else:
        # Delete previous data
        with engine.begin() as conn:
            conn.execute(text("TRUNCATE TABLE fastinn_data;"))

        # Append data
        df.to_sql("fastinn_data", engine, if_exists="append", index=False)

        print(f"Inserted {len(df)} records into Postgres.")

    os.remove("downloaded_file.csv")


if __name__ == "__main__":
    download_csv()
    save_data()
