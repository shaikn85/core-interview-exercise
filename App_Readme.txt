*****Installation
1. Clone the following repo https://github.com/shaikn85/core-interview-exercise.git
2. Go to the repo folder in your machine and build the docker image using the following command:
docker build -t  app .  

3. Deploy the container and run using the following command:
docker run -d -p 3000:3000 app



****Instructions for the weather module
The weather module includes the following 2 GET endpoint:
checkCurrentWeather
checkCityWeather


To use the first, go to the following URL:
http://localhost:3000/checkCityWeather
This will recive your country, city, and city tempreture according to your IP address location 

To use the second endpoint, go to the following URL:
http://localhost:3000/v1/api/checkCityWeather?city=<city_name>
Replace your desired city name instead of the <city_name> arrgument

This will recive the city name, country and the tempreture for the desired city 


*Instructions for the drivestatus module
This module includes 1 endpoint with 2 HTTP methods - GET and POST

The POST endpoint is:
http://<MachineIP>localhost:3000/v1/api/driveStatus

The POST endpoint will receive as body the data defined in input.json, and will save it to a local  file inside the container.


The GET endpoint is:
http://<MachineIP>:3000/v1/api/driveStatus?status=<drive_status>

The GET endpoint will receive as query parameter the status to filter the data by and will parse the data in the local file to return only the drives in the provided status.
You can get a query for "online" or "offline" drives .

The response for the GET query will be like the following:
{
  "message": "Found 1 offline drives",
  "data": [
    {
      "name": "SP4",
      "size": "4764771 MB",
      "free": "2333948 MB",
      "path": "/dev/sdk",
      "log": "0 MB",
      "port": 5660,
      "guid": "db53cc9f02524622005b30b0eb0947e3",
      "clusterUuid": "-8650609094877646407--116798096584060989",
      "disks": ["/dev/sdk", "/dev/sdl", "/dev/sdm"],
      "dare": 0
    }
  ]