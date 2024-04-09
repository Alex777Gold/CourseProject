import requests
from .models import Mission
from .models import MissionDetail


def update_missions():
    url = "https://api.spaceXdata.com/v4/launches/upcoming"

    response = requests.get(url)
    data = response.json()

    for mission_data in data:
        # Перевіряємо, чи місія вже існує в базі даних
        mission_exists = Mission.objects.filter(
            name=mission_data['name']).exists()

        # Якщо місія не існує, додаємо її в базу даних
        if not mission_exists:
            mission = Mission.objects.create(
                name=mission_data['name'],
                launch_date=str(mission_data['date_utc']),
                mission_type=mission_data['rocket'],
                country=mission_data['flight_number'],
            )
            # Отримуємо посилання на YouTube, Reddit та зображення з даних місії
            youtube_link = mission_data['links'].get('webcast')
            reddit_link = mission_data['links'].get(
                'reddit', {}).get('campaign')
            image_link = mission_data['links'].get('patch', {}).get('small')

            # Якщо хоча б одне посилання не порожнє, зберігаємо його разом із місією
            if youtube_link or reddit_link or image_link:
                MissionDetail.objects.create(
                    mission=mission,
                    youtube_link=youtube_link,
                    reddit_link=reddit_link,
                    image_link=image_link
                )
