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

    df['DATE'] = datetime.now().strftime('%d-%m-%Y')
    df['SOURCE'] = "Manual"
    df['POSTNR'] = (
        df['POSTNR']
        .apply(lambda x: str(int(x)) if isinstance(x, (float, int)) and not pd.isna(x) else x)  # remove .0
        .astype(str)
        .str.strip()
        .replace({'nan': '-', 'None': '-', '': '-'})
    )
    df['HEIMILISFANG'] = df['HEIMILISFANG'].astype(str).str.replace(r'\s+', ' ', regex=True).str.strip()

    df["KAUPVERD"] = pd.to_numeric(df["KAUPVERD"], errors="coerce")
    df["KAUPVERD"] = df["KAUPVERD"] * 1000
    df["EINFLM"] = pd.to_numeric(df["EINFLM"], errors="coerce").astype(float)
    df["BYGGAR"] = pd.to_numeric(df["BYGGAR"], errors="coerce")
    df["fermetravera"] = (df["KAUPVERD"].astype(float) / df["EINFLM"].astype(float)).round(2)
    df["THINGLYSTDAGS"] = pd.to_datetime(df["THINGLYSTDAGS"], errors="coerce")

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
            if "THINGLYSTDAGS" in col:
                sql_type = "TIMESTAMP"
            if "KAUPVERD" in col:
                sql_type = "BIGINT"

            with engine.begin() as conn:
                conn.execute(text(f'ALTER TABLE fastinn_data ADD COLUMN "{col}" {sql_type};'))
            print(f"Added missing column: {col} ({sql_type})")

    # Delete previous data
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE fastinn_data;"))
    # Append data
    df.to_sql("fastinn_data", engine, if_exists="append", index=False)
    print(f"Inserted {len(df)} records into Postgres.")
    return len(df)
