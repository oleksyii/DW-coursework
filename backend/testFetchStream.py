import requests


def fetch_game_data(app_id):
    url = f"https://store.steampowered.com/api/appdetails?key=C037D8F73D98B1A13C7A4CE76C4825EC&appids={app_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data and str(app_id) in data:
            app_data = data[str(app_id)]
            if app_data.get('success', False):
                return app_data.get('data', {})
    return {}

if __name__ == "__main__":
        for i in range(500):
            app_data = fetch_game_data(10)
            print(app_data.get('header_image', ''))
        