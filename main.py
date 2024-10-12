import os
import time

import requests
import json
from tqdm import tqdm
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Session settings
session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

# Function to split the input file into smaller files with a maximum of 100 lines each
def split_file(input_file, lines_per_file=100):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    file_count = 0
    for i in range(0, len(lines), lines_per_file):
        split_file_name = f"{input_file.split('.')[0]}_part_{file_count + 1}.txt"
        with open(split_file_name, 'w', encoding='utf-8') as split_file:
            split_file.writelines(lines[i:i + lines_per_file])
        file_count += 1
    return file_count

# Function to map status strings to status codes
def get_status(status_str):
    status_mapping = {
        "Просмотрено": "completed",
        "В планах": "planned",
        "Смотрю": "watching",
        "Брошено": "dropped",
        "Пересматриваю": "rewatching"
    }
    return status_mapping.get(status_str.strip(), "planned")  # Default to "planned" if status not found

# Function to map score strings to score values
def get_score(score_str):
    score_mapping = {
        "Не оценено": 0,
        "0 из 5": 1,
        "1 из 5": 2,
        "2 из 5": 4,
        "3 из 5": 5,
        "4 из 5": 7,
        "5 из 5": 10
    }
    return score_mapping.get(score_str.strip(), 0)  # Default to 0 if score not found

# Function to process each anime entry
def process_anime_entry(anime_entry):
    parts = anime_entry.split("/")
    if len(parts) < 7:
        return None  # Invalid entry

    anime_name = parts[1].strip().strip("\"")
    status_str = parts[5].strip()
    score_str = parts[6].strip()

    url = f"https://shikimori.one/api/animes?search={anime_name}"
    response = session.get(url, headers=headers)


    try:
        anime_info = response.json()
    except json.decoder.JSONDecodeError:
        print("Response is not in JSON format")
        return None

    if not anime_info:
        print(f"No results found for '{anime_name}'")
        return None

    target_title = anime_info[0]['name']
    target_id = anime_info[0]['id']
    status = get_status(status_str)
    score = get_score(score_str)
    episodes = anime_info[0]['episodes'] if status == "completed" else 0

    return {
        "target_title": target_title,
        "target_id": target_id,
        "target_type": "Anime",
        "score": score,
        "status": status,
        "episodes": episodes,
        "text": None
    }

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
}

anime_data_list = []

# Split the input file into smaller files
input_file = "Anixart_Bookmarks.txt"
file_count = split_file(input_file)

# Process each smaller file
for file_index in range(1, file_count + 1):
    split_file_name = f"{input_file.split('.')[0]}_part_{file_index}.txt"
    with open(split_file_name, "r", encoding="utf-8") as file:
        anime_list = file.readlines()

    # Use tqdm to display progress
    with tqdm(total=len(anime_list), desc=f"Processing {split_file_name}") as pbar:
        for anime_entry in anime_list:
            anime_data = process_anime_entry(anime_entry)
            if anime_data:
                anime_data_list.append(anime_data)
            pbar.update(1)
            # Delay to prevent "Too many requests"(code 429)
            time.sleep(0.5)

    # Optionally remove the processed split file
    os.remove(split_file_name)

# Write anime data to JSON file
with open("anime_info.json", "w", encoding="utf-8") as json_file:
    json.dump(anime_data_list, json_file, ensure_ascii=False, indent=4)
