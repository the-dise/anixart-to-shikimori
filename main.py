import requests
import json
from tqdm import tqdm

# Функция для определения статуса аниме
def get_status(status_str):
    status_mapping = {
        "Просмотрено": "completed",
        "В планах": "planned",
        "Смотрю": "watching",
        "Брошено": "dropped",
        "Пересматриваю": "rewatching"
    }
    return status_mapping.get(status_str.strip(), "planned")  # По умолчанию ставим "В планах", если статус не найден

# Функция для определения рейтинга аниме
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
    return score_mapping.get(score_str.strip(), 0)  # По умолчанию ставим 0, если рейтинг не найден

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
}

# Создаем список для хранения данных об аниме
anime_data_list = []

# Считываем названия аниме из файла
with open("Anixart_Bookmarks.txt", "r", encoding="utf-8") as file:
    anime_list = file.readlines()

# Используем tqdm для отображения прогресса
with tqdm(total=len(anime_list), desc="Processing") as pbar:
    # Проходим по каждой строке и извлекаем название аниме
    for anime in anime_list:
        # Извлекаем название аниме из строки
        anime_name = anime.split("/")[1].strip().strip("\"")
        
        # Формируем URL-адрес запроса с учетом названия аниме
        url = f"https://shikimori.one/api/animes?search={anime_name}"
        
        # Отправляем запрос к Shikimori API
        response = requests.get(url, headers=headers)
        
        # Получаем JSON ответа
        try: 
            anime_info = response.json()
        except json.decoder.JSONDecodeError:
            print("Response is not in JSON format")
        
        # Проверяем, есть ли результаты поиска
        if anime_info:
            # Извлекаем нужную информацию из первого результата поиска
            target_title = anime_info[0]['name']
            target_id = anime_info[0]['id']
            
            # Получаем рейтинг и статус из строки аниме
            status_str = anime.split("/")[5].strip()
            score_str = anime.split("/")[6].strip()
            
            # Преобразуем рейтинг и статус в соответствующие значения
            status = get_status(status_str)
            score = get_score(score_str)

            # Если статус "completed", берем количество эпизодов из ответа сайта, иначе количество эпизодов равно 0
            if status == "completed":
                episodes = anime_info[0]['episodes']
            else:
                episodes = 0
            
            # Создаем словарь с данными об аниме
            anime_data = {
                "target_title": target_title,
                "target_id": target_id,
                "target_type": "Anime",
                "score": score,
                "status": status,
                "episodes": episodes,
                "text": None
            }
            
            # Добавляем данные об аниме в список
            anime_data_list.append(anime_data)
        else:
            print(f"No results found for '{anime_name}'")

            # Обновляем индикатор прогресса
        pbar.update(1)

# Записываем список данных об аниме в JSON файл
with open("anime_info.json", "w", encoding="utf-8") as json_file:
    json.dump(anime_data_list, json_file, ensure_ascii=False, indent=4)
