#information about database
USER = "admin"
PASSWORD = "group8ucd"
# Yun's RDS
HOST = "dbbikes.czd4qxlz1ioy.us-east-1.rds.amazonaws.com"
# Yang's RDS
# HOST = "dbbikes.cqqckwqnmywv.eu-west-1.rds.amazonaws.com"
DATABASE = "dbbikes"
OPEN_WEATHER_API_KEY = "8f2e40db6b1c4dcc89b68735362dbc56"
# weatherForecast
weatherForecastAPI = "https://api.openweathermap.org/data/2.5/forecast?lat=53.3498006&lon=-6.2602964&units=metric&appid=8f2e40db6b1c4dcc89b68735362dbc56"
weatherCurrentAPI = "https://api.openweathermap.org/data/2.5/weather?lat=53.3498006&lon=-6.2602964&units=metric&appid=8f2e40db6b1c4dcc89b68735362dbc56"
GoogleMap_API_KEY = "AIzaSyBs_Crb12f2lIbUsBrjabD2AKXur_qY81o"
# class Config:
#     SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@{}/{}'.format(USER, PASSWORD, HOST, DATABASE)
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
