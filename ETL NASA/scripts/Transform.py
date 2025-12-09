import pandas as pd
import os
import glob
import json
def transform_NASA_data():
    os.makedirs("../data/staged",exist_ok=True)
    latest_file=sorted(glob.glob("../data/raw/nasa_apod_*.json"))[-1]
    with open(latest_file,"r") as f:
        data=json.load(f)
    
    df = pd.DataFrame({
        "date": [data.get("date")],
        "title": [data.get("title")],
        "explanation": [data.get("explanation")],
        "media_type": [data.get("media_type")],
        "image_url": [data.get("image_url")],
        "inserted_at": [data.get("date")]  
    })
    output_path="../data/staged/nasa_apod_staged.csv"
    df.to_csv(output_path,index=False)
    print(f"Transformed data saved to {output_path}")
    return df
if __name__=="__main__":
    transform_NASA_data()
