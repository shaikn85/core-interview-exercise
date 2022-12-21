from flask import Flask, request
import requests
import json

API_KEY = "c766a39d9c387c7527524122df20c77f"

app = Flask(__name__)


def get_weather_json_info(city, country, degrees):
    result_dic = {
        "city": city,
        "country": country,
        "degrees": degrees
    }

    result_json = json.dumps(result_dic)

    return result_json


@app.route("/v1/api/checkCurrentWeather", methods=["GET"])
def check_current_weather():
    data = requests.get("http://ipinfo.io/").json()

    # Replaced a problematic characters in order to show a clear city name in the response
    city = data["city"].replace(chr(817), "").replace(chr(7830), "h")

    country = data["country"]
    location = data["loc"]
    location_list = location.split(",")

    lat = float(location_list[0])
    lon = float(location_list[1])

    weather_data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric").json()

    try:
        temperature = round(weather_data["main"]["temp"])
        return get_weather_json_info(city, country, temperature)
    except:
        return  "Can't find the city in the database accroding to your location"


@app.route("/v1/api/checkCityWeather", methods=["GET"])
def check_city_weather():
    city_name = request.args.get("city")
    weather_data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&appid={API_KEY}").json()
    try:
        temperature = round(weather_data["main"]["temp"])
        country = weather_data["sys"]["country"]
        return get_weather_json_info(city_name, country, temperature)
    except:
        return  "Can't find the city in the database. Please try again."


@app.route("/driveStatus", methods=["POST"])
def update_drive_status():
    try:
        output_file = open("output.txt", "w")

        input_file = open("input.json", "r")
        file_string = input_file.read()

        dict = json.loads(file_string)

        # Read one line in file
        for key, value in dict.items():
            # Prepare new string line to write in new file
            curr_string = ""

            # Split parts in one line by ','
            parts = value.split(',')

            for v in parts:
                curr_string += v.strip().replace(" ", ":",  1)
                curr_string += ","

            # Delete last comma
            curr_string = curr_string[:-1] + "\n"

            # Write new string to local file
            output_file.write(curr_string)

        # Close open files
        input_file.close()
        output_file.close()

        return {"message": "success"}

    except Exception as e:
        return {"message": "failure: " + str(e)}


@app.route("/driveStatus", methods=["GET"])
def get_drive_status():
    try:
        # Get status argument
        status = request.args.get("status").lower()

        # Initialize output variables
        output_list_of_dict = list()
        output_found_counter = 0

        # Open database file
        input_file = open("output.txt", "r")

        # Read lines from database file
        lines = input_file.readlines()
        for line in lines:
            # Convert string line to dictionary
            curr_dict = {key: value for key, value in (item.split(':') for item in line.split(','))}
            # Get status from line
            curr_status = curr_dict["status"].strip().lower()

            # Check if status like requested
            if curr_status == status:
                output_list_of_dict.append(curr_dict)
                output_found_counter += 1

        # Close open file
        input_file.close()

        reponse = [
            {"message" : "Found " + str(output_found_counter) + " " + status + " drives"},
            {"data" : output_list_of_dict}
        ]

        return (json.dumps(reponse))

    except Exception as e:
        reponse = [
            {"message" : "failure - " + str(e)},
            {"data" : []}
        ]

        return (json.dumps(reponse))


if __name__ == '__main__':
     app.run(host="0.0.0.0", port=3000)

