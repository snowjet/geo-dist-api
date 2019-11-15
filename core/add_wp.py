import csv
import pathlib
import herepy
import json

from core.config import app_id, app_code

geocoderApi = herepy.GeocoderApi(app_id, app_code)

def get_waypoints(address):

    # Set Default Waypoint if all else fails
    postcode = None

    response = geocoderApi.free_form(address)
    parsed = json.loads(str(response))

    if len(parsed['Response']['View']) == 0:
        print("Address Not Found Using Postcode only")
        possible_postcodes = [int(s) for s in address.replace(',',' ').split() if s.isdigit()]
        for number in reversed(possible_postcodes):
            if number >= 2000 and number <= 4000:
                postcode = number
                print(postcode)
                break
        
        if postcode is not None:
            address = str(postcode) + ", Australia"
            response = geocoderApi.free_form(address)
            parsed = json.loads(str(response))

    if len(parsed['Response']['View']) != 0:
        waypoints = parsed['Response']['View'][0]['Result'][0]['Location']['NavigationPosition'][0]
    else:
        waypoints = {"Latitude":"0", "Longitude": "0"}

    return waypoints

def read_and_update_file(file_name, out_file_name):

    input_file = csv.DictReader(open(file_name))
    headers = input_file.fieldnames

    dict_data = []
    for row in input_file:
        waypoints = get_waypoints(address=row['Aust ZIP'])
        row.update(waypoints)
        dict_data.append(row)
        print(row)

    csv_columns = headers + ['Latitude','Longitude']
    csv_file = out_file_name
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in dict_data:
                writer.writerow(data)
    except IOError:
        print("I/O error")     
