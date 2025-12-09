import os
import time
import pandas as pd
import numpy as np
from supabase import create_client
from dotenv import load_dotenv

# Initialize Supabase client
load_dotenv()
supabase = create_client(os.getenv("Supabase_url"), os.getenv("Supabase_key"))

def load_to_supabase():
    csv_path = "../data/staged/nasa_apod_staged.csv"
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Missing file: {csv_path}")

    df = pd.read_csv(csv_path)

    # Add inserted_at if missing
    if "inserted_at" not in df.columns:
        df["inserted_at"] = pd.Timestamp.now()
    df["inserted_at"] = pd.to_datetime(df["inserted_at"]).dt.strftime("%Y-%m-%dT%H:%M:%S")

    # Rename url → image_url if needed
    if "url" in df.columns and "image_url" not in df.columns:
        df.rename(columns={"url": "image_url"}, inplace=True)

    # Keep only the required columns
    allowed_cols = ["date", "title", "explanation", "media_type", "image_url", "inserted_at"]
    df = df[[c for c in allowed_cols if c in df.columns]]

    # Replace NaN / inf / -inf → None
    df.replace([np.nan, np.inf, -np.inf], None, inplace=True)

    batch_size = 20
    for i in range(0, len(df), batch_size):
        batch_df = df.iloc[i:i + batch_size]
        records = batch_df.to_dict("records")

        resp = supabase.table("nasa_apod").insert(records).execute()
        print(f"Inserted rows {i+1} → {min(i+batch_size, len(df))}")

        time.sleep(0.5)

    print("Finished loading NASA data.")

if __name__ == "__main__":
    load_to_supabase()
