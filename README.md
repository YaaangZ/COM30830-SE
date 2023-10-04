# Dublin Bike
## Description
This is a group project for COM30830.

This web app allows users to view real-time and historical data on bike availability, weather conditions, and station information. The app also provides predictions about the availability of bikes and stands based on historical trends and weather conditions using a machine learning model.
## Contributors
- [Yang](https://github.com/YaaangZ)
- [Winnie](https://github.com/Winnie101995)
- [Yun](https://github.com/CraneWvs)
## Key features and functions
1. **Real-time bike station information**: Displaying basic information and real-time information on the availability of bikes and bike stands at each station, using the Google Map API and JCDecaux API.
2. **Weather information**: Provide real-time weather information and weather forecast information, using the OpenWeather API.
3. **Historical data chart**: Showing historical data on bike usage and availability at each station, using Google Chart API.
4. **Bike availability prediction**: Predicting the availability of bikes and bike stands at each station in 24 hours and 5 days based on a machine learning model and showing predictive data on charts, using Google Chart API.
5. **Route planner**: Allowing users to input their desired start, end points and time for their journey, and recommending the most appropriate Dublin Bikes stations and route based on their inputs
## Architecture
The architecture of the Dublin Bike app can be divided into three main components: the scrapers, the front-end and the back-end. The scrapers are responsible for crawling station data and weather data for information support. The front-end is responsible for providing the user with a graphical interface to interact with the app. The back-end is responsible for
interacting with the database and performing calculations and processing.
![whole_structure](https://github.com/CraneWvs/Pictures/blob/main/Dublin%20Bike/whole_structure.png)
## Screenshots
![main_page](https://github.com/CraneWvs/Pictures/blob/main/Dublin%20Bike/main_page.png)

main page

![main_page_bike](https://github.com/CraneWvs/Pictures/blob/main/Dublin%20Bike/main_page_bike.png)

bike markers

![marker](https://github.com/CraneWvs/Pictures/blob/main/Dublin%20Bike/marker.png)

marker detail

![planner](https://github.com/CraneWvs/Pictures/blob/main/Dublin%20Bike/planner.png)

route planner

![prompt](https://github.com/CraneWvs/Pictures/blob/main/Dublin%20Bike/prompt.png)

prompt

![trends](https://github.com/CraneWvs/Pictures/blob/main/Dublin%20Bike/trends.png)

trends
## Dependencies
Two environment files, one is from conda and another is from pip.

/flask_dbbikes/env/environment.yml

flask_dbbikes/env/requirements.txt

use yml file to create a new conda environment and then use txt file to install packages.
```
conda env create -f environment.yml -n myenv
conda activate myenv
pip install -r requirements.txt
```