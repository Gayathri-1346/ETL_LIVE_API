from pathlib import Path
from datetime import datetime
import requests

# Set up folders
data_dir = Path(__file__).resolve().parents[1] / "data" / "raw"
data_dir.mkdir(parents=True, exist_ok=True)

img_dir = Path(__file__).resolve().parents[1] / "data" / "images"
img_dir.mkdir(parents=True, exist_ok=True)

def extract_NASA_data():
    # Download NASA APOD JSON
    url = "https://api.nasa.gov/planetary/apod?api_key=6MO6pQS6Kos4ekPG4rJOxstMacKDJokTbq1F5RZm"
    resp = requests.get(url)
    resp.raise_for_status()

    json_filename = data_dir / f"nasa_apod_{datetime.now().strftime('%Y%m%d')}.json"
    json_filename.write_bytes(resp.content)
    print(f"NASA APOD JSON saved to {json_filename}")

    # Download the APOD image
    img_url = "https://apod.nasa.gov/apod/image/2512/Soul_Bugin_1080.jpg"
    img_resp = requests.get(img_url)
    img_resp.raise_for_status()

    img_filename = img_dir / "Soul_Bugin_1080.jpg"
    img_filename.write_bytes(img_resp.content)
    print(f"NASA APOD image saved to {img_filename}")

    return {"json_file": str(json_filename), "image_file": str(img_filename), "json_size_bytes": len(resp.content)}

if __name__ == "__main__":
    extract_NASA_data()
