import requests
import json
import time

def get_coordinates(location):
    time.sleep(1) # 1 second cooldown to avoid sending too frequent requests to the API
    response = requests.get(f'https://nominatim.openstreetmap.org/search?q={location}&format=json') # OpenStreetMap API
    if response.status_code == 200 and response.json():
        data = response.json()[0]
        coordinates = [float(data['lat']), float(data['lon'])]
        print(f'{location} = {coordinates}')
        return coordinates
    else:
        print(f'Koordinatlar bulunamadı (Couldn\'t find coordinates): {location}')
        return [None, None]  # If the coordinates cannot be found, they are written to the file as [None, None]

def add_coordinates_to_data(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for city in data['data']:
        city['coordinates'] = get_coordinates(city['il_adi'])
        for district in city['ilceler']:
            district['coordinates'] = get_coordinates(f'{city["il_adi"]}, {district["ilce_adi"]}')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


input_path = r'your_input_json_file_location'
output_path = r'your_output_json_file_location'
add_coordinates_to_data(input_path, output_path)
