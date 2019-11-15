import csv
import pathlib
import herepy
import json

from core.config import app_id, app_code

routingApi = herepy.RoutingApi(app_id, app_code)

def get_distance(address, hub):

    # Default on Failure
    distance = -1

    try:
        response = routingApi.car_route(address,hub,
                                        [herepy.RouteMode.car, herepy.RouteMode.fastest])
        parsed = json.loads(str(response))

        if len(parsed['response']['route'][0]['leg'][0]) != 0:
            distance = parsed['response']['route'][0]['leg'][0]['length']

        return distance
    
    except Exception as error:
        print("error")
        return distance

def read_and_update_file(file_name, out_file_name, hubname, hubway ):

    input_file = csv.DictReader(open(file_name))
    headers = input_file.fieldnames

    dict_data = []
    for row in input_file:
        waypoints = [float(row['Latitude']),float(row['Longitude'])]
        distance = get_distance(address=waypoints, hub=hubway)
        row.update({"Kyabram - Distance": distance})
        dict_data.append(row)

    field_name = '%s - Distance' % hubname

    csv_columns = headers + [field_name]
    csv_file = out_file_name
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in dict_data:
                writer.writerow(data)
    except IOError:
        print("I/O error")     
