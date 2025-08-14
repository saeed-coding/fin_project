import pandas as pd
from sqlalchemy import create_engine, text, inspect
from datetime import datetime
import os

def save_data(csv_file):
    temp_path = f"uploaded_file.csv"
    with open(temp_path, 'wb+') as f:
        for chunk in csv_file.chunks():
            f.write(chunk)

    df = pd.read_csv(temp_path, sep=';', encoding='latin-1')
    # optionally remove temp file
    os.remove(temp_path)

    df['DATE'] = datetime.now().strftime('%Y-%m-%d')
    df['SOURCE'] = "Manual"

    engine = create_engine("postgresql+psycopg2://saeed:django123@localhost:5432/fastinn_db")
    # engine = create_engine("postgresql+psycopg2://postgres:ubuntu_1122@localhost:5432/fastinn_db")
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
    return len(df)
